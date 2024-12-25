from dataclasses import dataclass

@dataclass
class Message():
    user: str
    text: str
    message_type: str