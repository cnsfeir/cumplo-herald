# pylint: disable=raise-missing-from

from http import HTTPStatus
from logging import getLogger
from typing import cast

from cumplo_common.database import firestore
from cumplo_common.models.notification import Notification
from cumplo_common.models.subject import Subject
from cumplo_common.models.template import Template
from cumplo_common.models.user import User
from fastapi import APIRouter, Request
from fastapi.exceptions import HTTPException

from cumplo_herald.business.channels import import_channels
from cumplo_herald.business.content import already_notified
from cumplo_herald.business.writers import import_writer
from cumplo_herald.models.subjects import SubjectContentFactory

logger = getLogger(__name__)

router = APIRouter()


@router.post("/{subject}/{template}/notify", status_code=HTTPStatus.NO_CONTENT)
async def notify_subject(request: Request, subject: Subject, template: Template, payload: dict) -> None:
    """
    Notifies the given subject with the given template and payload.
    """
    user = cast(User, request.state.user)

    if template.subject != subject:
        raise HTTPException(HTTPStatus.NOT_FOUND)

    if not (content := SubjectContentFactory.create_subject_content(subject, payload)):
        raise HTTPException(HTTPStatus.UNPROCESSABLE_ENTITY)

    if already_notified(user, template, content):
        raise HTTPException(HTTPStatus.CONFLICT)

    writer = import_writer(subject, template)(user)

    for channel in import_channels(user):
        message = writer.write_message(channel, content)
        channel.send(message=message)

        id_notification = Notification.build_id(template, content.id)
        firestore.client.notifications.put(str(user.id), id_notification)
