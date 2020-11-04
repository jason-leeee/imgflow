import os
import hashlib

import cv2
import tensorflow as tf

from .operation import OpOneToOne


class ImgConvertDetectionTFRecord(OpOneToOne):
    def initialized(self):
        self.process_all = True

    def process(self, collection, output_file, binary_class=True, all_classes=[]):
        tfwriter = tf.io.TFRecordWriter(output_file)
        i = 0
        for imgelem in collection:
            tfexample = self.create_example(i, imgelem, binary_class, all_classes)
            if tfexample:
                tfwriter.write(tfexample.SerializeToString())
                i += 1
            else:
                print("no bboxes")
            yield imgelem
        tfwriter.close()

    def create_example(self, id, imgelem, binary_class, all_classes):
        filename = imgelem.imgpath
        width = imgelem.width
        height = imgelem.height
        bboxes = imgelem.bboxes

        #img_raw = open(filename, "rb").read()
        img_raw = cv2.imencode(".jpg", imgelem.img)[1].tobytes()
        key = hashlib.sha256(img_raw).hexdigest()

        xmins = []
        ymins = []
        xmaxs = []
        ymaxs = []
        classes = []
        classes_text = []
        truncated = []
        views = []
        difficult_obj = []

        for bbox in bboxes:
            # category filter
            if all_classes and bbox.label not in all_classes:
                continue

            # dummy attributes
            views.append("Unspecified".encode("utf8"))
            truncated.append(0)
            difficult_obj.append(0)

            # bbox attributes
            xmins.append(bbox.xmin / float(width))
            xmaxs.append(bbox.xmax / float(width))
            ymins.append(bbox.ymin / float(height))
            ymaxs.append(bbox.ymax / float(height))

            if binary_class:
                classes.append(1)
                classes_text.append("obj".encode("utf8"))
            else:
                classes.append(all_classes.index(bbox.label) + 1)
                classes_text.append(bbox.label.encode("utf8"))

        # skip the images with no labels
        if len(classes) == 0:
            return None

        example = tf.train.Example(features=tf.train.Features(feature={
            "image/height": tf.train.Feature(int64_list=tf.train.Int64List(value=[height])),
            "image/width": tf.train.Feature(int64_list=tf.train.Int64List(value=[width])),
            "image/filename": tf.train.Feature(bytes_list=tf.train.BytesList(value=[filename.encode("utf8")])),
            "image/source_id": tf.train.Feature(bytes_list=tf.train.BytesList(value=[str(id).encode("utf8")])),
            "image/key/sha256": tf.train.Feature(bytes_list=tf.train.BytesList(value=[key.encode("utf8")])),
            "image/encoded": tf.train.Feature(bytes_list=tf.train.BytesList(value=[img_raw])),
            "image/format": tf.train.Feature(bytes_list=tf.train.BytesList(value=["jpg".encode("utf8")])),
            "image/object/bbox/xmin": tf.train.Feature(float_list=tf.train.FloatList(value=xmins)),
            "image/object/bbox/xmax": tf.train.Feature(float_list=tf.train.FloatList(value=xmaxs)),
            "image/object/bbox/ymin": tf.train.Feature(float_list=tf.train.FloatList(value=ymins)),
            "image/object/bbox/ymax": tf.train.Feature(float_list=tf.train.FloatList(value=ymaxs)),
            "image/object/class/text": tf.train.Feature(bytes_list=tf.train.BytesList(value=classes_text)),
            "image/object/class/label": tf.train.Feature(int64_list=tf.train.Int64List(value=classes)),
            "image/object/difficult": tf.train.Feature(int64_list=tf.train.Int64List(value=difficult_obj)),
            "image/object/truncated": tf.train.Feature(int64_list=tf.train.Int64List(value=truncated)),
            "image/object/view": tf.train.Feature(bytes_list=tf.train.BytesList(value=views)),
        }))
        return example
