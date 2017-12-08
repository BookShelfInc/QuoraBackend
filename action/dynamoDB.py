import requests
import json

from .env_getter import getVariable

def postQuestion(answerId, realQuestionId, answer, userId):
    API_ENDPOINT = getVariable('API_GATEWAY_DYNAMODB')

    # data = {
    #     "questionId": str(answerId),
    #     "answer": str(answer),
    #     "realQuestionId": str(realQuestionId),
    #     "userId": str(userId)
    # }

    data  = {
    "questionId": "21",
"answer": "I am Sanzha333333r!",
"realQuestionId": "4",
"userId": "8"
}

    print(data)
    headers = {'Content-type': 'application/json', 'Access-Control-Allow-Origin': '*'}

    r = requests.post(API_ENDPOINT, data=json.dumps(data), headers=headers)

    return r.text

def getNotifications(userId):
    API_ENDPOINT = getVariable('API_GATEWAY_DYNAMODB')+'/'+str(userId)

    headers = {'Content-type': 'application/json', 'Access-Control-Allow-Origin': '*'}

    r = requests.get(API_ENDPOINT, headers=headers)

    return r.json()['Items']