from dataclasses import dataclass
import uuid
from typing import Optional

@dataclass
class Starter:
    id: str
    owner_capsule_id: str
    name: Optional[str] = None
    
    @classmethod
    def generate(cls, owner_capsule_id: str) -> 'Starter':
        return cls(
            id=str(uuid.uuid4()),
            owner_capsule_id=owner_capsule_id
        )
