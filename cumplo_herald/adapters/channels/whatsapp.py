import json
import os
from decimal import Decimal
from logging import getLogger
from typing import Any, override

from cumplo_common.models import ChannelType, FundingRequest, PublicEvent, User, WhatsappConfiguration
from pydantic import Field
from twilio.rest import Client

from cumplo_herald.ports.channel import Channel, Message

logger = getLogger(__name__)

AUTH_TOKEN = os.getenv("TWILIO_AUTH_TOKEN")
ACCOUNT_SID = os.getenv("TWILIO_ACCOUNT_SID")
SENDER_PHONE_NUMBER = os.getenv("TWILIO_SENDER_PHONE_NUMBER")
MESSAGING_SERVICE_SID = os.getenv("TWILIO_MESSAGING_SERVICE_SID")
CONTENT_SID = json.loads(os.getenv("TWILIO_CONTENT_SID", "{}"))


class Whatsapp(Channel):
    configuration: WhatsappConfiguration
    type_ = ChannelType.WHATSAPP
    client: Client
    user: User

    def __init__(self, *args: Any, **kwargs: Any) -> None:
        super().__init__(*args, **kwargs)
        self.client = Client(ACCOUNT_SID, AUTH_TOKEN)

    @override
    def send(self, event: PublicEvent, message: Message) -> None:
        """Send the message to the user."""
        logger.info(f"Sending message: {message.model_dump_json()}")
        self.client.messages.create(
            content_sid=CONTENT_SID[event],
            from_=f"whatsapp:{SENDER_PHONE_NUMBER}",
            to=f"whatsapp:{self.configuration.phone_number}",
            content_variables=message.model_dump_json(),
            messaging_service_sid=MESSAGING_SERVICE_SID,
        )

    @override
    def _write_funding_request_promising(self, content: FundingRequest) -> Message:
        """Write the message for the funding_request.promising event."""

        class WhatsappMessage(Message):
            score: Decimal = Field(ge=0, le=1)
            borrower: str = Field(min_length=1)
            duration: str = Field(min_length=1)
            credit_type: str = Field(min_length=1)
            funding_request_id: str = Field(min_length=1)
            monthly_profit_rate: Decimal = Field(ge=0, le=100)
            installments: str = Field(...)

        monthly_profit_rate = round(Decimal(content.monthly_profit_rate * 100), ndigits=2)

        borrower = content.borrower.name if content.borrower else None
        borrower = borrower or (content.debtors[0].name if content.debtors else None)
        borrower = borrower or "unknown"

        return WhatsappMessage(
            score=content.score,
            borrower=borrower.title(),
            duration=str(content.duration),
            credit_type=content.credit_type.title(),
            funding_request_id=str(content.id),
            monthly_profit_rate=monthly_profit_rate,
            installments=str(content.installments),
        )
