from re import search
from django.http import request
from rest_framework import fields, serializers

from django.shortcuts import get_object_or_404
from rest_framework_simplejwt.serializers import TokenObtainSerializer
from rest_framework.validators import UniqueValidator
from django.contrib.auth.password_validation import validate_password
from rest_framework.relations import SlugRelatedField, StringRelatedField

from reviews.models import Comment, Review, Categories, Genres, Titles, Profile


class ProfileRegisterSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(
        required=True,
        validators=[UniqueValidator(queryset=Profile.objects.all())]
    )
    username = serializers.CharField(
        required=True,
        max_length=150,
        validators=[UniqueValidator(queryset=Profile.objects.all())]
    )

    class Meta:
        model = Profile
        fields = ('email', 'username')


class TokenSerializer(serializers.Serializer):
    username = serializers.CharField(
        max_length=150,
        required=True,
    )
    confirmation_code = serializers.CharField(max_length=150, required=True)


class ProfileSerializer(serializers.ModelSerializer):
    search = serializers.StringRelatedField()

    class Meta:
        model = Profile
        fields = '__all__'

"""Алексей Третий Разработчик"""
class CommentSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        read_only=True,
        slug_field='username',
        default=serializers.CurrentUserDefault()
    )

    class Meta:
        model = Comment
        exclude = ('review',)


class ReviewSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        read_only=True,
        slug_field='username',
        default=serializers.CurrentUserDefault()
    )

    class Meta:
        model = Review
        exclude = ('title',)

    def validate_score(self, value):
        if not isinstance(value, int) or not (value in range(1, 11)):
            raise serializers.ValidationError(
                'Оценка должна быть целым числом от 1 до 10'
            )
        return value

    def validate(self, data):
        view = self.context['view']
        title = get_object_or_404(Titles, id=view.kwargs.get('title_id'))
        if Review.objects.filter(author=self.context['request'].user,
                                 title=title).exists():
            raise serializers.ValidationError(
                'Можно оставить только один отзыв на произведение'
            )
        return data
"""Алексей Третий Разработчик"""


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
