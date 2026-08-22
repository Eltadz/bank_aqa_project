from abc import ABC, abstractmethod
from typing import Dict, Callable
from src.main.api.models.base_model import BaseModel

class Requester(ABC): # абстрактный класс который наследуется от абс предназначен для конкретных реализаций а не для непосредственного использования
    def __init__(self, request_spec: Dict[str, dict | str], response_spec: Callable):
        self.headers = request_spec['headers']   # сохраняем атрибуты класса для дальнейшей реализации в дочерних классах при наследовании
        self.base_url = request_spec['base_url'] # для того чтобы каждый раз не писать реализацию в каждом реквестере
        self.response_spec = response_spec

    @abstractmethod # обязывает что каждый кто наследуется обязан выполнить метод пост
    def post(self, model: BaseModel):
        ...



