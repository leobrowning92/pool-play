from typing import Callable
from pydantic.dataclasses import dataclass
from marshmallow import Schema, fields, post_load
import functools


@dataclass
class Player:
    id: int
    name: str
    rating: float


class PlayerSchema(Schema):
    id = fields.Int()
    name = fields.Str()
    rating = fields.Float()

    @post_load
    def make_player(self, data: dict, **kwargs):
        return Player(**data)


def request_schema(schema: Schema) -> Callable:
    def dec_schema(func: Callable):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            return func(*args, **kwargs)

        wrapper.request_schema = schema
        return wrapper

    return dec_schema


def result_schema(schema: Schema) -> Callable:
    def dec_schema(func: Callable):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            return func(*args, **kwargs)

        wrapper.result_schema = schema
        return wrapper

    return dec_schema
