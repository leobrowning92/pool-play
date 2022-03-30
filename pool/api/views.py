from aiohttp import web
from pool import db

routes = web.RouteTableDef()


async def get_all_records(conn):
    cursor = await conn.execute(db.player.select())
    records = await cursor.fetchall()
    return records


async def add_player(conn, name, rating):
    sql_string = "INSERT INTO player (name, rating) VALUES (%s, %s) RETURNING id;"
    id = await conn.execute(sql_string, (name, rating))
    return await id.fetchone()


async def get_player(conn, pid):
    sql_string = "SELECT * FROM player where id=%s"
    player = await conn.execute(sql_string, pid)
    return await player.fetchall()


@routes.get("/")
async def index_handler(request):
    async with request.app["db"].acquire() as conn:
        records = await get_all_records(conn)
    return web.Response(text=str(records), status=200)


@routes.post("/player")
async def add_player_handler(request):
    try:
        raw_data = await request.json()
        async with request.app["db"].acquire() as conn:

            pid = await add_player(conn, raw_data["name"], raw_data["rating"])
            return web.Response(
                text=f"success player with {pid[0]} created", status=201
            )
    except Exception as e:
        return web.Response(text=f"{e} for request {request}", status=500)


@routes.get("/player")
async def get_player_handler(request):
    raw_data = await request.json()
    try:
        async with request.app["db"].acquire() as conn:
            player = await get_player(conn, raw_data["id"])
            return web.Response(text=str(player), status=200)
    except Exception as e:
        return web.Response(text=e, status=500)
