import base64
import json
import logging
import gzip
import os
import boto3

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

def lambda_handler(event, context):
    data = gzip.decompress(base64.b64decode(event['awslogs']['data']))
    data_json = json.loads(data)
    events = data_json["logEvents"]
    logger.info(json.dumps(events))

    for event in events: 
        try:
            sns = boto3.client('sns')
            res = sns.publish(
                TopicArn = os.environ['SNS_TOPIC_ARN'],
                Subject = os.environ['ALARM_SUBJECT'],
                Message = event['message']
            )
        except Exception as e:
            logger.error(e)
