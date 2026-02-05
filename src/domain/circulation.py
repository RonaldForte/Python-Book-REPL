from dataclasses import dataclass
from datetime import datetime
from typing import Optional

@dataclass
class Circulation:
    book_id: str
    title: str
    author: str
    action: str  #"checkout" or "checkin"
    timestamp: datetime
    notes: Optional[str] = None

    def to_dict(self) -> dict:
        return {
            "action": self.action,
            "title": self.title,
            "author": self.author,
            "timestamp": self.timestamp.isoformat(),
            "book_id": self.book_id
        }