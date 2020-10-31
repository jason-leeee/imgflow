import os
import PIL.Image


class ImgElement:
    def __init__(self, img, imgpath):
        # TODO: img auto convert to PIL/OpenCV format
        self.img = img
        self.imgpath = imgpath

    def __repr__(self):
        return self.imgpath

    def __str__(self):
        return self.imgpath


class ImgCollectionBase:
    def __init__(self):
        self.collection = []

    def summary(self):
        return f"{self.__class__.__name__} contains {self.__len__()} images"


class ImgCollection(ImgCollectionBase):
    def __init__(self):
        super(ImgCollection, self).__init__()
        self.collection = []

        # TODO: create a global config file for constants
        self.max_print_lines = 20   # FIXME: odd number will be rounded: 9 / 2 = 4

    def __repr__(self):
        return self.summary()

    def __str__(self):
        retstr = ""
        l = len(self.collection)
        if l <= self.max_print_lines:
            retstr += "".join([f"[{i}] {img}\n" for i, img in enumerate(self.collection)])
        elif self.max_print_lines > 0:
            h = self.max_print_lines // 2
            retstr += "".join([f"[{i}] {img}\n" for i, img in enumerate(self.collection[:h])])
            retstr += "......\n"
            retstr += "".join([f"[{l - h + i}] {img}\n" for i, img in enumerate(self.collection[-h:])])
        return retstr

    def __len__(self):
        return len(self.collection)

    def __getitem__(self, idx):
        return self.collection[idx]

    def __setitem__(self, idx, elem):
        self.collection[idx] = elem

    # TODO: implement __iter__ and __next__

    def append(self, elem):
        self.collection.append(elem)

    def clear(self):
        self.collection = []
