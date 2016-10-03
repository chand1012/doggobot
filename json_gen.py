'''
This will generate the keys.json file for the app to use.
Just run this script before you try to run doggobot.py
'''
from __future__ import print_function
from builtins import input
import json

#get the API keys for the user
imgur_id = input('Imgur client id: ')
imgur_secret = input('Imgur client secret: ')
consumerkey = input('Twitter consumer key: ')
consumersecret = input('Twitter consumer secret key: ')
access = input('Twitter access token: ')
access_secret = input('Twitter access secret key: ')

#compiles information to object
data = {}
data["client_id_imgur"] = imgur_id
data["client_secret_imgur"] = imgur_secret
data["tw_consumer_key"] = consumerkey
data["tw_consumer_secret"] = consumersecret
data["access_token"] = access
data["access_secret"] = access_secret

#turns data into keys.json
json_data = json.dumps(data)
json_file = open('keys.json', 'w+')
json_file.write(json_data)
json_file.close()

print('File successfully written.')
