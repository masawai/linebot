import base64
import hashlib
import hmac
import json
import logging
import urllib.request
import os
import boto3
import create_item

logger = logging.getLogger(__name__)
logLevel=logging.DEBUG
logger.setLevel(logLevel)

url = 'https://api.line.me/v2/bot/message/reply'
headers = {
    'Content-Type': 'application/json',
    'Authorization': 'Bearer ' + create_item.access_token
}

def authorize_request(event):
    logger.debug(event)
    x_line_signature = event["headers"]["x-line-signature"] if event["headers"]["x-line-signature"] else event["headers"]["X-Line-Signature"]
    body = event["body"]
    hash = hmac.new(create_item.channel_secret.encode('utf-8'),
        body.encode('utf-8'), hashlib.sha256).digest()
    signature = base64.b64encode(hash)
    if signature != x_line_signature.encode(): raise Exception
    return True


def lambda_handler(event, context):
    authorize_request(event)
    for message_event in json.loads(event['body'])['events']:
        logger.debug(message_event)
        bibliograph = create_item.get_bibliograph_by_isbn(message_event['message']['text'])
        if bibliograph:
            create_item.create_item(bibliograph)
            text = '{}を登録したよ'.format(bibliograph['title'])
        else:
            text = 'その本は見つけられませんでした'
        body = {
            'replyToken': message_event['replyToken'],
            'messages': [
                {
                    'type': 'text',
                    'text': text,
                }
            ]
        }
        req = urllib.request.Request(url, data=json.dumps(body).encode('utf-8'), method='POST', headers=headers)
        with urllib.request.urlopen(req) as res:
            logger.info(res.read().decode("utf-8"))

    return {
        'statusCode': 200
    }
