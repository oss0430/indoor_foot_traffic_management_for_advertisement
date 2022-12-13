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
        'sample_time1' : newlist[0][13:],        # primary key
        'sample_time2' : newlist[1][13:]
    }
    print(items)
    
    
    resource = boto3.resource('dynamodb')
    table = resource.Table("face_count")

    time_range = [int(items['sample_time1']),int(items['sample_time2'])]
    scan1 = {"FilterExpression": Key("sample_time").between(time_range[0],time_range[1])}
    print(table.scan(**scan1)['Items'])
    
    response = table.scan(**scan1)['Items']
    print(response)
    
    for i in range (len(response)):
        dc_deviceid = response[i]['device_id']
        response[i]['device_id'] = int(dc_deviceid)
        dc_date = response[i]['date']
        response[i]['date'] = int(dc_date)        
        dc_time = response[i]['time']
        response[i]['time'] = int(dc_time)        
        
        dc_sampletime = response[i]['sample_time']
        response[i]['sample_time'] = int(dc_sampletime)
        dc_face_count = response[i]['facecount']
        response[i]['facecount'] = int(dc_face_count)        
        

    return {
        'statusCode' : 200,
        'body' : json.dumps(response)
    }