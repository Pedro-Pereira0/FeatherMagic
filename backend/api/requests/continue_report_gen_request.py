from pydantic import BaseModel

class continueReportGenRequest(BaseModel):
    user_input: str
