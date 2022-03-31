import pytest
import json
from pool.api.main import setup_app
from pool.api.settings import CONFIG
from pool.api.views import get_all_records, add_player, get_player


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
        player_row = await add_player(conn, "test", 350)
        assert player_row == (1, "test", 350.0)
        records = await get_all_records(conn)
        assert records == [(1, "test", 350.0)]


async def test_add_player_handler(cli):
    resp = await cli.post("/player", json={"name": "test", "rating": 350.0})
    text = await resp.text()
    assert json.loads(text) == {"name": "test", "rating": 350.0, "id": 1}
    assert resp.status == 200

    async with cli.server.app["db"].acquire() as conn:
        records = await get_all_records(conn)
        assert records == [(1, "test", 350.0)]


@pytest.fixture(scope="function")
async def single_player_db(cli, test_db):
    async with cli.server.app["db"].acquire() as conn:
        player_row = await add_player(conn, "test", 350)
        assert player_row == (1, "test", 350.0)


async def test_get_player(cli, single_player_db):
    async with cli.server.app["db"].acquire() as conn:
        player = get_player(conn, 1)
        assert await player == (1, "test", 350.0)


async def test_get_player_handler(cli, single_player_db):
    async with cli.server.app["db"].acquire() as conn:
        player = await get_player(conn, 1)
        assert player == (1, "test", 350.0)
    resp = await cli.get("/player?id=1")
    text = await resp.text()
    assert json.loads(text) == {"name": "test", "rating": 350.0, "id": 1}
    assert resp.status == 200
