import datetime
import os
import logging
import boto3
import requests

from notion_client import Client

logger = logging.getLogger(__name__)

#SSM
ssm = boto3.client('ssm')
access_token: str = ssm.get_parameter(Name='/linebot/book_management/access_token',WithDecryption=True)['Parameter']['Value']
notion_token: str = ssm.get_parameter(Name='/linebot/book_management/notion_token',WithDecryption=True)['Parameter']['Value']
database_id: str = ssm.get_parameter(Name='/linebot/book_management/database_id',WithDecryption=True)['Parameter']['Value']
channel_secret = ssm.get_parameter(Name='/linebot/book_management/channel_secret',WithDecryption=True)['Parameter']['Value']

notion = Client(auth=notion_token)

def get_bibliograph_by_isbn(isbn):
    r = requests.get(f'https://api.openbd.jp/v1/get?isbn={isbn}')
    return r.json()[0]['summary'] if r.json() else False

def parse_item(bibliograph=None):
    properties = {
        'Name': {
            'title': [{
                'text': {
                    'content': bibliograph['title']
                }
            }]
        },
        'Author': {
            'rich_text': [{
                'text': {
                    'content': bibliograph['author']
                }
            }]
        },
        'Publisher': {
            'rich_text': [{
                'text': {
                    'content': bibliograph['publisher']
                }
            }]
        },
        'Pubdate': {
            'rich_text': [{
                'text': {
                    'content': bibliograph['pubdate']
                }
            }]
        },
        'Display': {
            'files': [{
                'name': "image url",
                'type' : "external",
                'external':{
                    'url' : bibliograph['cover']
              }
            }]
        },
        'Isbn': {
            'rich_text': [{
                'text': {
                    'content': bibliograph['isbn']
                }
            }]
        },
    }
    return properties

def create_item(bibliograph):
    properties=parse_item(bibliograph)
    r = notion.pages.create(
        **{
            'parent': {'database_id' : database_id},
            'properties': properties
        }
        )
