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
        'id_user' : newlist[0][8:],        # primary key
        'market_name' : newlist[1][12:],
        'product_name'  : newlist[2][13:],
        'date' : newlist[3][5:-1].replace('-',''),
        'time' : newlist[4][5:].replace('-','')
    }

    print(items)
    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table('visit_store')
    response = table.put_item(Item = items)
    
    return response