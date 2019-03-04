from movies.models import Movie, Comment
from rest_framework import serializers
from datetime import datetime

from movies.utils import load_movie


class MovieSerializer(serializers.ModelSerializer):
    class Meta:
        model = Movie
        fields = '__all__'


class AddMovieSerializer(serializers.ModelSerializer):
    class Meta:
        model = Movie
        fields = ('title', )

    def create(self, validated_data):
        model = self.Meta.model
        try:
            movie_data = load_movie(validated_data['title'])
        except LookupError as e:
            raise serializers.ValidationError(str(e))
        available_fields = [f.name for f in model._meta.get_fields()]

        parsed_dict = {}
        for key, value in movie_data.items():
            key = key[0].lower() + key[1:]
            if key in available_fields:
                if value == 'N/A':
                    value = None
                if key == 'released':
                    parsed_dict[key] = datetime.strptime(value,
                                                         '%d %b %Y').date()
                else:
                    parsed_dict[key] = value

        instance = model(**parsed_dict)
        instance.save()
        return instance


class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ('movie', 'body')


class TopMovieSerializer(serializers.Serializer):
    start = serializers.DateField()
    end = serializers.DateField()

    def validate(self, data):
        if data['start'] > data['end']:
            raise serializers.ValidationError("End must occur after start")
        return data