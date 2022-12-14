import json
import boto3
import base64
from boto3.dynamodb.conditions import Key
from decimal import Decimal

def lambda_handler(event, context):
    data = event.get('body')
    result = base64.b64decode(data).decode('utf-8')
    print(result)
    
    newlist = result.split('&')
    items = {
        'user_id' : newlist[0][8:],        # primary key
        'time1' : newlist[1][6:],
        'time2' : newlist[2][6:],
    }
    print(items)
    
    
    resource = boto3.resource('dynamodb')
    table = resource.Table("local_data")

    time_range = [int(items['time1']),int(items['time2'])]
    scan1 = {"FilterExpression": Key("time").between(time_range[0],time_range[1])}
    print(table.scan(**scan1)['Items'])
    
    response = table.scan(**scan1)['Items']
    print(response)
    
    for i in range (len(response)):
        dc_deviceid = response[i]['user_id']
        response[i]['user_id'] = int(dc_deviceid)
        dc_date = response[i]['date']
        response[i]['date'] = int(dc_date)        
        dc_time = response[i]['time']
        response[i]['time'] = int(dc_time)        
        

    return {
        'statusCode' : 200,
        'body' : json.dumps(response)
    }
    
    '''
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
    
    dynamodb = boto3.resource('dynamodb')
    table_name = 'local_data'
    
    client = boto3.client('dynamodb')
    response = client.batch_get_item(
        RequestItems = {
            table_name : {
                'Keys' : [
                    {
                        'user_id' : {
                            'N' : items['user_id'],
                        },
                        'time' : {
                            'N' : items['time'],
                        },
                    }
                ]
            }
        }
    )
    result = response['Responses'].get(table_name)
    print(result)

    return {
        'statusCode' : 200,
        'body' : json.dumps(result)
    }
    '''