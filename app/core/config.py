from pathlib import Path

GEMINI_MODEL = "gemini-2.5-flash-lite"          # 답변 생성에 쓸 모델 이름

# 어디서 실행해도 CSV 경로를 찾아가도록
_ROOT = next((p for p in [Path(__file__).resolve().parent, *Path(__file__).resolve().parents]
              if (p / "data").exists()), Path(__file__).resolve().parents[2])
ORDERS_CSV = _ROOT / "data" / "orders.csv"