import requests

def web_search(google_api_key, cse_id, query, num_results=5):
    url = "https://www.googleapis.com/customsearch/v1"
    params = {
        'key': google_api_key,
        'cx': cse_id,
        'q': query,
        'num': num_results
    }
    response = requests.get(url, params=params)
    #print("API Response:", response.json())  # Debugging log
    return [item['snippet'] for item in response.json().get('items', [])]