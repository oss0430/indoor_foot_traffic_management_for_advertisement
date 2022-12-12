import json
from point_of_sales import Get_data



def main():
    get_data = Get_data()
    
    json_data = get_data.get_user_local_data_in_dynamoDB(11143,103834)
    print(json_data)
    
    with open("local_data.json", "w") as outfile:
        json.dump(json_data, outfile, indent=4)
        
        
        
'''
{'Items': [{'y': '-0.86', 'date': '20221208', 'user_id': Decimal('11143'), 'time': Decimal('103834'), 'x': '0.562'}, {'y': '-0.438', 'date': '20221208', 'user_id': Decimal('11143'), 'time': Decimal('103840'), 'x': '1.348'}, {'y': '-0.438', 'date': '20221208', 'user_id': Decimal('11143'), 'time': Decimal('103845'), 'x': '1.348'}, {'y': '-0.286', 'date': '20221208', 'user_id': Decimal('11143'), 'time': Decimal('103849'), 'x': '1.403'}, {'y': '-0.286', 'date': '20221208', 'user_id': Decimal('11143'), 'time': Decimal('103853'), 'x': '1.403'}, {'y': '-1.267', 'date': '20221208', 'user_id': Decimal('11143'), 'time': Decimal('104255'), 'x': '1.223'}, {'y': '1677721.6', 'date': '20221208', 'user_id': Decimal('11143'), 'time': Decimal('104303'), 'x': '13415.94'}, {'y': '1677721.6', 'date': '20221208', 'user_id': Decimal('11143'), 'time': Decimal('104308'), 'x': '13415.94'}, {'y': '1677721.6', 'date': '20221208', 'user_id': Decimal('11143'), 'time': Decimal('104341'), 'x': '13415.94'}, {'y': '1677721.6', 'date': '20221208', 'user_id': Decimal('11143'), 'time': Decimal('104345'), 'x': '13415.94'}, {'y': '1677721.6', 'date': '20221208', 'user_id': Decimal('11143'), 'time': Decimal('104349'), 'x': '13415.94'}, {'y': '1677721.6', 'date': '20221208', 'user_id': Decimal('11143'), 'time': Decimal('104353'), 'x': '13415.94'}, {'y': '0.051', 'date': '20221208', 'user_id': Decimal('11143'), 'time': Decimal('104524'), 'x': '-0.145'}, {'y': '0.058', 'date': '20221208', 'user_id': Decimal('11143'), 'time': Decimal('104529'), 'x': '-0.128'}, {'y': '0.058', 'date': '20221208', 'user_id': Decimal('11143'), 'time': Decimal('104533'), 'x': '-0.128'}, {'y': '0.056', 'date': '20221208', 'user_id': Decimal('11143'), 'time': Decimal('104537'), 'x': '-0.096'}, {'y': '0.056', 'date': '20221208', 'user_id': Decimal('11143'), 'time': Decimal('104542'), 'x': '-0.096'}, {'y': '0.104', 'date': '20221208', 'user_id': Decimal('11143'), 'time': Decimal('105457'), 'x': '0.039'}, {'y': '0.269', 'date': '20221208', 'user_id': Decimal('11143'), 'time': Decimal('105505'), 'x': '0.155'}, {'y': '0.289', 'date': '20221208', 'user_id': Decimal('11143'), 'time': Decimal('105510'), 'x': '0.13'}, {'y': '1.204', 'date': '20221208', 'user_id': Decimal('11143'), 'time': Decimal('105514'), 'x': '1.251'}, {'y': '0.978', 'date': '20221208', 'user_id': Decimal('11143'), 'time': Decimal('105519'), 'x': '1.325'}, {'y': '0.978', 'date': '20221208', 'user_id': Decimal('11143'), 'time': Decimal('105523'), 'x': '1.325'}, {'y': '0.797', 'date': '20221208', 'user_id': Decimal('11143'), 'time': Decimal('105527'), 'x': '1.495'}, {'y': '0.797', 'date': '20221208', 'user_id': Decimal('11143'), 'time': Decimal('105532'), 'x': '1.495'}], 'Count': 25, 'ScannedCount': 25, 'ResponseMetadata': {'RequestId': 'RPRITIPR1PQVR7KVF78E4Q7677VV4KQNSO5AEMVJF66Q9ASUAAJG', 'HTTPStatusCode': 200, 'HTTPHeaders': {'server': 'Server', 'date': 'Mon, 12 Dec 2022 05:13:03 GMT', 'content-type': 'application/x-amz-json-1.0', 'content-length': '2791', 'connection': 'keep-alive', 'x-amzn-requestid': 'RPRITIPR1PQVR7KVF78E4Q7677VV4KQNSO5AEMVJF66Q9ASUAAJG', 'x-amz-crc32': '3707951443'}, 'RetryAttempts': 0}}

'''
    
if __name__ == '__main__': 
    main()
