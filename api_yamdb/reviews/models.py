from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models


class Review(models.Model):
    text = models.TextField(verbose_name='Текст')
    author = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='reviews',
        verbose_name='Автор'
    )
    title = models.ForeignKey(
        Titles, on_delete=models.CASCADE, related_name='reviews',
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
        User, on_delete=models.CASCADE, related_name='comments',
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
