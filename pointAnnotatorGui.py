import tkinter as tk
import os
import sys
import argparse
from MainWindow import MainWindow

labels = ["head","right_hand","right_elbow","right_shoulder","neck", "left_shoulder","left_elbow","left_hand",
"right_foot","right_knee","right_hip","left_hip","left_knee","left_foot"]

ap = argparse.ArgumentParser()
ap.add_argument("-i", "--images", default="img", help="Path to the images")
ap.add_argument("-r", "--result", default="result.csv", help="Path to result file")
args = vars(ap.parse_args())

image_path = args["images"]
result = args["result"]
try:
    images = [k for k in sorted(os.listdir(os.path.join(image_path))) if '8bit.png' in k]
except FileNotFoundError:
    print("No image folder found or provided (default is img)")
    sys.exit(1)

dataset = []

try:
    data = []
    with open(result, 'rb') as features:
        data = features.readlines()
        for i, line in enumerate(data):
            if (i != 0):
                dataset.append(line.decode().split(';')[0])
    features.close()
    done = len(data)-1
except FileNotFoundError:
    print("No result file found, starting new annotation!\n")
    dataset = []
    done = 0
    with open(result, 'w') as features:
        header="image;"
        for item in labels:
            header+=item +";"
        header=header[:-1]+"\n"
        features.write(header)

images = [x for x in images if x not in dataset]


if images==[]:
    print("Nothing to do")
else:
    root = tk.Tk()
    MainWindow(root,images,result,labels,image_path,done)
    root.title("pyPointAnnotator")
    root.mainloop()
