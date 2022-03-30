from pool.api.schema import Player, PlayerSchema, request_schema


def test_request_schema():
    @request_schema(PlayerSchema)
    def f():
        return "complete"

    assert f.request_schema is PlayerSchema


def test_player_schema():

    json_blob = {"id": 1, "name": "test", "rating": 350}
    ps = PlayerSchema()
    player = ps.load(json_blob)
    player is Player
    player.id == 1
    player.name == "test"
    player.rating == 350.0
