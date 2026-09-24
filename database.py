"""Настройка подключения к PostgreSQL и фабрика ORM-сессий."""

from __future__ import annotations

import os

from sqlalchemy import create_engine
from sqlalchemy.engine import Engine
from sqlalchemy.orm import Session, sessionmaker


DEFAULT_DATABASE_URL = (
    "postgresql+psycopg://postgres:postgres@localhost:5432/"
    "sqlalchemy_orm_homework"
)


def get_engine(database_url: str | None = None, *, echo: bool = False) -> Engine:
    """Создать SQLAlchemy Engine для PostgreSQL."""
    url = database_url or os.getenv("DATABASE_URL", DEFAULT_DATABASE_URL)
    return create_engine(url, echo=echo, pool_pre_ping=True)


def get_session_factory(engine: Engine) -> sessionmaker[Session]:
    """Создать фабрику сессий, привязанную к переданному Engine."""
    return sessionmaker(bind=engine, expire_on_commit=False)

