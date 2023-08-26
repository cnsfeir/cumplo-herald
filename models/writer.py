# pylint: disable=missing-function-docstring

from typing import Any, Protocol

from cumplo_common.models.user import User

from models.channel import Channel
from models.message import Message


class Writer(Protocol):
    def __init__(self, user: User) -> None:
        ...

    def write_message(self, channel: Channel, content: Any) -> Message:
        ...
