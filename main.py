"""Небольшая демонстрация CRUD и каскадного удаления."""

from __future__ import annotations

import os

from sqlalchemy.exc import SQLAlchemyError

from crud import (
    CrudError,
    create_post,
    create_user,
    delete_user,
    get_user,
    list_posts,
    update_post,
    update_user,
)
from database import get_engine, get_session_factory


def run_demo() -> None:
    """Последовательно выполнить основные операции из задания."""
    engine = get_engine()
    session_factory = get_session_factory(engine)

    with session_factory() as session:
        unique_suffix = os.urandom(4).hex()
        user = create_user(
            session,
            name="Анна Петрова",
            email=f"anna.{unique_suffix}@example.com",
            age=24,
        )
        print("CREATE USER:", user)

        first_post = create_post(
            session,
            user.id,
            title="Первая публикация",
            body="Знакомство с SQLAlchemy ORM.",
        )
        create_post(
            session,
            user.id,
            title="Вторая публикация",
            body="Настройка миграций Alembic.",
        )
        print("CREATE POSTS:", list_posts(session, user.id))

        selected = get_user(session, user.id)
        print("READ USER WITH POSTS:", selected, selected.posts if selected else [])

        updated_user = update_user(
            session,
            user.id,
            {"age": 25, "bio": "Изучаю базы данных и Python."},
        )
        updated_post = update_post(
            session,
            first_post.id,
            {"title": "SQLAlchemy ORM: первые шаги"},
        )
        print("UPDATE USER:", updated_user)
        print("UPDATE POST:", updated_post)

        deleted_posts_count = delete_user(session, user.id)
        remaining_posts = list_posts(session, user.id)
        print(f"DELETE USER: каскадно удалено публикаций — {deleted_posts_count}")
        print("POSTS AFTER CASCADE DELETE:", remaining_posts)


if __name__ == "__main__":
    try:
        run_demo()
    except (CrudError, SQLAlchemyError) as error:
        print(f"Ошибка: {error}")
        raise SystemExit(1) from error

