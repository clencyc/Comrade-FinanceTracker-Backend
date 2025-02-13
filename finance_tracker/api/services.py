# FILE: services.py

import logging
import google.generativeai as genai
from django.conf import settings
import json

logger = logging.getLogger(__name__)

genai.configure(api_key=settings.GEMINI_API_KEY)

def get_book_recommendations(user_query):
    model = genai.GenerativeModel(model_name='gemini-1.5-flash')
    prompt = f"""
    Recommend financial books for the following query: {user_query}.
    For each book, include the title, author, genre, difficulty level, rating, and a URL to the book cover image.
    Format the response as follows:

    1. **Title** by Author  
       - Genre: Genre  
       - Difficulty Level: Difficulty Level  
       - Rating: Rating  
       - Cover Image: URL
    """
    try:
        response = model.generate_content(prompt)
    except Exception as e:
        logger.error(f"Error generating content: {e}")
        return []
    
    if hasattr(response, 'generations') and response.generations:
        text_response = response.generations[0].text.strip()
    else:
        logger.warning("Gemini API did not return any content")
        return []

    try:
        recommendations = json.loads(text_response)
    except json.JSONDecodeError:
        logger.warning("Gemini API did not return valid JSON, trying regex parsing.")
        recommendations = parse_recommendations(text_response)

    return recommendations

def parse_recommendations(text_response):
    recommendations = []
    pattern = re.compile(
        r"\d+\.\s+\*\*(.+?)\*\*\s+by\s+(.+?)\s+"  # Title and author
        r"-\s+Genre:\s+(.+?)\s+"  # Genre
        r"-\s+Difficulty Level:\s+(.+?)\s+"  # Difficulty level
        r"-\s+Rating:\s+([\d.]+)\s+"  # Rating
        r"-\s+Cover Image:\s+(.+?)\s*$",  # Cover image URL
        re.MULTILINE
    )

    matches = pattern.findall(text_response)
    for match in matches:
        recommendations.append({
            "title": match[0],
            "author": match[1],
            "genre": match[2],
            "difficulty_level": match[3],
            "rating": float(match[4]),
            "image_url": match[5]
        })

    return recommendations