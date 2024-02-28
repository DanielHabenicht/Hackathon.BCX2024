# Make a Http get request to a give url with a token
import os
import requests
from dotenv import load_dotenv

load_dotenv()


url = "https://agentverse.ai/v1beta1/engine/chat/sessions"
token = os.getenv("FETCH_AI_TOKEN")

headers = {
    "Authorization": f"Basic {token}",
    "X-API-KEY": token

}

response = requests.get(url, headers=headers)

if response.status_code == 200:
    # Request was successful
    data = response.json()
    # Process the response data here
else:
    # Request failed
    print(f"Error: {response.status_code}")

