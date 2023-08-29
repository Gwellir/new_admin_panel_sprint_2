"""Базовая миграция для моделей приложения учёта кинопроизведений."""

import uuid

from django.core import validators
from django.db import migrations, models

FORWARD_SQL = """
    CREATE SCHEMA IF NOT EXISTS content;
    CREATE TYPE FILM_TYPE as ENUM('tv_show', 'movie');
"""

REVERSE_SQL = """
    DROP TYPE IF EXISTS FILM_TYPE CASCADE;
    DROP SCHEMA IF EXISTS content CASCADE;
"""


class Migration(migrations.Migration):
    """Базовая Django-миграция приложения учёта кинопроизведений.

    Создаёт схему в postgres, типы, таблицы, индексы и ограничения.
    """

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.RunSQL(
            FORWARD_SQL,
            reverse_sql=REVERSE_SQL,
        ),
        migrations.CreateModel(
            name='FilmWork',
            fields=[
                ('created', models.DateTimeField(auto_now_add=True)),
                ('modified', models.DateTimeField(auto_now=True)),
                (
                    'id',
                    models.UUIDField(
                        default=uuid.uuid4,
                        editable=False,
                        primary_key=True,
                        serialize=False,
                    ),
                ),
                (
                    'title',
                    models.CharField(
                        db_index=True,
                        max_length=255,
                        verbose_name='title',
                    ),
                ),
                (
                    'description',
                    models.TextField(
                        blank=True,
                        verbose_name='description',
                    ),
                ),
                (
                    'creation_date',
                    models.DateField(
                        db_index=True,
                        null=True,
                        verbose_name='creation_date',
                    ),
                ),
                (
                    'rating',
                    models.FloatField(
                        db_index=True,
                        blank=True,
                        validators=[
                            validators.MinValueValidator(0),
                            validators.MaxValueValidator(100),
                        ],
                        verbose_name='rating',
                    ),
                ),
                (
                    'type',
                    models.CharField(
                        choices=[
                            ('tv_show', 'TV show'),
                            ('movie', 'Movie'),
                        ],
                        db_index=True,
                        max_length=50,
                        verbose_name='type',
                    ),
                ),
            ],
            options={
                'verbose_name': 'Кинопроизведение',
                'verbose_name_plural': 'Кинопроизведения',
                'db_table': 'content"."film_work',
            },
        ),
        migrations.CreateModel(
            name='Genre',
            fields=[
                ('created', models.DateTimeField(auto_now_add=True)),
                ('modified', models.DateTimeField(auto_now=True)),
                (
                    'id',
                    models.UUIDField(
                        default=uuid.uuid4,
                        editable=False,
                        primary_key=True,
                        serialize=False,
                    ),
                ),
                (
                    'name',
                    models.CharField(
                        max_length=255,
                        verbose_name='name',
                    ),
                ),
                (
                    'description',
                    models.TextField(
                        blank=True,
                        verbose_name='description',
                    ),
                ),
            ],
            options={
                'verbose_name': 'Жанр',
                'verbose_name_plural': 'Жанры',
                'db_table': 'content"."genre',
            },
        ),
        migrations.CreateModel(
            name='Person',
            fields=[
                ('created', models.DateTimeField(auto_now_add=True)),
                ('modified', models.DateTimeField(auto_now=True)),
                (
                    'id',
                    models.UUIDField(
                        default=uuid.uuid4,
                        editable=False,
                        primary_key=True,
                        serialize=False,
                    ),
                ),
                (
                    'full_name',
                    models.CharField(
                        db_index=True,
                        max_length=255,
                        verbose_name='full_name',
                    ),
                ),
            ],
            options={
                'verbose_name': 'Персона',
                'verbose_name_plural': 'Персоны',
                'db_table': 'content"."person',
            },
        ),
        migrations.CreateModel(
            name='PersonFilmWork',
            fields=[
                (
                    'id',
                    models.UUIDField(
                        default=uuid.uuid4,
                        editable=False,
                        primary_key=True,
                        serialize=False,
                    ),
                ),
                (
                    'role',
                    models.TextField(
                        null=True,
                        verbose_name='role',
                    ),
                ),
                (
                    'created',
                    models.DateTimeField(
                        auto_now_add=True,
                    ),
                ),
                (
                    'film_work',
                    models.ForeignKey(
                        null=True,
                        on_delete=models.deletion.DO_NOTHING,
                        to='movies.filmwork',
                    ),
                ),
                (
                    'person',
                    models.ForeignKey(
                        db_index=True,
                        null=True,
                        on_delete=models.deletion.DO_NOTHING,
                        related_name='film_works',
                        to='movies.person',
                    ),
                ),
            ],
            options={
                'db_table': 'content"."person_film_work',
                'constraints': [
                    models.UniqueConstraint(
                        fields=[
                            'film_work',
                            'person',
                            'role',
                        ],
                        name='film_work_person_role_un',
                    ),
                ],
            },
        ),
        migrations.CreateModel(
            name='GenreFilmWork',
            fields=[
                (
                    'id',
                    models.UUIDField(
                        default=uuid.uuid4,
                        editable=False,
                        primary_key=True,
                        serialize=False,
                    ),
                ),
                ('created', models.DateTimeField(auto_now_add=True)),
                (
                    'film_work',
                    models.ForeignKey(
                        on_delete=models.deletion.CASCADE,
                        related_name='genres',
                        to='movies.filmwork',
                    ),
                ),
                (
                    'genre',
                    models.ForeignKey(
                        db_index=True,
                        on_delete=models.deletion.CASCADE,
                        to='movies.genre',
                    ),
                ),
            ],
            options={
                'db_table': 'content"."genre_film_work',
                'constraints': [
                    models.UniqueConstraint(
                        fields=[
                            'film_work',
                            'genre',
                        ],
                        name='film_work_genre_un',
                    ),
                ],
            },
        ),
    ]
