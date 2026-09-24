"""CRUD-операции над ORM-моделями User и Post."""

from __future__ import annotations

from collections.abc import Mapping
from typing import Any

from sqlalchemy import select
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session, selectinload

from models import Post, User


class CrudError(RuntimeError):
    """Ошибка выполнения изменяющей операции с базой данных."""


class RecordNotFoundError(CrudError):
    """Запрошенная запись не найдена."""


def create_user(
    session: Session,
    name: str,
    email: str,
    age: int,
    bio: str = "",
) -> User:
    """Добавить пользователя и сохранить изменения."""
    user = User(name=name, email=email, age=age, bio=bio)
    session.add(user)
    try:
        session.commit()
        return user
    except SQLAlchemyError as error:
        session.rollback()
        raise CrudError(f"Не удалось создать пользователя: {error}") from error


def get_user(session: Session, user_id: int) -> User | None:
    """Получить пользователя вместе с публикациями по идентификатору."""
    statement = (
        select(User)
        .options(selectinload(User.posts))
        .where(User.id == user_id)
    )
    return session.scalars(statement).one_or_none()


def list_users(session: Session) -> list[User]:
    """Получить всех пользователей в порядке возрастания id."""
    statement = select(User).options(selectinload(User.posts)).order_by(User.id)
    return list(session.scalars(statement).all())


def update_user(
    session: Session,
    user_id: int,
    values: Mapping[str, Any],
) -> User:
    """Изменить разрешённые поля пользователя ORM-методами."""
    allowed_fields = {"name", "email", "age", "bio"}
    changes = {key: value for key, value in values.items() if key in allowed_fields}
    if not changes:
        raise ValueError("Укажите хотя бы одно поле: name, email, age или bio")

    user = session.get(User, user_id)
    if user is None:
        raise RecordNotFoundError(f"Пользователь с id={user_id} не найден")

    for field, value in changes.items():
        setattr(user, field, value)

    try:
        session.commit()
        return user
    except SQLAlchemyError as error:
        session.rollback()
        raise CrudError(f"Не удалось обновить пользователя: {error}") from error


def delete_user(session: Session, user_id: int) -> int:
    """Удалить пользователя и вернуть число каскадно удалённых публикаций."""
    user = get_user(session, user_id)
    if user is None:
        raise RecordNotFoundError(f"Пользователь с id={user_id} не найден")

    deleted_posts_count = len(user.posts)
    session.delete(user)
    try:
        session.commit()
        return deleted_posts_count
    except SQLAlchemyError as error:
        session.rollback()
        raise CrudError(f"Не удалось удалить пользователя: {error}") from error


def create_post(session: Session, user_id: int, title: str, body: str) -> Post:
    """Добавить публикацию существующему пользователю."""
    if session.get(User, user_id) is None:
        raise RecordNotFoundError(f"Пользователь с id={user_id} не найден")

    post = Post(user_id=user_id, title=title, body=body)
    session.add(post)
    try:
        session.commit()
        return post
    except SQLAlchemyError as error:
        session.rollback()
        raise CrudError(f"Не удалось создать публикацию: {error}") from error


def get_post(session: Session, post_id: int) -> Post | None:
    """Получить одну публикацию по идентификатору."""
    return session.get(Post, post_id)


def list_posts(session: Session, user_id: int | None = None) -> list[Post]:
    """Получить все публикации либо публикации выбранного пользователя."""
    statement = select(Post)
    if user_id is not None:
        statement = statement.where(Post.user_id == user_id)
    statement = statement.order_by(Post.id)
    return list(session.scalars(statement).all())


def update_post(
    session: Session,
    post_id: int,
    values: Mapping[str, Any],
) -> Post:
    """Изменить заголовок или текст публикации."""
    allowed_fields = {"title", "body"}
    changes = {key: value for key, value in values.items() if key in allowed_fields}
    if not changes:
        raise ValueError("Укажите хотя бы одно поле: title или body")

    post = session.get(Post, post_id)
    if post is None:
        raise RecordNotFoundError(f"Публикация с id={post_id} не найдена")

    for field, value in changes.items():
        setattr(post, field, value)

    try:
        session.commit()
        return post
    except SQLAlchemyError as error:
        session.rollback()
        raise CrudError(f"Не удалось обновить публикацию: {error}") from error


def delete_post(session: Session, post_id: int) -> Post:
    """Удалить одну публикацию."""
    post = session.get(Post, post_id)
    if post is None:
        raise RecordNotFoundError(f"Публикация с id={post_id} не найдена")

    session.delete(post)
    try:
        session.commit()
        return post
    except SQLAlchemyError as error:
        session.rollback()
        raise CrudError(f"Не удалось удалить публикацию: {error}") from error
