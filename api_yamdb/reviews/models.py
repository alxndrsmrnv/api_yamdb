from django.db import models


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
    year = models.DateField()
    category = models.ForeignKey('Categories',
                                 on_delete=models.SET_NULL,
                                 related_name='category')
    genre = models.ManyToManyField(Genres)

    def __str__(self):
        return self.title
