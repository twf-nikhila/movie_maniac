from django.conf.urls import patterns, include, url
from django.contrib import admin
from tastypie.api import Api

from movies.api import MovieResource
from movies.api import DirectorResource
from movies.api import GenreResource


v1_api = Api(api_name='v1')
v1_api.register(MovieResource())
v1_api.register(DirectorResource())
v1_api.register(GenreResource())

movie_resource = MovieResource()

urlpatterns = patterns('',
    url(r'^admin/', include(admin.site.urls)),
    (r'^api/', include(v1_api.urls)),
)
