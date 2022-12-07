import json
import boto3
from boto3.dynamodb.conditions import Key, Attr

def lambda_handler(event, context):
    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table('product_data')
    
    response = table.scan()
    
    
    print(response)
    items = response['Items']
    print(items)
    return {
        'statusCode' : 200,
        'body' : json.dumps(items)
    }