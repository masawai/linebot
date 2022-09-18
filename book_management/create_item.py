import datetime
import os
import logging
import boto3
import requests

from notion_client import Client

logger = logging.getLogger(__name__)
logLevel=logging.DEBUG
logger.setLevel(logLevel)

#SSM
ssm = boto3.client('ssm')
access_token: str = ssm.get_parameter(Name='/linebot/book_management/access_token',WithDecryption=True)['Parameter']['Value']
notion_token: str = ssm.get_parameter(Name='/linebot/book_management/notion_token',WithDecryption=True)['Parameter']['Value']
database_id: str = ssm.get_parameter(Name='/linebot/book_management/database_id',WithDecryption=True)['Parameter']['Value']
channel_secret = ssm.get_parameter(Name='/linebot/book_management/channel_secret',WithDecryption=True)['Parameter']['Value']

notion = Client(auth=notion_token)

def get_bibliograph_by_isbn(isbn):
    r = requests.get(f'https://api.openbd.jp/v1/get?isbn={isbn}')
    return r.json()[0]['summary'] if r.json() else None

def parse_item(bibliograph=None):
    title = bibliograph.get('title')
    author = bibliograph.get('author')
    publisher = bibliograph.get('publisher')
    pubdate = bibliograph.get('pubdate')
    cover =  bibliograph.get('cover') if bibliograph.get('cover') else 'https://www.shoshinsha-design.com/wp-content/uploads/2020/05/noimage-1-760x460.png'
    isbn = bibliograph.get('isbn')
    properties = {
        'Name': {
            'title': [{
                'text': {
                    'content': title
                }
            }]
        },
        'Author': {
            'rich_text': [{
                'text': {
                    'content': author
                }
            }]
        },
        'Publisher': {
            'rich_text': [{
                'text': {
                    'content': publisher
                }
            }]
        },
        'Pubdate': {
            'rich_text': [{
                'text': {
                    'content': pubdate
                }
            }]
        },
        'Display': {
            'files': [{
                'name': "image url",
                'type' : "external",
                'external':{
                    'url' : cover
              }
            }]
        },
        'Isbn': {
            'rich_text': [{
                'text': {
                    'content': isbn
                }
            }]
        },
    }
    return properties

def create_item(bibliograph):
    properties=parse_item(bibliograph)
    logger.info(properties)
    r = notion.pages.create(
        **{
            'parent': {'database_id' : database_id},
            'properties': properties
        }
        )
