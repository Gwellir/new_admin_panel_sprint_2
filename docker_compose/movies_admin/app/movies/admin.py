"""Административный модуль индекса кинопроизведений."""

from django.contrib import admin

from .models import FilmWork, Genre, GenreFilmWork, Person, PersonFilmWork


class GenreFilmWorkInline(admin.TabularInline):
    """Описание вложенной формы для жанров в карточке фильма."""

    model = GenreFilmWork


@admin.register(Genre)
class GenreAdmin(admin.ModelAdmin):
    """Административная модель для Жанра."""

    list_display = ('name', 'created_at', 'updated_at')


class PersonFilmWorkInline(admin.TabularInline):
    """Описание вложенной формы для персон в карточке фильма."""

    model = PersonFilmWork
    # дропдауны содержат слишком много позиций для нормального отображения
    autocomplete_fields = ('person',)


@admin.register(Person)
class PersonAdmin(admin.ModelAdmin):
    """Административная модель для Персоны."""

    list_display = ('full_name', 'created_at', 'updated_at')
    list_filter = ('personfilmwork__role', )
    search_fields = ('full_name', 'id')


@admin.register(FilmWork)
class FilmWorkAdmin(admin.ModelAdmin):
    """Административная модель для Кинопроизведения."""

    inlines = (
        GenreFilmWorkInline,
        PersonFilmWorkInline,
    )

    list_display = (
        'title', 'type', 'creation_date', 'rating', 'created_at', 'updated_at',
    )
    list_filter = ('type', 'genres__name')
    search_fields = ('title', 'description', 'id')
