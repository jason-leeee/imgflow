# ImgFlow

## Description

A handy image preprocessing pipeline.

## Mock-up

```python
import imgflow

dataset = imgflow.fromDir(
    input_dir="data/object-detection-dataset", 
    dataset_format=imgflow.DATASET_COCO,
    img_format=imgflow.IMAGE_JPEG
)

dataset = imgflow.resize(width=1024, height=1024)(dataset)
subsets = imgflow.train_test_split(train_val_test_percent=(0.8, 0.1, 0.1))(dataset)

for subset in subsets:
    imgflow.convert(
        output_file="data/tfrecords/xxx.tfrecord",
        output_format=imgflow.CONVERT_TFRECORD
    )(subset).execute()
```

## Features

### Core

- [ ] DAG based lazy or eager execution.
    
- [ ] Convert ImgFlow into Cloud Dataflow and run in parallel.

- [ ] Cache on local storage.

- [ ] Global config.py.

### Data loading
    
- [ ] Multiple data source, e.g. local directory, cloud storage bucket.

- [ ] Classic object detection dataset format, e.g. MS COCO, PASCAL VOC.

- [ ] Custom dataset parser and loader.

### Collection
- [ ] Attach shapes to images, e.g. bboxes.
- [ ] Attach extra info to images, e.g. labels.

### Functionality
- [ ] Basic stat anaylsis.
- [ ] Basic preprocessing, e.g. resize, pad, grayscale, RGB/BGR.
- [ ] Basic augmentations.
- [ ] Visualize bboxes, labels, etc.

### Storage
- [ ] Save all intermediate results for manual validation.
- [ ] Export the processed dataset to JSON, MS COCO, PASCAL VOC, TFRecord format.

### Model deployment

- [ ] Serialize/deserialize the pipeline.
- [ ] Model inference operation.
- [ ] Flask API integration.
- [ ] Dockerization.

### Intelligence
- [ ] Smart dataset loading, automatically detect the directory hierarchy.
