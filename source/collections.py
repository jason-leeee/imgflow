import os
import PIL.Image


class ImgElement:
    def __init__(self, **kwargs):
        self.data = dict(kwargs)


class ImgCollectionBase:
    def __init__(self):
        self.collection = []

    def summary(self):
        print(f"Total: {len(self.collection)} images")


class ImgCollection(ImgCollectionBase):
    def __init__(self):
        super(ImgCollection, self).__init__()

    def __len__(self):
        return len(self.collection)

    def clear(self):
        self.collection = []

    def from_directory(self, dir_root, exts=[".jpg"], recursive=True):

        def dir_iterator(dir_root, exts, recursive):
            imgpaths = []
            if recursive:
                for dirpath, dirnames, filenames in os.walk(dir_root):
                    for filename in filenames:
                        yield filename
            else:
                for filename in os.listdir(dir_root):
                    if os.path.splitext(filename.lower())[-1] in exts:
                        yield filename

        for imgpath in dir_iterator(dir_root, exts, recursive):
            img = PIL.Image.open(imgpath)
            self.collection.append(ImgElement(img=img, path=imgpath))

