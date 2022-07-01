from django.http import JsonResponse

import os
import json
from pathlib import Path
import shutil
import filetype
import hashlib
import time
import cv2
import numpy as np

from .label_file import LabelFile
from .annotation2voc import generate_voc_dataset
from .annotation2coco import generate_coco_dataset
""" -------------------------------------------------------------- """
""" -------------------------操作返回函数-------------------------- """
""" -------------------------------------------------------------- """
# 统一的返回结果，按实际情况修改
# 当然也可以可以自定义一个类
# 操作成功时只返回状态码code和数据data，（成功了就不需要message，同理失败了自然也不需要data）


def ok(data: object):
    return JsonResponse({'code': 20000, 'message': '操作成功', 'data': data})


# 操作失败时只返回状态码code和错误信息message
def error(message: str):
    return JsonResponse({'code': 20001, 'message': message})


""" -------------------------------------------------------------- """
""" ---------------------图片存储与视频帧提取----------------------- """
""" -------------------------------------------------------------- """

BACKEND_DIR = os.getcwd()

TMPFILE_DIR = os.path.join(BACKEND_DIR, 'tmpfile')
UPLOAD_FILE_DIR = os.path.join(BACKEND_DIR, 'upload_file', 'dataset')  # 图片存放路径


def convert_video_to_image(video_name, video_path, dst_dir, image_count):
    video_data = cv2.VideoCapture(video_path)
    count = 0
    frame_count = 0
    frameFrequency = 60  # 抽帧频率
    while video_data.isOpened():
        is_read, image = video_data.read()
        if not is_read:
            break
        else:
            if frame_count % frameFrequency == 0:
                cv2.imwrite(
                    os.path.join(
                        dst_dir, video_name[:video_name.rfind('.')] + '_' +
                        str(count) + '.jpg'), image)
                count += 1
            frame_count += 1
    return image_count + count


def move_upload_image_to_dir(dst_dir):
    """ 将压缩包中解压的文件类型进行判断 """
    image_count = 0
    file_list = os.listdir(TMPFILE_DIR)
    for file_name in file_list:
        file_path = os.path.join(TMPFILE_DIR, file_name)
        kind = filetype.guess(file_path)
        if kind is not None:
            if kind.extension in ['png', 'jpg', 'jpeg']:
                # 图片直接拷贝到新的数据集文件夹中
                shutil.copy(file_path, os.path.join(dst_dir, file_name))
                image_count += 1
            else:
                if kind.extension in ['mp4']:
                    # 如果文件是视频，抽取帧拷贝到新数据集文件夹中
                    image_count = convert_video_to_image(
                        file_name, file_path, dst_dir, image_count)
        # 删除临时图片
        os.remove(file_path)
    return image_count


def save_image_to_dir():
    dataset_dir_list = os.listdir(UPLOAD_FILE_DIR)
    dataset_index = str(len(dataset_dir_list) + 1)
    new_dataset_dir = os.path.join(UPLOAD_FILE_DIR, dataset_index)
    os.makedirs(new_dataset_dir)
    image_count = move_upload_image_to_dir(new_dataset_dir)
    return image_count, dataset_index


""" -------------------------------------------------------------- """
""" ----------------------特定格式数据集生成------------------------ """
""" -------------------------------------------------------------- """


# 为所有图片创建一个对应名字的JSON文件，并移到temp_path去
def create_JSON_file(temp_path, image, labelinfo):
    image_absolute_path = os.path.join(os.getcwd(), 'upload_file', 'dataset',
                                       image)
    image_name = os.path.basename(image)
    json_name = os.path.splitext(image_name)[0] + '.json'  # 文件名无后缀
    image_size = cv2.imread(image_absolute_path).shape
    height, width = image_size[0], image_size[1]

    shapes = []
    label = labelinfo['label']['text']
    for rect in labelinfo['rects']:
        shape = dict()
        shape['label'] = label
        point_1 = [rect['x'], rect['y']]
        point_2 = [rect['x'] + rect['w'], rect['y'] + rect['h']]
        shape['points'] = [point_1, point_2]
        shape['group_id'] = None
        shape['shape_type'] = 'rectangle'
        shape['flags'] = {}
        shapes.append(shape)

    label_file = LabelFile()
    label_file.save(
        filename=os.path.join(temp_path, json_name),
        shapes=shapes,
        imagePath=image_name,
        imageData=None,
        imageHeight=height,
        imageWidth=width,
    )
    shutil.copy(image_absolute_path, os.path.join(temp_path, image_name))

    return True


# 根据导出类型创建导出数据集
def generate_export_dataset(dataset_type, input_dir, output_dir, label_list):
    if (dataset_type == 'voc'):
        generate_voc_dataset(input_dir, output_dir, label_list)
    else:
        generate_coco_dataset(input_dir, output_dir, label_list)
    return