<<<<<<< HEAD
from random import choice, choices
from re import search
from django.http import request
from rest_framework import fields, serializers
from django.shortcuts import get_object_or_404
from rest_framework_simplejwt.serializers import TokenObtainSerializer
from rest_framework.validators import UniqueValidator
from django.contrib.auth.password_validation import validate_password
from rest_framework.relations import SlugRelatedField, StringRelatedField  # Возможно нужно все из serializers использовать

<<<<<<< HEAD
from reviews.models import Comment, Review, Categories, Genres, Title, Profile
=======
from reviews.models import Comment, Review, Categories, Genres, Titles, Profile, PERMISSION_LEVEL_CHOICES
>>>>>>> Profile2.0

=======
from rest_framework import serializers
from django.contrib.auth import get_user_model
from rest_framework.validators import UniqueValidator

from reviews.models import Comment, Review, Category, Genre, Title, Profile
>>>>>>> cat-gen-tit.v2



class ProfileRegisterSerializer(serializers.ModelSerializer):
<<<<<<< HEAD
    email = serializers.EmailField(
        required=True,
        validators=[UniqueValidator(queryset=Profile.objects.all())]
    )
    username = serializers.CharField(
        required=True,
        max_length=150,
        validators=[UniqueValidator(queryset=Profile.objects.all())]
    )
=======
    email = serializers.EmailField(required=True,
                                   validators=[UniqueValidator(
                                       queryset=Profile.objects.all())])
    username = serializers.CharField(required=True, max_length=150)
>>>>>>> cat-gen-tit.v2

    class Meta:
        model = Profile
        fields = ('email', 'username')


class TokenSerializer(serializers.Serializer):
    username = serializers.CharField(
        max_length=150,
        required=True,
    )
    confirmation_code = serializers.CharField(max_length=150, required=True)

<<<<<<< HEAD
class TokenRestoreSerializer(serializers.Serializer):
    username = serializers.CharField(
        max_length=150,
        required=True,
    )
    email = serializers.EmailField(max_length=150, required=True)


class ProfileSerializerAdmin(serializers.ModelSerializer):
    username = serializers.CharField(
        required=True,
        validators=[UniqueValidator(queryset=Profile.objects.all())]
    )
    email = serializers.EmailField(
        required=True,
        validators=[UniqueValidator(queryset=Profile.objects.all())]
    )
    class Meta:
        model = Profile
        fields = ('username', 'email', 'first_name', 'last_name', 'bio', 'role')
        #fields = '__all__'
=======
>>>>>>> cat-gen-tit.v2

class ProfileSerializer(serializers.ModelSerializer):
    username = serializers.CharField(
        required=True,
        validators=[UniqueValidator(queryset=Profile.objects.all())]
    )
    email = serializers.EmailField(
        required=True,
        validators=[UniqueValidator(queryset=Profile.objects.all())]
    )
    role = serializers.ReadOnlyField()
    class Meta:
        model = Profile
<<<<<<< HEAD
        fields = ('username', 'email', 'first_name', 'last_name', 'bio', 'role')
        #fields = '__all__'
=======
        fields = ('username', 'email', 'first_name',
                  'last_name', 'bio', 'role')

>>>>>>> cat-gen-tit.v2

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

    def create(self, validated_data):
        view = self.context['view']
        title = get_object_or_404(Title, id=view.kwargs.get('title_id'))
        if Review.objects.filter(author=self.context['request'].user,
                                 title=title).exists():
            raise serializers.ValidationError(
                'Можно оставить только один отзыв на произведение'
            )
<<<<<<< HEAD
        review = Review.objects.create(**validated_data)
        return review

    def update(self, instance, validated_data):
        instance.text = validated_data.get('text', instance.text)
        instance.score = validated_data.get('score', instance.score)
        instance.save()
        return instance
=======
        return data


>>>>>>> cat-gen-tit.v2
"""Алексей Третий Разработчик"""


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        exclude = ['id', ]
        model = Category


class GenreSerializer(serializers.ModelSerializer):
    class Meta:
        exclude = ['id', ]
        model = Genre


class TitleSerializer(serializers.ModelSerializer):
    category = CategorySerializer(read_only=True)
    genre = GenreSerializer(read_only=True, many=True)

    class Meta:
        model = Title
        fields = '__all__'


class TitleSerializerCreate(serializers.ModelSerializer):
    category = serializers.SlugRelatedField(slug_field='slug',
                                            queryset=Category.objects.all(),
                                            required=False)
    genre = serializers.SlugRelatedField(slug_field='slug',
                                         queryset=Genre.objects.all(),
                                         required=False, many=True)

    class Meta:
        model = Title
        fields = '__all__'
