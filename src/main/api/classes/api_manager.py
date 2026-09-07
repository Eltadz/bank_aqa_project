from typing import List, Any
from steps.admin_steps import AdminSteps
from steps.user_steps import UserSteps




# для управление всеми степами


class ApiManager:
    def __init__(self, created_obj: List[Any]):
        self.created_obj = created_obj
        self.admin_steps = AdminSteps(created_obj)
        self.user_steps = UserSteps(created_obj)