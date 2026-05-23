"""Workout Plan Agent — generates structured exercise plans in Vietnamese."""

from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser
from tenacity import retry, stop_after_attempt, wait_fixed
from agents.llm import get_llm, extract_json

PROMPT = PromptTemplate.from_template(
    """Bạn là một huấn luyện viên cá nhân AI chuyên nghiệp. Hãy tạo kế hoạch tập luyện.
Trả lời HOÀN TOÀN bằng TIẾNG VIỆT.

LỊCH SỬ HỘI THOẠI:
{chat_history}

CÂU HỎI HIỆN TẠI: {query}

CÁC BÀI TẬP CÓ SẴN:
{context}

LƯU Ý: Nếu user yêu cầu chỉnh sửa kết quả trước đó (ví dụ "đổi", "thêm", "bỏ", "ít hơn"), hãy dựa vào lịch sử hội thoại để hiểu ngữ cảnh.

Trả về CHỈ JSON:
{{
  "thought_process": "<1-3 câu giải thích lý do chọn bài tập>",
  "motivational_message": "<1-2 câu khích lệ>",
  "workout_plan": [
    {{
      "exercise_name": "<tên>",
      "muscle_group": "<nhóm cơ>",
      "equipment": "<thiết bị>",
      "sets": <số set>,
      "reps": "<số rep>",
      "rest_seconds": <giây nghỉ>,
      "coaching_tip": "<mẹo>"
    }}
  ]
}}"""
)


@retry(stop=stop_after_attempt(2), wait=wait_fixed(3))
def generate_workout(query: str, context: str, chat_history: str = "") -> dict:
    chain = PROMPT | get_llm() | StrOutputParser()
    raw = chain.invoke({"query": query, "context": context, "chat_history": chat_history})
    result = extract_json(raw)
    result.setdefault("thought_process", "Đã chọn bài tập phù hợp với yêu cầu.")
    result.setdefault("motivational_message", "Bạn làm được! Hãy bắt đầu nào!")
    result.setdefault("workout_plan", [])
    return result
