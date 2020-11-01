import os

import PIL.Image

from .operation import ImgTransformOp


class ImgTransformBase(ImgTransformOp):
    def __init__(self):
        super(ImgTransformBase, self).__init__()


class ImgTransformResize(ImgTransformBase):
    def __init__(self, *args, **kwargs):
        super(ImgTransformResize, self).__init__()
        self.op_func = self.process
        self.op_params = (args, kwargs)

    def process(self, collection, width, height):
        # TODO: visitor pattern?
        for img in collection:
            print(img)
        return collection
        

resize = ImgTransformResize
