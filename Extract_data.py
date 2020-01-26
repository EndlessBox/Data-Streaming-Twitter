import json
import sys
import os
import pandas as pd
import requests

class Extract:
    
    def __init__(self):
        self.data_source_file_name = "data_sources.json"
        self.data_sources = json.load(open(self.data_source_file_name))
        self.api = self.data_sources['data_sources']['api']
        self.csv = self.data_sources['data_sources']['csv']
        self.content_type = "content-type: application/json"
        self.auth = lambda access_token : {"Authorization": "Bearer {}".format(str(access_token))}

    """
        Read Data from a mentioned api in "data_sources.json"
    """

    def readAPIsData(self, api_name, id):
        try:

            api_url = self.api[api_name] + "?id=100," + str(id)
            access_token = os.environ.get('ACCESS_TOKEN_TWT')
            response = requests.get(api_url, headers=self.auth(access_token))
        except Exception as err:
            print(f'Error : {err}')
            sys.exit()
        else:
            print("Success !")
            return response.json()

    """
        Read Data from a mentioned csv file in "data_sources.json"
        ! : You have to manage errors.
    """

    def readCSVData(self, csv_name):
            return (pd.read_csv(self.csv[csv_name]))

    def usage_accessToken(self):
            print(f'The "ACCESS_TOKEN_TWT" env variable is not set')
            print(f'Run : source ./get_bearer.sh <API_KEY> <API_SECRET_KEY>')
            sys.exit()
