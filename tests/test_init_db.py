from pool.init_db import add_dummy_data


def test_create_dummy_data(test_db):
    engine = test_db
    n_players = 3
    add_dummy_data(engine, n_players=n_players)
    assert engine.execute("select count(id) from player").fetchall()[0][0] == n_players
