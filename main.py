import sys, json
sys.path.insert(0, './lib')
import requests
from edsby import Edsby
from ConfigParser import ConfigParser
config = ConfigParser()

def handle_request(event, context):
    config.readfp(open('config.cfg'))

    # If request body is empty
    if event['body'] is None:
        return formatResponse(400, None, 'error', 'bad request')

    # If the body is a string, then we need to parse it to JSON
    if isinstance(event['body'], basestring):
        try:
            event['body'] = json.loads(event['body'])
        except:
            # If parsing fails, that means we got invalid JSON. Return an error
            return formatResponse(400, None, 'error', 'bad request')

    # Check that the API key is valid
    if event['body']['key'] is None or config.get('api_key', 'key') != event['body']['key']:
        return formatResponse(403, None, 'error', 'invalid API key')

    # Constuct the message from the POSTed json. Defaults to ''
    link = event['body']['link'] if 'link' in event['body'] else ''
    text = event['body']['text'] if 'text' in event['body'] else ''
    # Function will either use credentials provided in the request or
    # fall back to credentials provided in the config file by default.
    classIDs = event['body']['classIDs'] if 'classIDs' in event['body'] else config.get('edsby', 'classIDs')
    username = event['body']['username'] if 'username' in event['body'] else config.get('edsby', 'username')
    password = event['body']['password'] if 'password' in event['body'] else config.get('edsby', 'password')

    message = postMessage((username, password), link, text, classIDs.split(','))

    return formatResponse(200, None, 'success', message)


def postMessage(creds, link, text, classIDs):
    edsby = Edsby(host=config.get('edsby', 'host'), username=creds[0],
        password=creds[1], meta={'nid':config.get('edsby', 'metaNID')})

    # Retrieve link metadata
    meta = edsby.scrapeURLMetadata(classIDs[0], link)
    meta = edsby.formatURLMetadata(meta)

    # Construct JSON payload with message
    message = {
            'text': text + ' ' + link,
            'url': json.dumps(meta),
            'pin': 8,
            'nodetype': 4,
            'node_subtype': 0,
            'filedata': '',
            'files': '',
    }

    # Submit message to Edsby for each class
    for NID in classIDs:
        edsby.postMessageInClassFeed(NID, message)

    return message

# Generic response formatter for return values.
def formatResponse(code, headers, message, content):
    return {"isBase64Encoded": False, "statusCode": code, "headers": headers, "body": json.dumps({message: content})}
