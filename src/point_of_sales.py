import json
import requests


class point_to_sales():
    def __init__(
        self,
        adv_name = None,
        adv_company = None,
        adv_url = None,
        aws_url = None
    ) -> None:
        self.sales_data = {
            'name' : adv_name,
            'company' : adv_company,
            'adv_url' : adv_url,
        }
        self.aws_url = "https://77gonk6cp7.execute-api.ap-northeast-1.amazonaws.com/default"
        
        return None
    
    {
    "market_name" : "iPhone 14",
    "product_name" : "Apple",
    "product_id" : 11343,
    "number" : 14,
    "price" : 1250000,
    "sales" : 17500000
}
    
    def load_sales_data_with_json(
        self,
        file_path
    ) -> None:
        with open(file_path, 'r') as file:
            data = json.load(file)
            self.sales_data['market_name'] = data['market_name']
            self.sales_data['product_name'] = data['product_name']
            self.sales_data['product_id'] = data['product_id']
            self.sales_data['count'] = data['count']
            self.sales_data['price'] = data['price']
            self.sales_data['product_id'] = data['product_id']
        
        print(self.sales_data)
        return None
    
    def _upload_to_dynamoDB(
        self,
    ):
        host = self.aws_url + '/point_of_sales'
        json_data = json.dumps(self.sales_data, ensure_ascii=False)
        response = requests.post(host, json = json_data, headers=None)

        return response
    
    def _search_in_dynamoDB(
        self,
        adv_name
    ):
        data = {
            "name" : adv_name
        }
        host = self.aws_url + '/search_advertisement'
        response = requests.post(host, data=data, headers=None)
        lambda_data = json.loads(response.content)
        adv_youtube_url = lambda_data[adv_name][0]['ad_url']['S']
        print(adv_youtube_url)     # DB에 존재하는 광고 이름의 유튜브 주소값 출력
        
        return adv_youtube_url 
    
sales = point_to_sales()
sales.load_sales_data_with_json("advertisement_data.json")
sales._upload_to_dynamoDB()
sales._search_in_dynamoDB("iPhone14")