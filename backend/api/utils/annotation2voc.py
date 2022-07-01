"""
    在labelme的源码基础上改动
"""

import argparse
import glob
import os
import os.path as osp
import sys

import imgviz

try:
    import lxml.builder
    import lxml.etree
except ImportError:
    print("Please install lxml:\n\n    pip install lxml\n")

from .label_file import LabelFile
from .image import img_data_to_arr


def generate_voc_dataset(input_dir,
                         output_dir,
                         label_list,
                         no_visualization=False):
    """
        @params input_dir和output_dir都是绝对路径
        @params label_file 包含所有标签的txt文件
    """

    if not osp.exists(output_dir):
        os.makedirs(output_dir)
        os.makedirs(osp.join(output_dir, "JPEGImages"))
        os.makedirs(osp.join(output_dir, "Annotations"))
    if not no_visualization:
        os.makedirs(osp.join(output_dir, "AnnotationsVisualization"))
    """ 开始生成voc数据集 """
    # 生成标签文件
    class_names = ["__ignore__", "_background_"]
    class_name_to_id = {}
    for class_name in label_list:
        if class_name == "__ignore__" or class_name == "_background_":
            continue
        class_names.append(class_name)
    class_names = tuple(class_names)
    # print("class_names:", class_names)
    out_class_names_file = osp.join(output_dir, "class_names.txt")
    with open(out_class_names_file, "w") as f:
        f.writelines("\n".join(class_names))
    # print("Saved class_names:", out_class_names_file)

    for filename in glob.glob(osp.join(input_dir, "*.json")):
        # print("Generating dataset from:", filename)
        label_file = LabelFile(filename=filename)

        base = osp.splitext(osp.basename(filename))[0]
        out_img_file = osp.join(output_dir, "JPEGImages", base + ".jpg")
        out_xml_file = osp.join(output_dir, "Annotations", base + ".xml")
        if not no_visualization:
            out_viz_file = osp.join(output_dir, "AnnotationsVisualization",
                                    base + ".jpg")

        img = img_data_to_arr(label_file.imageData)
        imgviz.io.imsave(out_img_file, img)

        maker = lxml.builder.ElementMaker()
        xml = maker.annotation(
            maker.folder(),
            maker.filename(base + ".jpg"),
            maker.database(),  # e.g., The VOC2007 Database
            maker.annotation(),  # e.g., Pascal VOC2007
            maker.image(),  # e.g., flickr
            maker.size(
                maker.height(str(img.shape[0])),
                maker.width(str(img.shape[1])),
                maker.depth(str(img.shape[2])),
            ),
            maker.segmented(),
        )

        bboxes = []
        labels = []
        for shape in label_file.shapes:
            if shape["shape_type"] != "rectangle":
                print("Skipping shape: label={label}, "
                      "shape_type={shape_type}".format(**shape))
                continue

            class_name = shape["label"]
            class_id = class_names.index(class_name)

            (xmin, ymin), (xmax, ymax) = shape["points"]
            # swap if min is larger than max.
            xmin, xmax = sorted([xmin, xmax])
            ymin, ymax = sorted([ymin, ymax])

            bboxes.append([ymin, xmin, ymax, xmax])
            labels.append(class_id)

            xml.append(
                maker.object(
                    maker.name(shape["label"]),
                    maker.pose(),
                    maker.truncated(),
                    maker.difficult(),
                    maker.bndbox(
                        maker.xmin(str(xmin)),
                        maker.ymin(str(ymin)),
                        maker.xmax(str(xmax)),
                        maker.ymax(str(ymax)),
                    ),
                ))

        if not no_visualization:
            captions = [class_names[label] for label in labels]
            viz = imgviz.instances2rgb(
                image=img,
                labels=labels,
                bboxes=bboxes,
                captions=captions,
                font_size=15,
            )
            imgviz.io.imsave(out_viz_file, viz)

        with open(out_xml_file, "wb") as f:
            f.write(lxml.etree.tostring(xml, pretty_print=True))

    return True