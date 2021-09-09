from rest_framework import fields, serializers
from django.contrib.auth import get_user_model
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework.validators import UniqueValidator
from django.contrib.auth.password_validation import validate_password
from rest_framework.relations import SlugRelatedField, StringRelatedField

from reviews.models import Comment, Review, Categories, Genres, Titles, Profile

User = get_user_model()

class ProfileRegisterSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(
            required=True,
            validators=[UniqueValidator(queryset=Profile.objects.all())]
            )
    username = serializers.CharField(required=True, max_length=150)
    class Meta:
        model = Profile
        fields = ('email', 'username')


class TokenSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=150, required=True)
    confirmation_code = serializers.CharField(max_length=150, required=True)

        
class ProfileSerializer(serializers.ModelSerializer):
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
    review = serializers.HiddenField()  # !!!!

    class Meta:
        model = Comment
        fields = '__all__'


class ReviewSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        read_only=True,
        slug_field='username',
        default=serializers.CurrentUserDefault()
    )
    title = serializers.HiddenField()  # !!!!

    class Meta:
        model = Review
        fields = '__all__'
        validators = []

    def validate_score(self, value):
        if not isinstance(value, int) or not value in range(1, 11):
            raise serializers.ValidationError(
                'Оценка должна быть целым числом от 1 до 10'
            )
        return value

    def validate(self, data):
        title = data.get('title')
        author = self.context['request'].user
        if Review.objects.filter(author=author, title=title).exist():
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
