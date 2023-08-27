from collections.abc import Iterator
from importlib import import_module
from logging import getLogger

from cumplo_common.models.user import User

from models.channel import Channel

logger = getLogger(__name__)


def import_channels(user: User) -> Iterator[Channel]:
    """
    Imports the channels for the given user.
    """
    for channel_type, channel_configuration in user.channels.items():
        try:
            module = import_module(f"business.channels.{channel_type}")
            channel = getattr(module, "channel")
            yield channel(channel_configuration)

        except (ImportError, AttributeError) as exception:
            raise NotImplementedError(f"Channel {channel_type} is not implemented.") from exception
