import cv2
import os
import argparse
import numpy as np

bubble_size=[25,15,15,15,15,15,15,15,15,15,15,15,15,15]

ap = argparse.ArgumentParser()
ap.add_argument("-i", "--images", default="img", help="Path to the images")
ap.add_argument("-d", "--dataset", default="result.csv", help="Path to result file")
ap.add_argument("-m", "--masks", default="masks", help="Path to result file")

args = vars(ap.parse_args())

images=[]
coordinates=[]
dst = args["masks"]
if not os.path.exists(dst):
    os.mkdir(dst)
    print("Directory ",dst ," created ")

try:
    with open(args["dataset"], 'rb') as features:
        data = features.readlines()
        for i, line in enumerate(data):
            if (i != 0):
                images.append(line.decode().split(';')[0])
                coordinates.append(line.decode()[:-1].split(';')[1:])
    features.close()
except FileNotFoundError:
    print("No dataset found!\n")

for idx,image in enumerate(images):
    cur_image=cv2.imread((os.path.join(args["images"], image)))
    height,width,depth = cur_image.shape
    mask = np.zeros((height,width))
    for idxpoint, point in enumerate(coordinates[idx]):
        x, y = point.split(',')
        if (int(x)!=-1) or (int(y)!=-1):
            cv2.circle(mask,(int(x),int(y)),bubble_size[idxpoint],(255,255,255),-1)
            cv2.imwrite(dst + "/" + image[:-4] + "_" + str(idxpoint) + ".png",mask)
            mask = np.zeros((height,width))

