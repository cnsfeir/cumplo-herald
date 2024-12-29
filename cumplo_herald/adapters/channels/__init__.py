from .ifttt import IFTTT
from .webhook import Webhook
from .whatsapp import Whatsapp

CHANNELS_BY_TYPE = {
    IFTTT.type_: IFTTT,
    Whatsapp.type_: Whatsapp,
    Webhook.type_: Webhook,
}
