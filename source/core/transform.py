import os
import cv2

from .operation import OpOneToOne


RESIZE_INTERPOLATION = cv2.INTER_AREA


class ImgTransformResize(OpOneToOne):
    def process(self, imgelem, width, height):
        print(imgelem)
        imgelem.img = cv2.resize(imgelem.img, (width, height), interpolation=RESIZE_INTERPOLATION)
    
Resize = ImgTransformResize


class ImgTransformSplit(OpOneToOne):
    def process(self, img, vertical, coord):
        raise NotImplementedError
