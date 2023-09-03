"""Модели БД для приложения учета кинопроизведений."""

import uuid

from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from django.utils.translation import gettext_lazy as _


class TimeStampedMixin(models.Model):
    """Миксин для маркировки записей временем создания и изменения."""

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class UUIDMixin(models.Model):
    """Миксин для реализации PRIMARY KEY записей в виде uuid4."""

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    class Meta:
        abstract = True


class Person(UUIDMixin, TimeStampedMixin):
    """Описывает участника создания кинопроизведения."""

    full_name = models.CharField(_('full_name'), max_length=255, db_index=True)

    class Meta:
        db_table = 'content\".\"person'
        verbose_name = 'Персона'
        verbose_name_plural = 'Персоны'

    def __str__(self):
        return self.full_name


class Genre(UUIDMixin, TimeStampedMixin):
    """Описывает жанр кинопроизведения."""

    name = models.CharField(_('name'), max_length=255, unique=True)
    description = models.TextField(_('description'), blank=True, null=True)

    class Meta:
        db_table = 'content\".\"genre'
        verbose_name = 'Жанр'
        verbose_name_plural = 'Жанры'

    def __str__(self):
        return self.name


class FilmTypes(models.TextChoices):
    """Константы для описания типов кинопроизведений."""

    TV_SHOW = 'tv_show', _('TV show')
    MOVIE = 'movie', _('Movie')


class FilmWork(UUIDMixin, TimeStampedMixin):
    """Описывает кинопроизведение."""

    title = models.CharField(_('title'), max_length=255, db_index=True)
    description = models.TextField(_('description'), blank=True, null=True)
    creation_date = models.DateField(
        _('creation_date'),
        null=True,
        db_index=True,
    )
    file_path = models.TextField(_('file_path'), blank=True, null=True)
    rating = models.FloatField(
        _('rating'),
        null=True,
        validators=[
            MinValueValidator(0),
            MaxValueValidator(100),
        ],
    )
    type = models.CharField(
        _('type'),
        choices=FilmTypes.choices,
        max_length=50,
        db_index=True,
    )
    genres = models.ManyToManyField(
        Genre,
        through='GenreFilmWork',
        related_name='film_works',
    )
    persons = models.ManyToManyField(
        Person,
        through='PersonFilmWork',
        related_name='film_works',
    )

    class Meta:
        db_table = 'content\".\"film_work'
        verbose_name = 'Кинопроизведение'
        verbose_name_plural = 'Кинопроизведения'

    def __str__(self):
        return self.title


class Roles(models.TextChoices):
    """Константы для описания возможных ролей."""

    ACTOR = 'actor', _('Actor')
    DIRECTOR = 'director', _('Director')
    WRITER = 'writer', _('Writer')


class PersonFilmWork(UUIDMixin):
    """Описывает роли (м2м связи фильм-персона)."""

    film_work = models.ForeignKey(
        'FilmWork',
        null=True,
        on_delete=models.DO_NOTHING,
    )
    person = models.ForeignKey(
        'Person',
        null=True,
        on_delete=models.DO_NOTHING,
    )
    role = models.CharField(
        _('role'),
        max_length=30,
        choices=Roles.choices,
        null=True,
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'content\".\"person_film_work'
        constraints = [
            models.UniqueConstraint(
                fields=[
                    'film_work',
                    'person',
                    'role',
                ],
                name='film_work_person_role_un',
            ),
        ]

    def __str__(self):
        return '{0}: {1}'.format(self.role, self.person)


class GenreFilmWork(UUIDMixin):
    """Описывает связи жанр-фильм м2м."""

    film_work = models.ForeignKey(
        'FilmWork',
        on_delete=models.CASCADE,
    )
    genre = models.ForeignKey('Genre', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'content\".\"genre_film_work'
        constraints = [
            models.UniqueConstraint(
                fields=[
                    'film_work',
                    'genre',
                ],
                name='film_work_genre_un',
            ),
        ]

    def __str__(self):
        return str(self.genre)
