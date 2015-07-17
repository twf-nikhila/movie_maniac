from tastypie.resources import ModelResource
from tastypie import fields
from tastypie.authentication import BasicAuthentication
from tastypie.authorization import DjangoAuthorization
from tastypie.utils import trailing_slash
from django.conf.urls import url
from django.db.models import Q
from tastypie.resources import ModelResource, ALL, ALL_WITH_RELATIONS
from tastypie.validation import Validation


from movies.models import Movie
from movies.models import Director
from movies.models import Genre


class DirectorResource(ModelResource):

    # TODO: Check to show all movies for director when get_obj method is called
    #movie = fields.ToManyField('movies.api.MovieResource', 'movie_set', use_in='detail', full=True)

    class Meta:
        queryset = Director.objects.all()
        resource_name = 'director'
        authentication = BasicAuthentication()
        authorization = DjangoAuthorization()
        always_return_data = True


class GenreResource(ModelResource):

    class Meta:
        queryset = Genre.objects.all()
        resource_name = 'genre'
        authentication = BasicAuthentication()
        authorization = DjangoAuthorization()
        filtering = {
            "name": ["iexact"]
        }
        always_return_data = True

    #TODO: Remove details method


class MovieValidator(Validation):
    """
    Validates the field for movie
    """
    def is_valid(self, bundle, request=None):

        errors = {}

        if 'imdb_score' in bundle.data:
            if bundle.data['imdb_score'] > 10:
                errors['imdb_score'] = "Imdb score cannot be greater than 10"

        if 'popularity_99' in bundle.data:
            if bundle.data['popularity_99'] > 99:
                errors['popularity_99'] = "Popularity cannot be greater than 99"

        return errors


class MovieResource(ModelResource):
    director = fields.ForeignKey(DirectorResource, 'director', full=True, use_in="detail")
    genre = fields.ManyToManyField(GenreResource, 'genre', full=True, null=True, use_in="detail")

    class Meta:
        queryset = Movie.objects.all()
        resource_name = 'movie'
        authentication = BasicAuthentication()
        authorization = DjangoAuthorization()
        ordering = ['name', 'imdb_score', 'popularity_99']  # order_by get param is used to specify sorting
        always_return_data = True
        filtering = {
            "name": ["icontains", "istartswith"],
            "genre": ALL_WITH_RELATIONS
        }
        validation = MovieValidator()

        #TODO: Restrict allowed methods according to user types


    def prepend_urls(self):
        return [
            url(r"^(?P<resource_name>%s)/search%s$" % (self._meta.resource_name, trailing_slash()),
                self.wrap_view('get_search'), name="api_get_search"),
        ]

    def get_search(self, request, **kwargs):

        self.method_check(request, allowed=['get'])
        self.is_authenticated(request)

        # Do the query to search by movie name or director name
        sqs = Movie.objects.filter(Q(name__contains=request.GET.get('q', '')) |
                                   Q(director__name__startswith=request.GET.get('q', '')))

        objects = []

        for result in sqs:
            bundle = self.build_bundle(obj=result, request=request)
            bundle = self.full_dehydrate(bundle)
            objects.append(bundle)

        object_list = {
            'objects': objects,
        }

        return self.create_response(request, object_list)