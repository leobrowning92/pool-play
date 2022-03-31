from aiohttp import web
from pool import db
from pool.api.schema import PlayerSchema, response_schema, request_schema

from aiohttp.web import middleware

routes = web.RouteTableDef()


@middleware
async def player_middleware(req, handler):
    """if no schema is specified, assume handler

    deals with request and response individually"""

    if hasattr(handler, "request_schema"):
        req_data = handler.request_schema().load(await req.json())
        req.req_data = req_data

    resp = await handler(req)

    if hasattr(handler, "response_schema"):
        resp_data = handler.response_schema().load(resp)
        resp = web.Response(
            text=str(handler.response_schema().dumps(resp_data)), status=200
        )

    return resp


async def get_all_records(conn):
    cursor = await conn.execute(db.player.select())
    records = await cursor.fetchall()
    return records


async def add_player(conn, name, rating):
    sql_string = (
        "INSERT INTO player (name, rating) VALUES (%s, %s) RETURNING id, name, rating;"
    )
    cursor = await conn.execute(sql_string, (name, rating))
    player_row = await cursor.fetchall()
    return player_row[0]


async def get_player(conn, pid):
    sql_string = "SELECT * FROM player where id=%s"
    cursor = await conn.execute(sql_string, pid)
    player = await cursor.fetchall()
    return player[0]


@routes.get("/")
async def index_handler(request):
    async with request.app["db"].acquire() as conn:
        records = await get_all_records(conn)
    return web.Response(text=str(records), status=200)


@routes.post("/player")
@request_schema(PlayerSchema)
@response_schema(PlayerSchema)
async def add_player_handler(req):
    player = req.req_data
    async with req.app["db"].acquire() as conn:
        player_row = await add_player(conn, player.name, player.rating)
        player_dict = dict(player_row.items())
        return player_dict


@routes.get("/player")
@response_schema(PlayerSchema)
async def get_player_handler(request):
    async with request.app["db"].acquire() as conn:
        player_row = await get_player(conn, request.query["id"])
        player_dict = dict(player_row.items())
        return player_dict
