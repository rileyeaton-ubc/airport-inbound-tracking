
import httpx

# HttpClient class to make HTTP requests from the backend to other APIs
class HttpClient:
    # Initialize the HttpClient with a base URL, optional headers, and timeout
    def __init__(self, base_url, headers=None, timeout=10):
        self.base_url = base_url
        self.headers = headers or {}
        self.timeout = timeout

    # Perform a GET request to the specified endpoint with optional query parameters
    # Parameters:
    #   => endpoint (str): The API endpoint
    #   => params (dict): Query parameters for the request (default is None)
    # Returns:
    #   => dict: JSON response from the API
    def get(self, endpoint, params=None):
        try:
            url = f"{self.base_url}{endpoint}"
            response = httpx.get(
                url, headers=self.headers, params=params, timeout=self.timeout
            )
            response.raise_for_status()
            return response.json()
        except httpx.RequestError as e:
            print(f"An error occurred while making the request: {e}")
            return None
        except httpx.HTTPStatusError as e:
            print(f"HTTP error occurred: {e}")
            return None