import requests
from typing import Optional, Any, Dict
from docs.error_messages import GENERAL_ERRORS

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
            print(GENERAL_ERRORS['auth'])
        elif response.status_code == 429:
            print(GENERAL_ERRORS['rate_limit'])
        else:
            print(GENERAL_ERRORS['http_error'].format(error=http_err))
    except requests.exceptions.ConnectionError:
        print(GENERAL_ERRORS['connection'])
    except requests.exceptions.Timeout:
        print(GENERAL_ERRORS['timeout'])
    except requests.exceptions.RequestException as e:
        print(GENERAL_ERRORS['request_error'].format(error=e))
    except Exception as e:
        print(GENERAL_ERRORS['unexpected'].format(error=e))
    return None 