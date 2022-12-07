#from setting import Device_setting, Network_setting
import time
import json

import uwb_localization
from datetime import datetime
from pytz import timezone
from spatical_db_management import SpetialDBManagement
from LocUpdater import Locupdater


def load_data_with_json(file_path):
    with open(file_path, 'r') as file:
        data = json.load(file)
    
    return data


def main():
    # init Database
    path = 'data/DB_account.json'
    data= load_data_with_json(path)
    dbms = SpetialDBManagement(data['account'], str(data['password']), data['table'])
    dbms.init_database()
    
    # init AWS
    aws = Locupdater()

    #Device_setting.device_setting()          # -> 시작할때 한번만 하기 (networkd 세팅은 no)

    life = 5
    while(1):
        now = datetime.now(timezone('Asia/Seoul'))
        # Location data for user & upload to AWS

        path = "data/user_data.json"
        data = load_data_with_json(path)
        #user_loc = uwb_localization.localization()              # loc_x, loc_y, loc_z
        
        user_loc = [0.027,-0.044,0.121]                         # 내일 시연할 때 여기 지워주기
        floor = (user_loc[2] // 3) + 1
        local_POINT_type = '(' + str(user_loc[0]) + ", " + str(user_loc[1]) + ")"
        formatted_data = now.strftime('%Y-%m-%d %H:%M:%S') # timestemp    
        
        aws.upload_localdata_to_dynamoDB(data['user_id'], user_loc[0], user_loc[1], formatted_data)
        
        dbms.add_user_local_data(data['user_id'], 'POINT(1,3)', floor, formatted_data)
        dbms.print_user_local_data(formatted_data)
        
        life -= 1
        if(life == 0):
            break
        time.sleep(1)


    

if __name__ == '__main__': 
    main()


