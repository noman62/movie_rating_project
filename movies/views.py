from rest_framework import viewsets, status, permissions
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import Movie, MovieRating, MovieReport
from rest_framework import serializers  # Add this import
from .serializers import MovieSerializer, MovieRatingSerializer, MovieReportSerializer
from .permissions import IsMovieCreatorOrReadOnly
from rest_framework.permissions import IsAuthenticated
from rest_framework import status, generics
from rest_framework.permissions import AllowAny
from rest_framework_simplejwt.tokens import RefreshToken
from .serializers import UserRegistrationSerializer, UserLoginSerializer
from django.utils import timezone

class LoginView(generics.GenericAPIView):
    serializer_class = UserLoginSerializer
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        try:
            serializer.is_valid(raise_exception=True)
            user = serializer.validated_data['user']
            refresh = RefreshToken.for_user(user)

            return Response({
                'status': 'success',
                'data': {
                    'user': {
                        'id': user.id,
                        'username': user.username,
                        'email': user.email,
                    },
                    'tokens': {
                        'refresh': str(refresh),
                        'access': str(refresh.access_token),
                    }
                }
            }, status=status.HTTP_200_OK)
            
        except serializers.ValidationError as e:
            return Response({
                'status': 'error',
                'message': 'Invalid credentials',
                'errors': serializer.errors
            }, status=status.HTTP_401_UNAUTHORIZED)

class RegisterView(generics.CreateAPIView):
    serializer_class = UserRegistrationSerializer
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            refresh = RefreshToken.for_user(user)
            
            return Response({
                'status': 'success',
                'data': {
                    'user': {
                        'id': user.id,
                        'username': user.username,
                        'email': user.email,
                    },
                    'tokens': {
                        'refresh': str(refresh),
                        'access': str(refresh.access_token),
                    }
                }
            }, status=status.HTTP_201_CREATED)
        
        return Response({
            'status': 'error',
            'errors': serializer.errors
        }, status=status.HTTP_400_BAD_REQUEST)


class MovieRatingViewSet(viewsets.ModelViewSet):
    serializer_class = MovieRatingSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return MovieRating.objects.filter(user=self.request.user)

    def create(self, request, *args, **kwargs):
        movie_id = request.data.get('movie')
        if not movie_id:
            return Response(
                {'error': 'Movie ID is required'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        try:
            movie = Movie.objects.get(pk=movie_id)
        except Movie.DoesNotExist:
            return Response(
                {'error': 'Movie not found'},
                status=status.HTTP_404_NOT_FOUND
            )

        existing_rating = MovieRating.objects.filter(
            user=request.user,
            movie=movie
        ).first()

        if existing_rating:
            existing_rating.rating = request.data.get('rating')
            existing_rating.save()
            movie.update_rating()
            return Response(
                MovieRatingSerializer(existing_rating).data,
                status=status.HTTP_200_OK
            )

        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        movie.update_rating()
        
        return Response(
            serializer.data,
            status=status.HTTP_201_CREATED
        )

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        
        if instance.user != request.user:
            return Response(
                {'error': 'You can only update your own ratings'},
                status=status.HTTP_403_FORBIDDEN
            )

        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        instance.movie.update_rating()

        return Response(serializer.data)
class MovieViewSet(viewsets.ModelViewSet):
    queryset = Movie.objects.all()
    serializer_class = MovieSerializer
    permission_classes = [permissions.IsAuthenticated, IsMovieCreatorOrReadOnly]

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)

    @action(detail=True, methods=['post'])
    def rate(self, request, pk=None):
        movie = self.get_object()
        rating_value = request.data.get('rating')
        
        if not rating_value:
            return Response(
                {'error': 'Rating is required'},
                status=status.HTTP_400_BAD_REQUEST
            )
            
        try:
            rating_value = int(rating_value)
            if not (1 <= rating_value <= 5):
                raise ValueError
        except ValueError:
            return Response(
                {'error': 'Rating must be an integer between 1 and 5'},
                status=status.HTTP_400_BAD_REQUEST
            )

        rating, created = MovieRating.objects.update_or_create(
            movie=movie,
            user=request.user,
            defaults={'rating': rating_value}
        )
        
        movie.update_rating()
        
        return Response({
            'message': 'Rating updated successfully',
            'rating': rating_value,
            'avg_rating': movie.avg_rating,
            'total_ratings': movie.total_ratings
        })
    @action(detail=True, methods=['post'])
    def report(self, request, pk=None):
        movie = self.get_object()
        reason = request.data.get('reason')
        
        if not reason:
            return Response({'error': 'Reason is required'}, 
                          status=status.HTTP_400_BAD_REQUEST)

        MovieReport.objects.create(
            movie=movie,
            reported_by=request.user,
            reason=reason
        )
        return Response({'status': 'movie reported'})

class MovieReportViewSet(viewsets.ModelViewSet):
    serializer_class = MovieReportSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        if self.request.user.is_staff:
            return MovieReport.objects.all()
        return MovieReport.objects.filter(reported_by=self.request.user)

    def perform_create(self, serializer):
        serializer.save(reported_by=self.request.user)

    def create(self, request, *args, **kwargs):
        movie_id = request.data.get('movie')
        try:
            movie = Movie.objects.get(pk=movie_id)
        except Movie.DoesNotExist:
            return Response(
                {'error': 'Movie not found'},
                status=status.HTTP_404_NOT_FOUND
            )

        existing_report = MovieReport.objects.filter(
            movie=movie,
            reported_by=request.user,
            resolved=False
        ).first()

        if existing_report:
            return Response(
                {'error': 'You have already reported this movie'},
                status=status.HTTP_400_BAD_REQUEST
            )

        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class AdminMovieReportViewSet(viewsets.ModelViewSet):
    queryset = MovieReport.objects.all()
    serializer_class = MovieReportSerializer
    permission_classes = [permissions.IsAdminUser]

    def get_queryset(self):
        status = self.request.query_params.get('status', None)
        if status == 'resolved':
            return MovieReport.objects.filter(resolved=True)
        elif status == 'pending':
            return MovieReport.objects.filter(resolved=False)
        return MovieReport.objects.all()

    @action(detail=True, methods=['post'])
    def resolve(self, request, pk=None):
        report = self.get_object()
        action = request.data.get('action', 'resolve')
        notes = request.data.get('notes', '')

        if action not in ['resolve', 'dismiss']:
            return Response(
                {'error': 'Invalid action. Use "resolve" or "dismiss"'},
                status=status.HTTP_400_BAD_REQUEST
            )

        report.resolved = True
        report.admin_notes = notes
        report.resolved_at = timezone.now()
        report.resolved_by = request.user
        report.save()

        return Response({
            'status': 'success',
            'message': f'Report {action}d successfully',
            'report': MovieReportSerializer(report).data
        })

    @action(detail=False, methods=['get'])
    def statistics(self, request):
        total_reports = MovieReport.objects.count()
        pending_reports = MovieReport.objects.filter(resolved=False).count()
        resolved_reports = MovieReport.objects.filter(resolved=True).count()
        
        return Response({
            'total_reports': total_reports,
            'pending_reports': pending_reports,
            'resolved_reports': resolved_reports,
            'resolution_rate': f"{(resolved_reports/total_reports)*100:.2f}%" if total_reports > 0 else "0%"
        })
