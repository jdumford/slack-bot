import requests
import json
from tokens import SLACK_TOKEN


def getUserName(user_id):
    user_endpoint = 'https://slack.com/api/users.info?token=' + SLACK_TOKEN + '&user=' + user_id

    r =requests.get(user_endpoint)
    data = json.loads(r.text)
    return data['user']['name']
