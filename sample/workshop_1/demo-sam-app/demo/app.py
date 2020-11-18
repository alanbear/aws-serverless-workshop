import os
import json
import boto3
import uuid

s3_client = boto3.client('s3')
dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table(os.environ['dynamodb_table'])

def lambda_handler(event, context):
    
    # upload s3 file
    bucket = os.environ['s3_bucket']
    object_name = 'upload_file'
    
    upload_file = 'requirements.txt'
    response = s3_client.upload_file(upload_file, bucket, object_name)
    
    # download s3 file
    download_file = '/tmp/download_file'
    s3_client.download_file(bucket, object_name, download_file)
    
    with open(download_file, 'r') as f:
        print(f.read())
    
    id = str(uuid.uuid1())
    
    # insert dynamodb table item
    table.put_item(
        Item={
            'id': id,
            'column_1': 'aaa',
            'column_2': 123
        }
    )
    
    # get dynamodb table item
    response = table.get_item(
        Key={
            'id': id
        },
        ConsistentRead=True
    )
    item = response['Item']
    print(item)
    
    return 'ok'
