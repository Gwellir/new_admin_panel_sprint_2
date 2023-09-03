"""Преобразует связи M2M через FK в связи через M2MField."""

from django.db import migrations, models


class Migration(migrations.Migration):
    """Класс, описывающий миграцию Django."""

    dependencies = [
        ('movies', '0002_alter_personfilmwork_idx_and_more'),
    ]

    state_operations = [
        migrations.AddField(
            model_name='filmwork',
            name='genres',
            field=models.ManyToManyField(
                related_name='film_works',
                through='movies.GenreFilmWork',
                to='movies.genre',
            ),
        ),
        migrations.AddField(
            model_name='filmwork',
            name='persons',
            field=models.ManyToManyField(
                related_name='film_works',
                through='movies.PersonFilmWork',
                to='movies.person',
            ),
        ),
        migrations.AlterField(
            model_name='genrefilmwork',
            name='film_work',
            field=models.ForeignKey(
                on_delete=models.deletion.CASCADE,
                to='movies.filmwork',
            ),
        ),
        migrations.AlterField(
            model_name='personfilmwork',
            name='person',
            field=models.ForeignKey(
                null=True,
                on_delete=models.deletion.DO_NOTHING,
                to='movies.person',
            ),
        ),
    ]

    operations = [
        migrations.SeparateDatabaseAndState(
            state_operations=state_operations,
        ),
    ]
