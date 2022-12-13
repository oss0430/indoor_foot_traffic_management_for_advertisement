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
        'product_id' : newlist[0][11:]        # primary key
    }
    print(items)
    
    
    resource = boto3.resource('dynamodb')
    table = resource.Table("product_data")
    query = {"KeyConditionExpression": Key("product_id").eq(int(items['product_id']))}

    print(table.query(**query)['Items'])
    
    response = table.query(**query)['Items']
    print(response)
    
    for i in range (len(response)):
        dc_productid = response[i]['product_id']
        response[i]['product_id'] = int(dc_productid)
        dc_marketid = response[i]['market_id']
        response[i]['market_id'] = int(dc_marketid)
        dc_userid = response[i]['user_id']
        response[i]['user_id'] = int(dc_userid)        
        
        dc_date = response[i]['date']
        response[i]['date'] = int(dc_date)
        dc_time = response[i]['time']
        response[i]['time'] = int(dc_time)        
        

    return {
        'statusCode' : 200,
        'body' : json.dumps(response)
    }