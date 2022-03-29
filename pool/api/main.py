from aiohttp import web
from pool.api.routes import setup_routes
from pool.api.settings import CONFIG
from pool.db import pg_context

if __name__ == "__main__":
    app = web.Application()
    app["config"] = CONFIG
    setup_routes(app)
    app.cleanup_ctx.append(pg_context)
    web.run_app(app)
