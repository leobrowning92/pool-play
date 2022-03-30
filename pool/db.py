from sqlalchemy import MetaData, Table, Column, Integer, String, Float
import aiopg.sa

meta = MetaData()

player = Table(
    "player",
    meta,
    Column("id", Integer, autoincrement=True, primary_key=True),
    Column("name", String(100), nullable=True),
    Column("rating", Float, nullable=False),
)


async def pg_context(app):
    conf = app["config"]["postgres"]
    engine = await aiopg.sa.create_engine(**conf)
    app["db"] = engine
    yield
    app["db"].close()
    await app["db"].wait_closed()
