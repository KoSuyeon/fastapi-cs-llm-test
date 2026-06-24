# 네트워크를 통해 들어오는 요청을 처리하는 라우터 모듈

from fastapi import APIRouter, HTTPException, Query, Path as PathParam
from app.schemas.cs import DraftRequest, DraftResponse, EchoRequest, EchoResponse
from app.core.state import state
from app.services.llm import make_draft

router = APIRouter()

# 상태 확인 API
@router.get("/health")                  # GET - 서버 살아있는지(모니터링 표준)
def health():
    return {"status": "ok"}

# 이건 현업에서 안 쓰지만 테스트용으로 만들어본 것
@router.post("/echo", response_model=EchoResponse)
def echo(req: EchoRequest):             # 들어온 JSON이 EchoRequest로 자동 검증(빈 message면 422)
    return EchoResponse(you_said=req.message, length=len(req.message))

# 주문 조회 API
@router.get("/orders")                  # 쿼리 파라미터 - 목록 필터/페이지네이션
def list_orders(status: str | None = Query(None, description="상태 필터(예: 배송중)"),
                limit: int = Query(10, ge=1, le=100)):
    items = list(state["orders"].values())
    if status is not None:
        items = [o for o in items if o["order_status"] == status]
    return {"count": len(items[:limit]), "total_matched": len(items), "items": items[:limit]}

# 주문 단건 조회
@router.get("/orders/{order_id}")       # 경로 파라미터 - 주문 단건 조회
def get_order(order_id: str = PathParam(..., description="예: O20260612002")):
    order = state["orders"].get(order_id)
    if order is None:
        raise HTTPException(status_code=400, detail=f"잘못 입력하셨습니다. 주문 {order_id} 를 찾을 수 없습니다.")  # band request → 400
    return order

# 상담사 답변 초안 생성 API
@router.post("/draft", response_model=DraftResponse)   # LLM 엔드포인트
def draft(req: DraftRequest):
    if state["client"] is None:
        raise HTTPException(status_code=503, detail="LLM 미설정: .env 의 GEMINI_API_KEY 를 확인하세요")
    return DraftResponse(inquiry=req.inquiry,
                         answer=make_draft(state["client"], req.inquiry, req.tone))