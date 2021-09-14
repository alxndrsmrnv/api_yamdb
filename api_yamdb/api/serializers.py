from rest_framework import fields, serializers

from django.shortcuts import get_object_or_404
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework.validators import UniqueValidator
from django.contrib.auth.password_validation import validate_password
from rest_framework.relations import SlugRelatedField, StringRelatedField  # Возможно нужно все из serializers использовать

from reviews.models import Comment, Review, Categories, Genres, Title, Profile



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
        review = Review.objects.create(**validated_data)
        return review

    def update(self, instance, validated_data):
        instance.text = validated_data.get('text', instance.text)
        instance.score = validated_data.get('score', instance.score)
        instance.save()
        return instance
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

#