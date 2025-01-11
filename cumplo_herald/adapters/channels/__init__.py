from cumplo_common.models.channel import ChannelType

from cumplo_herald.ports.channel import Channel

from .ifttt import IFTTT
from .webhook import Webhook
from .whatsapp import Whatsapp

CHANNELS_BY_TYPE: dict[ChannelType, type[Channel]] = {
    Whatsapp.type_: Whatsapp,
    Webhook.type_: Webhook,
    IFTTT.type_: IFTTT,
}
