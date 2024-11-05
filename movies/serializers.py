from rest_framework import serializers
from django.contrib.auth import authenticate
from .models import Movie, MovieRating, MovieReport, CustomUser

class UserLoginSerializer(serializers.Serializer):
    email = serializers.EmailField() 
    password = serializers.CharField(write_only=True)
    
    def validate(self, data):
        email = data.get('email') 
        password = data.get('password')
        
        if not email or not password:
            raise serializers.ValidationError({
                'error': 'Please provide both email and password'
            })
        
        user = authenticate(
            request=self.context.get('request'),
            username=email,  
            password=password
        )
        
        if not user:
            raise serializers.ValidationError({
                'error': 'Invalid email or password'
            })
            
        if not user.is_active:
            raise serializers.ValidationError({
                'error': 'User account is disabled'
            })
            
        data['user'] = user
        return data

class UserRegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, min_length=8)
    
    class Meta:
        model = CustomUser
        fields = ('username', 'email', 'password')
        extra_kwargs = {
            'email': {'required': True},
            'username': {'required': True}
        }
    
    def validate_username(self, value):
        if CustomUser.objects.filter(username=value).exists():
            raise serializers.ValidationError("Username is already taken")
        return value
    
    def validate_email(self, value):
        if CustomUser.objects.filter(email=value).exists():
            raise serializers.ValidationError("Email is already registered")
        return value
    
    def create(self, validated_data):
        return CustomUser.objects.create_user(**validated_data)

class MovieSerializer(serializers.ModelSerializer):
    created_by = serializers.ReadOnlyField(source='created_by.username')

    class Meta:
        model = Movie
        fields = ['id', 'title', 'description', 'released_at', 'duration',
                'genre', 'language', 'created_by', 'avg_rating', 'total_ratings',
                'created_at', 'updated_at']
        read_only_fields = ['created_by', 'avg_rating', 'total_ratings']

#     class Meta:
#         model = MovieRating
#         fields = ['id', 'movie', 'rating', 'created_at']
#         read_only_fields = ['created_at']
class MovieRatingSerializer(serializers.ModelSerializer):
    user = serializers.ReadOnlyField(source='user.username')
    
    class Meta:
        model = MovieRating
        fields = ['id', 'movie', 'user', 'rating', 'created_at']
        read_only_fields = ['created_at', 'user']

    def validate_rating(self, value):
        if not (1 <= value <= 5):
            raise serializers.ValidationError("Rating must be between 1 and 5")
        return value
class MovieReportSerializer(serializers.ModelSerializer):
    reported_by = serializers.ReadOnlyField(source='reported_by.username')
    movie_title = serializers.ReadOnlyField(source='movie.title')
    resolved_by = serializers.ReadOnlyField(source='resolved_by.username')
    
    class Meta:
        model = MovieReport
        fields = [
            'id', 'movie', 'movie_title', 'reported_by', 'reason',
            'created_at', 'resolved', 'resolved_at', 'resolved_by',
            'admin_notes'
        ]
        read_only_fields = [
            'created_at', 'resolved', 'resolved_at', 'resolved_by',
            'admin_notes'
        ]