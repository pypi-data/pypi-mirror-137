from typing import Dict, Any, Optional

from pydantic import BaseModel


class Node(BaseModel):
    label: str
    properties: Optional[Dict[str, Any]]
