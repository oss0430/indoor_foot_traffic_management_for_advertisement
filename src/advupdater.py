import json
import requests


class AdvUpdater():
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
        self.aws_url = "https://lsh16oncid.execute-api.ap-northeast-1.amazonaws.com/default"
        
        return None
    
    def load_advertisement_data_with_json(
        self,
        file_path
    ) -> None:
        with open(file_path, 'r') as file:
            data = json.load(file)
            self.adv_data['name'] = data['name']
            self.adv_data['company'] = data['company']
            self.adv_data['adv_url'] = data['adv_url']
        
        print(self.adv_data)
        return None
    
    def _upload_to_dynamoDB(
        self,
    ):
        host = self.aws_url + '/search_advertisement'
        json_data = json.dumps(self.adv_data, ensure_ascii=False)
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
        #adv_youtube_url = lambda_data[adv_name][0]['ad_url']['S']
        #print(adv_youtube_url)     # DB에 존재하는 광고 이름의 유튜브 주소값 출력
        
        #return adv_youtube_url 
    
    
def main():
    


    sales = AdvUpdater()
    sales._search_in_dynamoDB("iPhone14")    

if __name__ == '__main__': 
    main()
