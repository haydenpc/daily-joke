import os
import requests
from dotenv import load_dotenv
import smtplib

load_dotenv()

JOKE_API_URL = "https://api.api-ninjas.com/v1/dadjokes"
TEXTBELT_API_URL = "https://textbelt.com/text"

PHONE_NUMBER = os.getenv("PHONE_NUMBER")
TEXTBELT_API = os.getenv("TEXTBELT_API")
API_KEY_JOKE = os.getenv("API_KEY_JOKE")
EMAIL = os.getenv("EMAIL")
PASSWORD = os.getenv("PASSWORD")
CARRIERS_DOMAIN = os.getenv("CARRIERS_DOMAIN")

def get_joke():
    headers = {
        "X-Api-Key": API_KEY_JOKE,
    }
    response = requests.get(JOKE_API_URL, headers=headers)
    print(response.json())
    if response.status_code == 200:
        joke = response.json()[0]['joke']
        return joke
    else:
        print("couldnt get joke")
        return None
    
def send(message):
    to_number = PHONE_NUMBER.format(CARRIERS_DOMAIN)
    auth = (EMAIL, PASSWORD)

    server = smtplib.SMTP( "smtp.gmail.com", 587 )
    server.starttls()
    server.login(auth[0], auth[1])

    server.sendmail( auth[0], to_number, message)

send(get_joke())