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
        'market_id' : int(newlist[0][10:]),
        'product_id' : int(newlist[1][11:]),        # primary key
        'user_id' : int(newlist[6][8:]),
        'x'  : newlist[2][6:],
        'y' : newlist[3][6:],
        'market_name' : newlist[4][12:].replace('+',''),
        'product_name' : newlist[5][13:].replace('+',''),
        'date' : newlist[7][5:],
        'time' : newlist[8][5:]
    }

    print(items)
    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table('product_data')
    response = table.put_item(Item = items)
    
    return response