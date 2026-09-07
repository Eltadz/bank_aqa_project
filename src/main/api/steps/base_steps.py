

from typing import List, Any


# будем сохронять сюда айди новых юзеров которых создали
class BaseSteps:
    def __init__(self, created_obj: List[Any]):
        self.created_obj = created_obj