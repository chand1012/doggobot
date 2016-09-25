from imgurpython import ImgurClient
import random
import tweepy
from time import sleep
import sys, os
import json

#to wait
def wait(sleeptime):
    actual_time = 60*int(sleeptime)
    print "Waiting for {} minutes...".format(sleeptime)
    sleep(actual_time)

# handles the keys from the specified file
def keys(which_key='-1', file_name='keys.json'):
    try:
        file_keys = open(file_name)
    except:
        print "Error! JSON file does not exist!"
        raise
    parsed_json = json.loads(file_keys.read())

    if int(which_key) is 1:
        return parsed_json['client_id_imgur']
    elif int(which_key) is 2:
        return parsed_json['client_secret_imgur']
    elif int(which_key) is 3:
        return parsed_json['tw_consumer_key']
    elif int(which_key) is 4:
        return parsed_json['tw_consumer_secret']
    elif int(which_key) is 5:
        return parsed_json['access_token']
    elif int(which_key) is 6:
        return parsed_json['access_secret']
    else:
        return parsed_json

#wait time to prevent twitter from flagging you as a bot
def follow_user_followers_random(user, wait_time=1):
    mainkey = str(keys(3))
    mainsecret = str(keys(4))
    access = str(keys(5))
    accesssecret = str(keys(6))
    auth = tweepy.OAuthHandler(mainkey, mainsecret)
    auth.set_access_token(access, accesssecret)
    tclient = tweepy.API(auth)
    try:
        followers = tclient.followers_ids(user)
    except:
        print "User {} not found.".format(user)
        sys.exit()
    if len(followers) > 100:
        count = 0
        test_followers = []
        while True:
            if count >= 101:
                break
            else:
                count += 1
                follower = random.choice(followers)
                test_followers += [follower]
                if not follower in test_followers:
                    try:
                        tclient.create_friendship(follower)
                        print "Followed user {}".format(follower)
                        print "Waiting to follow for {} minutes.".format(wait_time)
                        wait(wait_time)
                    except:
                        print "Error! Already following or user {} doesn't exist.".format(follower)
                        print "Waiting to follow for {} minutes.".format(wait_time)
                        wait(wait_time)
                        pass
    else:
        for follower in followers:
            try:
                tclient.create_friendship(follower)
                print "User followed {}".format(follower)
                print "Waiting to follow for {} minutes.".format(wait_time)
                wait(wait_time)
            except:
                print "Error! Already following or user {} doesn't exist.".format(follower)
                pass

random_user = random.randint(1, 320000000) # this should cover most of the twitter users
follow_user_followers_random(random_user)
