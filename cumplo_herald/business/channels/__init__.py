from collections.abc import Iterator
from importlib import import_module
from logging import getLogger

from cumplo_common.models.user import User

from cumplo_herald.models.channel import Channel

logger = getLogger(__name__)


def import_channels(user: User) -> Iterator[Channel]:
    """
    Imports the channels for the given user.
    """
    for channel_type, channel_configuration in user.channels.items():
        if not channel_configuration.enabled:
            logger.info(f"Channel {channel_type} is disabled")
            continue
        try:
            module = import_module(f"cumplo_herald.business.channels.{channel_type.lower()}")
            channel = getattr(module, "channel")
            yield channel(channel_configuration)

        except (ImportError, AttributeError) as exception:
            raise NotImplementedError(f"Channel {channel_type} is not implemented.") from exception
