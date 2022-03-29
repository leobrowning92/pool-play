from sqlalchemy import MetaData, Table, Column, ForeignKey, Integer, String, Float

meta = MetaData()

player = Table(
    "player",
    meta,
    Column("id", Integer, primary_key=True),
    Column("name", String(100), nullable=True),
    Column("rating", Float, nullable=False),
)
