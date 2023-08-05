# generated by datamodel-codegen:
#   filename:  data.json
#   timestamp: 2021-01-27T04:36:07+00:00

from __future__ import annotations

from typing import Any, List, Optional

from pydantic import BaseModel


class Datum(BaseModel):
    section_id: str
    section_name: str
    section_type: str
    agent: str
    thumb: str
    art: str
    count: str
    is_active: int
    parent_count: Optional[str] = None
    child_count: Optional[str] = None


class Response(BaseModel):
    result: str
    message: Any
    data: List[Datum]


class Model(BaseModel):
    response: Response
