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
        'ID' : newlist[0][8:],        # primary key
        'x' : newlist[1][2:],
        'y'  : newlist[2][2:],
        'date' : newlist[3][5:-1].replace('-',''),
        'time' : newlist[4][5:].replace('-','')
    }

    print(items)
    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table('Local_data')
    response = table.put_item(Item = items)
    
    return response