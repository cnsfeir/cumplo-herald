from logging import getLogger

from cumplo_common.models.subject import Subject
from pydantic import TypeAdapter

from cumplo_herald.models.subjects.funding_requests import FundingRequestContent
from cumplo_herald.models.writer import SubjectContent

logger = getLogger(__name__)


class SubjectContentFactory:
    @staticmethod
    def create_subject_content(subject: Subject, payload: dict) -> SubjectContent | None:
        """
        Creates a new SubjectContent class.
        """
        try:
            match subject:
                case Subject.FUNDING_REQUESTS:
                    return TypeAdapter(FundingRequestContent).validate_python(payload)

        except ValueError:
            logger.warning(f"Invalid payload for subject '{subject}': {payload}")

        return None
