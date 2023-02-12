from collage_maker import collagify
import cv2
import glob
import os
import pathlib
import csv
from PIL import Image
import os
from PIL import Image, ImageOps
import numpy as np
import uuid
from time import gmtime, strftime
from tqdm import tqdm
import PIL
import pathlib
from os import execv, walk
from time import gmtime, strftime
from tqdm import tqdm
import numpy as np
import os.path
from os import path
from PIL import Image, ExifTags
import csv
from subprocess import Popen, PIPE
import uuid
from inputimeout import inputimeout, TimeoutOccurred
import sys

#This takes the RGB values inside the images and removes modulo. The bigger the worse, but faster it is. 0 nothing, 255 makes it all black. 10 is unnoticable before colligified,
#50 probably decent after turned into a collage
mod_num = 100 

#How high quality the checking of each patch is the pixels are squared
res_patch_check = 4

movie_name = "in.mp4"

#This takes the input images, and downscales them to be ready to paste. It will skip them if they have allready been calculated. 
def downscale_to_patch(image_name, patch):
    if image_name not in os.listdir(str(pathlib.Path().resolve()) + "\\computation\\patch_sized_photos"):
        f = image_name
        try:
            img = cv2.imread(str(pathlib.Path().resolve()) + "\\computation\\images\\"+f)
            heightzz, widthzz, sss = img.shape
            if widthzz > heightzz * 2 * 0.8:
                res = cv2.resize(img, dsize=(patch*2, patch), interpolation=cv2.INTER_AREA)
            elif widthzz * 2 * 0.8 < heightzz:
                res = cv2.resize(img, dsize=(patch, patch * 2), interpolation=cv2.INTER_AREA)
            else:
                res = cv2.resize(img, dsize=(patch, patch), interpolation=cv2.INTER_AREA)
            cv2.imwrite(str(pathlib.Path().resolve()) + "\\computation\\patch_sized_photos\\"+ image_name.split("\\")[-1], res)
        except:
            print('problem with: ', image_name)
            try:
                dels = inputimeout(prompt='Do you want to delete it? (y/n)\n', timeout=5)
            except TimeoutOccurred:
                dels = 'timeout'
            if dels == "y":
                try:
                    os.remove(str(pathlib.Path().resolve()) + "\\images\\" + image_name)
                except:
                    print("couln't delete")

#Creates and pastes all of the patches toghert into a collage
def paste(answer_as_list,output_location):
    print("Assembling collage from patches")
    print(len(patches_to_paste), " patches cached using ", str(sys.getsizeof(patches_to_paste)/1048576), "MiB")
    done = []
    l_img = np.zeros((collage_height,collage_width, 3), np.uint8)
    for a in range(0,number_of_patches_width):
        for b in range(0, number_of_patches_height):
            if str(a)+"-"+str(b) in answer_as_list and (a,b) not in done:
                best_photo_name = answer_as_list[str(a)+"-"+str(b)]
                downscale_to_patch(best_photo_name, patch)
                naems= str(glob.glob(str(pathlib.Path().resolve()))[0]) + "\\computation\\patch_sized_photos\\" + str(best_photo_name.split("\\")[-1])

                if naems not in patches_to_paste:
                    s_img = cv2.imread(naems)
                    patches_to_paste.update({naems: s_img})
                else:
                    s_img = patches_to_paste[naems]
                x_offset= a * patch
                y_offset= b * patch
                height, width,ss = s_img.shape
                
                if height > 0.8 * width * 2:
                    if y_offset+s_img.shape[0] < l_img.shape[0]:
                        done.append((a,b+1))
                        l_img[y_offset:y_offset+s_img.shape[0], x_offset:x_offset+s_img.shape[1]] = s_img
                    else:
                        x_offset= a * patch
                        y_offset= (b-1) * patch
                        done.append((a ,(b-1)))
                        l_img[y_offset:y_offset+s_img.shape[0], x_offset:x_offset+s_img.shape[1]] = s_img
                        
                elif width > 0.8 * 2 * height:
                    if x_offset+s_img.shape[1] < l_img.shape[1]:
                        done.append((a + 1,b))
                        l_img[y_offset:y_offset+s_img.shape[0], x_offset:x_offset+s_img.shape[1]] = s_img
                    else:
                        x_offset= (a-1) * patch
                        y_offset= b * patch
                        done.append(((a-1),b))
                        l_img[y_offset:y_offset+s_img.shape[0], x_offset:x_offset+s_img.shape[1]] = s_img
                else:
                    l_img[y_offset:y_offset+s_img.shape[0], x_offset:x_offset+s_img.shape[1]] = s_img
                done.append((a,b))      
    cv2.imwrite(output_location, l_img)

