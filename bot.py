import os, sys
import json
import requests
from flask import Flask, request
from pprint import pprint


try:
    import apiai
except ImportError:
    sys.path.append(
        os.path.join(os.path.dirname(os.path.realpath(__file__)), os.pardir))
    import apiai
PAGE_ACCESS_TOKEN = "EAAX3VL3mRiUBAOvqZCUD0LsBY8gXXYfFG3sy6gKY0OwQFzSeKLI6bXwRCeFmKjY7PiQZCKyMFOGQItZCAo5x4OphDieKa1wtEcNYZAxLHuwFOMVnZBmGHGZCgeR14H9kLvdrYLi8PVTpw3yIbp3UvYtd5Mt9uD5vxO9VvcZC9s4TAZDZD"
#PAGE_ACCESS_TOKEN = 'EAAfiZCUUkDzkBAO62ooNLNB0tFmVrsNQzZAW7rzu6Gsfsm0bha23M4VFJDUo3wA42FW9vXTZBkudX3FHsjDjmmz9j8w7knPeeVWGt7NhoTVFe7yrIcAowmMjF6nrLGmBxcgdDedXJ5OBT1KzEtaZA5ZBunFbAPkTww6iWrXGJmwZDZD'
VERIFY_TOKEN = "token_key"
CLIENT_ACCESS_TOKEN = "ce3f4f65635a446eab147290e59cdfe9"

app = Flask(__name__)               


@app.route('/', methods=['GET'])
def verify():
    if (request.args.get('hub.verify_token', '') == VERIFY_TOKEN):
        print("Verified")
        return request.args.get('hub.challenge', '')
    else:
        print('wrong verification token')
        return "Error, Verification Failed"
    return "Hello world", 200


@app.route('/', methods=['POST'])
def handle_messages():
    data = request.get_json()
    entry = data['entry'][0]
    if entry.get("messaging"):
        messaging_event = entry['messaging'][0]
        print("messaging event")
        print(messaging_event)

        sender_id = messaging_event['sender']['id']
        # get_started(PAGE_ACCESS_TOKEN, sender_id)
        try:
            message_text = messaging_event['message']['text']
            send_gif_message(sender_id, message_text)
        except KeyError:
            pass
        try:
            if messaging_event['postback'] and messaging_event['postback']['payload'] == "get_started":
                message = "Hi, I'm Jacky, I reply messages with gifs."
                print("About to send response for payload")
                send_message(PAGE_ACCESS_TOKEN, sender_id, message)
        except KeyError:
            print("Error replying gets started")
            pass
    return 'ok', 200


def search_gif(text):
    payload = {'s': text, 'api_key': "NYUxR9PmM3dJ61SVJWYrwZfBoSIksOYO"}
    r = requests.get('http://api.giphy.com/v1/gifs/translate', params=payload)
    r = r.json()
    url = r['data']['images']['original']['url']

    return url


def send_gif_message(recipient_id, message):
    gif_url = search_gif(message)

    print(gif_url)
    data = json.dumps({
        "recipient": {"id": recipient_id},
        "message": {
            "attachment": {
                "type": "image",
                "payload": {
                    "url": gif_url
                }
            }}
    })

    params = {
        "access_token": PAGE_ACCESS_TOKEN
    }

    headers = {
        "Content-Type": "application/json"
    }

    r = requests.post("https://graph.facebook.com/v2.6/me/messages",
                      params=params, headers=headers, data=data)

    print(r)


# def get_started(access_token, recipient):

data = {
    "setting_type": "call_to_actions",
    "thread_state": "new_thread",
    "call_to_actions": [
        {
            "payload": "get_started"
        }
    ]
}
get_started_data = json.dumps(data)
get_started_params = {
                    "access_token": PAGE_ACCESS_TOKEN
                    }

get_started_headers = {
            "Content-Type": "application/json"
        }
   

requests.post("https://graph.facebook.com/v2.6/me/thread_settings", params=get_started_params, headers=get_started_headers, data=get_started_data)

# data = {
#         "setting_type": "call_to_actions",
#         "thread_state": "new_thread",
#         "call_to_actions": [
#             {
#                 "payload": "get_started"
#             }
#         ]
#     }


def send_message(token, recipient, text):
    """hello world"""
    req = requests.post("https://graph.facebook.com/v2.8/me/messages",
    params={"access_token": token},
    data=json.dumps({
                    "recipient": {"id": recipient},
                    "message": {"text": text}
                    }),
    headers={'Content-type': 'application/json'})
    if req.status_code != requests.codes['ok']:
        print (req.text)

if __name__ == '__main__':
    app.run(debug=True)