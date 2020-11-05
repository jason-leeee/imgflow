import os
import copy

import cv2

from .collection import ImgElement, ImgBBox
from .operation import OpOneToOne, OpOneToMany


RESIZE_INTERPOLATION = cv2.INTER_AREA


class ImgTransformResize(OpOneToOne):
    def process(self, imgelem, width, height):
        new_imgelem = copy.deepcopy(imgelem)
        new_imgelem.img = cv2.resize(new_imgelem.img, (width, height), interpolation=RESIZE_INTERPOLATION)
        yield new_imgelem


class ImgTransformScale(OpOneToOne):
    def process(self, imgelem, width, height):
        width_src = imgelem.width
        height_src = imgelem.height

        scale = min(width / width_src, height / height_src)

        width_new = int(width_src * scale)
        height_new = int(height_src * scale)

        new_imgelem = copy.deepcopy(imgelem)
        new_imgelem.img = cv2.resize(new_imgelem.img, (width_new, height_new), interpolation=cv2.INTER_LINEAR)
        yield new_imgelem
        
        #TODO: padding


class ImgTransformSlice(OpOneToOne):
    def process(self, imgelem, vertical, coord):
        raise NotImplementedError


class ImgTransformSplitDataset(OpOneToMany):
    def initialized(self):
        self.process_all = True
        self.num_outputs = 3

    def process(self, collection):
        pass


class ImgTransformExtractBboxes(OpOneToOne):
    def process(self, imgelem):
        for i, bbox in enumerate(imgelem.bboxes):
            new_imgelem = ImgElement.fromArray(imgelem.img)
            xmin = int(bbox.xmin)
            ymin = int(bbox.ymin)
            xmax = int(bbox.xmax)
            ymax = int(bbox.ymax)
            new_imgelem.img = new_imgelem.img[ymin:ymax, xmin:xmax]
            oldfilename = os.path.splitext(os.path.basename(imgelem.imgpath))[0]
            new_imgelem.imgpath = "{}_bbox_{}.jpg".format(oldfilename, i)
            new_imgelem.label = bbox.label
            new_imgelem.bboxes = []
            yield new_imgelem


class ImgTransformSave(OpOneToOne):
    def __init__(self, output_dir, *args, **kwargs):
        super(ImgTransformSave, self).__init__(output_dir, *args, **kwargs)

        if not os.path.isdir(output_dir):
            os.makedirs(output_dir)

    def process(self, imgelem, output_dir):
        if not os.path.isdir(output_dir):
            os.makedirs(output_dir)

        filename = os.path.basename(imgelem.imgpath)
        filepath = os.path.join(output_dir, filename)
        img = cv2.cvtColor(imgelem.img, cv2.COLOR_RGB2BGR)
        cv2.imwrite(filepath, img)

        yield imgelem
