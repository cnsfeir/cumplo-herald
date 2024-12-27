from collections.abc import Iterator
from importlib import import_module
from logging import getLogger

from cumplo_common.models.user import User

from cumplo_herald.models.channel import Channel

logger = getLogger(__name__)


def import_channels(user: User) -> Iterator[Channel]:
    """
    Import the channels for the given user.

    Yields:
        Channel: An instance of a Channel.

    """
    for channel_configuration in user.channels.values():
        if not channel_configuration.enabled:
            logger.info(f"Channel {channel_configuration.id} is disabled")
            continue
        try:
            module = import_module(f"cumplo_herald.business.channels.{channel_configuration.type_.lower()}")
            channel = module.channel
            yield channel(channel_configuration)

        except (ImportError, AttributeError) as exception:
            raise NotImplementedError(f"Channel {channel_configuration.type_} is not implemented.") from exception
