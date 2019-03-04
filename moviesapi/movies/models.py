from django.db import models


class Movie(models.Model):
    #Not all the fields created because I don't see a point in it
    title = models.CharField(max_length=255)
    director = models.CharField(max_length=255, null=True)

    released = models.DateField()
    plot = models.TextField()
    metascore = models.IntegerField(null=True)
    imdbRating = models.FloatField(null=True)

    def __str__(self):
        return self.title + " - id: " + str(self.id)


class Comment(models.Model):
    movie = models.ForeignKey('Movie', on_delete=models.CASCADE)
    added = models.DateTimeField(auto_now_add=True)
    body = models.TextField()