#Returns the integers inside a string as an int
def take_ints(name):
    int_name = ""
    for x in name:
        if x in "0123456789":
            int_name += x
    return int(int_name)

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

downscaled = []
patch64data = {}
try:
    with open('computation\\downscaled_patches_data.csv', 'r', encoding='UTF8', newline='') as csvfile:
        spamreader = csv.reader(csvfile, delimiter=',', quotechar='|')
        for x in spamreader:
            downscaled.append(x[0])
            patch64data.update({x[0]: x})
except:
    downscaled = []
    patch64data = {}

print("Downscaling patches to 8*8px, and writing data to \"downscaled_patches_data.csv\"")
with open('computation\\downscaled_patches_data.csv', 'w', encoding='UTF8', newline='') as csvfile:
    writer = csv.writer(csvfile)
    for f in tqdm(glob.glob(str(pathlib.Path().resolve()) + "\\computation\\images\\*.*")):
        working = False
        if f.split("\\")[-1] not in downscaled:
            try:
                img =  cv2.imread(f)
                acurrh, acurrw,dd = img.shape
                working = True
            except:
                working = False
                print("There is something wrong with picture:", f)
        else:
            writer.writerow(patch64data[f.split("\\")[-1]])
        
        if working:
            data = []
            patch_name = str(str(f).split("\\")[-1])
            shape = "square"
            if acurrw > acurrh * 2 * 0.8:
                shape = "landscape"
                img = cv2.resize(img, dsize=(res_patch_check * 2, res_patch_check), interpolation=cv2.INTER_AREA )
                data = [patch_name,shape]
                for currw in range(0,res_patch_check):
                    for currh in range(0,res_patch_check):
                        data.append(img[currw, currh][0])
                        data.append(img[currw, currh][1])
                        data.append(img[currw, currh][2])
                for currw in range(0,res_patch_check):
                    for currh in range(0,res_patch_check):
                        data.append(img[currw, currh + res_patch_check][0])
                        data.append(img[currw, currh + res_patch_check][1])
                        data.append(img[currw, currh + res_patch_check][2])
            elif acurrw * 2 * 0.8 < acurrh:
                shape = "portrait"
                img = cv2.resize(img, dsize=(res_patch_check, res_patch_check * 2), interpolation=cv2.INTER_AREA )
                data = [patch_name,shape]
                for currw in range(0,res_patch_check):
                    for currh in range(0,res_patch_check):
                        data.append(img[currw, currh][0])
                        data.append(img[currw, currh][1])
                        data.append(img[currw, currh][2])
                for currw in range(0,res_patch_check):
                    for currh in range(0,res_patch_check):
                        data.append(img[currw + res_patch_check, currh][0])
                        data.append(img[currw + res_patch_check, currh][1])
                        data.append(img[currw + res_patch_check, currh][2])
            else:
                img = cv2.resize(img, dsize=(res_patch_check, res_patch_check), interpolation=cv2.INTER_AREA )
                data = [patch_name,shape]
                for currw in range(0,res_patch_check):
                    for currh in range(0,res_patch_check):
                        pixel = [img[currw, currh][0],img[currw, currh][1],img[currw, currh][2]]
                        data = data +  pixel
            writer.writerow(data)

def collegify():
    files = glob.glob(str(pathlib.Path().resolve()) + "\\input\\*.*")
    files.sort(key=take_ints)
    for f in files:
        answer = collagify(f,number_of_patches_width,number_of_patches_height)
        paste(answer,"output/" + f.split("\\")[-1])


#Stores images to paste in RAM
patches_to_paste = {}

#Calculates the final dimentions of collage and makes the actual png to be filled up
vidcap = cv2.VideoCapture(movie_name)
success,image = vidcap.read()
money_height,money_width, channels = image.shape
money_ratio = money_width/(money_width + money_height)
number_of_patches_width = round(money_ratio * res_of_comp)
number_of_patches_height = round((1-money_ratio) * res_of_comp)
collage_width = patch * number_of_patches_width
collage_height = patch * number_of_patches_height


print("Converting all images to PNG")
[os.rename(f, str(pathlib.Path().resolve()) +"\\computation\\images\\"+str(uuid.uuid4()) +".png") for f in glob.glob(str(pathlib.Path().resolve()) + "\\computation\\images\\*.*") if f.split("//")[-1][-4:] != ".png"]
try:
    os.remove("computation/calculated_answer.csv")
except:
    pass

[os.remove(f) for f in  glob.glob(str(pathlib.Path().resolve()) + "\\computation\\patch_sized_photos\\*.*")]
[os.remove(f) for f in  glob.glob(str(pathlib.Path().resolve()) + "\\output\\*.*")]

#sepearte_to_img(movie_name)
collegify()