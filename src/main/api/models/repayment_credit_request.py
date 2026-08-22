from src.main.api.models.base_model import BaseModel



class RepaymentCreditRequest(BaseModel):
    creditId: int
    accountId: int
    amount: float