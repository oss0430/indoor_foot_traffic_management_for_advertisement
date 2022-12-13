import json
import requests

from datetime import datetime
from pytz import timezone



class Point_to_sales():
    
    def __init__(self):
        self.sales_data = {}
        self.aws_url = "https://77gonk6cp7.execute-api.ap-northeast-1.amazonaws.com/default"
        
    
    def load_sales_data_with_json(
        self,
        file_path,
        formatted_data
    ) -> None:
        with open(file_path, 'r') as file:
            data = json.load(file)
            self.sales_data['market_name'] = data['market_name']
            self.sales_data['product_name'] = data['product_name']
            self.sales_data['product_id'] = data['product_id']
            self.sales_data['count'] = data['count']
            self.sales_data['price'] = data['price']
            self.sales_data['date'] = formatted_data[0:9]

        return None
    
    def upload_sales_data_to_dynamoDB(self):
        host = self.aws_url + '/point_of_sales'
        response = requests.post(host, data = self.sales_data, headers=None)

        return response
    
    
class Product():
       
    def __init__(self):
        self.aws_url = " https://77gonk6cp7.execute-api.ap-northeast-1.amazonaws.com/default"
        self.product_data = {}
    
    def load_product_data_with_json(self,file_path,formatted_data):
        with open(file_path, 'r') as file:
            data = json.load(file)
            self.product_data['market_id'] = data['market_id']
            self.product_data['product_id'] = data['product_id']  
            self.product_data['loc_x'] = data['x']
            self.product_data['loc_y'] = data['y']
            self.product_data['market_name'] = data['market_name']
            self.product_data['product_name'] = data['product_name']
            self.product_data['user_id'] = data['user_id']

            
        self.product_data['date'] = formatted_data[:8]
        self.product_data['time'] = formatted_data[10:]
        print("path" + file_path + " -> ")
        print(self.product_data)
        
    def upload_product_data_to_dynamoDB(self):
        host = self.aws_url + '/add_product_data'
        response = requests.post(host, data = self.product_data, headers=None)
                
        return response
    
    
    # def product_search_in_dynamoDB(
    #     self,
    #     product_id
    # ):
    #     data = {
    #         "product_id" : product_id
    #     }
    #     host = self.aws_url + '/search_product'
    #     response = requests.post(host, data=data, headers=None)
    #     return_data = json.loads(response.content)

    #     #{'date': {'S': '20221208'}, 'product_name': {'S': 'iPhone14'}, 'x': {'S': '0.162'}, 'y': {'S': '2.5'}, 'time': {'S': '64808'}, 'market_id': {'N': '11324'}, 'product_id': {'N': '3362'}, 'market_name': {'S': 'APPLE'}}
    #     result_dict = {
    #     'product_name' : return_data[0]['product_name']['S'],
    #     'x' : return_data[0]['x']['S'],
    #     'y' : return_data[0]['y']['S'],
    #     'market_id' : return_data[0]['market_id']['N'],
    #     'product_id' : return_data[0]['product_id']['N'],
    #     'market_name' : return_data[0]['market_name']['S'],
    #     'date' : return_data[0]['date']['S'],
    #     'time' : return_data[0]['time']['S']
    #     }
        
    #     return result_dict
    
    #     '''
    #     product_search_in_dynamoDB 함수 사용 코드 (현재 사용 x)
    #     product_id_list = []
    #     for i in range (3):
    #         file_path = 'data/product_data/product_data' + str(i+1) + '.json'
    #         with open(file_path, 'r') as file:
    #             data = json.load(file)
    #             product_id_list.append(data['product_id'])   
    
    #     product_list = {}
    #     for i in range(3):
    #         product_dt= product.product_search_in_dynamoDB(product_id_list[i])
    #         product_list[str(product_id_list[i])] = {'x' : product_dt['x'], 'y' : product_dt['y']}      
    #     '''
        
    

def main():
    now = datetime.now(timezone('Asia/Seoul'))
    formatted_data = now.strftime('%Y%m%d %H%M%S') # timestemp    

    
    sales = Point_to_sales()
      
    #AWS에 판매 데이터 올리기 (포스기)
    sales.load_sales_data_with_json("data/sales_data.json", formatted_data)
    sales.upload_sales_data_to_dynamoDB()
    # {'product_id': 11343, 'date': 2022120, 'market_name': 'iPhone 14', 'product_name': 'Apple', 'count': 14, 'price': 1250000}
 
    
    product = Product()
    
    # product 데이터를 AWS에 저장
    for i in range(3):
        path = 'data/product_data/product_data' + str(i+1) + '.json'
        product.load_product_data_with_json(path, formatted_data)
        # {'market_id': 73245, 'product_id': 6463, 'loc_x': 4.328, 'loc_y': 1.292, 'market_name': 'starbucks', 'product_name': 'americano', 'user_id': 11143, 'date': '20221212', 'time': '52620'}
        product.upload_product_data_to_dynamoDB()
        
    
        
  
    
    
    

if __name__ == '__main__': 
    main()
