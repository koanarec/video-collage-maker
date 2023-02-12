import cv2
import numpy as np
import glob
import pathlib

img_array = []
for filename in glob.glob(str(pathlib.Path().resolve()) + "\\output\\*.*"):
    img = cv2.imread(filename)
    height, width, layers = img.shape
    size = (width,height)
    img_array.append(img)
    print("added frame")
 
 
out = cv2.VideoWriter('project.avi',cv2.VideoWriter_fourcc(*'DIVX'), 15, size)
 
for i in range(len(img_array)):
    out.write(img_array[i])
out.release()