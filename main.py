import sys, json
sys.path.insert(0, './lib')
import requests
from edsby import Edsby
from ConfigParser import ConfigParser
config = ConfigParser()

def handle_request(event, context):
    config.readfp(open('config.cfg'))

    if event['body'] is None:
        return {"isBase64Encoded": False, "statusCode": 400, "headers": None, "body": json.dumps({"error": "bad request"})}

    if event['body']['key'] is None or config.get('api_key', 'key') is not event['body']['key']:
        return {"isBase64Encoded": False, "statusCode": 403, "headers": None, "body": json.dumps({"error": "no API key"})}

	link = event['body']['link'] if 'link' in event else ''
    text = event['body']['text'] if 'text' in event else ''
    classIDs = event['body']['classIDs'] if 'classIDs' in event else config.get('edsby', 'classIDs')
    username = event['body']['username'] if 'username' in event else config.get('edsby', 'username')
    password = event['body']['password'] if 'password' in event else config.get('edsby', 'password')

    message = postMessage((username, password), link, text, classIDs.split(','))

    return {"isBase64Encoded": False, "statusCode": 403, "headers": None, "body": json.dumps({"success":message})}


def postMessage(creds, link, text, classIDs):
    edsby = Edsby(host=config.get('edsby', 'host'), username=creds[0],
        password=creds[1], meta={'nid':config.get('edsby', 'metaNID')})

    meta = edsby.scrapeURLMetadata(classIDs[0], link)
    meta = edsby.formatURLMetadata(meta)

    message = {
            'text': text + ' ' + link,
            'url': json.dumps(meta),
            'pin': 8,
            'nodetype': 4,
            'node_subtype': 0,
            'filedata': '',
            'files': '',
    }

    for NID in classIDs:
        edsby.postMessageInClassFeed(NID, message)

    return message
