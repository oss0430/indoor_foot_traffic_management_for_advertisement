import json
import requests
import base64
import time

from datetime import datetime
from pytz import timezone
from point_of_sales import Product 
from spatical_db_management import SpatialDBManagement

class Get_data():
    def __init__(
        self,
        aws_url = None
    ) -> None:
        self.aws_url = "https://77gonk6cp7.execute-api.ap-northeast-1.amazonaws.com/default"
        
        return None
    
    
    def get_user_local_data_in_dynamoDB(
        self,
        user_id,
        time
    ):
        data = {
            "user_id" : user_id,
            "time" : time
        }
        host = self.aws_url + '/search_user_local_data'
        response = requests.post(host, data=data, headers=None)
        return_data = json.loads(response.content)
        
        if(len(return_data) == 0):
            return -1
                    
        
        result_dict = {
        'user_id' : return_data[0]['user_id']['N'],
        'x' : return_data[0]['x']['S'],
        'y' : return_data[0]['y']['S'],
        'date' : int(return_data[0]['date']['S']),
        'time' : return_data[0]['time']['N']
        }
        
        return result_dict


    def get_product_data_in_range():
        host = self.aws_url + '/get_product_condition_data'
        data = {}
        response = requests.post(host, data=data, headers=None)

        return response
        

def load_data_with_json(file_path):
    with open(file_path, 'r') as file:
        data = json.load(file)
    
    return data
    
    
def main():

    now = datetime.now(timezone('Asia/Seoul'))    
    get_data = Get_data()   
    product_data = Product()
    
    '''
    
    dbms = SpatialDBManagement('admin1', '1234', 'location_data')
    dbms.init_database()
    
    user_id_json = load_data_with_json('data/user_data.json') 
    user_id = user_id_json['user_id']
    
    formatted_data = now.strftime('%Y-%m-%d %H%M%S') # timestemp   
    time1 = formatted_data[11:] 
    time_late = int(time1)
    time_late -= 6
    '''
    a = get_data.get_product_data_in_range()
    print(a)


    '''
    operate_list = []
    i = 0
    count = 0
    while(1):
        time_late -= 1
        print(time_late, i)
        result_dict = get_data.get_user_local_data_in_dynamoDB(user_id,time_late)
        print(result_dict)
        if (result_dict != -1):
            operate_list.append(result_dict)
        print(operate_list)
        
        
        # 

        if (i == 10):  # 나중에 숫자 변경해주기
            break
        i += 1    
    #print(result_dict)
    '''

if __name__ == '__main__': 
    main()
