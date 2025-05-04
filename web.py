import requests
import json

def web_search(google_api_key, cse_id, query, num_results=10):
    url = "https://www.googleapis.com/customsearch/v1"
    params = {
        'key': google_api_key,
        'cx': cse_id,
        'q': query,
        'num': num_results
    }

    try:
        response = requests.get(url, params=params, timeout=10)
        response.raise_for_status()
    except requests.exceptions.RequestException as e:
        raise ValueError(f"Request to Google API failed: {e}")

    try:
        response_json = response.json()
        items = response_json.get('items', [])
        return [
            f"{item.get('title', 'No title')}\n{item.get('link', 'No link')}\n{item.get('snippet', 'No snippet')}\n"
            for item in items
        ] if items else ["No relevant search results found."]
    except (ValueError, json.JSONDecodeError) as e:
        raise ValueError(f"Error parsing JSON response: {e}")
