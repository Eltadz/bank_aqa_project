from src.main.api.models.base_model import BaseModel





class TransferBankAccountResponse(BaseModel):
    fromAccountId: int
    toAccountId: int
    fromAccountIdBalance: float