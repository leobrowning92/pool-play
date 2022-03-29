from aiohttp import web
from pool.api.routes import setup_routes
from pool.api.settings import CONFIG

if __name__ == "__main__":
    app = web.Application()
    setup_routes(app)
    app["config"] = CONFIG
    web.run_app(app)
