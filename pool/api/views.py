from aiohttp import web
from pool import db

routes = web.RouteTableDef()


async def get_all_records(conn):
    cursor = await conn.execute(db.player.select())
    records = await cursor.fetchall()
    return records


async def add_player(conn, name, rating):
    # await conn.execute(db.player.insert(), [{"id":2,"name":name, "rating":rating}])
    sql_string = "INSERT INTO player (name, rating) VALUES (%s, %s) RETURNING id;"
    id = await conn.execute(sql_string, (name, rating))
    return await id.fetchone()


@routes.get("/")
async def index_handler(request):
    async with request.app["db"].acquire() as conn:
        records = await get_all_records(conn)
    return web.Response(text=str(records))


@routes.post("/player")
async def add_player_handler(request):
    async with request.app["db"].acquire() as conn:
        add_player(conn, "test", 350)
        return web.Response(text="success", status=201)
