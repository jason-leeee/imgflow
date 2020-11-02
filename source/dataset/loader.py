import os
import pandas as pd

from ..core.collection import ImgElement, ImgCollection


class DatasetLoader:
    def __init__(self, *args, **kwargs):
        self.params = (args, kwargs)
    
    def execute(self):
        return self.load(*self.params[0], **self.params[1])
    
    def load(self, *args, **kwargs):
        raise NotImplementedError


class ClassificationDatasetLoader(DatasetLoader):
    def load(self, csv_path, img_dir):
        df = pd.read_csv(csv_path)
        df = df[df.label.notnull()]
        
        imgpaths = [imgpath for imgpath in df.imgpath]
        labels = [label for label in df.label]

        coll = ImgCollection()
        for i, img_name in enumerate(os.listdir(img_dir)[:10]):
            img = ImgElement.fromFile(os.path.join(img_dir, img_name))
            img.label = labels[i]
            coll.append(img)
        return coll
