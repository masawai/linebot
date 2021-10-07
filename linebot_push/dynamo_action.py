import boto3
import datetime
from boto3.dynamodb.conditions import Key

# DynamoDB
dynamodb = boto3.resource('dynamodb')
table    = dynamodb.Table('linebot')

def query_item(event=None):
    # This code will be executed at the beginning of the month.
    # The month of last day is last month
    last_day = datetime.datetime.now() - datetime.timedelta(days=1)
    year_month = last_day.strftime('%Y/%-m')
    res = table.query(
        KeyConditionExpression=Key('name').eq('Masaya') & Key('date').begins_with(year_month)
    )
    text = ''
    total_payment = 0
    for row in res['Items']:
        text += f"{row['description']} {row['price']}円\n" 
        total_payment += row['price']
    text += f"{last_day.month}月の合計：{total_payment}円"
    return text 
