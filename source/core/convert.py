import os
import cv2

from .operation import OpOneToOne


RESIZE_INTERPOLATION = cv2.INTER_AREA


class ImgConvertDetectionTFRecord(OpOneToOne):
    def process(self, img, width, height):
        print(img)
        img.img = cv2.resize(img.img, (width, height), interpolation=RESIZE_INTERPOLATION)
    
Resize = ImgTransformResize


class ImgTransformSplit(OpOneToOne):
    def process(self, img, vertical, coord):
        raise NotImplementedError
