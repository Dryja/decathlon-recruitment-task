from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.mixins import CreateModelMixin
from rest_framework.settings import api_settings
from django.db.models import Count, Q

from movies.models import Movie, Comment
from movies.serializers import MovieSerializer, AddMovieSerializer, CommentSerializer, TopMovieSerializer


class Movies(viewsets.ViewSet):
    """
    View for listing and adding movies
    """

    def list(self, request):
        queryset = Movie.objects.all()
        serializer = MovieSerializer(queryset, many=True)
        return Response(serializer.data)

    def create(self, request):
        serializer = AddMovieSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        instance = serializer.save()

        response = MovieSerializer(instance.__dict__)
        try:
            headers = {
                'Location': str(serializer.data[api_settings.URL_FIELD_NAME])
            }
        except (TypeError, KeyError):
            headers = {}
        return Response(
            response.data, status=status.HTTP_201_CREATED, headers=headers)


class Comments(viewsets.ViewSet, CreateModelMixin):
    """
    View for listing, retrieving by movie id and adding comments
    """
    get_serializer = CommentSerializer

    def list(self, request):
        queryset = Comment.objects.all()
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    def retrieve(self, request, pk=None):
        queryset = Comment.objects.filter(movie_id=pk)
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)


class TopMovies(viewsets.ViewSet):
    """
    View for listing top movies based on date range.
    Example query: /top/?start=2012-12-12&end=2019-12-12
    """

    def list(self, request):
        serializer = TopMovieSerializer(data=request.query_params)
        serializer.is_valid(raise_exception=True)
        date_range = serializer.data
        queryset = Movie.objects.annotate(
            total_comments=Count(
                'comment',
                filter=Q(comment__added__range=[
                    date_range['start'], date_range['end']
                ]))).order_by('-total_comments')

        response = []
        rank = 1
        last_comments_number = None
        for row in list(queryset):
            if last_comments_number and row.total_comments != last_comments_number:
                rank = rank + 1
            last_comments_number = row.total_comments
            response.append({
                'movie_id': row.id,
                'total_comments': row.total_comments,
                'rank': rank
            })
        return Response(response)
