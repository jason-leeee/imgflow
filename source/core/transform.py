import os

import PIL.Image

from .operation import ImgTransformOp


class ImgTransformBase(ImgTransformOp):
    def __init__(self):
        super(ImgTransformBase, self).__init__()


class ImgTransformResize(ImgTransformBase):
    def __init__(self, *args, **kwargs):
        super(ImgTransformResize, self).__init__()
        self.op_func = self.resize
        self.op_params = (args, kwargs)

    def __call__(self, ex):
        self.op_ex = ex
        return self

    def resize(self, collection, width, height):
        #for img in collection:
        #    pass
        return collection
        

resize = ImgTransformResize
