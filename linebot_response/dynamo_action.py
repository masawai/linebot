import datetime
import os
import logging
import boto3
from boto3.dynamodb.conditions import Key

logger = logging.getLogger(__name__)
dynamodb = boto3.resource('dynamodb')
table    = dynamodb.Table('linebot')

# get userId of me
masawai = os.environ.get('userId')

def create_item(message_event=None):
    name = 'Masaya' if message_event['source']['userId'] == masawai else 'Mayu'
    Item={
        'date'          : str(datetime.datetime.now().strftime('%Y/%-m/%-d %H:%M:%S')),
        'price'         : int(message_event['message']['text'].splitlines()[0]),
        'description'   : message_event['message']['text'].splitlines()[1],
        'name'          : name,
       }
    table.put_item(Item=Item)
    text = f'{message_event["message"]["text"]}\nで登録したよ'
    return text

def query_item(message_event=None):
    mayu_list = os.environ.get('mayu_list')
    masaya_list = os.environ.get('masaya_list')
    message = message_event['message']['text']
    # If there is a name in the message, query by that name.
    # Otherwise, query by sender's name.
    if name_check(message, mayu_list):
        name = 'Mayu'
    elif name_check(message, masaya_list):
        name = 'Masaya'
    else:
        name = 'Masaya' if message_event['source']['userId'] == masawai else 'Mayu'
    if '月' in message:
        month = message.split("月")[0]
        year = datetime.datetime.now().year
        year_month = f'{year}/{month}' if month != 12 else f'{year-1}/{month}'
    else:
        year_month = datetime.datetime.now().strftime('%Y/%-m')
    res = table.query(
        KeyConditionExpression=Key('name').eq(name) & Key('date').begins_with(year_month)
    )
    text = ''
    total_payment = 0
    for row in res['Items']:
        text += f"{row['description']} {row['price']}円\n" 
        total_payment += row['price']
    text += f"合計：{total_payment}円"
    return text 

def name_check(message, names):
    for name in names:
        if name in message:
            return True
    return False
