from aiohttp import web
from pool import db

routes = web.RouteTableDef()


@routes.get("/")
async def index(request):
    async with request.app["db"].acquire() as conn:
        cursor = await conn.execute(db.player.select())
        records = await cursor.fetchall()

    return web.Response(text=str(records))
