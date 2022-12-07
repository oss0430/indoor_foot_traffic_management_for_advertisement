import json
import requests
import base64


class Get_data():
    def __init__(
        self,
        adv_name = None,
        adv_company = None,
        adv_url = None,
        aws_url = None
    ) -> None:
        self.adv_data = {
            'name' : adv_name,
            'company' : adv_company,
            'adv_url' : adv_url,
        }
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
        
        result_dict = {
        'user_id' : return_data[0]['user_id']['N'],
        'x' : return_data[0]['x']['S'],
        'y' : return_data[0]['y']['S'],
        'date' : int(return_data[0]['date']['S']),
        'time' : return_data[0]['time']['N']
        }
        
        return result_dict
    
    
def main():

    get_data = Get_data()    
    result_dict = get_data.get_user_local_data_in_dynamoDB(11111,2222)
    
    print(result_dict)

if __name__ == '__main__': 
    main()
