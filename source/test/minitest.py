from ..core.imgio import fromDir

def test_load_data():
    dataset = fromDir("data/CCPD2019", image_format=".jpg").execute()
    dataset.summary()
    print(dataset)

if __name__ == "__main__":
    test_load_data()
