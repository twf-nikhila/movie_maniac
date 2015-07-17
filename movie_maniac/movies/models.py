from django.db import models
from datetime import date


class Genre(models.Model):
    name = models.CharField(max_length=24, unique=True)

    def __unicode__(self):
        return self.name


class Director(models.Model):
    name = models.CharField(max_length=225, unique=True)

    def __unicode__(self):
        return self.name


class Movie(models.Model):
    name = models.CharField(max_length=225, db_index=True)
    director = models.ForeignKey(Director)
    imdb_score = models.DecimalField(max_digits=3, decimal_places=1, default=0)
    popularity_99 = models.PositiveSmallIntegerField(default=0)
    genre = models.ManyToManyField(Genre)

    def __unicode__(self):
        return self.name

    class Meta:

        # Director and movie name should be unique
        unique_together = ("name", "director")