from importlib import import_module
from logging import getLogger

from caseconverter import pascalcase, snakecase
from cumplo_common.models.template import Template
from cumplo_common.models.subject import Subject

from cumplo_herald.models.writer import Writer

logger = getLogger(__name__)


def import_writer(subject: Subject, template: Template) -> type[Writer]:
    """
    Imports the writer class for the given subject and template
    """
    module = import_module(f"cumplo_herald.business.writers.{snakecase(subject)}")
    writer = getattr(module, pascalcase(f"{template}-{subject}-writer"))
    return writer
