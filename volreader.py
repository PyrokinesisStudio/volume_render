"""
volreader.py
Author: Mahesh Venkitachalam, Patrick Moore
Utilities for reading 3D volumetric data as a 3D OpenGL texture.

function modified for dicom support
"""

import os
from PIL import Image
import pydicom
from bgl import *

#from scipy import misc

def loadVolume(dirName, texture):
    """read volume from directory as a 3D texture"""
    # list images in directory
    files = sorted(os.listdir(dirName))
    print('loading mages from: %s' % dirName)
    depth = 0
    width, height = 0, 0
    for file in files:
        file_path = os.path.abspath(os.path.join(dirName, file))
        try:
            # read image
            img = Image.open(file_path)

             # check if all are of the same size
            if depth is 0:
                width, height = img.size[0], img.size[1] 
                data = Buffer(GL_BYTE, [len(files), width * height])
                data[depth] = img.getdata()
            else:
                if (width, height) == (img.size[0], img.size[1]):
                   data[depth] = img.getdata()
                else:
                    print('mismatch')
                    raise RunTimeError("image size mismatch")
            depth += 1
        except:
            # skip
            print('Invalid image: %s' % file_path)

    # load image data into single array
    print('volume data dims: %d %d %d' % (width, height, depth))

    # load data into 3D texture
    glPixelStorei(GL_UNPACK_ALIGNMENT,1)
    glBindTexture(GL_TEXTURE_3D, texture)
    glTexParameterf(GL_TEXTURE_3D, GL_TEXTURE_WRAP_S, GL_CLAMP_TO_EDGE)
    glTexParameterf(GL_TEXTURE_3D, GL_TEXTURE_WRAP_T, GL_CLAMP_TO_EDGE)
    glTexParameterf(GL_TEXTURE_3D, GL_TEXTURE_WRAP_R, GL_CLAMP_TO_EDGE)
    glTexParameterf(GL_TEXTURE_3D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)
    glTexParameterf(GL_TEXTURE_3D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
    glTexImage3D(GL_TEXTURE_3D, 0, GL_RED, 
                 width, height, depth, 0, 
                 GL_RED, GL_UNSIGNED_BYTE, data)
    #return texture
    return (width, height, depth)



def loadDCMVolume(dirName, texture):
    """read dcm volume from directory as a 3D texture"""
    # list images in directory
    files = sorted(os.listdir(dirName))
    print('loading mages from: %s' % dirName)
    imgDataList = []
    depth = 0
    width, height = 0, 0
    for file in files:
        #skip non dcm files
        if not file.endswith(".dcm"): 
            print('skipping junk file: ' + file)
            continue
        file_path = os.path.abspath(os.path.join(dirName, file))
        try:
            # read image
            ds = pydicom.read_file(file_path)
            img_size = ds.pixel_array.shape  
            imgData = ds.pixel_array.flat.copy() #necessary?  

            # check if all are of the same size
            if depth is 0:
                width, height = img_size[0], img_size[1] 
                data = Buffer(GL_INT, [len(files), width * height])
                data[depth] = imgData[0]
            else:
                if (width, height) == (img_size[0], img_size[1]):
                   data[depth] = imgData[0]

                else:
                    print('mismatch')
                    raise RunTimeError("image size mismatch")
                
            depth += 1
        except:
            # skip
            print('Invalid image: %s' % file_path)
    print(data)
    # load image data into single array
    print('volume data dims: %d %d %d' % (width, height, depth))

    # load data into 3D texture
    glPixelStorei(GL_UNPACK_ALIGNMENT,1)
    glBindTexture(GL_TEXTURE_3D, texture)
    glTexParameterf(GL_TEXTURE_3D, GL_TEXTURE_WRAP_S, GL_CLAMP_TO_EDGE)
    glTexParameterf(GL_TEXTURE_3D, GL_TEXTURE_WRAP_T, GL_CLAMP_TO_EDGE)
    glTexParameterf(GL_TEXTURE_3D, GL_TEXTURE_WRAP_R, GL_CLAMP_TO_EDGE)
    glTexParameterf(GL_TEXTURE_3D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)
    glTexParameterf(GL_TEXTURE_3D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
    glTexImage3D(GL_TEXTURE_3D, 0, GL_RED, 
                 width, height, depth, 0, 
                 GL_RED, GL_UNSIGNED_BYTE, data)
    return (width, height, depth)

# load texture
def loadTexture(filename):
    img = Image.open(filename)
    #img_data = np.array(list(img.getdata()), 'B')
    #texture = GL.glGenTextures(1)
    width, height = img.size[0], img.size[1] 
    img_data = Buffer(GL_BYTE, [width * height * 4])
    texture = Buffer(GL_INT, [1])
    glGenTextures(1, texture)
    glPixelStorei(GL_UNPACK_ALIGNMENT,1)
    glBindTexture(GL_TEXTURE_2D, texture)
    glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_CLAMP_TO_EDGE)
    glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_CLAMP_TO_EDGE)
    glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)
    glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
    glTexImage2D(GL_TEXTURE_2D, 0, GL_RGBA, img.size[0], img.size[1], 
                 0, GL_RGBA, GL_UNSIGNED_BYTE, img_data)
    return texture