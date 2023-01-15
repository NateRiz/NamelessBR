from dataclasses import dataclass


@dataclass
class Message:
    owner_id: int
    message: dict
