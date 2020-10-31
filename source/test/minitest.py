from ..core.input import fromDir
from ..core.transform import resize

def test_load_data():
    dataset = fromDir("data/CCPD2019", image_format=".jpg")
    dataset = resize(width=1024, height=1024)(dataset)
    print(dataset.execute())

if __name__ == "__main__":
    test_load_data()
