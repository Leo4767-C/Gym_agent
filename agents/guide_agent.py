"""Exercise Guide Agent — explains form and technique in Vietnamese."""

from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser
from tenacity import retry, stop_after_attempt, wait_fixed
from agents.llm import get_llm, extract_json
from agents.tools import get_exercise_video

PROMPT = PromptTemplate.from_template(
    """Bạn là huấn luyện viên AI chuyên hướng dẫn kỹ thuật.
Trả lời HOÀN TOÀN bằng TIẾNG VIỆT.

LỊCH SỬ HỘI THOẠI:
{chat_history}

CÂU HỎI HIỆN TẠI: {query}

THÔNG TIN BÀI TẬP:
{context}

LƯU Ý: Nếu user yêu cầu bổ sung thêm chi tiết, hãy dựa vào lịch sử hội thoại.

Trả về CHỈ JSON:
{{
  "thought_process": "<giải thích>",
  "motivational_message": "<khích lệ>",
  "exercise_guide": {{
    "exercise_name": "<tên bài tập chuẩn tiếng Anh hoặc tiếng Việt>",
    "muscle_group": "<nhóm cơ>",
    "equipment": "<thiết bị>",
    "difficulty": "<độ khó>",
    "steps": ["<bước 1>", "<bước 2>", "<bước 3>"],
    "common_mistakes": ["<lỗi 1>", "<lỗi 2>"],
    "breathing": "<cách thở>",
    "sets_reps_recommendation": "<gợi ý sets x reps>"
  }}
}}"""
)


@retry(stop=stop_after_attempt(2), wait=wait_fixed(3))
def generate_guide(query: str, context: str, chat_history: str = "") -> dict:
    chain = PROMPT | get_llm() | StrOutputParser()
    raw = chain.invoke({"query": query, "context": context, "chat_history": chat_history})
    result = extract_json(raw)

    guide = result.get("exercise_guide", {})
    if guide and "exercise_name" in guide:
        video_url = get_exercise_video(guide["exercise_name"])
        if video_url:
            guide["video_url"] = video_url

    result["exercise_guide"] = guide
    result.setdefault("thought_process", "Hướng dẫn chi tiết bài tập kèm video minh hoạ.")
    result.setdefault("motivational_message", "Form chuẩn là nền tảng!")
    return result
