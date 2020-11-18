import json
import boto3

dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('alanbear-agw-sample-table')

def lambda_handler(event, context):
    
    id = event['pathParameters']['id']

    # insert dynamodb table item
    table.put_item(
        Item={
            'id': id,
            'value': json.loads(event['body'])['value']
        }
    )

    return {
        "statusCode": 200,
        "body": 'successfully saved',
    }
