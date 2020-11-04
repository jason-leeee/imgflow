import os
import cv2

from .collection import ImgElement, ImgBBox
from .operation import OpOneToOne, OpOneToMany


RESIZE_INTERPOLATION = cv2.INTER_AREA


class ImgTransformResize(OpOneToOne):
    def process(self, imgelem, width, height):
        # TODO: new_imgelem
        print(imgelem)
        imgelem.img = cv2.resize(imgelem.img, (width, height), interpolation=RESIZE_INTERPOLATION)
    
Resize = ImgTransformResize


class ImgTransformSlice(OpOneToOne):
    def process(self, imgelem, vertical, coord):
        raise NotImplementedError


class ImgTransformSplitDataset(OpOneToMany):
    def initialized(self):
        self.process_all = True
        self.num_outputs = 3

    def process(self, collection):
        pass


class ImgTransformExtractBboxes(OpOneToOne):
    def process(self, imgelem: ImgElement):
        for i, bbox in enumerate(imgelem.bboxes):
            new_imgelem = ImgElement.fromArray(imgelem.img)
            xmin = int(bbox.xmin)
            ymin = int(bbox.ymin)
            xmax = int(bbox.xmax)
            ymax = int(bbox.ymax)
            new_imgelem.img = new_imgelem.img[ymin:ymax, xmin:xmax]
            oldfilename = os.path.splitext(os.path.basename(imgelem.imgpath))[0]
            new_imgelem.imgpath = "{}_bbox_{}.jpg".format(oldfilename, i)
            new_imgelem.label = bbox.label
            new_imgelem.bboxes = []
            yield new_imgelem


class ImgTransformSave(OpOneToOne):
    def __init__(self, output_dir, *args, **kwargs):
        super(ImgTransformSave, self).__init__(output_dir, *args, **kwargs)

        if not os.path.isdir(output_dir):
            os.makedirs(output_dir)

    def process(self, imgelem, output_dir):
        if not os.path.isdir(output_dir):
            os.makedirs(output_dir)

        filename = os.path.basename(imgelem.imgpath)
        filepath = os.path.join(output_dir, filename)
        cv2.imwrite(filepath, imgelem.img)

        yield imgelem
