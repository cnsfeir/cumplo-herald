from pydantic import BaseModel


class Message(BaseModel):
    """
    Base class for messages to be sent through channels
    """
