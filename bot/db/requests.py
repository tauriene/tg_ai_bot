from datetime import datetime
from typing import Sequence

from sqlalchemy import select, func, update
from sqlalchemy.ext.asyncio import AsyncSession

from bot.db.models import User, Request, AiModel
from bot.db.engine import session_maker


def connection(function):
    async def inner(*args, **kwargs):
        async with session_maker() as session:
            return await function(session, *args, **kwargs)

    return inner


@connection
async def add_user(session: AsyncSession, tg_id: int) -> None:
    async with session.begin():
        stmt = select(User).where(User.tg_id == tg_id)
        user = await session.scalar(stmt)

        if not user:
            session.add(User(tg_id=tg_id))


@connection
async def get_user(session: AsyncSession, tg_id: int) -> User | None:
    return await session.scalar(select(User).where(User.tg_id == tg_id))


@connection
async def add_request(session: AsyncSession, tg_id: int) -> None:
    async with session.begin():
        req = Request(tg_id=tg_id)
        session.add(req)


@connection
async def get_requests_count(session: AsyncSession, tg_id: int) -> int:
    stmt = select(func.count(Request.id)).where(
        Request.tg_id == tg_id,
        func.date(Request.created_at) == datetime.utcnow().date(),
    )
    return await session.scalar(stmt) or 0


@connection
async def get_ai_models(session: AsyncSession) -> Sequence[AiModel]:
    result = await session.scalars(select(AiModel))
    return result.all()


@connection
async def set_user_ai_model(
    session: AsyncSession, tg_id: int, ai_model_id: int
) -> None:
    async with session.begin():
        stmt = update(User).where(User.tg_id == tg_id).values(ai_model=ai_model_id)
        await session.execute(stmt)


@connection
async def get_user_ai_model(session: AsyncSession, tg_id: int) -> AiModel:
    stmt = select(User).where(User.tg_id == tg_id)
    user = await session.scalar(stmt)

    stmt = select(AiModel).where(AiModel.id == user.ai_model)
    return await session.scalar(stmt)
