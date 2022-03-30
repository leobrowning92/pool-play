from aiohttp import web
from pool.api.settings import CONFIG
from pool.db import pg_context
from pool.api.views import routes


def setup_app(config):
    app = web.Application()
    app["config"] = config
    app.add_routes(routes)
    app.cleanup_ctx.append(pg_context)
    return app


if __name__ == "__main__":
    app = setup_app(CONFIG)
    web.run_app(app)
