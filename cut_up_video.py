from PIL import Image, ImageOps
import PIL
import pathlib
import time
from os import execv, walk
import copy
import random
import math
import os
from time import gmtime, strftime
from tqdm import tqdm
import glob
import cv2
import numpy as np
import os.path
from os import path
from PIL import Image, ExifTags
import csv
from subprocess import Popen, PIPE
import subprocess
import uuid
from inputimeout import inputimeout, TimeoutOccurred
from os.path import exists

movie_name = "in.mp4"

#reads the setup file for the given dimentions of your output. The first number is the number of patches, the second is the resolution of patches
try:
    f = open("setup.txt", "r")
    data = f.readlines()
    res_of_comp = int(data[0].rstrip("\n"))
    patch = int(data[1].rstrip("\n"))
    f.close()
except:
    res_of_comp = 40
    patch = 40

#Calculates the final dimentions of collage and makes the actual png to be filled up
vidcap = cv2.VideoCapture(movie_name)
success,image = vidcap.read()
money_height,money_width, channels = image.shape
money_ratio = money_width/(money_width + money_height)
number_of_patches_width = round(money_ratio * res_of_comp)
number_of_patches_height = round((1-money_ratio) * res_of_comp)
collage_width = patch * number_of_patches_width
collage_height = patch * number_of_patches_height



files = glob.glob(str(pathlib.Path().resolve()) + "\\input\\*.*")
for f in files:
    os.remove(f)
files = glob.glob(str(pathlib.Path().resolve()) + "\\output\\*.*")
for f in files:
    os.remove(f)
vidcap = cv2.VideoCapture(movie_name)
success,image = vidcap.read()
count = 0
while success:
    print('Read a new frame: ', success, count)
        
    image = cv2.resize(image, dsize=(collage_width, collage_height), interpolation=cv2.INTER_AREA)
    div = 64
    image = image // div * div + div // 2
    cv2.imwrite("input/frame%d.png" % count, image)

    success,image = vidcap.read()
    count += 1