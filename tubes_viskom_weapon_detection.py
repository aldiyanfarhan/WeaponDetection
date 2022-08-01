# -*- coding: utf-8 -*-
"""Tubes-Viskom_Weapon-detection.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1-sozDQiWVqJI70PisDVyU1LJeQ0LudU_

Anggota Kelompok:

- M Rifqi Wiliatama (1301184278)

- Aldiyan Farhan N  (1301180344)

- Andika Elang D    (1301184153)

Link Dataset:
https://drive.google.com/drive/folders/1AV42HGeyydxV7KIHzEGXV6dPDcqKaKAY
"""

from google.colab import drive
drive.mount('/content/drive')

# Sesuaikan dengan directory zip
!unzip '/content/drive/MyDrive/UASViskom/Sohas_weapon-Detection_Fix_2.zip' -d ''

"""Import library"""

import os
import numpy as np
import pandas as pd
from pathlib import Path
from shutil import copyfile
from xml.dom.minidom import parse

"""Membuat Directory untuk gambar dan label"""

!mkdir -p Dataset/labels
!mkdir -p Dataset/images

"""Mendefinisikan class"""

classes = ['pistol', 'knife', 'smartphone', 'monedero', 'tarjeta', 'billete'] # monedero = purse, tarjeta = card, billete = bill

"""Fungsi untuk konversi PascalVOC ke YOLO"""

def convert_annot(size, box):
    x1 = int(box[0])
    y1 = int(box[1])
    x2 = int(box[2])
    y2 = int(box[3])

    dw = np.float32(1. / int(size[0]))
    dh = np.float32(1. / int(size[1]))

    w = x2 - x1
    h = y2 - y1
    x = x1 + (w / 2)
    y = y1 + (h / 2)

    x = x * dw
    w = w * dw
    y = y * dh
    h = h * dh
    
    return [x, y, w, h]

"""Fungsi untuk menyimpan anotasi YOLO kedalam file labels dengan format .txt"""

def save_txt_file(img_jpg_file_name, size, img_box):
    save_file_name = '/content/Dataset/labels/' +  img_jpg_file_name + '.txt'
    print(save_file_name)
    
    with open(save_file_name ,'a+') as file_path:
        for box in img_box:
            cls_num = classes.index(box[0])
            new_box = convert_annot(size, box[1:])
            file_path.write(f"{cls_num} {new_box[0]} {new_box[1]} {new_box[2]} {new_box[3]}\n")

        file_path.flush()
        file_path.close()

"""Fungsi untuk mengekstrak anotasi dari file xml (PascalVOC)"""

def get_xml_data(file_path, img_xml_file):
    img_path = file_path + '/' + img_xml_file + '.xml'
    dom = parse(img_path)
    root = dom.documentElement
    img_name = root.getElementsByTagName("filename")[0].childNodes[0].data
    img_size = root.getElementsByTagName("size")[0]
    objects = root.getElementsByTagName("object")
    img_w = img_size.getElementsByTagName("width")[0].childNodes[0].data
    img_h = img_size.getElementsByTagName("height")[0].childNodes[0].data
    img_c = img_size.getElementsByTagName("depth")[0].childNodes[0].data
   
    img_box = []
    for box in objects:
        cls_name = box.getElementsByTagName("name")[0].childNodes[0].data
        x1 = int(box.getElementsByTagName("xmin")[0].childNodes[0].data)
        y1 = int(box.getElementsByTagName("ymin")[0].childNodes[0].data)
        x2 = int(box.getElementsByTagName("xmax")[0].childNodes[0].data)
        y2 = int(box.getElementsByTagName("ymax")[0].childNodes[0].data)
        img_jpg_file_name = img_xml_file + '.jpg'
        img_box.append([cls_name, x1, y1, x2, y2])
  

    save_txt_file(img_xml_file, [img_w, img_h], img_box)

"""Mengkonversi semua anotasi PascalVCO kebentuk YOLO untuk data train"""

files = os.listdir('Sohas_weapon-Detection/annotations/xmls')
for file in files:
    print("file name: ", file)
    file_xml = file.split(".")
    print(file_xml[0])
    get_xml_data('Sohas_weapon-Detection/annotations/xmls', file_xml[0])

"""Mengkonversi semua anotasi PascalVCO kebentuk YOLO untuk data validasi"""

files = os.listdir('Sohas_weapon-Detection/annotations_test/xmls')
for file in files:
    print("file name: ", file)
    file_xml = file.split(".")
    print(file_xml[0])
    get_xml_data('Sohas_weapon-Detection/annotations_test/xmls', file_xml[0])

"""Memasukkan data citra kedalam list train dan test"""

# from sklearn.model_selection import train_test_split
image_list_train = os.listdir('/content/Sohas_weapon-Detection/images')
image_list_test = os.listdir('/content/Sohas_weapon-Detection/images_test')
train_list = image_list_train
test_list = image_list_test
print('total =',len(train_list + image_list_test))
print('train :',len(train_list))
print('test  :',len(test_list))

