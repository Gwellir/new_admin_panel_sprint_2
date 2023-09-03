"""Модуль с описаниями представлений API."""

from config import settings
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.contrib.postgres.aggregates import ArrayAgg
from django.db.models import Q  # noqa: WPS347
from django.http import JsonResponse
from django.views.generic.detail import BaseDetailView
from django.views.generic.list import BaseListView
from movies.models import FilmWork, Roles


class MoviesApiMixin(PermissionRequiredMixin):
    """Основной миксин для представлений MoviesApi.

    Содержит указания на модели, настройки разрешений, описание запроса для
    выдачи релевантной информации о кинопроизведениях в нужной форме.
    """

    model = FilmWork
    http_method_names = ['get']
    login_url = '/admin/login/'
    permission_required = settings.PERMISSION_REQUIRED

    def get_queryset(self):
        """Описывает запрос для выдачи информации о кинопроизведениях.

        Returns:
            Queryset, содержащий информацию о фильме, расширенную списками
                участников и жанров.
        """
        genres_related_subquery = """
            SELECT array (
                SELECT name
                FROM genre_film_work gfw
                JOIN genre g
                    ON g.id = gfw.genre_id
                WHERE gfw.film_work_id = film_work.id
            )
            """
        return (
            self.model.objects.  # noqa: S610
            # используется отдельный подзапрос, так как django annotate
            # начинает выдавать дубликаты результатов при использовании
            # обращений к разным таблицам в одном запросе
            extra(
                select={'genres': genres_related_subquery},
            ).values(
                'id',
                'title',
                'description',
                'creation_date',
                'rating',
                'type',
                'genres',
            ).annotate(
                actors=ArrayAgg(
                    'persons__full_name',
                    filter=Q(personfilmwork__role=Roles.ACTOR),
                ),
                directors=ArrayAgg(
                    'persons__full_name',
                    filter=Q(personfilmwork__role=Roles.DIRECTOR),
                ),
                writers=ArrayAgg(
                    'persons__full_name',
                    filter=Q(personfilmwork__role=Roles.WRITER),
                ),
            ).prefetch_related('genre', 'person')
        )

    def render_to_response(self, context, **response_kwargs):
        """Возвращает контекст с информацией о фильме в виде JSON.

        Args:
            context: Сформированный контекст ответа.
            response_kwargs: Опциональные дополнительные аргументы.

        Returns:
            JSON с информацией о кинопроизведении.
        """
        return JsonResponse(context)


class MoviesListApi(MoviesApiMixin, BaseListView):
    """Класс представления списка кинопроизведений в виде для API."""

    paginate_by = 50

    def get_context_data(self, *, object_list=None, **kwargs):
        """Формирует список для выдачи по запросу с фильтрацией.

        Осуществляет фильтрацию по жанру и части названия.

        Returns:
            Страницу списка произведений, подходящих под фильтры.
        """  # noqa: DAR101
        queryset = self.get_queryset()
        title = self.request.GET.get('title')
        if title:
            queryset = queryset.filter(title__icontains=title)
        genre_name = self.request.GET.get('genre')
        if genre_name:
            queryset = queryset.filter(genres__name__iexact=genre_name)

        context = self._get_context_paginated(queryset)
        context['title_filter'] = title
        context['genre_filter'] = genre_name

        return context

    def _get_context_paginated(self, queryset):
        paginator, page, queryset, is_paginated = self.paginate_queryset(
            queryset,
            self.paginate_by,
        )
        return {
            'total_pages': paginator.num_pages,
            'count': paginator.count,
            'prev': page.previous_page_number()
            if page.has_previous()
            else None,
            'next': page.next_page_number() if page.has_next() else None,
            'results': list(queryset),
        }


class MoviesDetailApi(MoviesApiMixin, BaseDetailView):
    """Класс детального представления информации о кинопроизведении."""

    def get_context_data(self, **kwargs):
        """Возвращает представления для одного объекта.

        Returns:
            Данные об одном кинопроизведении.
        """  # noqa: DAR101
        return self.get_object()
