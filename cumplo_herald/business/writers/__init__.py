from importlib import import_module
from logging import getLogger

from caseconverter import pascalcase, snakecase
from cumplo_common.models.template import Template
from cumplo_common.models.topic import Topic

from cumplo_herald.models.writer import Writer

logger = getLogger(__name__)


def import_writer(topic: Topic, template: Template) -> type[Writer]:
    """
    Imports the writer class for the given topic and template
    """
    module = import_module(f"business.writers.{snakecase(topic)}")
    writer = getattr(module, pascalcase(f"{template}-{topic}-writer"))
    return writer
