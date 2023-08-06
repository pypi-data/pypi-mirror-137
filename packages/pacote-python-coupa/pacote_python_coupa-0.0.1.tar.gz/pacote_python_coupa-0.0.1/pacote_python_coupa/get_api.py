#------------------------------------------------------------------------------------------------------
# imports
import requests, json, pprint

#------------------------------------------------------------------------------------------------------
# Funções
def get_api(URL: str, HEADERS_COUPA: dict):
    response = requests.get(URL, headers=HEADERS_COUPA)
    
    return pprint.pprint(response.json(), sort_dicts=False)

#------------------------------------------------------------------------------------------------------