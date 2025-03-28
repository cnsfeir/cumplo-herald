from typing import override

from cumplo_common.integrations.cloud_tasks import CloudTasks
from cumplo_common.models import ChannelType, FundingRequest, PublicEvent, WebhookConfiguration

from cumplo_herald.ports.channel import Channel, Message
from cumplo_herald.utils.constants import WEBHOOK_QUEUE


class WebhookMessage(Message):
    event: PublicEvent
    data: dict


class Webhook(Channel):
    configuration: WebhookConfiguration
    type_ = ChannelType.WEBHOOK

    @override
    def send(self, event: PublicEvent, message: Message) -> None:
        """Send the message to the user."""
        CloudTasks.create_task(
            url=self.configuration.url,
            queue=WEBHOOK_QUEUE,
            payload=message.model_dump(),
            task_id="WEBHOOK-WEBHOOK",
            is_internal=False,
        )

    @staticmethod
    @override
    def _write_funding_request_promising(content: FundingRequest) -> WebhookMessage:
        """Write the message for the funding_request.promising event."""
        return WebhookMessage(event=PublicEvent.FUNDING_REQUEST_PROMISING, data=content.json())
