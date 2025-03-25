from enum import StrEnum
from logging import getLogger

from cumplo_common.database import firestore
from fastapi import APIRouter, Depends, Form, Request
from twilio.request_validator import RequestValidator
from twilio.rest import Client

from cumplo_herald.utils.constants import TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN, TWILIO_SENDER_PHONE_NUMBER

logger = getLogger(__name__)

router = APIRouter(prefix="/whatsapp")


class TwilioMessageType(StrEnum):
    """Twilio message types."""

    BUTTON = "button"


class TwilioQuickReply(StrEnum):
    """Twilio quick reply types."""

    DISMISS = "dismiss"


async def validate_twilio_request(request: Request) -> None:
    """Validate that the request actually came from Twilio."""
    # NOTE: Use the original URL from the forwarded headers if available
    # This handles the case when requests come through API Gateway
    forwarded_proto = request.headers.get("x-forwarded-proto")
    forwarded_host = request.headers.get("x-forwarded-host")

    if forwarded_proto and forwarded_host:
        url = f"{forwarded_proto}://{forwarded_host}{request.url.path}"
    else:
        # NOTE: Fallback to the request URL if forwarded headers aren't available
        url = str(request.url)

    logger.info(f"Validating Twilio request with URL: {url}")

    form_data = await request.form()
    signature = request.headers.get("x-twilio-signature", "")
    validator = RequestValidator(TWILIO_AUTH_TOKEN)

    return validator.validate(url, dict(form_data), signature)


@router.post("/messages")
async def whatsapp_webhook(
    sender: str | None = Form(None, alias="From"),
    text: str | None = Form(None, alias="ButtonText"),
    payload: str | None = Form(None, alias="ButtonPayload"),
    message_type: str | None = Form(None, alias="MessageType"),
    valid: bool = Depends(validate_twilio_request),  # noqa: FBT001
) -> None:
    """Handle WhatsApp webhook requests for button responses."""
    # if not valid:
    #     raise HTTPException(status_code=HTTPStatus.UNAUTHORIZED, detail="Invalid Twilio signature")

    if not payload or not text or message_type != TwilioMessageType.BUTTON:
        logger.warning("Twilio webhook is missing required fields")
        return

    id_user, id_notification = payload.split(":")

    if not (user := firestore.client.users.get(id_user)):
        logger.error(f"User {id_user} not found")
        return

    if not (notification := user.notifications.get(id_notification)):
        logger.error(f"Notification {id_notification} not found for user {id_user}")
        return

    response = None
    match text.casefold():
        case TwilioQuickReply.DISMISS:
            notification.dismissed = True
            user.notifications[id_notification] = notification
            firestore.client.users.update(user, "notifications")
            response = f"*Funding Request N° {notification.content_id}*\n🔕 *Dismissed*"
        case _:
            logger.warning(f"Unknown button text: {text}")

    if not sender or not sender.startswith("whatsapp:"):
        logger.error("No sender phone number provided in WhatsApp webhook")
        return

    if response:
        logger.info(f"Sending WhatsApp response to {sender}: {response}")
        client = Client(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)
        client.messages.create(to=sender, from_=f"whatsapp:{TWILIO_SENDER_PHONE_NUMBER}", body=response)
