import json

from django.urls import reverse
from movies.models import Movie, Comment
from rest_framework.test import APITestCase
from datetime import date

sample_movies = [
    {
        'title': 'Blade Runner',
        'director': 'Ridley Scott',
        'released': date(1982, 6, 25),
        'plot':
        'A blade runner must pursue and terminate four replicants who stole a ship in space, and have returned to Earth to find their creator.',
        'metascore': 89,
        'imdbRating': 8.2
    },
    {
        'title': 'Matrix',
        'director': None,
        'released': date(1993, 3, 1),
        'plot':
        'Steven Matrix is one of the underworld\'s foremost hitmen until his luck runs out, and someone puts a contract out on him. Shot in the forehead by a .22 pistol, Matrix "dies" and finds ...',
        'metascore': None,
        'imdbRating': 8.2
    }
]
sample_comments = [
    {
        'body': "Nice movie"
    },
    {
        'body': "Test comment"
    },
]


class MoviesViewSetTestCase(APITestCase):
    url = reverse("movies:movies-list")

    def test_add_movie(self):
        response = self.client.post(self.url, {"title": "The Hunt"})
        self.assertEqual(response.status_code, 201)
        content = json.loads(response.content)
        instance = Movie.objects.get()
        self.assertTrue(content['title'] == instance.title)

    def test_list_movies(self):
        Movie(**sample_movies[0]).save()
        Movie(**sample_movies[1]).save()

        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)

        content = json.loads(response.content)
        self.assertEqual(len(content), 2)


class CommentsViewSetTestCase(APITestCase):
    url = reverse("movies:comments-list")

    def test_add_comment(self):
        instance = Movie(**sample_movies[0])
        instance.save()

        data = {'movie': instance.id, 'body': "Test comment"}
        response = self.client.post(self.url, data)
        self.assertEqual(response.status_code, 201)

        content = json.loads(response.content)
        self.assertEqual(content['body'], data['body'])
        self.assertEqual(content['movie'], data['movie'])

    def test_list_comments(self):
        instance = Movie(**sample_movies[0])
        instance.save()
        Comment(movie=instance, **sample_comments[0]).save()

        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)

        content = json.loads(response.content)
        self.assertEqual(len(content), 1)
        self.assertEqual(content[0]['movie'], instance.id)

    def test_list_by_movie_id(self):
        instance1 = Movie(**sample_movies[0])
        instance1.save()

        instance2 = Movie(**sample_movies[1])
        instance2.save()
        Comment(movie=instance1, **sample_comments[0]).save()
        Comment(movie=instance1, **sample_comments[1]).save()

        response = self.client.get(self.url + str(instance1.id) + '/')
        self.assertEqual(response.status_code, 200)

        content = json.loads(response.content)
        self.assertEqual(len(content), 2)

        response = self.client.get(self.url + str(instance2.id) + '/')
        self.assertEqual(response.status_code, 200)

        content = json.loads(response.content)
        self.assertEqual(len(content), 0)


class TopMoviesViewSetTestCase(APITestCase):
    url = reverse("movies:top-list")

    def test_list_top_movies(self):
        instance1 = Movie(**sample_movies[0])
        instance1.save()

        instance2 = Movie(**sample_movies[1])
        instance2.save()

        Comment(movie=instance1, **sample_comments[0]).save()
        Comment(movie=instance1, **sample_comments[0]).save()
        Comment(movie=instance1, **sample_comments[1]).save()

        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 400)

        data = {'start': '2012-12-12', 'end': '2015-12-12'}
        response = self.client.get(self.url, data)
        self.assertEqual(response.status_code, 200)

        content = json.loads(response.content)
        self.assertEqual(content[0]['total_comments'], 0)
        self.assertEqual(content[0]['rank'], 1)
        self.assertEqual(content[1]['rank'], 1)

        data = {
            'start': '2018-12-12',
            'end': '2100-12-12'
        }  # test will fail in the end of 2100

        response = self.client.get(self.url, data)
        content = json.loads(response.content)
        self.assertEqual(len(content), 2)

        self.assertEqual(content[0]['total_comments'], 3)
        self.assertEqual(content[1]['total_comments'], 0)

        self.assertEqual(content[0]['rank'], 1)
        self.assertEqual(content[1]['rank'], 2)
