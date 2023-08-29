"""Применяет изменения для адаптации к формату таблиц SQLite."""


from django.core import validators
from django.db import migrations, models


class Migration(migrations.Migration):
    """Класс, описывающий миграцию Django."""

    dependencies = [
        ('movies', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='filmwork',
            old_name='created',
            new_name='created_at',
        ),
        migrations.RenameField(
            model_name='genre',
            old_name='created',
            new_name='created_at',
        ),
        migrations.RenameField(
            model_name='person',
            old_name='created',
            new_name='created_at',
        ),
        migrations.RenameField(
            model_name='filmwork',
            old_name='modified',
            new_name='updated_at',
        ),
        migrations.RenameField(
            model_name='genre',
            old_name='modified',
            new_name='updated_at',
        ),
        migrations.RenameField(
            model_name='person',
            old_name='modified',
            new_name='updated_at',
        ),
        migrations.RenameField(
            model_name='genrefilmwork',
            old_name='created',
            new_name='created_at',
        ),
        migrations.RenameField(
            model_name='personfilmwork',
            old_name='created',
            new_name='created_at',
        ),
        migrations.AddField(
            model_name='filmwork',
            name='file_path',
            field=models.TextField(blank=True, verbose_name='file_path'),
        ),
        migrations.AlterField(
            model_name='filmwork',
            name='rating',
            field=models.FloatField(
                null=True,
                validators=[
                    validators.MinValueValidator(0),
                    validators.MaxValueValidator(100),
                ],
                verbose_name='rating',
            ),
        ),
        migrations.AlterField(
            model_name='genre',
            name='name',
            field=models.CharField(
                max_length=255,
                unique=True,
                verbose_name='name',
            ),
        ),
        migrations.AlterField(
            model_name='filmwork',
            name='file_path',
            field=models.TextField(
                blank=True,
                null=True,
                verbose_name='file_path',
            ),
        ),
        migrations.AlterField(
            model_name='filmwork',
            name='description',
            field=models.TextField(
                blank=True,
                null=True,
                verbose_name='description',
            ),
        ),
        migrations.AlterField(
            model_name='genre',
            name='description',
            field=models.TextField(
                blank=True,
                null=True,
                verbose_name='description',
            ),
        ),
        migrations.AlterField(
            model_name='personfilmwork',
            name='role',
            field=models.CharField(
                choices=[
                    ('actor', 'Actor'),
                    ('director', 'Director'),
                    ('writer', 'Writer'),
                ],
                max_length=30,
                null=True,
                verbose_name='role',
            ),
        ),
    ]
