import requests
from typing import Optional, Any, Dict
from src.locales.loader import get_message

def get_api_data(
    url: str, 
    headers: Optional[Dict[str, str]] = None, 
    params: Optional[Dict[str, Any]] = None, 
    timeout: int = 10
) -> Optional[Any]:
    """
    Fetches data from an API via HTTP GET, with error handling.

    Args:
        url (str): The API endpoint URL.
        headers (dict, optional): Request headers.
        params (dict, optional): Request parameters.
        timeout (int, optional): Request timeout in seconds. Defaults to 10.

    Returns:
        The JSON response from the API, or None if an error occurs.
    """
    try:
        response = requests.get(url, headers=headers, params=params, timeout=timeout)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.HTTPError as http_err:
        if response.status_code == 401:
            print(get_message("GENERAL_ERRORS.auth"))
        elif response.status_code == 429:
            print(get_message("GENERAL_ERRORS.rate_limit"))
        else:
            print(get_message("GENERAL_ERRORS.http_error", error=http_err))
    except requests.exceptions.ConnectionError:
        print(get_message("GENERAL_ERRORS.connection"))
    except requests.exceptions.Timeout:
        print(get_message("GENERAL_ERRORS.timeout"))
    except requests.exceptions.RequestException as e:
        print(get_message("GENERAL_ERRORS.request_error", error=e))
    except Exception as e:
        print(get_message("GENERAL_ERRORS.unexpected", error=e))
    return None 