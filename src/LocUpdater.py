import time
import requests
import json
import base64

from datetime import datetime
from datetime import datetime
from pytz import timezone

class Locupdater():
       
    def __init__(self) -> None:
        self.WAITTIME = 5
        self.aws_url = None
        self.aws_url = " https://77gonk6cp7.execute-api.ap-northeast-1.amazonaws.com/default"

    
    def upload_localdata_to_dynamoDB(self, id_user, loc_x, loc_y, formatted_data):
        #formatted_data = self.now.strftime('%Y-%m-%d %H:%M:%S')
        
        local_data = {
            'id_user' : id_user,
            # 'x' : self.point_list[i][0],
            # 'y' : self.point_list[i][1],
            'x' : loc_x,
            'y' : loc_y,
            'date' : formatted_data[0:11],
            'time' : formatted_data[11:].replace(":","-")
            }
        host = self.aws_url + '/user_local_data'
        response = requests.post(host, data = local_data, headers=None)
        print(response)
            
        
    def upload_product_hold_data_to_dynamoDB(self, id_user, market_name, product_name, formatted_data):
        #formatted_data = self.now.strftime('%Y-%m-%d %H:%M:%S')
        pd_hold_data = {
            'id_user' : id_user,
            'market_name' : market_name,
            'product_name' : product_name,
            'date' : formatted_data[0:11],
            'time' : formatted_data[11:].replace(":","-")
        }
        host = self.aws_url + '/user_hold_product'
        response = requests.post(host, data = pd_hold_data, headers=None)
        print(response)
        return response


def main():
    now = datetime.now(timezone('Asia/Seoul'))

    file_path = 'data/user_data.json'
    with open(file_path, 'r') as file:
        data = json.load(file)    

    
    aws = Locupdater()
    print(aws.WAITTIME)
    user_loc = [0.027,-0.044,0.121]
    floor = (user_loc[2] // 3) + 1
    formatted_data = now.strftime('%Y-%m-%d %H:%M:%S') # timestemp    
    aws.upload_localdata_to_dynamoDB(data['user_id'], user_loc[0], user_loc[1], formatted_data) 
    

if __name__ == '__main__': 
    main()


'''
sample_data = {
    'market_id' : 333,
    'market_name' : 'APPLE',
    'product_name' : 'iPhone14',
    'user_id' :  99231,
    'x_user' : 3,
    'y_user' : 4,
    'timestemp' : None
}

test = locupdater()
#print(test.upload_localdata_to_dynamoDB())
now = datetime.now(timezone('Asia/Seoul'))
formatted_data = now.strftime('%Y-%m-%d %H:%M:%S')
# print(formatted_data)
# print(test.upload_localdata_to_dynamoDB())
# test.upload_product_hold_data_to_dynamoDB(sample_data['user_id'], sample_data['market_name'], sample_data['product_name'],formatted_data)
test.get_location_point()

test.upload_localdata_to_dynamoDB(sample_data['user_id'], formatted_data)


test = SpetialDBManagement('admin1', '1234', 'location_data')
now = datetime.now(timezone('Asia/Seoul'))

# 사용자가 상품 근처에 WAITTIME 만큼 있을때 클라우드에 업로드
sample_data = {
    'market_id' : 333,
    'user_id' :  99231,
    'x_user' : 3,
    'y_user' : 4,
    'timestemp' : None
}

sample_data['timestemp'] = timestemp = now.strftime('%Y-%m-%d %H:%M:%S')
temp1 = test.user_hold_product(sample_data['market_id'], sample_data['user_id'], sample_data['x_user'], sample_data['y_user'], sample_data['timestemp'])
if (temp1 != -1):
    product_name1 = temp1[1]

time.sleep(WAITTIME)

sample_data['timestemp'] = timestemp = now.strftime('%Y-%m-%d %H:%M:%S')
temp2 = test.user_hold_product(sample_data['market_id'], sample_data['user_id'], sample_data['x_user'], sample_data['y_user'], sample_data['timestemp'])
if (temp2 != -1):
    product_name2 = temp2[1]
    
if (product_name1 == product_name2):
    temp = 'market ID = {market_id}, product name = {product_name}'.format(market_id = temp2[0], product_name = temp2[1])
    print('->  ' + temp)
    
'''