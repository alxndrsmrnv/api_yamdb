from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.conf import settings
from rest_framework.fields import CharField


PERMISSION_LEVEL_CHOICES = [
    ('admin', 'Администратор'),
    ('moderator', 'Модератор'),
    ('user', 'Пользователь')
]

class Profile(AbstractUser):
    bio = models.TextField('Биография',
                           blank=True)
    role = models.CharField(max_length=10,
                            choices=PERMISSION_LEVEL_CHOICES,
                            default='user')
    confirmation_code = models.CharField(max_length=12,
                                         blank=True,
                                         editable=False,
                                         null=True,
                                         unique=True)


class Categories(models.Model):
    name = models.CharField(max_length=50,
                            verbose_name='Наименование категории')
    slug = models.SlugField(max_length=255,
                            db_index=True,
                            unique=True,
                            verbose_name='URL')

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'


class Genres(models.Model):
    name = models.CharField(max_length=50, verbose_name='Наименование жанра')
    slug = models.SlugField(max_length=255,
                            db_index=True,
                            unique=True,
                            verbose_name='URL')

    class Meta:
        verbose_name = 'Жанр'
        verbose_name_plural = 'Жанры'


class Titles(models.Model):
    name = models.CharField(max_length=50)
    year = models.PositiveSmallIntegerField()
    category = models.ForeignKey('Categories',
                                 on_delete=models.SET_NULL,
                                 null=True,
                                 related_name='category')
    genre = models.ManyToManyField(Genres)

    def __str__(self):
        return self.title






class Review(models.Model):
    text = models.TextField(verbose_name='Текст')
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='reviews',
        verbose_name='Автор'
    )
    title = models.ForeignKey(
        Title, on_delete=models.CASCADE, related_name='reviews',
        verbose_name='Произведение'
    )
    score = models.PositiveSmallIntegerField(
        verbose_name='оценка',
        validators=[
            MinValueValidator(
                1, message='Оценка должна быть целым числом от 1 до 10'
            ),
            MaxValueValidator(
                10, message='Оценка должна быть целым числом от 1 до 10'
            )
        ]
    )
    pub_date = models.DateTimeField(
        auto_now_add=True, verbose_name='Дата публикации'
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['author', 'title'],
                                    name='unique_review'),
            models.CheckConstraint(
                check=(models.Q(score__gte=1) & models.Q(score__lte=10)),
                name='score_range'
            )
        ]
        ordering = ('-pub_date',)
        verbose_name = 'Отзыв'

        def __str__(self):
            return f'Отзыв: {self.id}; Автор: {self.author.username}; ' \
                   f'Произведение: {self.title.name}; ' \
                   f'Текст: {self.text[:15]}; Оценка: {self.score}'


class Comment(models.Model):
    text = models.TextField(verbose_name='Текст')
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='comments',
        verbose_name='Автор'
    )
    review = models.ForeignKey(
        Review, on_delete=models.CASCADE, related_name='comments',
        verbose_name='Отзыв'
    )
    pub_date = models.DateTimeField(
        auto_now_add=True, verbose_name='Дата публикации'
    )

    class Meta:
        ordering = ('-pub_date',)
        verbose_name = 'Комментарий'

    def __str__(self):
        return f'Комментарий: {self.id}, Автор: {self.author.username}; ' \
               f'Отзыв: {self.review.id}; Текст: {self.text[:15]}'
