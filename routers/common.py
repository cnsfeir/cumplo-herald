from http import HTTPStatus
from logging import getLogger
from typing import Any, cast

from cumplo_common.models.template import Template
from cumplo_common.models.topic import Topic
from cumplo_common.models.user import User
from fastapi import APIRouter, Request
from fastapi.exceptions import HTTPException

from business.channels import import_channels
from business.writers import import_writer

logger = getLogger(__name__)

router = APIRouter()


@router.post("/{topic}/{template}/notify", status_code=HTTPStatus.NO_CONTENT)
async def notify_topic(request: Request, topic: Topic, template: Template, payload: Any) -> None:
    """
    Notifies the given topic with the given template and payload.
    """
    user = cast(User, request.state.user)

    if template.topic != topic:
        raise HTTPException(HTTPStatus.BAD_REQUEST, detail=f"Topic {topic} doesn't have {template} template")

    writer = import_writer(topic, template)(user)

    for channel in import_channels(user):
        message = writer.write_message(channel, payload)
        channel.send(message=message)
