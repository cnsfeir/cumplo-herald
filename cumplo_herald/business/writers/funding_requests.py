# mypy: disable-error-code="override"

from decimal import Decimal

from cumplo_common.models.channel import ChannelType

from cumplo_herald.business.channels.ifttt import IFTTTMessage
from cumplo_herald.models.channel import Channel
from cumplo_herald.models.message import Message
from cumplo_herald.models.topics.funding_requests import FundingRequestContent
from cumplo_herald.models.writer import Writer


class PromisingFundingRequestsWriter(Writer):
    def write_message(self, channel: Channel, content: FundingRequestContent) -> Message:
        """
        Writes the message about the given topic to be sent through the given channel
        """
        match channel.type_:
            case ChannelType.IFTTT:
                return self._write_ifttt_message(content)

        raise NotImplementedError(f"Channel {channel} not implemented")

    def _write_ifttt_message(self, content: FundingRequestContent) -> IFTTTMessage:
        """
        Writes the message about the given topic to be sent through the given channel
        """
        monthly_profit_rate = round(Decimal(content.monthly_profit_rate * 100), ndigits=2)
        return IFTTTMessage(
            title=f"💹 {monthly_profit_rate}% | ⏳ {content.duration} | 🎖️ {content.score}",
            message=f"N° {content.id} - {content.credit_type.title()}",
            url=content.url,
        )
