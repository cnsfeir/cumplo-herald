# pylint: disable=raise-missing-from

from http import HTTPStatus
from logging import getLogger
from typing import cast

from cumplo_common.models.template import Template
from cumplo_common.models.topic import Topic
from cumplo_common.models.user import User
from fastapi import APIRouter, Request
from fastapi.exceptions import HTTPException

from cumplo_herald.business.channels import import_channels
from cumplo_herald.business.content import already_notified
from cumplo_herald.business.writers import import_writer
from cumplo_herald.models.topics import TopicContentFactory

logger = getLogger(__name__)

router = APIRouter()


@router.post("/{topic}/{template}/notify", status_code=HTTPStatus.NO_CONTENT)
async def notify_topic(request: Request, topic: Topic, template: Template, payload: dict) -> None:
    """
    Notifies the given topic with the given template and payload.
    """
    user = cast(User, request.state.user)

    if template.topic != topic:
        raise HTTPException(HTTPStatus.NOT_FOUND)

    if not (content := TopicContentFactory.create_topic_content(topic, payload)):
        raise HTTPException(HTTPStatus.UNPROCESSABLE_ENTITY)

    if already_notified(user, template, content):
        raise HTTPException(HTTPStatus.CONFLICT)

    writer = import_writer(topic, template)(user)

    for channel in import_channels(user):
        message = writer.write_message(channel, content)
        channel.send(message=message)
