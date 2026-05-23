"""Custom tools for the AI Agent."""

import logging
from typing import Optional
from youtubesearchpython import VideosSearch

logger = logging.getLogger(__name__)

def get_exercise_video(exercise_name: str) -> Optional[str]:
    """
    Searches YouTube for a short, instructional video on how to perform
    the given exercise and returns the embed URL.
    """
    try:
        query = f"how to do {exercise_name} exercise form short"
        videos_search = VideosSearch(query, limit=1)
        results = videos_search.result()
        
        if results and results.get("result"):
            video_id = results["result"][0]["id"]
            # Trả về link dạng nhúng (embed) để frontend có thể dùng iFrame
            return f"https://www.youtube.com/embed/{video_id}"
    except Exception as e:
        logger.error("Error searching YouTube for %s: %s", exercise_name, e)
    
    return None