"""Fungsi untuk mencopy data gambar dan label ke file nya masing-masing (train/test)"""

def copy_data(file_list, img_labels_root, imgs_source, mode):

    root_file = Path( '/content/Dataset/images/'+  mode)
    if not root_file.exists():
        print(f"Path {root_file} does not exit, making a new one")
        os.makedirs(root_file)

    root_file = Path('/content/Dataset/labels/' + mode)
    if not root_file.exists():
        print(f"Path {root_file} does not exit, making a new one")
        os.makedirs(root_file)

    for file in file_list:               
        img_name = file.replace('.jpg', '')        
        img_src_file = imgs_source + '/' + img_name + '.jpg'        
        label_src_file = img_labels_root + '/' + img_name + '.txt'

        DICT_DIR = '/content/Dataset/images/'  + mode
        img_dict_file = DICT_DIR + '/' + img_name + '.jpg'
        copyfile(img_src_file, img_dict_file)

        DICT_DIR = '/content/Dataset/labels/' + mode
        img_dict_file = DICT_DIR + '/' + img_name + '.txt'
        copyfile(label_src_file, img_dict_file)

"""Mengcopy data gambar dan label ke file masing-masing (train/test)"""

copy_data(train_list, '/content/Dataset/labels', '/content/Sohas_weapon-Detection/images', "train")
copy_data(test_list,  '/content/Dataset/labels', '/content/Sohas_weapon-Detection/images_test', "test")

"""![4834244.jpg](data:image/jpeg;base64,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)

Mengekstrak data untuk dilakukan deteksi
"""

!unzip '/content/drive/MyDrive/UASViskom/PotoTestBaru.zip' -d ''

!unzip '/content/drive/MyDrive/UASViskom/PotoTest.zip' -d ''

"""Melakukan clone repository YOLOv5 dari github"""

# Commented out IPython magic to ensure Python compatibility.
!git clone https://github.com/ultralytics/yolov5
# %cd yolov5

"""Membuat file yaml untuk konfigurasi YOLO"""

import yaml

dict_file = {'train':'/content/Dataset/images/train',
            'val': '/content/Dataset/images/test',
            'nc' : '6',
            'names' : ['pistol', 'knife', 'smartphone', 'monedero', 'tarjeta', 'billete']}

with open('/content/yolov5/data/od_weapon.yaml', 'w+') as file:
    documents = yaml.dump(dict_file, file)

"""Melakukan instalasi requirements untuk penggunaan YOLOv5"""

pip install -r requirements.txt  # install

!python train.py --img 416 --batch 32 --epochs 30 --data data/od_weapon.yaml --cfg models/yolov5s.yaml --weights yolov5s.pt

!python val.py --weights runs/train/exp/weights/best.pt --data data/od_weapon.yaml --img 640

!python detect.py --source /content/PotoTest --weights runs/train/exp/weights/best.pt --conf 0.25

from IPython.display import Image

from glob import glob
import matplotlib.pyplot as plt
testfiles = glob('runs/detect/exp2/*')
img = plt.imread(testfiles[6])
plt.figure(figsize=(15,7))
plt.imshow(img)
# plt.savefig('detect_1.png')
plt.show

"""LOCAL RUNNING"""

import os
import numpy as np
import pandas as pd
from pathlib import Path
from shutil import copyfile
from xml.dom.minidom import parse

classes = ['pistol', 'knife', 'smartphone', 'monedero', 'tarjeta', 'billete'] # monedero = purse, tarjeta = card, billete = bill

def convert_annot(size, box):
    x1 = int(box[0])
    y1 = int(box[1])
    x2 = int(box[2])
    y2 = int(box[3])

    dw = np.float32(1. / int(size[0]))
    dh = np.float32(1. / int(size[1]))

    w = x2 - x1
    h = y2 - y1
    x = x1 + (w / 2)
    y = y1 + (h / 2)

    x = x * dw
    w = w * dw
    y = y * dh
    h = h * dh
    
    return [x, y, w, h]

def save_txt_file(img_jpg_file_name, size, img_box):
    save_file_name = r'C:\KULIAH\Visi Komputer\UAS\Sohas_weapon-Detection\label/' +  img_jpg_file_name + '.txt'
    print(save_file_name)
    
    with open(save_file_name ,'a+') as file_path:
        for box in img_box:
            cls_num = classes.index(box[0])
            new_box = convert_annot(size, box[1:])
            file_path.write(f"{cls_num} {new_box[0]} {new_box[1]} {new_box[2]} {new_box[3]}\n")

        file_path.flush()
        file_path.close()

