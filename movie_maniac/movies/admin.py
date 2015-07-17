from django.contrib import admin
from movies.models import Genre, Director, Movie


class GenreAdmin(admin.ModelAdmin):
    search_fields = ['name']


class DirectorAdmin(admin.ModelAdmin):
    search_fields = ['name']


class MovieAdmin(admin.ModelAdmin):
    search_fields = ['name', 'director']
    list_display = ['name', 'director', 'imdb_score', 'popularity_99']


admin.site.register(Genre, GenreAdmin)
admin.site.register(Director, DirectorAdmin)
admin.site.register(Movie, MovieAdmin)