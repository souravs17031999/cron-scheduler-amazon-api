from cmath import log
from apscheduler.schedulers.blocking import BlockingScheduler
import datetime
import json
import os
import datetime
from twilio.rest import Client
import logging
import requests
import pytz

logging.basicConfig()
logging.getLogger('apscheduler').setLevel(logging.DEBUG)

# Instantiating the scheduler for the cronjob
cron_schedular = BlockingScheduler()

print("Initializing CRON Schedular.... ")

TWILIO_ACCOUNT_SID = os.environ['TWILIO_ACCOUNT_SID']
TWILIO_AUTH_TOKEN = os.environ['TWILIO_AUTH_TOKEN']
client = Client(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)

AMAZON_API_KEY = os.environ['AMAZON_API_KEY']
CRON_INTERVAL_SECONDS = os.environ['CRON_INTERVAL_SECONDS']
TWILIO_PHONE_USER_SENDER = os.environ['TWILIO_PHONE_SENDER']
TWILIO_PHONE_USER_RECEIVER = os.environ['TWILIO_PHONE_RECEIVER']
AMAZON_PRODUCT_ID_ASIN = os.environ['AMAZON_PRODUCT_ID']
AMAZON_PRODUCT_TRIGGER_PRICE_LIMIT_INR = [os.environ['AMAZON_TRIGGER_LOW_LIMIT'], os.environ['AMAZON_TRIGGER_HIGH_LIMIT']]

AMAZON_PRODUCT_API = "https://api.rainforestapi.com/request"
tz_AK = pytz.timezone("Asia/Kolkata")

def get_message_for_twilio_SMS(json_response, current_price_of_product):

    productTitle = json_response["product"]["title"][:30]
    productId = json_response["product"]["asin"]
    productBuyLink = json_response["product"]["link"]
    messageBody = f"Hurry up ! Your requested Product {productTitle} is available within your budget for rs. {current_price_of_product}. Click on link now to order it. \
        {productBuyLink}"

    return messageBody


def send_twilio_notifications(message_body):

    try:
        print("[TWILIO] : sending SMS to user ")
        print("[TWILIO] : message for SMS: ")
        print(message_body)
        message = client.messages.create(
                    body=message_body,
                    from_=TWILIO_PHONE_USER_SENDER,
                    to=TWILIO_PHONE_USER_RECEIVER
                )
        print(message.sid)
        print("[TWILIO]: Message (SMS) send successfully !")
    except Exception as e:
        print(f"[ERROR]: {e}")
        print(
            "status: failure, message: SMS notifications sending to user failed !"
        )



def get_amazon_product_response():
    
    apiParams = {
        'api_key': AMAZON_API_KEY,
        'type': 'product',
        'amazon_domain': 'amazon.in',
        'asin': 'B093L8FSP2',
        'output': 'json'
    }
    headers = {"Content-Type": "application/json"}
    print(f"[AMAZON]: Trying for product ID {AMAZON_PRODUCT_ID_ASIN}")
    try:
        print(f"[REQUEST]: GET {AMAZON_PRODUCT_API} {apiParams}")
        product_get_response = requests.get(
                AMAZON_PRODUCT_API,
                headers=headers,
                params=apiParams
            )
        print(f"[RESPONSE]: {product_get_response.status_code}")
        json_product_response = product_get_response.json()
        # print(json_product_response)

    except Exception as e:
        print(f"[ERROR]: {e}")
        print(
            "status: failure, message: Failure in sending request to Amazon Server !"
        )
    
    return json_product_response

# cron Job
@cron_schedular.scheduled_job(trigger="interval", seconds=int(CRON_INTERVAL_SECONDS))
def trigger_amazon_product_price_notifications():

    print(
        "*********************** CRON for sending notifications for AMAZON Offers deal of the day ********************"
    )
    datetime_NY = datetime.datetime.now(tz_AK)
    print("[CRON TIME (IST)]: ", datetime_NY.strftime("%A, %d %B %Y %I:%M%p"))
    print("[CRON TIME (UTC)]: ", datetime.datetime.utcnow())
    
    try:
        json_product_response = get_amazon_product_response()
        send_notify = False 
        current_price_of_product = json_product_response["product"]["buybox_winner"]["rrp"]["value"]
        if json_product_response["product"]["buybox_winner"]["save"] is not None:
            current_price_of_product -= json_product_response["product"]["buybox_winner"]["save"]["value"]

        print(f"[AMAZON]: Found product price for product ID {AMAZON_PRODUCT_ID_ASIN}: {current_price_of_product}")
        if int(AMAZON_PRODUCT_TRIGGER_PRICE_LIMIT_INR[0]) <= current_price_of_product < int(AMAZON_PRODUCT_TRIGGER_PRICE_LIMIT_INR[1]):
            send_notify = True

        if send_notify:
            print("Yeay ! Found Product within range specified. Requesting Twilio to send SMS....")
            message_body = get_message_for_twilio_SMS(json_product_response, current_price_of_product)
            send_twilio_notifications(message_body)
        else: 
            print("Missed for this CRON attempt ! Current price was beyond your budget.")

    except Exception as e:
        print(f"[ERROR]: {e}")
        print(
            "status: failure, message: Cron service failed to execute Job !!!"
        )

cron_schedular.start()