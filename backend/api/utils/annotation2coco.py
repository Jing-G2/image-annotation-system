"""
    在labelme的源码基础上改动
"""

import collections
import datetime
import glob
import json
import os
import os.path as osp
import sys
import uuid

import imgviz
import numpy as np

try:
    import pycocotools.mask
except ImportError:
    print("Please install pycocotools:\n\n    pip install pycocotools\n")

from .label_file import LabelFile
from .image import img_data_to_arr, shape_to_mask


def generate_coco_dataset(input_dir,
                          output_dir,
                          label_list,
                          no_visualization=False):
    if not osp.exists(output_dir):
        os.makedirs(output_dir)
        os.makedirs(osp.join(output_dir, "JPEGImages"))
        os.makedirs(osp.join(output_dir, "Annotations"))
    if not no_visualization:
        os.makedirs(osp.join(output_dir, "Visualization"))
    """ 开始生成coco数据集 """
    now = datetime.datetime.now()
    data = dict(
        info=dict(
            description=None,
            url=None,
            version=None,
            year=now.year,
            contributor=None,
            date_created=now.strftime("%Y-%m-%d %H:%M:%S.%f"),
        ),
        licenses=[dict(
            url=None,
            id=0,
            name=None,
        )],
        images=[
            # license, url, file_name, height, width, date_captured, id
        ],
        type="instances",
        annotations=[
            # segmentation, area, iscrowd, image_id, bbox, category_id, id
        ],
        categories=[
            # supercategory, id, name
        ],
    )

    class_names = ["__ignore__", "_background_"]
    for class_name in label_list:
        if class_name == "__ignore__" or class_name == "_background_":
            continue
        class_names.append(class_name)

    class_name_to_id = {}
    for i, class_name in enumerate(class_names):
        class_id = i - 1  # starts with -1
        data["categories"].append(
            dict(
                supercategory=None,
                id=class_id,
                name=class_name,
            ))

    out_ann_file = osp.join(output_dir, "annotations.json")
    label_files = glob.glob(osp.join(input_dir, "*.json"))
    for image_id, filename in enumerate(label_files):
        # 生成标注数据文件
        # print("Generating dataset from:", filename)
        label_file = LabelFile(filename=filename)

        base = osp.splitext(osp.basename(filename))[0]
        out_img_file = osp.join(output_dir, "JPEGImages", base + ".jpg")

        img = img_data_to_arr(label_file.imageData)
        imgviz.io.imsave(out_img_file, img)
        data["images"].append(
            dict(
                license=0,
                url=None,
                file_name=osp.relpath(out_img_file, osp.dirname(out_ann_file)),
                height=img.shape[0],
                width=img.shape[1],
                date_captured=None,
                id=image_id,
            ))

        masks = {}  # for area
        bboxes = []
        labels = []
        segmentations = collections.defaultdict(list)  # for segmentation
        for shape in label_file.shapes:
            points = shape["points"]
            label = shape["label"]
            group_id = shape.get("group_id")
            shape_type = shape.get("shape_type", "polygon")
            mask = shape_to_mask(img.shape[:2], points, shape_type)

            if group_id is None:
                group_id = uuid.uuid1()

            instance = (label, group_id)

            if instance in masks:
                masks[instance] = masks[instance] | mask
            else:
                masks[instance] = mask

            if shape_type == "rectangle":
                (x1, y1), (x2, y2) = points
                x1, x2 = sorted([x1, x2])
                y1, y2 = sorted([y1, y2])
                points = [x1, y1, x2, y1, x2, y2, x1, y2]
                class_id = class_names.index(label)
                bboxes.append([y1, x1, y2, x2])
                labels.append(class_id)
            if shape_type == "circle":
                (x1, y1), (x2, y2) = points
                r = np.linalg.norm([x2 - x1, y2 - y1])
                n_points_circle = 12
                i = np.arange(n_points_circle)
                x = x1 + r * np.sin(2 * np.pi / n_points_circle * i)
                y = y1 + r * np.cos(2 * np.pi / n_points_circle * i)
                points = np.stack((x, y), axis=1).flatten().tolist()
            else:
                points = np.asarray(points).flatten().tolist()

            segmentations[instance].append(points)
        segmentations = dict(segmentations)

        if shape_type == "rectangle" and not no_visualization:
            captions = [class_names[label] for label in labels]
            viz = imgviz.instances2rgb(
                image=img,
                labels=labels,
                bboxes=bboxes,
                captions=captions,
                font_size=15,
            )
            out_viz_file = osp.join(output_dir, "Visualization", base + ".jpg")
            imgviz.io.imsave(out_viz_file, viz)

        for instance, mask in masks.items():
            cls_name, group_id = instance
            if cls_name not in class_name_to_id:
                continue
            cls_id = class_name_to_id[cls_name]

            mask = np.asfortranarray(mask.astype(np.uint8))
            mask = pycocotools.mask.encode(mask)
            area = float(pycocotools.mask.area(mask))
            bbox = pycocotools.mask.toBbox(mask).flatten().tolist()

            data["annotations"].append(
                dict(
                    id=len(data["annotations"]),
                    image_id=image_id,
                    category_id=cls_id,
                    segmentation=segmentations[instance],
                    area=area,
                    bbox=bbox,
                    iscrowd=0,
                ))

        if shape_type != "rectangle" and not no_visualization:
            viz = img
            if any(masks):
                labels, captions, masks = zip(
                    *[(class_name_to_id[cnm], cnm, msk)
                      for (cnm, gid), msk in masks.items()
                      if cnm in class_name_to_id])
                viz = imgviz.instances2rgb(
                    image=img,
                    labels=labels,
                    masks=masks,
                    captions=captions,
                    font_size=15,
                    line_width=2,
                )
            out_viz_file = osp.join(output_dir, "Visualization", base + ".jpg")
            imgviz.io.imsave(out_viz_file, viz)

    with open(out_ann_file, "w") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
    return
