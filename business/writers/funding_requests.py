from decimal import Decimal

from cumplo_common.models.channel import ChannelType

from business.channels.ifttt import IFTTTMessage
from models.channel import Channel
from models.message import Message
from models.writer import Writer
from schemas.topics.funding_requests import FundingRequestContent


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
