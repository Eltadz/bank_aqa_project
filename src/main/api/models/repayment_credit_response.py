from src.main.api.models.base_model import BaseModel




class RepaymentCreditResponse(BaseModel):
    creditId: int
    amountDeposited: float