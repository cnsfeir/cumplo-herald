from http import HTTPStatus
from logging import getLogger
from typing import cast

from cumplo_common.database import firestore
from cumplo_common.models.event import Event
from cumplo_common.models.notification import Notification
from cumplo_common.models.user import User
from fastapi import APIRouter, HTTPException, Request

from cumplo_herald.adapters.channels import CHANNELS_BY_TYPE

logger = getLogger(__name__)

router = APIRouter()


@router.post("/{event}/notify", status_code=HTTPStatus.NO_CONTENT)
async def notify_event(request: Request, event: Event, payload: dict) -> None:
    """
    Notifies the given event with the given payload through the user's channels.

    Raises:
        HTTPException: If the notification was already sent (status 208 ALREADY_REPORTED)

    """
    user = cast(User, request.state.user)
    content = event.model.model_validate(payload)

    if user.already_notified(event, content):
        raise HTTPException(HTTPStatus.ALREADY_REPORTED)

    for channel_configuration in user.channels.values():
        if not channel_configuration.enabled:
            logger.info(f"Channel {channel_configuration.id} is disabled")
            continue

        if not channel_configuration.event_enabled(event):
            logger.info(f"Channel {channel_configuration.id} is not enabled for event {event}")
            continue

        channel = CHANNELS_BY_TYPE[channel_configuration.type_](user, channel_configuration)
        channel.notify(event, content)

        id_notification = Notification.build_id(event, content.id)
        firestore.client.notifications.put(str(user.id), id_notification)
