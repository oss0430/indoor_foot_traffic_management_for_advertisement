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
        time1,
        time2
    ):
        host = self.aws_url + '/search_user_local_data'
        data = {
            "user_id" : user_id,
            "time1" : time1,
            "time2" : time2
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

    def get_face_count_data(self, sample_time1, sample_time2):
        host = self.aws_url + '/get_face_count_data'
        data = {
            "sample_time1" : sample_time1,
            "sample_time2" : sample_time2
        }
        response = requests.post(host, data=data, headers=None)
        return_data = json.loads(response.content)

        return return_data



def main():
    get_data = Get_data()
    
    # id = 11143, sample_time 범위 내의 user local 데이터 가져오기
    sample_time =  [int(155056),int(155134)]
    user_data = get_data.get_user_local_data_in_dynamoDB(11143,sample_time[0],sample_time[1])
    print(user_data)
    
    with open("aws_get_data/local_data.json", "w") as outfile:
        json.dump(user_data, outfile, indent=4)
        
        
    # product_id = 6463인 항목 가져오기
    product_data = get_data.get_product_data(6463)
    print(product_data)
    
    with open("aws_get_data/product_data.json", "w") as outfile:
        json.dump(product_data, outfile, indent=9)


    # product_id = 11343인 상품의 판매기록 가져오기 (point_of_sales)
    product_data = get_data.get_point_of_sales_data(11343)
    print(product_data)
    
    with open("aws_get_data/point_of_sales_data.json", "w") as outfile:
        json.dump(product_data, outfile, indent=6)         

    
    # sample_time 범위 내의 Face_count 데이터 가져오기
    sample_time = [20221208014953,20221208020104]
    face_count_data = get_data.get_face_count_data(sample_time[0], sample_time[1])
    print(face_count_data)
    
    with open("aws_get_data/face_count_data.json", "w") as outfile:
        json.dump(face_count_data, outfile, indent=5)   
    
if __name__ == '__main__': 
    main()
