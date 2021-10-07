import boto3
import json 
import os 
from linebot import LineBotApi
from linebot.models import TextSendMessage
import dynamo_action
import logging

logger = logging.getLogger(__name__)

#SSM
ssm = boto3.client('ssm')
access_token = ssm.get_parameter(Name='/linebot/access_token',WithDecryption=True)['Parameter']['Value']
masawai = ssm.get_parameter(Name='/linebot/user_id',WithDecryption=True)['Parameter']['Value']

line_bot_api = LineBotApi(access_token)


def lambda_handler(event, context):
    user_id = masawai
    text = dynamo_action.query_item(event)
    messages = TextSendMessage(text=text)
    line_bot_api.push_message(user_id, messages=messages)

    return {
        'statusCode': 200,
        'body': json.dumps('Hello from Lambda!')
    }