import os
import zipfile

import numpy as np

from keras.applications.resnet50 import ResNet50, preprocess_input
from keras.preprocessing import image

from PIL import Image

"""
Extracts a face/image from a file
"""
def extract_face(filename, required_size=(160, 160)):
    # load image from file
    image = Image.open(filename)
    # convert to RGB, if needed
    image = image.convert('RGB')
    # convert to array
    pixels = np.asarray(image)
    # resize pixels to the model size
    image = Image.fromarray(pixels)
    image = image.resize(required_size)
    face_array = np.asarray(image)
    return face_array


"""
Extracts a face/image from a file
"""
def extract_face_(image_path, image_target_shape=(160, 160)):
    # load image from file
    image_tensor = image.load_img(image_path, target_size = image_target_shape)
    image_tensor = image.img_to_array(image_tensor)
    image_tensor = np.expand_dims(image_tensor, axis=0)
    image_tensor = preprocess_input(image_tensor)
    return image_tensor

"""
Load all image files from a directory.
This directory holds images of a single person.
"""
def load_face(dir,  required_size=(160, 160)):
    faces = list()
    for filename in os.listdir(dir):
        path = dir + filename
        face = extract_face(path, required_size)
        faces.append(face)
    return faces

"""
Loads a dataset of images from a given directory
It's subdirectories are named after a person, whose images
are in the subdirectory.
"""
def load_dataset(dir, required_size=(160,160)):
    print("[DEBUG] Loading dataset...", dir)
    
    # list for faces and labels
    X, y    = list(), list()
    subdirs = os.listdir(dir)

    i = 0
    for subdir in subdirs:
        # Filter out a person whose images don't exist in the
        # training set.
        if (subdir == "Larry_Coker"):
            continue

        path   = dir + subdir + '/'
        faces  = load_face(path, required_size)
        labels = [subdir for i in range(len(faces))]

        X.extend(faces)
        y.extend(labels)
        
        if (i % 500 == 0):
            print("i={}; subdir={}".format(i, subdir))
        i += 1

    return np.asarray(X), np.asarray(y)

"""
Download a file from an S3 bucket and save to a local file,
if the local file is not already present.
"""
def download_s3_file(s3_bucketname: str, s3_filename: str, local_filename):
    if (not os.path.isfile(local_filename)):
        print("[INFO] Downloading '{}' from bucket '{}'...".format(s3_filename, s3_bucketname), end="")
        s3        = boto3.resource('s3')
        s3_bucket = s3.Bucket(s3_bucketname)
        s3_bucket.download_file(s3_filename, local_filename)
        print("DONE.")
    else:
        print("[INFO] '{}' exists.".format(local_filename))

def extract_zipfile(filename: str, extract_dirname: str, extract_path: str):
    # Extract the inputs from the zip file.
    if (not os.path.isdir(extract_dirname)):
        print("[INFO] Extracting from '{}' to '../'...".format(filename), end=" ")
        with zipfile.ZipFile(filename, "r") as zip_ref:
            zip_ref.extractall(extract_path)
        print("DONE.")
    else:
        print("[INFO] Directory '{}' exists.".format(extract_dirname))
