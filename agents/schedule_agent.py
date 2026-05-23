"""Schedule Agent — generates weekly workout schedules in Vietnamese."""

from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser
from tenacity import retry, stop_after_attempt, wait_fixed
from agents.llm import get_llm, extract_json

PROMPT = PromptTemplate.from_template(
    """Bạn là huấn luyện viên AI. Hãy lên lịch tập tuần.
Trả lời HOÀN TOÀN bằng TIẾNG VIỆT.

LỊCH SỬ HỘI THOẠI:
{chat_history}

CÂU HỎI HIỆN TẠI: {query}

CÁC BÀI TẬP CÓ SẴN:
{context}

Nguyên tắc:
- Tăng cân: Tập nặng 4-5 ngày/tuần, compound, nghỉ ngơi đủ
- Giảm cân: 3-4 ngày tạ + 2-3 ngày cardio, cường độ cao

LƯU Ý: Nếu user yêu cầu chỉnh sửa (ví dụ "đổi sang 3 ngày", "thêm cardio"), hãy dựa vào lịch sử hội thoại.

Trả về CHỈ JSON:
{{
  "thought_process": "<giải thích>",
  "motivational_message": "<khích lệ>",
  "goal": "<tăng cân hoặc giảm cân>",
  "weekly_schedule": [
    {{
      "day": "<Thứ 2/3/4/5/6/7/CN>",
      "focus": "<nhóm cơ hoặc nghỉ>",
      "exercises": ["<tên bài tập>"],
      "duration_minutes": <phút>,
      "notes": "<ghi chú>"
    }}
  ]
}}"""
)


@retry(stop=stop_after_attempt(2), wait=wait_fixed(3))
def generate_schedule(query: str, context: str, chat_history: str = "") -> dict:
    chain = PROMPT | get_llm() | StrOutputParser()
    raw = chain.invoke({"query": query, "context": context, "chat_history": chat_history})
    result = extract_json(raw)
    result.setdefault("thought_process", "Đã xây dựng lịch tập phù hợp.")
    result.setdefault("motivational_message", "Kiên trì là chìa khóa!")
    result.setdefault("weekly_schedule", [])
    result.setdefault("goal", "")
    return result
