import requests
import os
import dotenv

dotenv.load_dotenv()  

APP_ID = os.getenv("ANTONIA_META_APP_ID")
APP_SECRET = os.getenv("ANTONIA_META_APP_SECRET")
TOKEN = os.getenv("ANTONIA_META_APP_TOKEN")

def refresh_token():
    """
    This will provide you a long lived token that should last for about 60 days. 
    You can use this token in your InstagramPublisher initialization and it should 
    work without needing to refresh it again for a while.

    First, you will need to get a short-lived token using the Facebook Graph API 
    Explorer or by following the OAuth flow. Set it as your ANTONIA_META_APP_TOKEN 
    in the .env file. Then run this script to get a long-lived token and set it in
    ANTONIA_META_APP_TOKEN, replacing the short-lived token.
    """

    url = "https://graph.facebook.com/v18.0/oauth/access_token"

    params = {
        "grant_type": "fb_exchange_token",
        "client_id": APP_ID,
        "client_secret": APP_SECRET,
        "fb_exchange_token": TOKEN
    }

    r = requests.get(url, params=params)
    r.raise_for_status()

    new_token = r.json()["access_token"]

    print(r.json())

    return new_token

if __name__ == "__main__":
    new_token = refresh_token()
    print("New token:", new_token)