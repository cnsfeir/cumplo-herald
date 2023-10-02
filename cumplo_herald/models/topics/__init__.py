from logging import getLogger

from cumplo_common.models.topic import Topic
from pydantic import TypeAdapter

from cumplo_herald.models.topics.funding_requests import FundingRequestContent
from cumplo_herald.models.writer import TopicContent

logger = getLogger(__name__)


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
