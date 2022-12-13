import json
import boto3
import base64
from boto3.dynamodb.conditions import Key
from decimal import Decimal

def lambda_handler(event, context):
    data = event.get('body')
    result = base64.b64decode(data).decode('utf-8')
    print(list)
    print(result)
    
    newlist = result.split('&')
    items = {
        'user_id' : newlist[0][8:],        # primary key
        'time' : newlist[1][5:]
    }
    print(items)
    
    resource = boto3.resource('dynamodb')
    table = resource.Table("local_data")
    query = {"KeyConditionExpression": Key("user_id").eq(int(items['user_id']))}
    print(table.query(**query)['Items'])
    
    response = table.query(**query)['Items']
    print(response)
    
    for i in range (len(response)):
        dc_time = response[i]['time']
        response[i]['time'] = int(dc_time)
        dc_userid = response[i]['user_id']
        response[i]['user_id'] = int(dc_userid)

    return {
        'statusCode' : 200,
        'body' : json.dumps(response)
    }