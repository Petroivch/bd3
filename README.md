# Домашнее задание по SQLAlchemy ORM и Alembic

Проект демонстрирует ORM-моделирование двух связанных таблиц `users` и `posts`,
управление схемой PostgreSQL через Alembic и полный набор CRUD-операций.

## Что реализовано

- ORM-модели `User` и `Post` на SQLAlchemy 2.0;
- связь One-to-Many: у одного пользователя может быть несколько публикаций;
- каскадное удаление публикаций через ORM и `ON DELETE CASCADE` в PostgreSQL;
- первая миграция с таблицами `users` и `posts`;
- вторая миграция после рефакторинга — добавление поля `User.bio`;
- вставка, выборка, обновление и удаление пользователей и публикаций;
- обработка ошибок с обязательным `rollback()` после неудачной записи;
- демонстрационный сценарий, показывающий каскадное удаление.

## Структура проекта

```text
alembic/
  versions/
    20260924_01_create_users_and_posts.py
    20260924_02_add_user_bio.py
  env.py
alembic.ini
crud.py
database.py
docker-compose.yml
main.py
models.py
requirements.txt
```

## Запуск PostgreSQL

Если PostgreSQL не установлен локально, базу можно запустить в контейнере:

```powershell
docker compose up -d
```

Контейнер создаст базу `sqlalchemy_orm_homework` и пользователя `postgres` с
паролем `postgres`.

## Подготовка Python

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
```

По умолчанию используется строка подключения:

```text
postgresql+psycopg://postgres:postgres@localhost:5432/sqlalchemy_orm_homework
```

Для другого подключения задайте переменную окружения:

```powershell
$env:DATABASE_URL="postgresql+psycopg://USER:PASSWORD@HOST:PORT/DATABASE"
```

## Применение миграций

Посмотреть историю миграций и применить их:

```powershell
alembic history
alembic upgrade head
alembic current
```

Последовательность изменений схемы:

1. `20260924_01` — создание таблиц `users` и `posts`;
2. `20260924_02` — добавление нового обязательного поля `users.bio`.

Проверить, что текущие ORM-модели совпадают со схемой базы:

```powershell
alembic check
```

Для отката только второй миграции:

```powershell
alembic downgrade 20260924_01
```

## Демонстрация CRUD

После применения миграций выполните:

```powershell
python main.py
```

Сценарий создаёт пользователя и две публикации, читает и обновляет записи,
затем удаляет пользователя. Обе связанные публикации удаляются каскадно, а
заключительный запрос возвращает пустой список.

Основные функции находятся в `crud.py`:

- `create_user`, `get_user`, `list_users`, `update_user`, `delete_user`;
- `create_post`, `get_post`, `list_posts`, `update_post`, `delete_post`.

Таблицы не создаются через `Base.metadata.create_all()`: состояние схемы
контролируется только миграциями Alembic.
