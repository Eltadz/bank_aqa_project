from src.main.api.models.base_model import BaseModel




class DepositBankAccountResponse(BaseModel):
    id: int
    balance: float