import json
import boto3


def lambda_handler(event, context):
    dynamodb = boto3.resource('dynamodb')
    print(event)
    adv_name = event['name']
    print(adv_name)
    
    table_name = 'Advertisement'
    holiday_info = {
        
    }
    client = boto3.client('dynamodb')
    response = client.batch_get_item(
        RequestItems = {
            table_name : {
                'Keys' : [
                    {
                        'ad_name' : {
                            'S' : adv_name
                        }
                    }
                ]
            }
        }
    )
    adv_data_return = response['Responses'].get(table_name)
    print(adv_data_return)

    return {
        'statusCode' : 200,
        'body' : json.dumps(adv_data_return)
    }