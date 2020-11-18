import os
import jwt
import logging
import re

JWT_SECRET = 'test'

def lambda_handler(event, context):
    
    request = event['Records'][0]['cf']['request']
    headers = request['headers']
    uri = request['uri']

    if uri == '/' or uri.startswith('/js') or uri.startswith('/css') or uri.startswith('/img'):
        return request

    jwt_token_headers = headers.get('Authorization', [])

    jwt_token = ''
    if len(jwt_token_headers) > 0:
        header_value = jwt_token_headers[0]['value']
        jwt_token = re.sub('Bearer ', '', header_value)

    try:
        jwt.decode(jwt_token, JWT_SECRET, algorithms=['HS256'])
        return request
    except Exception as e:
        logging.warning(e)
        return {
            'status': '401',
            'statusDescription': 'Unauthorized please enter correct jwt token',
        }