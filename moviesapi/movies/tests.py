from django.urls import reverse

from rest_framework.test import APITestCase


class MoviesViewSetTestCase(APITestCase):
    url = reverse("movies")


class CommentsViewSetTestCase(APITestCase):
    pass


class TopMoviesViewSetTestCase(APITestCase):
    pass