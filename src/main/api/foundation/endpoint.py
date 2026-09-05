from typing import Optional, Type

from main.api.models.base_model import BaseModel
from dataclasses import dataclass




@dataclass
class EndpointConfiguration:
    url: str
    request_model: Optional[Type[BaseModel]]
    response_model: Optional[Type[BaseModel]]



class Endpoint:
    