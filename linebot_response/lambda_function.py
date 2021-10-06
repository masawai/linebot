import json
import urllib.request
import os
import boto3
import dynamo_action
import logging

logger = logging.getLogger(__name__)

url = 'https://api.line.me/v2/bot/message/reply'
headers = {
    'Content-Type': 'application/json',
    'Authorization': 'Bearer ' + dynamo_action.access_token
}

def lambda_handler(event, context):
    for message_event in json.loads(event['body'])['events']:
        logger.info(message_event)
        if '教えて' in message_event['message']['text']:
            text = dynamo_action.query_item(message_event)
        elif 'help' in message_event['message']['text']:
            text = '<使い方>\nデータを登録する場合:\n"使用した金額(単位なし)"\n"用途"\n\n例：\n130\n自販機\n\n\n' \
                   '使った金額を確認する場合:\n"{確認したい月}月""教えて"\n\n例：\n8月\n教えて'
        else:
            # DynamoDBにデータを登録する
            try:
                text = dynamo_action.create_item(message_event)
            except:
                text = '金額\n用途\nの形式で教えてね'
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
