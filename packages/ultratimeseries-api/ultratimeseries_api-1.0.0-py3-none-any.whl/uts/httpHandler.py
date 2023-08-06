import requests
import json
from uts import utils

def post(url,endpoint,host,payload):

    headers = {
        "Host" : host,
        "Content-Type" : 'application/json',
    }

    request = requests.post(url+endpoint,data=json.dumps(payload),headers=headers)

    if(utils.validate(request,endpoint)):
        return request.text

def get(url,endpoint,host,payload):

    headers = {
        "Host" : host,
    }

    request = requests.get(url+endpoint+payload,{},headers=headers)

    if(utils.validate(request,endpoint)):
        return request.text