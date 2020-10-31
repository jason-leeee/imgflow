import imgflow

dataset = imgflow.fromDir(
    input_dir="data/dataset", 
    dataset_format=imgflow.DATASET_LABELME,
    img_format=[imgflow.IMAGE_JPEG],
    label_loader=None,
    max_samples=None
)

dataset = imgflow.resize(width=1024, height=1024, padding=None, save_dir=None)(dataset)
subsets = imgflow.train_test_split(train_val_test_percent=(0.8, 0.1, 0.1))(dataset)

for subset in subsets:
    imgflow.convert(
        output_file="data/tfrecords/xxx.tfrecord",
        output_format=imgflow.CONVERT_TFRECORD
    )(subset).execute()
