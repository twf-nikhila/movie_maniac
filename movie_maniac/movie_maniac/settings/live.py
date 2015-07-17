from movie_maniac.settings.settings import *
import os


# Parse database configuration from $DATABASE_URL
import dj_database_url

DEBUG = True

DATABASES = {
    'default': dj_database_url.config()
}