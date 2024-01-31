from logging import getLogger

from cumplo_common.models.notification import Notification
from cumplo_common.models.template import Template
from cumplo_common.models.user import User

from cumplo_herald.models.writer import SubjectContent

logger = getLogger(__name__)


def already_notified(user: User, template: Template, content: SubjectContent) -> bool:
    """
    Checks if the given user has already been notified with the given template and content.

    Args:
        user (User): The user who's being notified
        template (Template): The template used to notify the user
        content (SubjectContent): The content of the notification

    Returns:
        bool: Whether the user has already been notified with the given template and content
    """
    if not template.is_recurring:
        return False

    id_notification = Notification.build_id(template, content.id)
    if not (notification := user.notifications.get(id_notification)):
        return False

    return notification.has_expired
