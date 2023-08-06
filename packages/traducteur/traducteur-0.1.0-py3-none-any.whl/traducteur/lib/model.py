from pydantic import BaseModel as BasePydanticModel
from datetime import datetime
from typing import Optional, Any

class BaseModel(BasePydanticModel):
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
    deleted_at: Optional[datetime] = None

    def __init__(__pydantic_self__, **data: Any):
        super().__init__(**data)

    def save(self):
        pass

    def delete(self):
        pass

    @classmethod
    def get(cls, id: str):
        pass


