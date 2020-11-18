import json
import boto3

dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('alanbear-agw-sample-table')

def lambda_handler(event, context):

    id = event['pathParameters']['id']

    # get dynamodb table item
    response = table.get_item(
        Key={
            'id': id
        },
        ConsistentRead=True
    )
    
    if 'Item' in response:
        item = response['Item']
    
        return {
            "statusCode": 200,
            "body": item['value'],
        }
    else:
        return {
            "statusCode": 404,
            "body": 'not found',
        }
