from logging import getLogger

from cumplo_common.models.topic import Topic
from pydantic import TypeAdapter

from schemas.topics.funding_requests import FundingRequestContent

logger = getLogger(__name__)

TopicContent = FundingRequestContent


class TopicContentFactory:
    @staticmethod
    def create_topic_content(topic: Topic, payload: dict) -> TopicContent | None:
        """
        Creates a new TopicContent class.
        """
        try:
            match topic:
                case Topic.FUNDING_REQUESTS:
                    return TypeAdapter(FundingRequestContent).validate_python(payload)

        except ValueError:
            logger.warning(f"Invalid payload for topic '{topic}': {payload}")

        return None
