import dotenv
from dotenv import load_dotenv
import requests
import json
import os

# Load environment variables from .env file
load_dotenv()
def get_access_token():
    TOKEN_URL = os.getenv("TOKEN_URL")
    CLIENT_ID = os.getenv("CLIENT_ID")
    CLIENT_SECRET = os.getenv("CLIENT_SECRET")
    TENANT_ID = os.getenv("TENANT_ID")
    if not all([TOKEN_URL, CLIENT_ID, CLIENT_SECRET, TENANT_ID]):
        raise Exception("Missing required environment variables in .env file.")
    


    payload = {
        "grant_type": "client_credentials",
        "client_id": CLIENT_ID,
        "client_secret": CLIENT_SECRET,
        "tenant_id": TENANT_ID  # Include the tenant ID here
    }
    response = requests.post(TOKEN_URL, data=payload)
    if response.status_code == 200:
        return response.json().get("access_token")
    else:
        raise Exception(f"Failed to get access token: {response.status_code}, {response.text}")

def fetch_data(api_url, access_token):
    headers = {
        "Authorization": f"B.. {access_token}"
    }
    response = requests.get(api_url, headers=headers)
    if response.status_code == 200:
        return response.json()
    else:
        raise Exception(f"Failed to fetch data: {response.status_code}, {response.text}")

def save_metadata_to_file(data, file_path):
    """Save metadata to a file in JSON format."""
    with open(file_path, "w", encoding="utf-8") as file:
        json.dump(data, file, indent=4)
    print(f"Metadata saved to {file_path}")

# Main script
if __name__ == "__main__":
    try:
        # Step 1: Get the access token
        access_token = get_access_token()
        print(f"Access Token: {access_token}")

        # Step 2: Fetch data
        API_URL = "https://api.example.com/..."  # Replace with the actual API endpoint
        data = fetch_data(API_URL, access_token)
        print("Data fetched successfully.")

        # Step 3: Save data to a file
        FILE_PATH = "metadata.json"  # File to save the metadata
        save_metadata_to_file(data, FILE_PATH)

    except Exception as e:

        print(f"Error: {e}")
