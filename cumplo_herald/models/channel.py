from abc import ABC, abstractmethod
from typing import TypeVar

from cumplo_common.models.channel import ChannelConfiguration, ChannelType
from pydantic import BaseModel

Model = TypeVar("Model", bound=BaseModel)


class Channel(ABC):
    configuration: ChannelConfiguration
    type_: ChannelType

    def __init__(self, configuration: ChannelConfiguration) -> None:
        self.configuration = configuration

    @abstractmethod
    def send(self, message: Model) -> None:
        """
        Writes the message about the given subject to be sent through the given channel
        """
