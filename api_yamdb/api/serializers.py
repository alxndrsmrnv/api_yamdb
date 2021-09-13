from rest_framework import serializers
from django.contrib.auth import get_user_model
from rest_framework.validators import UniqueValidator

from reviews.models import Comment, Review, Category, Genre, Title, Profile

User = get_user_model()


class ProfileRegisterSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(required=True,
                                   validators=[UniqueValidator(
                                       queryset=Profile.objects.all())])
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
        fields = ('username', 'email', 'first_name',
                  'last_name', 'bio', 'role')


"""Алексей Третий Разработчик"""


class CommentSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        read_only=True,
        slug_field='username',
        default=serializers.CurrentUserDefault()
    )
    """
    review = serializers.HiddenField()  # !!!!
    """
    class Meta:
        model = Comment
        fields = '__all__'


class ReviewSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        read_only=True,
        slug_field='username',
        default=serializers.CurrentUserDefault()
    )
    """
    title = serializers.HiddenField()  # !!!!
    """
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
