# Generated by Django 2.2.16 on 2021-09-10 18:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('reviews', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='titles',
            name='year',
            field=models.PositiveSmallIntegerField(),
        ),
    ]
