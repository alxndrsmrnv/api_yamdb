from rest_framework import serializers
from rest_framework.relations import SlugRelatedField, StringRelatedField
from reviews.models import Categories, Genres, Titles


class CategoriesSerializer(serializers.ModelSerializer):
    name = StringRelatedField(read_only=True)

    class Meta:
        fields = '__all__'
        model = Categories


class GenresSerializer(serializers.ModelSerializer):
    name = StringRelatedField(read_only=True, many=True)

    class Meta:
        fields = '__all__'
        model = Genres


class TitlesSerializer(serializers.ModelSerializer):
    genre = SlugRelatedField(read_only=True, slug_field='name', many=True)
    category = SlugRelatedField(read_only=True, slug_field='name')

    class Meta:
        fields = '__all__'
        model = Titles
