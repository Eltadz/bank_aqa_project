from src.main.api.models.base_model import BaseModel




class DepositBankAccountRequest(BaseModel):
    accountId: int
    amount: float