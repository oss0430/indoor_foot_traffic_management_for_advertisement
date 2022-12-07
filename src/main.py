import json

from setting import device_setting, network_setting
from spatical_db_management import SpetialDBManagement
from LocUpdater import LocUpdater



def init():
    device_setting.device_setting()
    network_setting.network_setting()
    
def open_user_data_file():
    user_data = {
        'user_id' : None
    }
    with open('data/user_data.json', 'r') as file:
            data = json.load(file)
            user_data['user_id'] = data['user_id']
            
    return user_data

    
# 공간DB 초기 설정
spetial_DB = SpetialDBManagement()
spetial_DB.init_database()

# 사용자 위치 정보 AWS로 업로드
user_data = open_user_data_file()

location = LocUpdater()
init()
location.upload_localdata_to_dynamoDB()

# 사용자 위치 local database에 저장
spetial_DB.add_user_local_data(user_data['user_id'], )
    
    