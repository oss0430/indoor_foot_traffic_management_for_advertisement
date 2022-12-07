import json
import requests

from datetime import datetime
from pytz import timezone
from spatical_db_management import SpatialDBManagement



class Point_to_sales():
    def __init__(
        self,
        adv_name = None,
        adv_company = None,
        adv_url = None,
        aws_url = None
    ) -> None:
        self.sales_data = {}
        self.adv_data = {
            'name' : adv_name,
            'company' : adv_company,
            'adv_url' : adv_url,
            'date' : None
        }
        self.aws_url = "https://77gonk6cp7.execute-api.ap-northeast-1.amazonaws.com/default"
        
        return None
    
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

                    
        print(self.sales_data)
        return None
    
    def _upload_to_dynamoDB(self):
        host = self.aws_url + '/point_of_sales'
        response = requests.post(host, data = self.sales_data, headers=None)

        return response
    
    def _search_in_dynamoDB(self,product_id):
        data = {
            "name" : adv_name
        }
        host = self.aws_url + '/search_advertisement'
        response = requests.post(host, data=data, headers=None)
        lambda_data = json.loads(response.content)
        adv_youtube_url = lambda_data[adv_name][0]['ad_url']['S']
        print(adv_youtube_url)     # DB에 존재하는 광고 이름의 유튜브 주소값 출력
        
        return adv_youtube_url 
    
class Product():
       
    def __init__(self) -> None:
        self.aws_url = " https://77gonk6cp7.execute-api.ap-northeast-1.amazonaws.com/default"
        self.product_data = {}
    
    
    def load_product_data_with_json(self,file_path,formatted_data) -> None:
        with open(file_path, 'r') as file:
            data = json.load(file)
            self.product_data['market_id'] = data['market_id']
            self.product_data['product_id'] = data['product_id']            
            self.product_data['loc_x'] = data['x']
            self.product_data['loc_y'] = data['y']
            self.product_data['market_name'] = data['market_name']
            self.product_data['product_name'] = data['product_name']
            
        self.product_data['date'] = formatted_data[:8]
        self.product_data['time'] = formatted_data[10:]
        print(self.product_data)

        
    def upload_product_data_to_dynamoDB(self):
        host = self.aws_url + '/add_product_data'
        response = requests.post(host, data = self.product_data, headers=None)
        print(response)
                
        return response
    
    def product_search_in_dynamoDB(
        self,
        product_id
    ):
        data = {
            "product_id" : product_id
        }
        host = self.aws_url + '/search_product'
        response = requests.post(host, data=data, headers=None)
        return_data = json.loads(response.content)
        print(return_data)
        
        result_dict = {
        'product_name' : return_data[0]['product_name']['S'],
        'x' : return_data[0]['x']['N'],
        'y' : return_data[0]['y']['N'],
        'market_id' : return_data[0]['market_id']['N'],
        'product_id' : return_data[0]['product_id']['N'],
        'market_name' : return_data[0]['market_name']['S'],
        'date' : return_data[0]['date']['S'],
        'time' : return_data[0]['time']['S']
        }
        
        return result_dict
        
    
    

def main():
    now = datetime.now(timezone('Asia/Seoul'))
    formatted_data = now.strftime('%Y%m%d %H%M%S') # timestemp    

    
    sales = Point_to_sales()
    sales.load_sales_data_with_json("data/sales_data.json", formatted_data)
    
    '''
    # AWS에 판매 데이터 올리기
    sales._upload_to_dynamoDB()
    # AWS에 저장된 iPhone14 의 데이터 가져오기
    # url = sales._search_in_dynamoDB("iPhone14")    
    '''
    
    product = Product()
    product.load_product_data_with_json("data/product_data.json", formatted_data)
    
    
    # product 데이터를 AWS에 저장
    product.upload_product_data_to_dynamoDB()
    
    
    # AWS에 저장된 product_id = 3362 데이터 가져오기
    product_data = product.product_search_in_dynamoDB(3362) 
    # {'market_id': 11324, 'product_id': 3362, 'loc_x': 3, 'loc_y': 4, 'market_name': 'APPLE', 'product_name': 'iPhone14'}
    
    
    

    

if __name__ == '__main__': 
    main()