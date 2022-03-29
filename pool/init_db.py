from sqlalchemy import create_engine, MetaData
import sqlalchemy as sa
from pool.db import player
import random, string
from pool.api.settings import CONFIG


DSN = "postgresql://{user}:{password}@{host}:{port}/{database}"
admin_config = CONFIG["postgres"].copy()
admin_config["database"] = "postgres"
ADMIN_URL = DSN.format(**admin_config)


def setup_db(config):
    engine = create_engine(ADMIN_URL, isolation_level="AUTOCOMMIT")
    conn = engine.connect()
    conn.execute(f"DROP DATABASE IF EXISTS {config['database']}")
    conn.execute(f"CREATE DATABASE {config['database']} ENCODING 'UTF8'")
    conn.close()


def teardown_db(config):
    engine = create_engine(ADMIN_URL, isolation_level="AUTOCOMMIT")
    conn = engine.connect()
    conn.execute(
        f"""
      SELECT pg_terminate_backend(pg_stat_activity.pid)
      FROM pg_stat_activity
      WHERE pg_stat_activity.datname = '{config['database']}'
        AND pid <> pg_backend_pid();"""
    )
    conn.execute(f"DROP DATABASE IF EXISTS {config['database']}")
    conn.execute(f"CREATE DATABASE {config['database']} ENCODING 'UTF8'")
    conn.close()


def create_tables(engine):
    meta = MetaData()
    meta.create_all(bind=engine, tables=[player])


def add_dummy_data(engine, name_size=3, n_players=10):
    conn = engine.connect()
    new_players = [
        {
            "name": "".join(
                random.choice(string.ascii_lowercase) for _ in range(name_size)
            ),
            "rating": 350,
        }
        for i in range(n_players)
    ]
    conn.execute(player.insert(), new_players)
    conn.close()


if __name__ == "__main__":
    db_url = DSN.format(**CONFIG["postgres"])
    engine = create_engine(db_url)
    setup_db(CONFIG["postgres"])
    create_tables(engine)
    add_dummy_data(engine)
    assert sa.inspect(engine).has_table("player")
