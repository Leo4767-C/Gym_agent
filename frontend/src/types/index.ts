export interface WorkoutExercise {
  exercise_name: string;
  muscle_group:  string;
  equipment:     string;
  sets:          number;
  reps:          string;
  rest_seconds:  number;
  coaching_tip:  string;
}

export interface NutritionAdvice {
  daily_calories?: number;
  protein_grams?:  number;
  carbs_grams?:    number;
  fat_grams?:      number;
  goal?:           string;
}

export interface MealItem {
  meal_name: string;
  foods:     string;
  calories:  number;
  protein:   number;
}

export interface ScheduleDay {
  day:              string;
  focus:            string;
  exercises:        string[];
  duration_minutes: number;
  notes:            string;
}

export interface ExerciseGuide {
  exercise_name:  string;
  video_url?:     string;
  muscle_group:   string;
  equipment:      string;
  difficulty:     string;
  steps:          string[];
  common_mistakes: string[];
  breathing:      string;
  sets_reps_recommendation: string;
}

export interface ChatResponse {
  response_type:        'workout_plan' | 'nutrition' | 'schedule' | 'exercise_guide';
  thought_process:      string;
  motivational_message: string;
  latency_ms:           number;
  filters_used:         Record<string, unknown>;
  workout_plan:         WorkoutExercise[];
  nutrition_advice:     NutritionAdvice;
  meal_plan:            MealItem[];
  supplements:          string[];
  goal:                 string;
  weekly_schedule:      ScheduleDay[];
  exercise_guide:       ExerciseGuide;
}

export interface HealthResponse {
  status:  'ok' | 'degraded';
  db_docs: number;
  model:   string;
}
