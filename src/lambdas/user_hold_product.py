import json
import boto3
import base64


def lambda_handler(event, context):
    
    
    data = event.get('body')
    result = base64.b64decode(data).decode('utf-8')
    print(list)
    print(result)
    
    newlist = result.split('&')
    
    items = {
        'product_id' : int(newlist[0][11:]),        # primary key
        'user_id' : newlist[1][8:]
        'time' : newlist[2][5:]
    }

    print(items)
    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table('hold_product')
    response = table.put_item(Item = items)
    
    return response