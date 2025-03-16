from decimal import Decimal
from typing import override

from cumplo_common.integrations.cloud_tasks import CloudTasks
from cumplo_common.models import ChannelType, FundingRequest, IFTTTConfiguration, PublicEvent
from pydantic import Field

from cumplo_herald.ports.channel import Channel, Message
from cumplo_herald.utils.constants import IFTTT_QUEUE


class IFTTTMessage(Message):
    value1: str = Field(..., alias="message")
    value2: str = Field(..., alias="title")
    value3: str = Field(..., alias="url")


class IFTTT(Channel):
    configuration: IFTTTConfiguration
    type_ = ChannelType.IFTTT

    @property
    def url(self) -> str:
        """Builds the IFTTT trigger URL to send the message to."""
        return f"https://maker.ifttt.com/trigger/{self.configuration.event}/with/key/{self.configuration.key}"

    @override
    def send(self, event: PublicEvent, message: Message) -> None:
        """Send the message to the user."""
        CloudTasks.create_task(
            url=self.url,
            queue=IFTTT_QUEUE,
            payload=message.model_dump(),
            task_id="IFTTT-WEBHOOK",
            is_internal=False,
        )

    @staticmethod
    @override
    def _write_funding_request_promising(content: FundingRequest) -> IFTTTMessage:
        """Write the message for the funding_request.promising event."""
        monthly_profit_rate = round(Decimal(content.monthly_profit_rate * 100), ndigits=2)
        return IFTTTMessage(
            message=f"💹 {monthly_profit_rate}% | ⏳ {content.duration} | 🎖️ {content.score}",
            title=f"N° {content.id} - {content.credit_type.title()}",
            url=content.url,
        )
