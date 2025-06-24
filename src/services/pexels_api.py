"""A service for fetching images from the Pexels API."""

import os
from src.utils.api_client import get_api_data

PEXELS_API_KEY = os.getenv("PEXELS_API_KEY")

def fetch_pexels_images(query: str):
    """
    Fetch images from the Pexels API.
    """
    if not PEXELS_API_KEY:
        print("❌ PEXELS_API_KEY не знайдено. Перевірте ваш .env файл.")
        return []
        
    url = "https://api.pexels.com/v1/search"
    headers = {"Authorization": PEXELS_API_KEY}
    params = {"query": query, "per_page": 16}
    
    data = get_api_data(url, headers=headers, params=params, timeout=20)
    
    if data and "photos" in data:
        return data["photos"]
    
    print(f"⚠️ Не вдалося отримати зображення для '{query}' з Pexels.")
    return [] 