import os

import PIL.Image

from .collection import ImgElement, ImgCollection
from .operation import ImgInputOp


class InputLoader(ImgInputOp):
    def __init__(self, loader):
        super(InputLoader, self).__init__()
        self.loader = loader
        self.ex = None
        self.op_func = self.call_loader
        self.op_params = ()

    def call_loader(self):
        return self.loader.execute()


class InputFromDir(ImgInputOp):
    def __init__(self, *args, **kwargs):
        super(InputFromDir, self).__init__()
        self.ex = None
        self.op_func = self.load_from_dir
        self.op_params = (args, kwargs)

    def load_from_dir(self, input_dir, image_format):
        collection = ImgCollection()
        for imgfile in os.listdir(input_dir):
            if os.path.splitext(imgfile)[-1].lower() in image_format:
                imgpath = os.path.join(input_dir, imgfile)
                collection.append(ImgElement.fromFile(imgpath))
        return collection


"""
        if recursive:
            for dirpath, dirnames, filenames in os.walk(dir_root):
                for filename in filenames:
                    yield filename
        else:
"""
