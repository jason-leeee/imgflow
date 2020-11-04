import os
import cv2

from .collection import ImgElement, ImgBBox
from .operation import OpOneToOne, OpOneToMany


RESIZE_INTERPOLATION = cv2.INTER_AREA


class ImgTransformResize(OpOneToOne):
    def process(self, imgelem, width, height):
        # TODO: new_imgelem
        print(imgelem)
        imgelem.img = cv2.resize(imgelem.img, (width, height), interpolation=RESIZE_INTERPOLATION)
    
Resize = ImgTransformResize


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
    def process(self, imgelem: ImgElement):
        for bbox in imgelem.bboxes:
            new_imgelem = ImgElement.fromArray(imgelem.img)
            xmin = int(bbox.xmin)
            ymin = int(bbox.ymin)
            xmax = int(bbox.xmax)
            ymax = int(bbox.ymax)
            new_imgelem.img = new_imgelem.img[ymin:ymax, xmin:xmax]
            new_imgelem.label = bbox.label
            new_imgelem.bboxes = []
            yield new_imgelem
