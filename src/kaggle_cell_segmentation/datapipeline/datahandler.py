from kaggle_cell_segmentation.utils.config import get_root_path, read_yaml

config = read_yaml(root_path=get_root_path())
print(config)