def get_xml_data(file_path, img_xml_file):
    img_path = file_path + '/' + img_xml_file + '.xml'
    dom = parse(img_path)
    root = dom.documentElement
    img_name = root.getElementsByTagName("filename")[0].childNodes[0].data
    img_size = root.getElementsByTagName("size")[0]
    objects = root.getElementsByTagName("object")
    img_w = img_size.getElementsByTagName("width")[0].childNodes[0].data
    img_h = img_size.getElementsByTagName("height")[0].childNodes[0].data
    img_c = img_size.getElementsByTagName("depth")[0].childNodes[0].data
   
    img_box = []
    for box in objects:
        cls_name = box.getElementsByTagName("name")[0].childNodes[0].data
        x1 = int(box.getElementsByTagName("xmin")[0].childNodes[0].data)
        y1 = int(box.getElementsByTagName("ymin")[0].childNodes[0].data)
        x2 = int(box.getElementsByTagName("xmax")[0].childNodes[0].data)
        y2 = int(box.getElementsByTagName("ymax")[0].childNodes[0].data)
        img_jpg_file_name = img_xml_file + '.jpg'
        img_box.append([cls_name, x1, y1, x2, y2])
  

    save_txt_file(img_xml_file, [img_w, img_h], img_box)

files = os.listdir(r'C:\KULIAH\Visi Komputer\UAS\Sohas_weapon-Detection\annotations\xmls/')
for file in files:
    print("file name: ", file)
    file_xml = file.split(".")
    print(file_xml[0])
    get_xml_data(r'C:\KULIAH\Visi Komputer\UAS\Sohas_weapon-Detection\annotations\xmls/', file_xml[0])

from sklearn.model_selection import train_test_split
image_list = os.listdir(r'C:\KULIAH\Visi Komputer\UAS\Sohas_weapon-Detection\images/')
train_list, test_list = train_test_split(image_list, test_size=0.2, random_state=42)
val_list, test_list = train_test_split(test_list, test_size=0.5, random_state=42)
print('total =',len(image_list))
print('train :',len(train_list))
print('val   :',len(val_list))
print('test  :',len(test_list))

type(image_list[0])

def copy_data(file_list, img_labels_root, imgs_source, mode):

    root_file = Path(r'C:\KULIAH\Visi Komputer\UAS\Sohas_weapon-Detection\Dataset\image/'+  mode)
    if not root_file.exists():
        print(f"Path {root_file} does not exit, making a new one")
        os.makedirs(root_file)

    root_file = Path(r'C:\KULIAH\Visi Komputer\UAS\Sohas_weapon-Detection\Dataset\label/' + mode)
    if not root_file.exists():
        print(f"Path {root_file} does not exit, making a new one")
        os.makedirs(root_file)

    for file in file_list:               
        img_name = file.replace('.jpg', '')        
        img_src_file = imgs_source + '/' + img_name + '.jpg'        
        label_src_file = img_labels_root + '/' + img_name + '.txt'

        DICT_DIR = r'C:\KULIAH\Visi Komputer\UAS\Sohas_weapon-Detection\Dataset\image/'  + mode
        img_dict_file = DICT_DIR + '/' + img_name + '.jpg'
        copyfile(img_src_file, img_dict_file)

        DICT_DIR = r'C:\KULIAH\Visi Komputer\UAS\Sohas_weapon-Detection\Dataset\label/' + mode
        img_dict_file = DICT_DIR + '/' + img_name + '.txt'
        copyfile(label_src_file, img_dict_file)

copy_data(train_list, r'C:\KULIAH\Visi Komputer\UAS\Sohas_weapon-Detection\label/', r'C:\KULIAH\Visi Komputer\UAS\Sohas_weapon-Detection\images/', "train")
copy_data(val_list,   r'C:\KULIAH\Visi Komputer\UAS\Sohas_weapon-Detection\label/', r'C:\KULIAH\Visi Komputer\UAS\Sohas_weapon-Detection\images/', "val")
copy_data(test_list,  r'C:\KULIAH\Visi Komputer\UAS\Sohas_weapon-Detection\label/', r'C:\KULIAH\Visi Komputer\UAS\Sohas_weapon-Detection\images/', "test")

# Commented out IPython magic to ensure Python compatibility.
!git clone https://github.com/ultralytics/yolov5/
# %cd C:\Users\Aldiyan Farhan N\yolov5

import yaml

dict_file = {'train':r'C:\KULIAH\Visi Komputer\UAS\Sohas_weapon-Detection\Dataset\image\train/',
            'val': r'C:\KULIAH\Visi Komputer\UAS\Sohas_weapon-Detection\Dataset\image\val/',
            'nc' : '6',
            'names' : ['pistol', 'knife', 'smartphone', 'monedero', 'tarjeta', 'billete']}

with open(r'C:\Users\Aldiyan Farhan N\yolov5\data\hard_head.yaml', 'w+') as file:
    documents = yaml.dump(dict_file, file)

!pip install -r requirements.txt

!python train.py --img 416 --batch 32 --epochs 30 --data data/hard_head.yaml --cfg models/yolov5s.yaml --weights yolov5s.pt