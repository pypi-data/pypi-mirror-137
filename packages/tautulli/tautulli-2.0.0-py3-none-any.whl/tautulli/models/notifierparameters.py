# generated by datamodel-codegen:
#   filename:  data.json
#   timestamp: 2021-01-27T03:54:30+00:00

from __future__ import annotations

from typing import Any, List

from pydantic import BaseModel


class Datum(BaseModel):
    name: str
    type: str
    value: str


class Response(BaseModel):
    result: str
    message: Any
    data: List[Datum]


class Model(BaseModel):
    response: Response
