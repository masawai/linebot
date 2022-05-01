import json

import query_item

def lambda_handler(event, context):
    items = query_item.query_item()

    return {
        'statusCode' : 200,
        'body' : json.dumps(items),
        'headers': {
            # 'Access-Control-Allow-Origin': 'http://vue-test-site-155385059623.s3-website-ap-northeast-1.amazonaws.com',
            'Access-Control-Allow-Origin': '*',
            'Access-Control-Allow-Methods': 'OPTIONS,POST,GET'
        }
    }
