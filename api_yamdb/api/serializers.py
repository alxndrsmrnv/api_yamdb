from django.db.models import Avg
from django.shortcuts import get_object_or_404
from rest_framework import serializers
from rest_framework.validators import UniqueValidator
from reviews.models import Category, Comment, Genre, Profile, Review, Title


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
        fields = ('username', 'email', 'first_name',
                  'last_name', 'bio', 'role')


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
        fields = ('username', 'email', 'first_name',
                  'last_name', 'bio', 'role')


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
    rating = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Title
        fields = '__all__'

    def get_rating(self, obj):
        rating = obj.reviews.all().aggregate(Avg('score'))['score__avg']
        if not rating:
            return rating
        return int(rating)


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
