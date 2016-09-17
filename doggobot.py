from imgurpython import ImgurClient
from datetime import datetime
import tweepy
import time
from bs4 import BeautifulSoup
import urllib
import sys, os
import json
'''
TO DO:
-- clean up code
-- make the clock function to execute code at certian time
-- add some more comments
'''
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

#get times from the file
def get_times(which_time='-1', file_name='times.json'):
        try:
            file_times = open(file_name)
        except:
            print "Error! JSON file does not exist!"
            raise
        parsed_json = json.loads(file_keys.read())

        if which_time is -1:
            return parsed_json
        else:
            return parsed_json['time{}'.format(which_time)]

#this will be replaced later
def min_sleep(sleeptime):
    actual_time = 60*int(sleeptime)
    print "Waiting for {} minutes...".format(sleeptime)
    time.sleep(actual_time)
#simple function for wget
#if you are on Windows (such as myself) please use Windows wget
def wget(url, name):
    os.system("wget {} -O {}".format(url, name))

#handles image retreval
def get_img(url):
    if 'imgur' in url:
        #check for cache then if not found creates it
        if not os.path.exists('cache'):
            print "Cache not found, creating one..."
            os.makedirs('cache')

            #checks for file extension, and if true, skips to download.
            #If not it parses the html and extracts the image link
        extensions = ['.jpg', '.gif', '.png']
        if not any(thing in url for thing in extensions):
            print "No extension, extracting direct link..."
            imgur_item = urllib.urlopen(url)
            page = BeautifulSoup(imgur_item, 'html.parser')
            image_link_raw = page.img.get('src')
            image_link = image_link_raw[2:]
        else:
            print "Direct link, downloading..."
            image_link = url
        if 'http://' in image_link:
            image_link_http = image_link
        else:
            image_link_http = "http://{}".format(image_link)
            name = image_link[12:]
        wget(image_link_http, "cache/{}".format(name))
        return name
    else:
        return None


def post_photo(text, tweet_image):
    #Twitter id's and login
    print "Posting image {}...".format(tweet_image)
    mainkey = str(keys(3))
    mainsecret = str(keys(4))
    access = str(keys(5))
    accesssecret = str(keys(6))
    auth = tweepy.OAuthHandler(mainkey, mainsecret)
    auth.set_access_token(access, accesssecret)
    tclient = tweepy.API(auth)
    tclient.update_with_media(tweet_image, text)


def clear_cache():
    print "Clearing cache..."
    os.chdir('cache')
    stuff = os.listdir('.')
    for thing in stuff:
        os.remove(thing)
    os.chdir('..')

def main(time_in_between_posts=1, amt_of_posts=1, clear_data='true'):
    if len(sys.argv) > 2:
        print "Running with default or code-set parameters."
    else:
        print "Running with Args set as:"
        print "Time inbetween posts: {}".format(time_in_between_posts)
        print "Amount of posts: {}".format(amt_of_posts)
        if clear_data == 'true':
            answer_clear = clear_data
        else:
            answer_clear = 'false'
        print "Clear data after run?: {}".format(answer_clear)
    if time_in_between_posts is -1:
        time_list = time_in_between_posts

    #Imgur ids
    client_id = str(keys(1))
    client_secret = str(keys(2))
    iclient = ImgurClient(client_id, client_secret)

    print "Finding Images..."
    get_photos = iclient.gallery_search("title:dogs ext:jpg", sort='time', window='day')
    dog_photos = []
    stop = 0

    for photo in get_photos:
        stop += 1
        dog_photos += [photo.link]
        if stop >= amt_of_posts:
            break

    print "Found! Beginning posting..."
    for dog in dog_photos:
        ''' this needs fixed
        # wait at beginning so that it will not start the first post until the specified time
        counter = 0
        if time_in_between_posts is -1:
            while True:
                current_time = str(datetime.now().time())
                if current_time[:5] == str(time_list):
                    counter += 1
                    break
                else:
                    pass
        else:
            min_sleep(int(time_in_between_posts))
        '''
        image_of_dog = get_img(dog)
        if not image_of_dog == None:
            post_photo("#dogs #dog #imgur {}".format(dog), "cache/{}".format(image_of_dog))
            print "Posted!"
            min_sleep(int(time_in_between_posts))
        else:
            print "Image not valid, skipping to next image."

    if clear_data == 'true':
        clear_cache()
    else:
        pass

main(60, 6, 'true')
