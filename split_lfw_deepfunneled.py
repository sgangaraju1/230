import os
from shutil import copyfile

def create_dir(path):
    if (not os.path.isdir(path)):
        os.mkdir(path)

def copy_file(src, dst):
    if (not os.path.isfile(dst)):
        print("copying:", src, dst)
        copyfile(src, dst)

SOURCE_DIR = "../lfw-deepfunneled.source/"
DEST_DIR   = "../lfw-deepfunneled"

# SOURCE_DIR = "../lfw-masked.source/"
# DEST_DIR   = "../lfw-masked"

DEST_DIR_TRAIN = DEST_DIR + "/train/"
DEST_DIR_VAL   = DEST_DIR + "/validation/"
DEST_DIR_TEST  = DEST_DIR + "/test/"

subdirs = os.listdir(SOURCE_DIR)

create_dir(DEST_DIR)
create_dir(DEST_DIR_TRAIN)
create_dir(DEST_DIR_VAL)
create_dir(DEST_DIR_TEST)

count_ids   = 0
count_train = 0
count_test  = 0
count_val   = 0
for subdir in subdirs:
    count_ids += 1
    images = os.listdir(SOURCE_DIR + subdir)
    
    if (len(images) <= 1):
        images_train = images
        images_val   = []
        images_test  = []
    elif (len(images) == 2):
        images_train = [images[0]]
        images_val   = [images[1]]
        images_test  = []
    else:
        images_train = images[:-2]
        images_val   = [images[-2]]
        images_test  = [images[-1]]

    create_dir(DEST_DIR_TRAIN + subdir)

    count_train += len(images_train)
    count_val   += len(images_val)
    count_test  += len(images_test)

    for img in images_train:
        copy_file(SOURCE_DIR + subdir + "/" + img, DEST_DIR_TRAIN + subdir + "/" + img)

    for img in images_val:
        create_dir(DEST_DIR_VAL + subdir)
        copy_file(SOURCE_DIR + subdir + "/" + img, DEST_DIR_VAL + subdir + "/" + img)

    for img in images_test:       
        create_dir(DEST_DIR_TEST + subdir)
        copy_file(SOURCE_DIR + subdir + "/" + img, DEST_DIR_TEST + subdir + "/" + img)
    
count_total = count_train + count_val + count_test

print("total: {:5d} ({:.2f}%)".format(count_total, 100))
print("train: {:5d} ({:.2f}%)".format(count_train, count_train/count_total*100))
print("val  : {:5d} ({:.2f}%)".format(count_val, count_val/count_total*100))
print("test : {:5d} ({:.2f}%)".format(count_test, count_test/count_total*100))