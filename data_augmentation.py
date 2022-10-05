from posixpath import splitext
from PIL import Image, ImageEnhance, ImageFilter, ImageOps
from pathlib import Path
import os
import random
import numpy as np
from datetime import datetime

#############################################
#############################################
#                                           #
#    DATA AUGMENTATION                      #
#                                           # 
#       0 Daten laden                       #
#       1 Rotation                          #
#       2 Horizontal und Vertikal spiegeln  #
#       3 Helligkeit variieren              #
#      (4 Gaußsches Rauschen)              #
#       5 Schwarz Weiß                      #
#                                           #  
#############################################
#############################################


##################
# 0. Daten laden #
##################

source = "augmentation/01_train/01 Basic"
path, dirs, files = next(os.walk(source))

begin_time = datetime.now()

print("Enthaltene Dateien:", len(files))



for j in range(len(files)):
    if j % 10 == 0:
        print("File Number:", j, "of", len(files))
    img = Image.open(path+files[j])
    name = str(files[j])[:-5]

    ###############
    # 1. Rotation #
    ###############
    rot_ankle = []
    save_path_rot = []
    img_rot = []

    random_rot_ankle = True

    if random_rot_ankle == True:
        rot_ankle = random.sample(range(1, 360), 4)
    else:
        rot_ankle = [30, 100, 200, 300]

    for i in range(len(rot_ankle)):
        img_rot.append(img.rotate(rot_ankle[i]))
        save_path_rot.append(str(path) + str(name) + "_" + "img_rot_"  + str(rot_ankle[i]) + ".jpeg")
        img_rot[i].save(save_path_rot[i])

    #######################################
    # 2. Horizontal und Vertikal spiegeln #
    #######################################
    transposed_img_lr = img.transpose(Image.FLIP_LEFT_RIGHT)
    transposed_img_tb = img.transpose(Image.FLIP_TOP_BOTTOM)

    save_path_flip_lr = str(path) + str(name) + "_" + "flip_lr.jpeg"
    save_path_flip_tb = str(path) + str(name) + "_" + "flip_tb.jpeg"

    transposed_img_lr.save(save_path_flip_lr)
    transposed_img_tb.save(save_path_flip_tb)

    ###########################
    # 3. Helligkeit variieren #
    ###########################
    bright_factor = []
    save_path_bright = []
    img_bright = []

    random_bright_factor = True

    if random_bright_factor == True:
        for i in range(6):
            bright_factor.append(round((random.random()*4),2))
    else:
        bright_factor = [0.2, 0.3, 0.8, 1.2, 2.0, 4.0]

    for i in range(len(bright_factor)):
        img_bright.append(ImageEnhance.Brightness(img).enhance(bright_factor[i]))
        save_path_bright.append(str(path) + str(name) + "_" + "img_bright_" + str(bright_factor[i]) + ".jpeg")
        img_bright[i].save(save_path_bright[i])

    #########################
    # 4. Gaußsches Rauschen #
    #########################
    """ gauß_factor = []
    save_path_gauß = []
    img_gauß = []

    random_gauß_factor = True

    if random_gauß_factor == True:
        for i in range(6):
            gauß_factor.append(round((random.random()*4),2))
    else:
        gauß_factor = [0.2, 0.3, 0.8, 1.2, 2.0, 4.0]

    for i in range(len(gauß_factor)):
        img_gauß.append(img.filter(ImageFilter.GaussianBlur(gauß_factor[i])))
        save_path_gauß.append(str(path) + str(name) + "_" + "img_gauß_" + str(gauß_factor[i]) + ".jpeg")
        img_gauß[i].save(save_path_gauß[i]) """

    ###################
    # 5. Schwarz-Weiß #
    ###################
    grey = ImageOps.grayscale(img)
    save_path_grey = str(path) + str(name) + "_" + "grey.jpeg"
    grey.save(save_path_grey)

print()
print("done.")
print("Runtime: ", (datetime.now() - begin_time).strftime("%M:%S"))