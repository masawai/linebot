import json
import logging
import os

import boto3
import requests

import create_item

logger = logging.getLogger(__name__)
logLevel=logging.DEBUG
logger.setLevel(logLevel)

url = 'https://api.line.me/v2/bot/message/reply'
headers = {
    'Content-Type': 'application/json',
    'Authorization': 'Bearer ' + create_item.access_token
}

def lambda_handler(event, context):
    for message_event in json.loads(event['body'])['events']:
        logger.debug(message_event)
        word = message_event['message']['text']
        try:
            create_item.create_item(word)  
            text = f'{word}を登録したよ'
        except:
            text = '登録でエラーが発生したみたい...'
        body = {
            'replyToken': message_event['replyToken'],
            'messages': [
                {
                    'type': 'text',
                    'text': text,
                }
            ]
        }
        req = requests.post(url, data=json.dumps(body).encode('utf-8'), headers=headers)

    return {
        'statusCode': 200
    }
