from src.main.api.models.base_model import BaseModel






class DepositCreditAccountRequest(BaseModel):
    accountId: int
    amount: float
    termMonths: int




class DepositCreditAccountResponse(BaseModel):
    id: int
    amount: float
    termMonths: int
    balance: float
    creditId: int

