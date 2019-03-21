# pyPointAnnotator
Point annotation on images and mask generator.

Show an image to the user and let him annotate all the point defined, with a fixed order.
This software scan the images folder selecting only those with name ending in "8bit.png", to be used directly 
with [pyOniExtractor](https://github.com/roccopietrini/pyOniExtractor), you can change this accordingly to your files in the code.
You can quit and resume where you left. All points defined in the labels array must be annotated in that order, with the possibility to skip points. 
The coordinates of the points will be saved in the result file. In this example we annotate body joints.

![Image of man](https://i.ibb.co/rs9QnH2/done.png)


If you need a web version (tested on Amazon MTurk) check this repo: [pointAnnotatorWeb](https://github.com/roccopietrini/pointAnnotatorWeb)

Result file is a csv with semicolon as delimeter where after the header for each image:
```
image_path;x1,y1;...xn,yn
```

# Requirements
Python 3 with the following modules:

Pillow
```bash
python3 -m pip install Pillow
```

OpenCV 3
```bash
python3 -m pip install opencv-python==3.4.5.20
```

Numpy
```bash
python3 -m pip install numpy
```

# Usage
```bash
python3 pointAnnotatorGui.py [-h] [-i IMAGES_FOLDER] [-r RESULT]

```

optional arguments:
```
  -h, --help        show this help message and exit

  -i IMAGES_FOLDER  path images folder, default "img"
  
  -r RESULT         Result file, default "result.csv"
```

The image is displayed with the following indication:

* Progress in annotation of the images (blue label)
* Next point to annotate (red label)
* Reset button to restart the annotation of the current image
* Undo button to undo last annotated point
* Save/Next button to save the result of the current annotation and go to the next image

Left click to annotate, right mouse click to skip the point (i.e. the point is not visible), in this case in the result file we will have -1,-1 as coordinates.

# Mask Generator

For every point annotated a binary mask can be generated. The following will create a binary mask for every point for every image.  

```bash
python3 pointAnnotatorMask.py [-h] [-i IMAGES_FOLDER] [-d DATASET] [-m MASK_FOLDER]

```

optional arguments:
```
  -h, --help        show this help message and exit

  -i IMAGES_FOLDER  path images folder, default "img"
  
  -d DATASET        Result file, default "result.csv"
  
  -m MASK_FOLDER    path to save masks
```
