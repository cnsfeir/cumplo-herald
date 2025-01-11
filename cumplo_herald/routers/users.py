from http import HTTPStatus
from logging import getLogger
from typing import cast

from cumplo_common.database import firestore
from cumplo_common.models import User
from fastapi import APIRouter
from fastapi.requests import Request

logger = getLogger(__name__)


router = APIRouter(prefix="/users")


@router.post("/channels", status_code=HTTPStatus.OK)
def _clear_users_cache(request: Request) -> None:
    """Clear a specific user from the Firestore cache so it can be updated."""
    user = cast(User, request.state.user)
    logger.debug(f"Clearing user {user.id} from the cache")
    firestore.users.cache.remove(id_user=user.id, api_key=user.api_key)


@router.post("/notifications", status_code=HTTPStatus.OK)
def _update_notifications(request: Request, update: User) -> None:
    """Update the notifications of a specific user."""
    user = cast(User, request.state.user)
    logger.debug(f"Updating notifications for user {user.id}")
    user.notifications.update(update.notifications)
