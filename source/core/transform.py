import os

import PIL.Image

from .operation import ImgTransformOp


class ImgTransformBase(ImgTransformOp):
    def __init__(self):
        super(ImgTransformBase, self).__init__()


class ImgTransformResize(ImgTransformBase):
    def __init__(self):
        super(ImgTransformResize, self).__init__()
