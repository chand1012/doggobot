from __future__ import print_function
from future import standard_library
standard_library.install_aliases()
from builtins import str
from imgurpython import ImgurClient
import tweepy
from time import sleep
from bs4 import BeautifulSoup
import urllib.request, urllib.parse, urllib.error
import sys, os
import json
import argparse

global version
version = int(sys.version[:1])

def wait(sleeptime):
    actual_time = 60*int(sleeptime)
    print("Waiting for {} minutes...".format(sleeptime))
    sleep(actual_time)

# handles the keys from the specified file
def keys(which_key='-1', file_name='keys.json'):
    while True:
        try:
            file_keys = open(file_name)
        except:
            print("Error! JSON file does not exist!")
            print("Would you like to make the file with the JSON generator?")
            if version > 2:
                run = input("(Y/N):")
            else:
                run = raw_input("(Y/N):")
            if run == 'y' or run? == 'Y':
                os.system('python json_gen.py')
                pass
            else:
                raise
        else:
            break
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

#simple function for wget
#if you are on Windows (such as myself) please use Windows wget
def wget(url, name):
    os.system("wget {} -O {}".format(url, name))

#handles image retreval
def get_img(url):
    if 'imgur' in url:
        #check for cache then if not found creates it
        if not os.path.exists('cache'):
            print("Cache not found, creating one...")
            os.makedirs('cache')

            #checks for file extension, and if true, skips to download.
            #If not it parses the html and extracts the image link
        extensions = ['.jpg', '.gif', '.png']
        if not any(thing in url for thing in extensions):
            print("No extension, extracting direct link...")
            imgur_item = urllib.request.urlopen(url)
            page = BeautifulSoup(imgur_item, 'html.parser')
            image_link_raw = page.img.get('src')
            image_link = image_link_raw[2:]
        else:
            print("Direct link, downloading...")
            image_link = url
        if 'http://' in image_link:
            image_link_http = image_link
        else:
            image_link_http = "http://{}".format(image_link)
            name = image_link[12:]
        wget(image_link_http, "cache/{}".format(name))
        print("Done!")
        return name
    else:
        return None

def get_img_by_ids(id_array):
    amt = 0
    for image in id_array:
        img_url = "http://imgur.com/a/{}".format(image)
        get_img(img_url)
        amt += 1
    return amt

def clear_cache():
    print("Clearing cache...")
    try:
        os.chdir('cache')
        stuff = os.listdir('.')
        for thing in stuff:
            os.remove(thing)
        os.chdir('..')
    except:
        print("Cache does not exist!")
    print("Done!")

def post_photo(keyfile='keys.json', text, tweet_image):
    #Twitter id's and login
    print("Posting image {}...".format(tweet_image))
    mainkey = str(keys(3, keyfile))
    mainsecret = str(keys(4, keyfile))
    access = str(keys(5, keyfile))
    accesssecret = str(keys(6, keyfile))
    auth = tweepy.OAuthHandler(mainkey, mainsecret)
    auth.set_access_token(access, accesssecret)
    tclient = tweepy.API(auth)
    tclient.update_with_media(tweet_image, text)
    print("Done!")

def get_photo_ids(search, limit=1, keyfile='keys.json'):
    client_id = str(keys(1, keyfile))
    client_secret = str(keys(2, keyfile))
    iclient = ImgurClient(client_id, client_secret)
    print("Finding images with search criteria {}".format(search))
    get_photos = iclient.gallery_search(search, sort='time', window='day')
    photo_ids = []
    stop = 0

    print("Getting ids of {} images".format(limit))
    for photo in get_photos:
        stop += 1
        photo_ids += [photo.id]
        if stop >= int(limit):
            break
    print("Done!")
    return photo_ids

def get_cache():
    extensions = ['.jpg', '.gif', '.png']
    os.chdir('cache')
    items = os.listdir('.')
    for item in items:
        if not any(thing in item for thing in extensions):
            items.remove(item)
        else:
            pass
    os.chdir('..')
    return items

def main(keyfile='keys.json', text="#dogs #imgur", search='title:dogs', limit=1, timer=5, clear=False):
    gotten = get_photo_ids(search, limit, keyfile)
    get_img_by_ids(gotten)
    cached_images = get_cache()
    for image in cached_images:
        image_location = "cache/{}".format(image)
        post_photo(text, image_location)
        wait(timer)
    if clear == True:
        clear_cache()
    else:
        pass

parser = argparse.ArgumentParser(description="Doggobot for Twitter and Imgur")
#-db DATABSE -u USERNAME -p PASSWORD -size 20
parser.add_argument("-f", "--keyfile", help="File name of the keyfile")
parser.add_argument("-text", "--text", help="Text for Twitter post")
parser.add_argument("-s", "--search", help="Text for Imgur search")
parser.add_argument("-l", "--limit", help="Limit for how many images to find and download", type=int)
parser.add_argument("-t", "--time", help="The amount of time in minutes between posts", type=int)
parser.add_argument("-c", "--clear", help="If enabled, clears cache when completed.", action='store_true')

args = parser.parse_args()

main()
