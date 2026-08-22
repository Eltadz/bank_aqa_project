from src.main.api.models.base_model import BaseModel


class DepositCreditAccountResponse(BaseModel):
    id: int
    amount: float
    termMonths: int
    balance: float
    creditId: int
