from src.main.api.models.base_model import BaseModel





class TransferBankAccountRequest(BaseModel):
    fromAccountId: int
    toAccountId: int
    amount: float