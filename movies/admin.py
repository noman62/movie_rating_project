from django.contrib import admin
from .models import Movie, MovieRating, MovieReport

@admin.register(Movie)
class MovieAdmin(admin.ModelAdmin):
    list_display = ('title', 'genre', 'language', 'created_by', 'avg_rating')
    search_fields = ('title', 'description')
    list_filter = ('genre', 'language')

@admin.register(MovieRating)
class MovieRatingAdmin(admin.ModelAdmin):
    list_display = ('movie', 'user', 'rating', 'created_at')
    list_filter = ('rating', 'created_at')

@admin.register(MovieReport)
class MovieReportAdmin(admin.ModelAdmin):
    list_display = ('movie', 'reported_by', 'resolved', 'created_at')
    list_filter = ('resolved', 'created_at')