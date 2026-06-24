# '주방' - LLM 호출 서비스(라우터는 make_draft만 부른다)
from app.core.config import GEMINI_MODEL


def make_draft(client, inquiry: str, tone: str) -> str:
    """공유 클라이언트로 문의에 대한 상담사 답변 초안을 생성한다."""
    prompt = (f"너는 승승장구몰 고객상담사다. {tone} 말투로 2~3문장으로 답하라.\n"
              f"문의: {inquiry}")
    return client.models.generate_content(model=GEMINI_MODEL, contents=prompt).text