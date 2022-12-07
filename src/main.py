import json

from datetime import datetime
from pytz import timezone
# from setting import device_setting, network_setting
from spatical_db_management import SpetialDBManagement
from LocUpdater import LocUpdater



# def init():
#     print("init")
#     network_setting.network_setting()
#     device_setting.device_setting()
    
def open_file(path):
    user_data = {
        'user_id' : None
    }
    with open(path, 'r') as file:
            data = json.load(file)
            
    return data

# {'account': 'admin1', 'password': 1234, 'table': 'location_data'}


now = datetime.now(timezone('Asia/Seoul'))
floor = 3
    
# 공간DB 초기 설정
path = 'data/DB_account.json'
db_account = open_file(path)
spetial_DB = SpetialDBManagement(db_account['account'], db_account['password'], db_account['table'])
spetial_DB.init_database()

# market 정보 DB에 저장
path = 'data/market_data.json'
market_data = open_file(path)
spetial_DB.add_market_data(
    market_data['market_id'], 
    market_data['market_name'], 
    market_data['POLYGON'], 
    market_data['floor'], 
    market_data['sector'], 
    market_data['detail_type']
)

# product 정보 DB에 저장
test.add_product_data(333, 99231, 3, 4, 'galaxy S22', '1001')
path = 'data/product_data.json'
product_data = open_file(path)
spatical_DB.add_product_data(
    product_data['market_id'], 
    product_data['product_id'], 
    product_data['x'], 
    product_data['y'], 
    product_data['product_name'], 
    product_data['product_type']
)

#사용자 위치 정보 AWS로 업로드
path = 'data/user_data.json'
user_data = open_file(path)
location = LocUpdater()
#init() -----------------------
formatted_data = self.now.strftime('%Y-%m-%d %H:%M:%S')
location.upload_localdata_to_dynamoDB()
user_uwb_local = location.point_list

#사용자 위치 local database에 저장
# for i in range(len(user_uwb_local))
#     spetial_DB.add_user_local_data(
#         user_data['user_id'], 
#         i, 
#         floor, 
#         formatted_data
#     )
#     spetial_DB.print_user_local_data(formatted_data)
    


    