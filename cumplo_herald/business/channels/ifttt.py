# mypy: disable-error-code="override"

from cumplo_common.integrations.cloud_tasks import create_http_task
from cumplo_common.models.channel import ChannelType, IFTTTConfiguration
from pydantic import Field

from cumplo_herald.models.channel import Channel
from cumplo_herald.models.message import Message
from cumplo_herald.utils.constants import IFTTT_QUEUE


class IFTTTMessage(Message):
    value1: str = Field(..., alias="title")
    value2: str = Field(..., alias="message")
    value3: str = Field(..., alias="url")


class IFTTT(Channel):
    configuration: IFTTTConfiguration
    type_ = ChannelType.IFTTT

    @property
    def url(self) -> str:
        """Builds the IFTTT trigger URL to send the message to"""
        return f"https://maker.ifttt.com/trigger/{self.configuration.event}/with/key/{self.configuration.key}"

    def send(self, message: IFTTTMessage) -> None:
        """
        Sends the message to the user.
        """
        create_http_task(
            url=self.url,
            queue=IFTTT_QUEUE,
            payload=message.model_dump(),
            task_id="IFTTT-WEBHOOK",
            is_internal=False,
        )


channel = IFTTT  # pylint: disable=invalid-name
