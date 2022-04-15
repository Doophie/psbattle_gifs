#!/usr/bin/env python3

import secret.secrets as s
import praw
import glob
import imageio
import requests
import urllib.request
import re
from bs4 import BeautifulSoup
from os import listdir
from os.path import isfile, join
import os, shutil
from PIL import Image
from PIL import ImageFont
from PIL import ImageDraw 

class ImageFetcher:

    supported_types = ['png', 'jpg', 'jpeg']
    saved_images = 0

    def __init__(this, reddit_submission):
        this.submission = reddit_submission

    def collect_non_direct_imgur(this, comment):
        end = comment.body.split("http")[1]
        if '/a/' in end:
            url = "http" + end[0:23] 
        else:
            url = "http" + end[0:21]

        try:
            with urllib.request.urlopen(url) as f:
                r = f.read()
                soup = BeautifulSoup(r,'lxml')
                big_string = str(soup)
                imgur_url = "https://i.imgur" + re.split('|'.join(this.supported_types), big_string.split("i.imgur")[1])[0]
                for t in this.supported_types:
                    if t in big_string.split("i.imgur")[1]:
                        imgur_url += t

                        this.save_image(imgur_url, t)
                        break
                        
        except Exception as e:
            print("failed to read url {}".format(url))
            print(e)

    def save_image(this, image_url, extension):
        image = requests.get(image_url).content
        with open('cache/image_{}.{}'.format(this.saved_images, extension), "wb+") as image_file:
            image_file.write(image)
        this.saved_images += 1

    # takes a submission and saves all commented images into the 'cache' folder
    def collect_images(this):
        submission = this.submission

        for t in this.supported_types:
            if t in submission.url:
                post_url = submission.url
                image = requests.get(post_url).content
                with open('cache/z_post.{}'.format(t), 'wb+') as image_file:
                    image_file.write(image)
                this.update_post_image(submission.title, t)
            
            commented_image_urls = []
            for i, comment in enumerate(list(submission.comments)):
                if t in comment.body:
                    end_of_url = comment.body.split("https")[1]
                    start_of_url = end_of_url.split("." + t)[0]
                    image_url = "https" + start_of_url + "." + t

                    this.save_image(image_url, t)
                    #image = requests.get(image_url).content
                    #with open('cache/image_{}.{}'.format(i, t), "wb+") as image_file:
                    #    image_file.write(image)
                elif "imgur" in comment.body and t == "png" and not any(ext in comment.body for ext in this.supported_types):
                    this.collect_non_direct_imgur(comment)

    def update_post_image(this, title, png_or_jpg):
        img = Image.open("cache/z_post.{}".format(png_or_jpg))
        draw = ImageDraw.Draw(img)
        font = ImageFont.truetype("Montserrat-Bold.ttf", 26)
        draw.text((10, 10), title, (255,255,255), font=font)
        img.save("cache/z_post.{}".format(png_or_jpg))

