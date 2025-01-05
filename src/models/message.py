from dataclasses import dataclass
from enum import Enum

@dataclass
class Message():
    user: str
    text: str
    message_type: str

class MessageType(Enum):
    CHAT_MESSAGE = "chat_message"
    LOGIN_MESSAGE = "login_message"
    ERROR_MESSAGE = "error_message"

    def __str__(self):
        return self.value