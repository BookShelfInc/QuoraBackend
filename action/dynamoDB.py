import requests
import json

from .env_getter import getVariable

def postQuestion(answerId, realQuestionId, answer, userId):
    API_ENDPOINT = getVariable('API_GATEWAY_DYNAMODB')

    data = {
        "questionId": answerId,
        "realQuestionId": realQuestionId,
        "answer" :answer,
        "userId": userId
    }
    headers = {'Content-type': 'application/json', 'Access-Control-Allow-Origin': '*'}

    r = requests.post(API_ENDPOINT, data=json.dumps(data), headers=headers)

    return r.text

def getNotifications(userId):
    API_ENDPOINT = getVariable('API_GATEWAY_DYNAMODB')+'/'+str(userId)

    headers = {'Content-type': 'application/json', 'Access-Control-Allow-Origin': '*'}

    r = requests.get(API_ENDPOINT, headers=headers)

    return r.json()['Items']