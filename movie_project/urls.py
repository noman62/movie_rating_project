from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenRefreshView
from movies.views import (
    MovieViewSet, 
    MovieReportViewSet,
     AdminMovieReportViewSet,
    RegisterView,
     MovieRatingViewSet,  
    LoginView
)

router = DefaultRouter()
router.register(r'movies', MovieViewSet)
router.register(r'reports', MovieReportViewSet, basename='report')
router.register(r'admin/reports', AdminMovieReportViewSet, basename='admin-report')
router.register(r'ratings', MovieRatingViewSet, basename='rating')  # Add this line

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include(router.urls)),
    path('api-auth/', include('rest_framework.urls')),
    path('api/auth/register/', RegisterView.as_view(), name='register'),
    path('api/auth/login/', LoginView.as_view(), name='login'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]