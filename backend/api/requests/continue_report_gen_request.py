from pydantic import BaseModel

class ContinueReportGenRequest(BaseModel):
    user_input: str
