from pool.api.views import index


def setup_routes(app):
    app.router.add_get("/", index)
