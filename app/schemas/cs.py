from pydantic import BaseModel, Field

class EchoResponse(BaseModel):
    message: str = Field(..., min_length=1 ,description="되돌려줄 메시지")

class EchoRequest(BaseModel):
    you_said: str
    length: int

class DraftRequest(BaseModel):
    inquiry: str = Field(..., min_length=2)
    tone: str = Field("정중한", description="답변 톤")   # 기본값 → 선택 입력

class DraftResponse(BaseModel):
    inquiry: str
    answer: str