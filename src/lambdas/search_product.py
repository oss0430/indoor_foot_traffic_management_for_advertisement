import json
import boto3
import base64


def lambda_handler(event, context):
    data = event.get('body')
    result = base64.b64decode(data).decode('utf-8')
    print(result)

    dynamodb = boto3.resource('dynamodb')
    table_name = 'product_data'
    
    items = {
        'user_id' : result[11:]        # primary key
    }
    print(items)
    
    client = boto3.client('dynamodb')
    response = client.batch_get_item(
        RequestItems = {
            table_name : {
                'Keys' : [
                    {
                        'product_id' : {
                            'N' : items['user_id']
                        }
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