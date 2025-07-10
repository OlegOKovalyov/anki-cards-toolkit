"""A service for fetching images from the Pexels API."""

from src.config.settings import PEXELS_API_KEY, PEXELS_API_URL
from docs.messages import PEXELS_ERRORS
from src.utils.api_client import get_api_data

def fetch_pexels_images(query: str):
    """
    Fetch images from the Pexels API.
    """
    if not PEXELS_API_KEY:
        print(PEXELS_ERRORS["missing_api_key"])
        return []
    
    url = PEXELS_API_URL
    headers = {"Authorization": PEXELS_API_KEY}
    params = {"query": query, "per_page": 16}
    
    data = get_api_data(url, headers=headers, params=params, timeout=20)
    
    if data and "photos" in data:
        return data["photos"]
    
    print(PEXELS_ERRORS["image_not_found"].format(query=query))
    return [] 