from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404
from rest_framework import serializers
from rest_framework.validators import UniqueTogetherValidator

from reviews.models import Comment, Review, Title

User = get_user_model()


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
