#!/usr/bin/env python3

import secret.secrets as s
import praw
import glob
import imageio
import requests
from parse_images import ImageFetcher
from os import listdir
from os.path import isfile, join
import os, shutil
from PIL import Image
from PIL import ImageFont
from PIL import ImageDraw 


reddit = praw.Reddit(
    client_id = s.client_id,
    client_secret = s.client_secret,
    password = s.password,
    user_agent = s.user_agent,
    username = s.username
)

ps_battles = reddit.subreddit("photoshopbattles")

# clears the cached data from the last time this was run
def clear_cache():
    folder = 'cache'
    for filename in os.listdir(folder):
        file_path = os.path.join(folder, filename)
        try:
            if os.path.isfile(file_path) or os.path.islink(file_path):
                os.unlink(file_path)
            elif os.path.isdir(file_path):
                shutil.rmtree(file_path)
        except Exception as e:
            print('Failed to delete %s. Reason: %s' % (file_path, e))


# makes a gif out of all the images in the cache folder
def generate_gif():
    # make a gif
    image_files = [f for f in listdir("cache") if isfile(join("cache", f))]

    images = []
    for filename in image_files:
        images.append(imageio.imread("cache/"+filename))
    imageio.mimsave('cache/movie.gif', images, duration=1.5)


for submission in ps_battles.hot(limit=5):
    # get main image
    if not submission.link_flair_text == "Battle":
        continue

    print("making gif for submission {}".format(submission.title))
    print("selftext {}".format(submission.url))

    clear_cache()
    ImageFetcher(submission).collect_images()
    generate_gif()
