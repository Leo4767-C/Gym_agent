"""Nutrition Agent — calculates macros & suggests meal plans in Vietnamese."""

from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser
from tenacity import retry, stop_after_attempt, wait_fixed
from agents.llm import get_llm, extract_json

PROMPT = PromptTemplate.from_template(
    """Bạn là chuyên gia dinh dưỡng thể hình AI. Hãy tư vấn dinh dưỡng.
Trả lời HOÀN TOÀN bằng TIẾNG VIỆT.

LỊCH SỬ HỘI THOẠI:
{chat_history}

CÂU HỎI HIỆN TẠI: {query}

THÔNG TIN DINH DƯỠNG:
{context}

Hãy tính TDEE nếu có cân nặng/chiều cao/tuổi. Nếu không, ước lượng cho 70kg.
- Tăng cơ: Protein 2g/kg, Carbs 4-5g/kg, Fat 0.8-1g/kg, TDEE + 300-500 calo
- Giảm mỡ: Protein 2.2g/kg, Carbs 2-3g/kg, Fat 0.8g/kg, TDEE - 300-500 calo

LƯU Ý: Nếu user yêu cầu chỉnh sửa kết quả trước đó, hãy dựa vào lịch sử hội thoại để hiểu ngữ cảnh.

Trả về CHỈ JSON:
{{
  "thought_process": "<giải thích cách tính>",
  "motivational_message": "<khích lệ>",
  "nutrition_advice": {{
    "daily_calories": <calo/ngày>,
    "protein_grams": <gram>,
    "carbs_grams": <gram>,
    "fat_grams": <gram>,
    "goal": "<tăng cơ hoặc giảm mỡ>"
  }},
  "meal_plan": [
    {{"meal_name": "<bữa>", "foods": "<món ăn>", "calories": <calo>, "protein": <gram>}}
  ],
  "supplements": ["<bổ sung nếu cần>"]
}}"""
)


@retry(stop=stop_after_attempt(2), wait=wait_fixed(3))
def generate_nutrition(query: str, context: str, chat_history: str = "") -> dict:
    chain = PROMPT | get_llm() | StrOutputParser()
    raw = chain.invoke({"query": query, "context": context, "chat_history": chat_history})
    result = extract_json(raw)
    result.setdefault("thought_process", "Đã tính toán macro dựa trên mục tiêu.")
    result.setdefault("motivational_message", "Dinh dưỡng đúng cách là 70% thành công!")
    result.setdefault("nutrition_advice", {})
    result.setdefault("meal_plan", [])
    result.setdefault("supplements", [])
    return result
