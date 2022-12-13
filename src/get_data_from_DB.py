import json
import requests

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
        host = self.aws_url + '/search_user_local_data'
        data = {
            "user_id" : user_id,
            "time" : time
        }
        response = requests.post(host, data=data, headers=None)
        return_data = json.loads(response.content)
        
        return return_data
    

    def get_product_data(self, product_id):
        host = self.aws_url + '/get_product_condition_data'
        data = {
            "product_id" : product_id
        }
        response = requests.post(host, data=data, headers=None)
        return_data = json.loads(response.content)

        return return_data

    def get_point_of_sales_data(self, product_id):
        host = self.aws_url + '/get_sales_of_point_data'
        data = {
            "product_id" : product_id
        }
        response = requests.post(host, data=data, headers=None)
        return_data = json.loads(response.content)

        return return_data

    # def get_face_count_data(self, device_id):
    #     host = self.aws_url + '/get_face_count_data'
    #     data = {
    #         "device_id" : device_id
    #     }
    #     response = requests.post(host, data=data, headers=None)
    #     return_data = json.loads(response.content)

    #     return return_data



def main():
    get_data = Get_data()
    
    user_data = get_data.get_user_local_data_in_dynamoDB(11143,103834)
    print(user_data)
    
    with open("aws_get_data/local_data.json", "w") as outfile:
        json.dump(user_data, outfile, indent=4)
        
    #product_id = 6463인 항목 가져오기
    product_data = get_data.get_product_data(6463)
    print(product_data)
    
    with open("aws_get_data/product_data.json", "w") as outfile:
        json.dump(product_data, outfile, indent=9)

    product_data = get_data.get_point_of_sales_data(11343)
    print(product_data)
    
    with open("aws_get_data/point_of_sales_data.json", "w") as outfile:
        json.dump(product_data, outfile, indent=6)         

    #face count 데이터는 키 값이 좀 이상해서 가져오는데 무리...
    # face_count_data = get_data.get_face_count_data(0)
    # print(face_count_data)
    
    # with open("aws_get_data/face_count_data.json", "w") as outfile:
    #     json.dump(face_count_data, outfile, indent=5)   
    
if __name__ == '__main__': 
    main()
