from typing import List, Any

from steps.base_steps import BaseSteps


class UserSteps(BaseSteps):
        def __init__(self, created_obj: List[Any]):
            super().__init__(created_obj)
            