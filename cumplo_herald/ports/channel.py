from abc import ABC, abstractmethod
from typing import Any, Protocol, final

from cumplo_common.models import FundingRequest
from cumplo_common.models.channel import ChannelConfiguration, ChannelType
from cumplo_common.models.event import Event
from cumplo_common.models.user import User
from overrides import EnforceOverrides
from pydantic import BaseModel


class Message(BaseModel):
    """Base class for messages to be sent through channels."""


class ChannelPayload(Protocol):
    """Base class for payloads to be sent through channels."""

    id: int


class Channel(EnforceOverrides, ABC):
    configuration: ChannelConfiguration
    type_: ChannelType
    user: User

    def __init__(self, user: User, configuration: ChannelConfiguration) -> None:
        self.configuration = configuration
        self.user = user

    @final
    def notify(self, event: Event, content: ChannelPayload) -> None:
        """Notify the given channel with the given content."""
        message = self.write(event, content)
        self.send(event, message)

    @final
    def write(self, event: Event, content: Any) -> Message:
        """Write the given event with the given payload."""
        match event:
            case Event.FUNDING_REQUEST_PROMISING:
                return self._write_funding_request_promising(content)

        raise NotImplementedError(f"Event {event} not implemented")

    @abstractmethod
    def send(self, event: Event, message: Message) -> None:
        """Send the given content to the given channel."""

    @abstractmethod
    def _write_funding_request_promising(self, content: FundingRequest) -> Message: ...
