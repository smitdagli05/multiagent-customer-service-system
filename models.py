from pydantic import BaseModel
from typing import Literal

class CustomerQuery(BaseModel):
    original_message: str
    category: Literal['feature request', 'bug report', 'no action']
    details: str
    urgency: Literal['high', 'medium', 'low']
    summary: str
    description: str
    issue_type: Literal['Bug', 'Story', 'Task']
    priority: Literal['High', 'Medium', 'Low']

