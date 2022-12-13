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
    table = resource.Table("point_of_sales")
    query = {"KeyConditionExpression": Key("product_id").eq(int(items['product_id']))}

    print(table.query(**query)['Items'])
    
    response = table.query(**query)['Items']
    print(response)
    
    for i in range (len(response)):
        dc_productid = response[i]['product_id']
        response[i]['product_id'] = int(dc_productid)
        dc_price = response[i]['price']
        response[i]['price'] = int(dc_price)        
        
        dc_date = response[i]['date']
        response[i]['date'] = int(dc_date)
        dc_count = response[i]['count']
        response[i]['count'] = int(dc_count)        
        

    return {
        'statusCode' : 200,
        'body' : json.dumps(response)
    }