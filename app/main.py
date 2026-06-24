import os
from contextlib import asynccontextmanager
from fastapi import FastAPI
from dotenv import load_dotenv, find_dotenv
from app.core.state import state
from app.services.orders import load_orders
from app.routers import cs

# .env 파일 로드 - GEMINI_API_KEY 
load_dotenv(find_dotenv(usecwd=True))

#요청마다 새로 만들지 않기 위해 llm client를 만들어두고 전역 공유 state에 보관
@asynccontextmanager
async def lifespan(app: FastAPI):
    # [시작 1회] 무거운 준비물을 만들어 state 에 공유(요청마다 새로 안 만든다)
    state["orders"] = load_orders()                       # 주문 CSV → 메모리 인덱스
    api_key = os.environ.get("GEMINI_API_KEY")
    if api_key:
        from google import genai
        state["client"] = genai.Client(api_key=api_key)   # LLM 클라이언트 1회 생성
    else:
        state["client"] = None                            # 키 없어도 서버는 뜬다(LLM 외 정상)
    yield                                                  # 여기부터 서버 '실행 중'
    state.clear()                                         # 종료 시 정리


app = FastAPI(title="승승장구몰 CS API", version="0.1.0", lifespan=lifespan)
app.include_router(cs.router)             # 라우터 등록
# 실행명령어: uvicorn app.main:app --reload