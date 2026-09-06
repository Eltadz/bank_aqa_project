from dataclasses import dataclass
from enum import Enum
from typing import Optional, Type

from models.create_user_request import CreateUserRequest
from models.create_user_response import CreateUserResponse
from src.main.api.models.base_model import BaseModel


# для управления эндпоинатми и реквест и респонс спеками





@dataclass
class EndpointConfiguration:
    url: str
    request_model: Optional[Type[BaseModel]]
    response_model: Optional[Type[BaseModel]]




class Endpoint(Enum):

    ADMIN_CREATE_USER = EndpointConfiguration(
        request_model = CreateUserRequest,
        url = '/admin/create',
        response_model = CreateUserResponse
    )


    ADMIN_DELETE_USER = EndpointConfiguration(
        request_model = None,
        url = '/admin/users',
        response_model = None
    )


