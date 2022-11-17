import json
import boto3


def lambda_handler(event, context):
    
    body = event['body'].encode("utf8")
    body = body.decode('unicode_escape')
    body = body[1:-1]
    
    newdict = eval(body)
    
    items = {
        'ad_name' : newdict['name'],        # primary key
        'company' : newdict['company'],
        'ad_url'  : newdict['adv_url']
        
    }

    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table('Advertisement')
    response = table.put_item(Item = items)
    
    return response