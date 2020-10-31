import os
import PIL.Image


class ImgElement:
    def __init__(self, img):
        # TODO: type auto convert
        self.img = img


class ImgCollectionBase:
    def __init__(self):
        self.collection = []

    def summary(self):
        print(f"Total: {len(self.collection)} images")


class ImgCollection(ImgCollectionBase):
    def __init__(self):
        super(ImgCollection, self).__init__()
        self.collection = []

    def __len__(self):
        return len(self.collection)

    def __getitem__(self, idx):
        return self.collection[idx]

    def __setitem__(self, idx, elem):
        self.collection[idx] = elem

    def append(self, elem):
        self.collection.append(elem)

    def clear(self):
        self.collection = []
