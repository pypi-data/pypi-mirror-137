import typing


class EventAction(typing.NamedTuple):
    timestamp: int
    article: str


class User(typing.NamedTuple):
    id: str
