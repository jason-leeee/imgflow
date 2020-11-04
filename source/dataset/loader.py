import os

import pandas as pd
import xml.etree.ElementTree as ET

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


class CVATDatasetLoader(DatasetLoader):
    def __init__(self, *args, **kwargs):
        super(CVATDatasetLoader, self).__init__(*args, **kwargs)
        self.max_instances = 200

    def load(self, dataset_dir):
        xmlpath = os.path.join(dataset_dir, "labels.xml")
        data_dir = os.path.join(dataset_dir, "data")
        if not os.path.exists(xmlpath):
            raise ValueError("missing labels.xml in the dataset directory")
        if not os.path.isdir(data_dir):
            raise ValueError("missing data folder in the dataset directory")


        root = ET.parse(xmlpath).getroot()

        coll = ImgCollection()
        for image in root:
            if image.tag == "image":
                id = int(image.attrib["id"])
                imgname = image.attrib["name"]
                width = int(image.attrib["width"])
                height = int(image.attrib["height"])

                bboxes = []
                for box in image:
                    label = box.attrib["label"].lower()

                    x0 = float(box.attrib["xtl"])
                    y0 = float(box.attrib["ytl"])
                    x1 = float(box.attrib["xbr"])
                    y1 = float(box.attrib["ybr"])
                    bboxes.append((label, x0, y0, x1, y1))

                if len(bboxes) > self.max_instances:
                    print(f"skipping {imgname} with >{self.max_instances} bboxes")
                elif len(bboxes) == 0:
                    print(f"skipping empty image {imgname}")
                else:
                    imgpath = os.path.join(data_dir, imgname)
                    img = ImgElement.fromFile(imgpath)
                    # TODO: replace loop with a method
                    for bbox in bboxes:
                        img.add_bbox(x0, y0, x1, y1, label)
                    coll.append(img)

                # TODO: change it to max_samples argument
                #if len(coll) > 10:
                #    break

        return coll
