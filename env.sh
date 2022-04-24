#!/usr/bin/env sh

echo "--------------- TESTING FOR REQUIRED ENV VARIABLES HERE FOR CRON-SERVICE ------------------"

if [ -z $AMAZON_API_KEY ]; then 
    echo "------------------ [ERROR]: AMAZON_API_KEY ENV VAR NOT DEFINED"
    exit 1
elif [ -z $TWILIO_ACCOUNT_SID ]; then 
    echo "------------------ [ERROR]: TWILIO_SID_AUTH ENV VAR NOT DEFINED"
    exit 1
elif [ -z $TWILIO_AUTH_TOKEN ]; then 
    echo "------------------ [ERROR]: TWILIO_AUTH_TOKEN ENV VAR NOT DEFINED"
    exit 1
elif [ -z $TWILIO_PHONE_SENDER ]; then 
    echo "------------------ [ERROR]: TWILIO_PHONE_NUMBER ENV VAR NOT DEFINED"
    exit 1
elif [ -z $TWILIO_PHONE_RECEIVER ]; then 
    echo "------------------ [ERROR]: TWILIO_PHONE_NUMBER ENV VAR NOT DEFINED"
    exit 1
elif [ -z $AMAZON_PRODUCT_ID ]; then 
    echo "------------------ [ERROR]: AMAZON_PRODUCT_ID ENV VAR NOT DEFINED"
    exit 1
elif [ -z $AMAZON_TRIGGER_HIGH_LIMIT ]; then 
    echo "------------------ [WARNING]: AMAZON_TRIGGER_HIGH_LIMIT ENV VAR NOT DEFINED"
    export AMAZON_TRIGGER_HIGH_LIMIT=100000
elif [ -z $AMAZON_TRIGGER_LOW_LIMIT ]; then 
    echo "------------------ [WARNING]: AMAZON_TRIGGER_LOW_LIMIT ENV VAR NOT DEFINED"
    export AMAZON_TRIGGER_LOW_LIMIT=10000
elif [ -z $CRON_INTERVAL_SECONDS ]; then 
    echo "------------------ [WARNING]: CRON_INTERVAL ENV VAR NOT DEFINED"
    export CRON_INTERVAL_SECONDS=20
fi