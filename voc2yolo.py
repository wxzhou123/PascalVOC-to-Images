import os
import random
import glob
import xml.etree.ElementTree as ET
import shutil


def xml_reader(filename):
    """ Parse a PASCAL VOC xml file """
    tree = ET.parse(filename)
    size = tree.find('size')
    width = int(size.find('width').text)
    height = int(size.find('height').text)
    objects = []
    for obj in tree.findall('object'):
        obj_struct = {}
        obj_struct['name'] = obj.find('name').text
        bbox = obj.find('bndbox')
        obj_struct['bbox'] = [int(bbox.find('xmin').text),
                              int(bbox.find('ymin').text),
                              int(bbox.find('xmax').text),
                              int(bbox.find('ymax').text)]
        objects.append(obj_struct)
    return width, height, objects


def voc2yolo(filename):
    classes_dict = {}
    with open("classes.txt", 'r', encoding='utf-8') as f:
        for idx, line in enumerate(f.readlines()):
            class_name = line.strip()
            classes_dict[class_name] = idx

    width, height, objects = xml_reader(filename)

    lines = []
    for obj in objects:
        x, y, x2, y2 = obj['bbox']
        class_name = obj['name']
        label = classes_dict[class_name]
        cx = (x2 + x) * 0.5 / width
        cy = (y2 + y) * 0.5 / height
        w = (x2 - x) * 1. / width
        h = (y2 - y) * 1. / height
        line = "%s %.6f %.6f %.6f %.6f\n" % (label, cx, cy, w, h)
        lines.append(line)

    txt_name = filename.replace(".xml", ".txt").replace("labels_voc", "labels")
    with open(txt_name, "w") as f:
        f.writelines(lines)


def get_image_list(image_dir, suffix=['jpg', 'jpeg', 'JPG', 'JPEG', 'png']):
    '''get all image path ends with suffix'''
    if not os.path.exists(image_dir):
        print("PATH:%s not exists" % image_dir)
        return []
    imglist = []
    for root, sdirs, files in os.walk(image_dir):
        if not files:
            continue
        for filename in files:
            filepath = "data/custom/" + os.path.join(root, filename) + "\n"
            if filename.split('.')[-1] in suffix:
                imglist.append(filepath)
    return imglist


def imglist2file(imglist):
    random.shuffle(imglist)
    train_list = imglist[:-100]
    valid_list = imglist[-100:]
    with open("train.txt", "w") as f:
        f.writelines(train_list)
    with open("valid.txt", "w") as f:
        f.writelines(valid_list)


if __name__ == "__main__":
    os.chdir("f:/radar/labeldata")
    xml_path_list = glob.glob("*.xml")
    #for xml_path in xml_path_list:
    #    voc2yolo(xml_path)

    for xml_path in xml_path_list:
        source = xml_path.split(".")[0]+'.bmp'
        print(source)
        shutil.copyfile(source,'images/'+source)

    # imglist = get_image_list("images")
