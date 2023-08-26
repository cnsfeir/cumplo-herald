from cumplo_common.models.channel import ChannelType

from business.channels.ifttt import IFTTTMessage
from models.channel import Channel
from models.message import Message
from models.writer import Writer


class PromisingFundingRequestsWriter(Writer):
    def write_message(self, channel: Channel, content: dict) -> Message:
        """
        Writes the message about the given topic to be sent through the given channel
        """
        match channel.type_:
            case ChannelType.IFTTT:
                return self._write_ifttt_message(content)

        raise NotImplementedError(f"Channel {channel} not implemented")

    def _write_ifttt_message(self, content: dict) -> IFTTTMessage:
        """
        Writes the message about the given topic to be sent through the given channel
        """
        return IFTTTMessage(
            title=content["company_name"],
            message=content["company_rut"],
            url=content["company_funding_url"],
        )
