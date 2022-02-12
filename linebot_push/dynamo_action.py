import boto3
import datetime
import os
from boto3.dynamodb.conditions import Key

# DynamoDB
dynamodb = boto3.resource('dynamodb')
table    = dynamodb.Table('linebot')

names = os.environ.get('names', 'Masaya,Mayu').split(',')

def query_item(event=None):
    # This code will be executed at the beginning of the month.
    # The month of last day is last month
    last_day = datetime.datetime.now() - datetime.timedelta(days=1)
    year_month = last_day.strftime('%Y/%-m')
    text = ''
    for name in names:
        res = table.query(
            KeyConditionExpression=Key('name').eq(name) & Key('date').begins_with(year_month)
        )
        total_payment = 0
        for row in res['Items']:
            text += f"{row['date'][:-9]} {row['description']} {row['price']}円\n" 
            total_payment += row['price']
        text += f'{name}の{last_day.month}月の合計：{total_payment}円\n'
    text += '忘れずに精算してね^_^'
    return text 