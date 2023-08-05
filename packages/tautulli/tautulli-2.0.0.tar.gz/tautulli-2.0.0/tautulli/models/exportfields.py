# generated by datamodel-codegen:
#   filename:  data.json
#   timestamp: 2021-01-27T04:29:06+00:00

from __future__ import annotations

from typing import Any, Dict

from pydantic import BaseModel


class Response(BaseModel):
    result: str
    message: str
    data: Dict[str, Any]


class Model(BaseModel):
    response: Response
