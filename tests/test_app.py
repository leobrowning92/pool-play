import pytest
from pool.api.main import setup_app
from pool.api.settings import CONFIG
from pool.api.views import get_all_records, add_player


@pytest.fixture
def cli(event_loop, aiohttp_client, test_db):
    app = setup_app(CONFIG)
    return event_loop.run_until_complete(aiohttp_client(app))


async def test_get_all_records(cli):
    async with cli.server.app["db"].acquire() as conn:
        records = await get_all_records(conn)
    assert records == []


async def test_index_handler(cli):
    resp = await cli.get("/")
    assert resp.status == 200
    assert await resp.text() == "[]"


async def test_add_player(cli):
    async with cli.server.app["db"].acquire() as conn:
        id = await add_player(conn, "test", 350)
        assert id[0] == 1
        records = await get_all_records(conn)
        assert records == [(1, "test", 350.0)]


async def test_add_player_handler(cli):
    resp = await cli.post("/player")
    assert resp.status == 201
    assert await resp.text() == "success"
