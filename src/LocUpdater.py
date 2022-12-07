import time
import requests
import json
import base64

from datetime import datetime
from pytz import timezone

class Locupdater():
       
    def __init__(self) -> None:
        self.aws_url = " https://77gonk6cp7.execute-api.ap-northeast-1.amazonaws.com/default"

    
    def upload_localdata_to_dynamoDB(self, id_user, loc_x, loc_y, formatted_data):
        #formatted_data = self.now.strftime('%Y-%m-%d %H:%M:%S')
        
        local_data = {
            'id_user' : id_user,
            'x' : loc_x,
            'y' : loc_y,
            'date' : formatted_data[0:11],
            'time' : formatted_data[11:].replace(":","-")
            }
        host = self.aws_url + '/user_local_data'
        response = requests.post(host, data = local_data, headers=None)
        print(response)
            


def main():
    now = datetime.now(timezone('Asia/Seoul'))
    aws = Locupdater()
    user_loc = [0.027,-0.044,0.121]     # loc_x, loc_y
    floor = (user_loc[2] // 3) + 1      # floor
    formatted_data = now.strftime('%Y-%m-%d %H:%M:%S') # timestemp    


    file_path = 'data/user_data.json'
    with open(file_path, 'r') as file:
        data = json.load(file)          # user_id
    
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
'''