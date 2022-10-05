from posixpath import splitext
from PIL import Image, ImageEnhance, ImageFilter, ImageOps
from pathlib import Path
import os
import random
import numpy as np
import time

#############################################
#############################################
#                                           #
#    DATA AUGMENTATION                      #
#                                           # 
#       0 Daten laden                       #
#       1 Schwarz Weiß                      #
#                                           #  
#############################################
#############################################


classes = ('01 Basic', '02 Pure', '03 S Pure', '04 X Pure', '05 GP 4')
start_time = time.time()

for i in ("01_train/", "02_test/"):

    for j in classes:
        ##################
        # 0. Daten laden #
        ##################

        source = "augmentation/" + i + j +"/"
        path, dirs, files = next(os.walk(source))


        print(path)
        print("Enthaltene Dateien:", len(files))
  

        
        for k in range(len(files)):
            if k % 10 == 0:
                print("File Number:", k, "of", len(files))
            img = Image.open(path+files[k])
            name = str(files[k])[:-5]

            ###################
            # 1  Schwarz-Weiß #
            ###################
            grey = ImageOps.grayscale(img)
            save_path_grey = str(path) + str(name) + "_" + "grey.jpeg"
            grey.save(save_path_grey)


runtime = round((time.time() - start_time), 1)
print()
print("done.")

convert = time.strftime("%M:%S", time.gmtime(runtime))
print("Runtime: ", convert)