from datetime import datetime
from sqlalchemy.ext.asyncio import AsyncAttrs
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy import BigInteger, func, ForeignKey


class Base(AsyncAttrs, DeclarativeBase):
    __abstract__ = True


class AiModel(Base):
    __tablename__ = "ai_models"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(unique=True)

    def __str__(self):
        return self.__repr__()

    def __repr__(self):
        return f"<AiModel(id={self.id}, name={self.name})>"


class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True)
    tg_id = mapped_column(BigInteger, unique=True)
    ai_model: Mapped[int] = mapped_column(ForeignKey("ai_models.id"), default=1)

    def __str__(self):
        return self.__repr__()

    def __repr__(self):
        return f"<User(id={self.id}, tg_id={self.tg_id}, ai_model={self.ai_model})>"


class Request(Base):
    __tablename__ = "requests"

    id: Mapped[int] = mapped_column(primary_key=True)
    tg_id: Mapped[int] = mapped_column(BigInteger)
    created_at: Mapped[datetime] = mapped_column(server_default=func.now())

    def __str__(self):
        return self.__repr__()

    def __repr__(self):
        return (
            f"<Request(id={self.id}, tg_id={self.tg_id}, created_at={self.created_at})>"
        )
