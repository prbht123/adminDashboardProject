from django.conf import settings
import jwt
import requests
import json
from time import time

# ======================== ZOOM INTEGRATION ============================


def generateToken():
    token = jwt.encode(

        # Create a payload of the token containing
        # API Key & expiration time
        {'iss': settings.API_KEY, 'exp': time() + 5000},

        # Secret used to generate token signature
        settings.API_SEC,

        # Specify the hashing alg
        algorithm='HS256'
    )
    return token.encode().decode('utf-8')


# send a request with headers including
# a token and meeting details


def createMeeting(topic, date_time, duration):
    # create json data for post requests
    meetingdetails = {"topic": topic,
                      "type": 2,
                      "start_time": date_time,
                      "duration": duration,
                      "timezone": "Asia/Calcutta",
                      "agenda": "test",

                                "recurrence": {"type": 1,
                                               "repeat_interval": 1
                                               },
                                "settings": {"host_video": "true",
                                             "participant_video": "true",
                                             "join_before_host": "False",
                                             "mute_upon_entry": "False",
                                             "watermark": "true",
                                             "audio": "voip",
                                             "auto_recording": "cloud"
                                             }
                      }
    headers = {'authorization': 'Bearer ' + generateToken(),
               'content-type': 'application/json'}
    r = requests.post(
        f'https://api.zoom.us/v2/users/me/meetings',
        headers=headers, data=json.dumps(meetingdetails))

    print("\n creating zoom meeting ... \n")
    # print(r.text)
    # converting the output into json and extracting the details
    y = json.loads(r.text)
    join_URL = y["join_url"]
    meetingPassword = y["password"]
    context = {
        'link': join_URL,
        'password': meetingPassword
    }

    print(
            f'\n here is your zoom meeting link {join_URL} and your \
		password: "{meetingPassword}"\n')

    return context
