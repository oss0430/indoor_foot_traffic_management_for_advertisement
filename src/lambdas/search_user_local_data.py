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