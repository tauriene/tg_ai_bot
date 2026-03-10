from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession

engine = create_async_engine(url="sqlite+aiosqlite:///db.sqlite")
session_maker = async_sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)
