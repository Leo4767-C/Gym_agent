"""Exercise seed data — 31 exercises across all muscle groups."""

from langchain_core.documents import Document

EXERCISE_DOCUMENTS: list[Document] = [
    # ── CHEST (5) ──
    Document(page_content="Dumbbell Flat Bench Press: Lie on a flat bench holding a dumbbell in each hand at chest level. Press upward until arms are extended, then lower slowly. Targets pectoralis major, anterior deltoid, triceps.",
        metadata={"name": "Dumbbell Flat Bench Press", "muscle_group": "chest", "equipment": "dumbbell", "difficulty": "beginner", "sets": 3, "reps": "10-12", "rest_seconds": 60}),
    Document(page_content="Barbell Incline Bench Press: Set bench to 30-45 degrees. Grip barbell wider than shoulder-width, lower to upper chest, press up. Targets upper pectoralis major.",
        metadata={"name": "Barbell Incline Bench Press", "muscle_group": "chest", "equipment": "barbell", "difficulty": "intermediate", "sets": 4, "reps": "6-8", "rest_seconds": 90}),
    Document(page_content="Push-Up: High plank position, lower chest to floor keeping body straight, push back up. Ultimate bodyweight chest exercise. Targets pectoralis major, deltoids, triceps, core.",
        metadata={"name": "Push-Up", "muscle_group": "chest", "equipment": "bodyweight", "difficulty": "beginner", "sets": 3, "reps": "15-20", "rest_seconds": 45}),
    Document(page_content="Cable Fly: Stand between cable machines, grab handles at chest height. Step forward, bring hands together in a hugging motion. Isolates pectoralis major with constant tension.",
        metadata={"name": "Cable Fly", "muscle_group": "chest", "equipment": "cable", "difficulty": "intermediate", "sets": 3, "reps": "12-15", "rest_seconds": 60}),
    Document(page_content="Dumbbell Decline Press: Lie on a decline bench, press dumbbells from chest level upward. Emphasizes lower chest (sternal head of pectoralis major).",
        metadata={"name": "Dumbbell Decline Press", "muscle_group": "chest", "equipment": "dumbbell", "difficulty": "intermediate", "sets": 3, "reps": "10-12", "rest_seconds": 60}),

    # ── BACK (6) ──
    Document(page_content="Dumbbell Single-Arm Row: One knee on bench, row dumbbell to hip. Trains lats, rhomboids, rear deltoid unilaterally.",
        metadata={"name": "Dumbbell Single-Arm Row", "muscle_group": "back", "equipment": "dumbbell", "difficulty": "beginner", "sets": 3, "reps": "10-12", "rest_seconds": 60}),
    Document(page_content="Pull-Up: Hang from bar with overhand grip, pull chest to bar. Gold-standard bodyweight exercise for lat width and bicep strength.",
        metadata={"name": "Pull-Up", "muscle_group": "back", "equipment": "bodyweight", "difficulty": "intermediate", "sets": 3, "reps": "6-10", "rest_seconds": 90}),
    Document(page_content="Barbell Bent-Over Row: Hinge at hips, pull barbell to lower chest. Builds thick back muscles — lats, traps, rhomboids. Keep core braced.",
        metadata={"name": "Barbell Bent-Over Row", "muscle_group": "back", "equipment": "barbell", "difficulty": "intermediate", "sets": 4, "reps": "8-10", "rest_seconds": 90}),
    Document(page_content="Lat Pulldown: Sit at lat pulldown machine, pull bar to upper chest. Great alternative to pull-ups for beginners building lat strength.",
        metadata={"name": "Lat Pulldown", "muscle_group": "back", "equipment": "machine", "difficulty": "beginner", "sets": 3, "reps": "10-12", "rest_seconds": 60}),
    Document(page_content="Cable Seated Row: Sit at cable row station, pull handle to torso. Targets mid-back, rhomboids, and rear deltoids with constant cable tension.",
        metadata={"name": "Cable Seated Row", "muscle_group": "back", "equipment": "cable", "difficulty": "beginner", "sets": 3, "reps": "10-12", "rest_seconds": 60}),
    Document(page_content="Barbell Deadlift: Stand with barbell over mid-foot, hinge and grip bar, drive through heels to stand. King of posterior chain — works back, glutes, hamstrings, traps.",
        metadata={"name": "Barbell Deadlift", "muscle_group": "back", "equipment": "barbell", "difficulty": "advanced", "sets": 4, "reps": "5-6", "rest_seconds": 120}),

    # ── LEGS (6) ──
    Document(page_content="Dumbbell Goblet Squat: Hold dumbbell at chest, squat until thighs parallel. Perfect beginner squat, trains quads, glutes, hamstrings, core.",
        metadata={"name": "Dumbbell Goblet Squat", "muscle_group": "legs", "equipment": "dumbbell", "difficulty": "beginner", "sets": 3, "reps": "12-15", "rest_seconds": 60}),
    Document(page_content="Barbell Back Squat: Bar on upper traps, squat to parallel or below. King of lower body exercises — maximal quad, glute, hamstring development.",
        metadata={"name": "Barbell Back Squat", "muscle_group": "legs", "equipment": "barbell", "difficulty": "intermediate", "sets": 4, "reps": "5-8", "rest_seconds": 120}),
    Document(page_content="Dumbbell Lunges: Step forward holding dumbbells, lower back knee toward floor, push back up. Unilateral leg exercise improving balance and stability.",
        metadata={"name": "Dumbbell Lunges", "muscle_group": "legs", "equipment": "dumbbell", "difficulty": "beginner", "sets": 3, "reps": "10-12 each", "rest_seconds": 60}),
    Document(page_content="Leg Press: Sit in leg press machine, push platform away with feet. Safe alternative to squats for heavy quad and glute loading.",
        metadata={"name": "Leg Press", "muscle_group": "legs", "equipment": "machine", "difficulty": "beginner", "sets": 3, "reps": "10-12", "rest_seconds": 90}),
    Document(page_content="Romanian Deadlift: Hold barbell, hinge at hips with slight knee bend, lower bar along legs. Targets hamstrings and glutes with eccentric emphasis.",
        metadata={"name": "Romanian Deadlift", "muscle_group": "legs", "equipment": "barbell", "difficulty": "intermediate", "sets": 3, "reps": "8-10", "rest_seconds": 90}),
    Document(page_content="Bodyweight Squat: Stand shoulder-width, squat down keeping chest up. Foundational movement pattern for beginners, no equipment needed.",
        metadata={"name": "Bodyweight Squat", "muscle_group": "legs", "equipment": "bodyweight", "difficulty": "beginner", "sets": 3, "reps": "15-20", "rest_seconds": 45}),

    # ── SHOULDERS (4) ──
    Document(page_content="Dumbbell Lateral Raise: Stand with dumbbells at sides, raise arms to parallel. Isolates medial deltoid for shoulder width.",
        metadata={"name": "Dumbbell Lateral Raise", "muscle_group": "shoulders", "equipment": "dumbbell", "difficulty": "beginner", "sets": 3, "reps": "12-15", "rest_seconds": 45}),
    Document(page_content="Dumbbell Overhead Press: Sit or stand, press dumbbells from shoulder height to overhead. Primary compound shoulder builder targeting all deltoid heads.",
        metadata={"name": "Dumbbell Overhead Press", "muscle_group": "shoulders", "equipment": "dumbbell", "difficulty": "intermediate", "sets": 3, "reps": "8-10", "rest_seconds": 60}),
    Document(page_content="Barbell Military Press: Press barbell from front shoulders to overhead. Heavy compound movement for raw shoulder strength and mass.",
        metadata={"name": "Barbell Military Press", "muscle_group": "shoulders", "equipment": "barbell", "difficulty": "intermediate", "sets": 4, "reps": "6-8", "rest_seconds": 90}),
    Document(page_content="Face Pull: Cable at high position, pull rope to face with elbows high. Essential for rear deltoid and rotator cuff health. Prevents shoulder injuries.",
        metadata={"name": "Face Pull", "muscle_group": "shoulders", "equipment": "cable", "difficulty": "beginner", "sets": 3, "reps": "15-20", "rest_seconds": 45}),

    # ── ARMS (6) ──
    Document(page_content="Dumbbell Bicep Curl: Stand holding dumbbells, curl up by bending elbows. Classic isolation exercise for biceps brachii peak and mass.",
        metadata={"name": "Dumbbell Bicep Curl", "muscle_group": "arms", "equipment": "dumbbell", "difficulty": "beginner", "sets": 3, "reps": "10-12", "rest_seconds": 45}),
    Document(page_content="Barbell Curl: Stand with barbell, curl weight up. Allows heavier loading than dumbbells for maximum bicep overload.",
        metadata={"name": "Barbell Curl", "muscle_group": "arms", "equipment": "barbell", "difficulty": "beginner", "sets": 3, "reps": "8-10", "rest_seconds": 60}),
    Document(page_content="Hammer Curl: Curl dumbbells with neutral (palms facing) grip. Targets brachialis and brachioradialis for arm thickness.",
        metadata={"name": "Hammer Curl", "muscle_group": "arms", "equipment": "dumbbell", "difficulty": "beginner", "sets": 3, "reps": "10-12", "rest_seconds": 45}),
    Document(page_content="Tricep Dips: Support body on parallel bars, lower by bending elbows to 90 degrees, push up. Compound tricep builder also hitting chest and shoulders.",
        metadata={"name": "Tricep Dips", "muscle_group": "arms", "equipment": "bodyweight", "difficulty": "intermediate", "sets": 3, "reps": "8-12", "rest_seconds": 60}),
    Document(page_content="Cable Tricep Pushdown: Stand at cable machine, push rope/bar down extending elbows. Excellent tricep isolation with constant tension.",
        metadata={"name": "Cable Tricep Pushdown", "muscle_group": "arms", "equipment": "cable", "difficulty": "beginner", "sets": 3, "reps": "12-15", "rest_seconds": 45}),
    Document(page_content="Overhead Tricep Extension: Hold dumbbell overhead with both hands, lower behind head, extend arms. Stretches long head of triceps for maximum development.",
        metadata={"name": "Overhead Tricep Extension", "muscle_group": "arms", "equipment": "dumbbell", "difficulty": "beginner", "sets": 3, "reps": "10-12", "rest_seconds": 45}),

    # ── CORE (4) ──
    Document(page_content="Plank: Forearm plank, body straight from head to heels, hold position. Foundational isometric core exercise for spinal stability.",
        metadata={"name": "Plank", "muscle_group": "core", "equipment": "bodyweight", "difficulty": "beginner", "sets": 3, "reps": "30-60 seconds", "rest_seconds": 30}),
    Document(page_content="Russian Twist: Sit with knees bent, lean back slightly, rotate torso side to side holding weight. Targets obliques and rotational core strength.",
        metadata={"name": "Russian Twist", "muscle_group": "core", "equipment": "bodyweight", "difficulty": "beginner", "sets": 3, "reps": "20 each side", "rest_seconds": 30}),
    Document(page_content="Hanging Leg Raise: Hang from bar, raise legs to parallel or higher. Advanced core exercise targeting lower abs and hip flexors.",
        metadata={"name": "Hanging Leg Raise", "muscle_group": "core", "equipment": "bodyweight", "difficulty": "intermediate", "sets": 3, "reps": "10-15", "rest_seconds": 45}),
    Document(page_content="Cable Woodchop: Stand sideways to cable, pull handle diagonally across body. Functional rotational core exercise for athletes.",
        metadata={"name": "Cable Woodchop", "muscle_group": "core", "equipment": "cable", "difficulty": "intermediate", "sets": 3, "reps": "12-15 each", "rest_seconds": 45}),
]
