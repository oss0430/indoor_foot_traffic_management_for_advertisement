#from setting import Device_setting, Network_setting
import time
import json
import requests
import uwb_localization
from datetime import datetime
from pytz import timezone
from MDEK_setting import Device_setting


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
            

def load_data_with_json(file_path):
    with open(file_path, 'r') as file:
        data = json.load(file)
    
    return data


def main():

    # init AWS
    aws = Locupdater()

    Device_setting.device_setting()          # -> 시작할때 한번만 하기 (networkd 세팅은 no)

    life = 5
    while(1):
        now = datetime.now(timezone('Asia/Seoul'))
        # Location data for user & upload to AWS

        path = "data/user_data.json"
        data = load_data_with_json(path)
        user_loc = uwb_localization.localization()              # loc_x, loc_y, loc_z
        
        floor = (user_loc[2] // 3) + 1
        formatted_data = now.strftime('%Y-%m-%d %H:%M:%S') # timestemp    
        aws.upload_localdata_to_dynamoDB(data['user_id'], user_loc[0], user_loc[1], formatted_data)
        
        
        life -= 1
        if(life == 0):
            break
        time.sleep(1)


    

if __name__ == '__main__': 
    main()


