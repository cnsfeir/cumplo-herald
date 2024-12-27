# pylint: disable=missing-function-docstring

from typing import Protocol

from cumplo_common.models.user import User

from cumplo_herald.models.channel import Channel
from cumplo_herald.models.message import Message


class SubjectContent(Protocol):
    id: int


class Writer(Protocol):
    def __init__(self, user: User) -> None: ...

    def write_message(self, channel: Channel, content: SubjectContent) -> Message: ...
