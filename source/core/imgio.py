import os

import PIL.Image

from .collection import ImgElement, ImgCollection
from .operation import ImgInputOp


class ImgIOBase(ImgInputOp):
    def __init__(self):
        super(ImgIOBase, self).__init__()


class ImgPlaceholder(ImgIOBase):
    def __init__(self):
        super(ImgPlaceholder, self).__init__()


class ImgLoadFromDir(ImgPlaceholder):
    def __init__(self, *args, **kwargs):
        super(ImgLoadFromDir, self).__init__()
        self.ex = None
        self.op_func = self.load_from_dir
        self.op_params = (args, kwargs)

    def load_from_dir(self, input_dir, image_format):
        collection = ImgCollection()
        for imgfile in os.listdir(input_dir):
            if os.path.splitext(imgfile)[-1].lower() in image_format:
                imgpath = os.path.join(input_dir, imgfile)
                img = ImgElement(PIL.Image.open(imgpath))
                collection.append(img)
        return collection

fromDir = ImgLoadFromDir

"""
        if recursive:
            for dirpath, dirnames, filenames in os.walk(dir_root):
                for filename in filenames:
                    yield filename
        else:
"""
