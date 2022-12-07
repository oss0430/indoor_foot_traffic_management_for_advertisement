import json
import boto3
import base64


def lambda_handler(event, context):
    data = event.get('body')
    result = base64.b64decode(data).decode('utf-8')
    print(list)
    print(result)
    
    '''
    items = {
        'user_id' : newlist[0][8:],        # primary key
        'time' : newlist[0][5:].replace('-','')
    }
    print(items)
    '''
    
    dynamodb = boto3.resource('dynamodb')
    table_name = 'local_data'
    
    items = {
        'user_id' : str(11143),        # primary key
        'time' : str(203711)
    }
    
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