from aiohttp import web
from pool.api.settings import CONFIG
from pool.db import pg_context
from pool.api.views import routes

if __name__ == "__main__":
    app = web.Application()
    app["config"] = CONFIG
    app.add_routes(routes)
    app.cleanup_ctx.append(pg_context)
    web.run_app(app)
