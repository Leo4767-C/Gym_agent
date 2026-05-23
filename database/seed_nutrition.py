"""Nutrition seed data — Vietnamese food & supplement knowledge base."""

from langchain_core.documents import Document

NUTRITION_DOCUMENTS: list[Document] = [
    # ── PROTEIN ──
    Document(page_content="Ức gà: 31g protein, 3.6g fat, 0g carbs per 100g. Nguồn protein nạc tốt nhất cho tăng cơ. Nên nướng hoặc hấp.",
        metadata={"name": "Ức gà", "category": "protein", "goal": "muscle_gain", "calories_per_100g": 165, "protein_per_100g": 31, "meal_type": "lunch"}),
    Document(page_content="Trứng gà: 13g protein, 11g fat, 1.1g carbs per 100g. Protein hoàn chỉnh, 1 quả ~70 calo. Ăn cả lòng đỏ để có choline và vitamin D.",
        metadata={"name": "Trứng gà", "category": "protein", "goal": "muscle_gain", "calories_per_100g": 155, "protein_per_100g": 13, "meal_type": "breakfast"}),
    Document(page_content="Cá hồi: 20g protein, 13g fat (omega-3), 0g carbs per 100g. Omega-3 giúp giảm viêm cơ sau tập.",
        metadata={"name": "Cá hồi", "category": "protein", "goal": "muscle_gain", "calories_per_100g": 208, "protein_per_100g": 20, "meal_type": "dinner"}),
    Document(page_content="Thịt bò nạc: 26g protein, 11g fat, 0g carbs per 100g. Giàu creatine tự nhiên, sắt, kẽm.",
        metadata={"name": "Thịt bò nạc", "category": "protein", "goal": "muscle_gain", "calories_per_100g": 250, "protein_per_100g": 26, "meal_type": "lunch"}),
    Document(page_content="Whey Protein: 80g protein, 5g fat, 5g carbs per 100g bột. Hấp thu nhanh, lý tưởng sau tập. 1 scoop ~25g protein.",
        metadata={"name": "Whey Protein", "category": "supplement", "goal": "muscle_gain", "calories_per_100g": 400, "protein_per_100g": 80, "meal_type": "snack"}),

    # ── CARBS ──
    Document(page_content="Cơm trắng: 2.7g protein, 0.3g fat, 28g carbs per 100g. Nguồn năng lượng chính. 1 bát ~200 calo.",
        metadata={"name": "Cơm trắng", "category": "carbs", "goal": "muscle_gain", "calories_per_100g": 130, "protein_per_100g": 2.7, "meal_type": "lunch"}),
    Document(page_content="Yến mạch: 17g protein, 7g fat, 66g carbs per 100g. Carbs phức hợp, giàu chất xơ, tốt cho tiêu hóa.",
        metadata={"name": "Yến mạch", "category": "carbs", "goal": "muscle_gain", "calories_per_100g": 389, "protein_per_100g": 17, "meal_type": "breakfast"}),
    Document(page_content="Khoai lang: 1.6g protein, 0.1g fat, 20g carbs per 100g. GI thấp, giàu vitamin A. Lý tưởng cho giảm cân.",
        metadata={"name": "Khoai lang", "category": "carbs", "goal": "fat_loss", "calories_per_100g": 86, "protein_per_100g": 1.6, "meal_type": "lunch"}),
    Document(page_content="Chuối: 1.1g protein, 0.3g fat, 23g carbs per 100g. Năng lượng nhanh trước tập, giàu kali chống chuột rút.",
        metadata={"name": "Chuối", "category": "carbs", "goal": "muscle_gain", "calories_per_100g": 89, "protein_per_100g": 1.1, "meal_type": "snack"}),

    # ── FATS ──
    Document(page_content="Bơ (Avocado): 2g protein, 15g fat, 9g carbs per 100g. Chất béo không bão hòa, giàu kali và vitamin E.",
        metadata={"name": "Bơ (Avocado)", "category": "fat", "goal": "muscle_gain", "calories_per_100g": 160, "protein_per_100g": 2, "meal_type": "breakfast"}),
    Document(page_content="Hạnh nhân: 21g protein, 49g fat, 22g carbs per 100g. Snack giàu năng lượng và chất béo tốt. 30g ~170 calo.",
        metadata={"name": "Hạnh nhân", "category": "fat", "goal": "muscle_gain", "calories_per_100g": 579, "protein_per_100g": 21, "meal_type": "snack"}),
    Document(page_content="Dầu ô liu: 0g protein, 100g fat, 0g carbs per 100g. Chất béo không bão hòa đơn, chống viêm. 1 muỗng canh ~120 calo.",
        metadata={"name": "Dầu ô liu", "category": "fat", "goal": "muscle_gain", "calories_per_100g": 884, "protein_per_100g": 0, "meal_type": "lunch"}),

    # ── FAT LOSS ──
    Document(page_content="Salad rau xanh: 2g protein, 0.3g fat, 3.6g carbs per 100g. Rất ít calo, giàu chất xơ. Giúp no lâu khi giảm cân.",
        metadata={"name": "Salad rau xanh", "category": "carbs", "goal": "fat_loss", "calories_per_100g": 20, "protein_per_100g": 2, "meal_type": "lunch"}),
    Document(page_content="Greek Yogurt: 10g protein, 0.7g fat, 3.6g carbs per 100g. Giàu protein, ít calo, probiotics tốt cho tiêu hóa.",
        metadata={"name": "Greek Yogurt", "category": "protein", "goal": "fat_loss", "calories_per_100g": 59, "protein_per_100g": 10, "meal_type": "snack"}),
    Document(page_content="Cá ngừ đóng hộp: 26g protein, 1g fat, 0g carbs per 100g. Protein cực nạc, tiện lợi cho meal prep.",
        metadata={"name": "Cá ngừ đóng hộp", "category": "protein", "goal": "fat_loss", "calories_per_100g": 116, "protein_per_100g": 26, "meal_type": "lunch"}),

    # ── SUPPLEMENTS ──
    Document(page_content="Creatine Monohydrate: 5g/ngày, không calo. Tăng sức mạnh, thể tích cơ. Bổ sung phổ biến nhất, an toàn.",
        metadata={"name": "Creatine", "category": "supplement", "goal": "muscle_gain", "calories_per_100g": 0, "protein_per_100g": 0, "meal_type": "snack"}),
    Document(page_content="BCAA: Leucine, isoleucine, valine. Uống trước/trong tập để giảm mỏi cơ và hỗ trợ phục hồi.",
        metadata={"name": "BCAA", "category": "supplement", "goal": "muscle_gain", "calories_per_100g": 0, "protein_per_100g": 0, "meal_type": "snack"}),
]
