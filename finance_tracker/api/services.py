from django.conf import settings
import google.generativeai as genai

genai.configure(api_key=settings.GEMINI_API_KEY)
def get_book_recommendations(user_query):
    model = genai.GenerativeModel(model_name='gemini-1.5-flash')
    prompt = f"Recommend financial books for the following query: {user_query}"
    response = model.generate_content(prompt)
    return response.text.strip()