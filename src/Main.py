import json
import requests
import base64
import time

from datetime import datetime
from pytz import timezone
from point_of_sales import Product, Get_data, Point_to_sales
from spatical_db_management import SpatialDBManagement
        

def load_data_with_json(file_path):
    with open(file_path, 'r') as file:
        data = json.load(file)
    
    return data
    
    
def main():

    now = datetime.now(timezone('Asia/Seoul'))    
    get_data = Get_data()   
    product_data = Product()
    sales = Point_to_sales()
    
    
    # # AWS에 판매 데이터 올리기
    # formatted_data = now.strftime('%Y%m%d %H%M%S') # timestemp    
    # sales.load_sales_data_with_json("data/sales_data.json", formatted_data)
    # sales._upload_to_dynamoDB()  
    
    
    # # 저장된 상품 데이터를 AWS에 저장
    # formatted_data = now.strftime('%Y%m%d %H%M%S') # timestemp    
    # for i in range(3):
    #     path = 'data/product_data/product_data' + str(i+1) + '.json'
    #     product_data.load_product_data_with_json(path, formatted_data)
    #     product_data.upload_product_data_to_dynamoDB()

    
    # AWS에 저장된 product_id = 3362 데이터 가져오기
    product_id_list = []

    for i in range (3):
        file_path = 'data/product_data/product_data' + str(i+1) + '.json'
        with open(file_path, 'r') as file:
            data = json.load(file)
            product_id_list.append(data['product_id'])   
    
    product_list = {}
    for i in range(3):
        product_dt= product_data.product_search_in_dynamoDB(product_id_list[i])
        product_list[str(product_id_list[i])] = {'x' : product_dt['x'], 'y' : product_dt['y']}
        
    print(product_list)
    
    # 사용자 위치 정보를 AWS로부터 불러와서 product_list의 값과 비교
    user_id_json = load_data_with_json('data/user_data.json') 
    user_id = user_id_json['user_id']
    formatted_data = now.strftime('%Y%m%d %H%M%S') # timestemp
    time1 = formatted_data[9:] 
    time_late = int(time1)

    operate_list = [0,0,0]
    i = 0
    count = 0
    valid_area = 0.5        # 접촉 유효 거리
    # if 조건문의 숫자만큼의 시간동안 사용자가 상품 근처에 있었는지 count
    while(1):
        time_late -= 1
        print(time_late, i)
        result_dict = get_data.get_user_local_data_in_dynamoDB(user_id,time_late)
        print(result_dict)
        
        result_dict = {
            'user_id' : return_data[0]['user_id']['N'],
            'x' : return_data[0]['x']['S'],
            'y' : return_data[0]['y']['S'],
            'date' : int(return_data[0]['date']['S']),
            'time' : return_data[0]['time']['N']
            }
        
        if (result_dict != -1):
            for i in range (product_id_list):
                pd_x = float(product_list.get(str(i))['x'])
                pd_y = float(product_list.get(str(i))['y'])
                user_x = float(result_dict['x'])
                user_y = float(result_dict['y'])
                if(abs(user_x - pd_x) < valid_area and abs(user_y - pd_y) < valid_area):
                    operate_list[product_id.index(i)] += 1
            
            
        print(operate_list)
        
        if (i == 31):  # 나중에 숫자 변경해주기
            max_index = product_id.index(max(operate_list))
            if (operate_list[max_index] > (i / 4)):
                data = {
                    'product_id' : operate_list[max_index],
                    'user_id' : user_id,
                    'time' : result_dict['time']
                }
                product_data.user_hold_product(data)
            
            break
        i += 1    
    #print(result_dict)


if __name__ == '__main__': 
    main()
