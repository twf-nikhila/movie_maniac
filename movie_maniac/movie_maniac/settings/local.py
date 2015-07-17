from movie_maniac.settings.settings import *


DEBUG = True

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'movie_maniac',
        'USER': 'root',
        'PASSWORD': 'mindfire'
    }
}

