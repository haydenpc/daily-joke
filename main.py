import os
import requests
from dotenv import load_dotenv
import smtplib
import time

load_dotenv()

JOKE_API_URL = "https://api.api-ninjas.com/v1/dadjokes"

PHONE_NUMBER = os.getenv("PHONE_NUMBER")
API_KEY_JOKE = os.getenv("API_KEY_JOKE")
EMAIL = os.getenv("EMAIL")
PASSWORD = os.getenv("PASSWORD")
CARRIERS = {
    'cricket': '@mms.cricketwireless.net',
    'att':'@mms.att.net',
    'tmobile': '@tomail.net',
    'verizon': '@vtext.com',
    'sprint': '@page.nextel.com'
}
CARRIER = os.getenv("CARRIER", "cricket")
SMPT_DOMAIN = os.getenv("SMTP_DOMAIN")
SMTP_PORT = int(os.getenv("SMTP_PORT"))


def get_joke():
    print("attempting to fetch joke")
    headers = {
        "X-Api-Key": API_KEY_JOKE,
    }
    while True :
        try:
            response = requests.get(JOKE_API_URL, headers=headers)
            response.raise_for_status()
            joke = response.json()[0]['joke']
            print("Joke fetched succesfully {joke}")
            return joke
        except requests.exceptions.RequestException as e:
                print(f"couldnt get joke {e}")
                time.sleep(3)
    
def send(message):
    print("attempting to send sms")
    carrier_domain = CARRIERS.get(CARRIER)
    to_number = f"{PHONE_NUMBER}{carrier_domain}"

    try:
        with smtplib.SMTP(SMPT_DOMAIN, SMTP_PORT) as server:
            server.starttls()
            server.login(EMAIL, PASSWORD)
            server.sendmail(EMAIL, to_number, message.encode('utf-8'))
        print("sent!")
    except smtplib.SMTPException as e:
        print("error failed to sent joke: {e}")

def main():
    joke = get_joke()
    if joke:
        send(joke)
    else:
        print("no joke to send")

main()