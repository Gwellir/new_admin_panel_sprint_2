## Порядок настройки и развёртывания

### Основной образ админки и API в связке с uwsgi и nginx.

Скопируйте репозиторий на локальный компьютер с установленным Docker.

Перейдите в папку `docker_compose/movies_admin` и выполните `docker compose up -d`.
Будет создан образ докера для основного скрипта для работы с админкой кинопроизведений,
в нём будет установлен gettext и выполнена компиляция .po файлов, для настройки параметров используется
файл .env.

Переменные окружения для подключения к базе данных описаны в файле .env.example
Не забудьте сформировать полный .env файл в папке с файлами compose.

Пример дополнительной настройки для проверочного подключения:
```
DB_NAME=movies_database
DB_USER=app
DB_PASSWORD=123qwe
SECRET_KEY=django-insecure-zlqy)&i@b^t4gt5!i#q)z^4(r&vg%x0ccgg_u$4($xnj($gueg
DJANGO_SUPERUSER_PASSWORD=admin
DJANGO_SUPERUSER_USERNAME=admin
DJANGO_SUPERUSER_EMAIL=admin@localhost
```

Теперь, для заполнения БД проверочными данными вы можете запустить 
`docker exec -it service python manage.py loaddata /opt/app/fixtures/fixture.json`.
Дождитесь завершения загрузки фикстуры с данными по кинопроизведениям в БД. Суперпользовательская запись admin:admin
также будет внесена в базу.

После этого админка с записями должна стать доступна на локальном хосте по адресу http://localhost/admin/

Также доступно API V1 по адресу http://localhost/api/v1/movies/, оно поддерживает параметры: 
- page (номер страницы выдачи)
- title (часть названия фильма)
- genre (точное название жанра без учёта регистра)

Доступ к API требует логина.

### Дебажный образ со swagger

Выполните в папке `docker_compose/movies_admin` `docker compose -f ./docker-compose.swagger.yml up`

Админка с API в этой конфигурации запускаются в другом контейнере service-debug.

Если шаги по наполнению БД данными ещё не были выполнены - запустите `docker exec -it service python manage.py loaddata /opt/app/fixtures/fixture.json`.
Дождитесь завершения загрузки фикстуры с данными по кинопроизведениям в БД. Суперпользовательская запись admin:admin
также будет создана.

Теперь кроме указанных выше эндпоинтов станет доступен swagger-ui на http://localhost:8080/. Данные по
поддерживаемым параметрам запроса внесены в openapi.yml.

---


# Проектное задание: Docker-compose

Приступим к улучшению сервиса в области DevOps. Настройте запуск всех компонентов системы — Django, Nginx и Postgresql — с использованием docker-compose.

Для упрощения выполнения задания мы подготовили проект, где настроена работа связки Django + uWSGI + Nginx + Docker. Вы можете взять его за основу, но его придётся дополнительно доработать, чтобы подключить Postgres, а также устранить мелкие ошибки в конфигурировании Django: например, `debug = True` или отсутствие настроек чтения переменных окружения.

Сама заготовка уже показывает админку с примером одного метода API. Однако статика не собирается, миграций нет, конфиги Nginx, uWSGI и Docker, возможно, придётся подправить.

Если вы считаете, что всё нужно сделать по-другому, воспользуйтесь пустой заготовкой проекта и напишите его самостоятельно.

**Требования к работе:**

- Напишите dockerfile для Django.
- Для настройки Nginx можно пользоваться наработками из этой темы, но ревьюеры будут запускать ваше решение. Перед сдачей проекта убедитесь, что всё работает правильно.
- Уберите версию Nginx из заголовков. Версии любого ПО лучше скрывать от посторонних глаз, чтобы вашу админку случайно не взломали. Найдите необходимую настройку в официальной документации и проверьте, что она работает корректно. Убедиться в этом можно с помощью «Инструментов разработчика» в браузере.
- Отдавайте статические файлы Django через Nginx, чтобы не нагружать сервис дополнительными запросами. Перепишите `location` таким образом, чтобы запросы на `/admin` шли без поиска статического контента. То есть, минуя директиву `try_files $uri @backend;`.

**Подсказки и советы:**

- Теории на платформе должно быть достаточно для понимания принципов конфигурирования. Если у вас появятся какие-то вопросы по параметрам, ищите ответы [в официальной документации](https://nginx.org/ru/).
- Для выполнения задачи про `/admin` нужно посмотреть порядок поиска `location`.
- Для работы со статикой нужно подумать, как залить данные в файловую систему контейнера с Nginx.
- Для задания дана базовая структура, которой можно пользоваться.
- При настройке docker-compose важно проверять пути до папок. Большинство проблем связанно именно с этим.
