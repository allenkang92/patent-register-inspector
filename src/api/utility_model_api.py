import requests

def fetch_utility_model_data(rgstNo, service_key):
    url = 'http://apis.data.go.kr/1430000/PttRgstRtInfoInqSvc/getUtilityModelHistory'
    params = {
        'serviceKey': service_key,
        'type': 'json',
        'rgstNo': rgstNo
    }
    response = requests.get(url, params=params)
    return response.json() if response.status_code == 200 else None
