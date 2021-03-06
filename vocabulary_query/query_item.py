import time

import boto3
from notion_client import Client

#SSM
ssm = boto3.client('ssm')
notion_token: str = ssm.get_parameter(Name='/linebot/vocabulary/notion_token',WithDecryption=True)['Parameter']['Value']
database_id: str = ssm.get_parameter(Name='/linebot/vocabulary/database_id',WithDecryption=True)['Parameter']['Value']

notion = Client(auth=notion_token)


def parse_item(items, res):
    items.extend([
        {
            'Word' : result['properties']['Word']['title'][0]['plain_text'],
            'Japanese' : result['properties']['Japanese']['rich_text'][0]['plain_text'],
            'User' : result['properties']['User']['formula']['string'],
        }
        for result in res['results'] 
        if result['properties'].get('Word') and result['properties'].get('Japanese')
        ])
    return items

def query_item(items=[], cnt=0, next_cursor=None):
    print(f'cnt:{cnt}, next_cursor:{next_cursor}')
    param = {"database_id" : database_id} if cnt == 0 else {"database_id" : database_id, "start_cursor" : next_cursor}
    res = notion.databases.query(**param)
    items = parse_item(items, res)
    has_more = res['has_more']
    next_cursor = res['next_cursor']
    if has_more:
        cnt += 1
        return query_item(items, cnt, next_cursor)
    return items

if __name__ == '__main__':
    start_time = time.perf_counter()
    items = query_item()
    end_time = time.perf_counter()
    print(end_time - start_time)