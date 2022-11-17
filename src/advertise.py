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
            'adv_url' : adv_url
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
        host = self.aws_url + '/add_advertisement'
        json_data = json.dumps(self.adv_data, ensure_ascii=False)
        response = requests.post(host, json = json_data, headers=None)

        return response
    
    
    
adv_data_updater = AdvUpdater()
adv_data_updater.load_advertisement_data_with_json("advertisement_data.json")
adv_data_updater._upload_to_dynamoDB()