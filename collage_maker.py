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


res_patch_check = 4

def bestphot(a,b):
    file = open("computation\\answer.csv")
    csvreader = csv.reader(file)
    for row in csvreader:
        if int(row[0]) == int(a) and int(row[1]) == int(b):
            best_now = row[2]
    file.close()
    return best_now

def collagify(name_of_image, number_of_patches_width,number_of_patches_height ):
    f = open("computation\\num_patches_height.txt", "w")
    f.writelines([str(number_of_patches_height)])
    f.close()

    with open('computation\\num_patches_height.csv', 'w', encoding='UTF8', newline='') as csvfile:
        writer =  csv.writer(csvfile)
        writer.writerow([number_of_patches_height])

    b_max = number_of_patches_height
    with open('computation\\cut_and_downscaled_money_patches.csv', 'w', encoding='UTF8', newline='') as csvfile:
        writer =  csv.writer(csvfile)
        files = glob.glob(str(pathlib.Path().resolve()) +"\\computation\\cut_and_downscaled_money_patches\\*.*")
        for f in files:
            os.remove(f)
        img =  cv2.imread(name_of_image)
        main_h, main_w ,sssss= img.shape
        patch = (main_w/number_of_patches_width)
        holdr = tqdm(range(0,number_of_patches_width), desc = "Cutting the final image into squares and downscaling to 8*8")
        for a in holdr:
            for b in range(0,b_max):
                addw = 0
                addh = 0
                if a == number_of_patches_width:
                    a = number_of_patches_width -1
                    addw = 1
                if b == b_max:
                    b = b_max -1
                    addh = 1
                w1 = math.floor(a * patch)
                w2 = math.floor((a+ 1) * patch)
                h1 = math.floor(b * patch)
                h2 = math.floor((b + 1) * patch) 
                if h2 > main_h:
                    h1 = math.floor((b-1) * patch) - 1 
                    h2 = math.floor((b) *   patch) - 1 
                if w2 > main_w:
                    w1 = math.floor((a-1) * patch) - 1
                    w2 = math.floor((a) * patch)   - 1
                cropped_image = img[h1:h2,w1:w2]
                cropped_image = cv2.resize(cropped_image, dsize=(res_patch_check,res_patch_check), interpolation=cv2.INTER_AREA)
                img_list  = [a,b]
                for eightw in range(0,res_patch_check):
                    for eighth in range(0,res_patch_check):
                        img_list += [cropped_image[eightw,eighth][0],cropped_image[eightw,eighth][1],cropped_image[eightw,eighth][2]]
                writer.writerow(img_list)
                newpath = str(pathlib.Path().resolve()) +"\\computation\\cut_and_downscaled_money_patches\\"+str(a+addw)+"_"+ str(b+addh)+".png"
                cv2.imwrite(newpath, cropped_image)


    print("Starting C++ code to do the maths")
    start = time.time()
    subprocess.check_call([str(pathlib.Path().resolve()) +"\\computation\\collagemaths\\collagemaths.exe"])
    end = time.time()
    print("Finished maths, in " + str(end-start) + " seconds.")

    answer_dict = {}
    for a in range(0,number_of_patches_width):
        for b in range(0, number_of_patches_height):
            answer_dict.update({str(a)+"-"+str(b):bestphot(a,b)})
    return answer_dict