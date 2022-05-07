import logging
import sys

import boto3
from bs4 import BeautifulSoup 
from notion_client import Client
import requests

#SSM
ssm = boto3.client('ssm')
access_token: str = ssm.get_parameter(Name='/linebot/vocabulary/access_token',WithDecryption=True)['Parameter']['Value']
notion_token: str = ssm.get_parameter(Name='/linebot/vocabulary/notion_token',WithDecryption=True)['Parameter']['Value']
database_id: str = ssm.get_parameter(Name='/linebot/vocabulary/database_id',WithDecryption=True)['Parameter']['Value']

notion = Client(auth=notion_token)
url='https://ejje.weblio.jp/content/'

def search_weblio(word):
    response = requests.get(url+word)
    soup = BeautifulSoup(response.text, 'html.parser')
    return soup

def parse_item(word, user_id):
    soup = search_weblio(word)
    pronunciation = soup.find(class_='phoneticEjjeDesc').get_text() if soup.find(class_='phoneticEjjeDesc') else ''
    japanese = soup.find(class_='content-explanation ej').get_text().strip()
    
    properties = {
        'Word': {
            'title': [{
                'text': {
                    'content': word
                }
            }]
        },
        'Pronunciation': {
            'rich_text': [{
                'text': {
                    'content': pronunciation
                }
            }]
        },
        'Japanese': {
            'rich_text': [{
                'text': {
                    'content': japanese
                }
            }]
        },
        'Line ID': {
            'rich_text': [{
                'text': {
                    'content': user_id
                }
            }]
        },
        'Weblio': {
            'url': url+word.replace(' ', '+')
        },
    }
    return properties

def create_item(word, user_id):
    properties=parse_item(word, user_id)
    r = notion.pages.create(
        **{
            'parent': {'database_id' : database_id},
            'properties': properties
        }
        )
    print(r)

if __name__ == '__main__':
    create_item(sys.argv[1], sys.argv[2])