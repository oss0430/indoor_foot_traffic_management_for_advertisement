import json
import boto3
import base64


def lambda_handler(event, context):
    
    
    data = event.get('body')
    result = base64.b64decode(data).decode('utf-8')
    print(list)
    print(result)
    
    newlist = result.split('&')
    print(newlist)
    
    '''
    ['market_name=iPhone+14', 'product_name=Apple', 'product_id=11343', 'count=14', 'price=1250000', 'date=2022-12-07']

    '''
    items = {
        'product_id'  : int(newlist[2][11:]),  
        'date' : int(newlist[5][5:].replace('-','')),
        'market_name' : newlist[0][12:].replace('+',' '),   
        'product_name' : newlist[1][13:].replace('+',' '),
        'count' : int(newlist[3][6:]),
        'price' : int(newlist[4][6:])
    }

    print(items)
    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table('point_of_sales')
    response = table.put_item(Item = items)
    
    return response