import torch
import torchvision.transforms
from torchvision import transforms
from kaggle_cell_segmentation.utils.config import get_root_path, read_yaml
from kaggle_cell_segmentation.utils.custom_logger import CustomLogger
from matplotlib import pyplot as plt
import os
import pandas as pd
import cv2.cv2 as cv2
import numpy as np
from PIL import Image

PREPROCESSOR = transforms.Compose([
    transforms.ToTensor(),
    # transforms.Normalize([0.5018, 0.5018, 0.5018], [0.0541, 0.0532, 0.0539]),
])
CONFIG = read_yaml(root_path=get_root_path())
importer_logger = CustomLogger.construct_logger(name="importer",
                                                log_file_path=get_root_path() + "logs/importer.log",
                                                logger_level=20
                                                )


def csv_meta_data_loader() -> pd.DataFrame:
    csv_path = CONFIG["data_absolute_path"] + CONFIG["train_meta_data_path"]
    try:
        return pd.read_csv(filepath_or_buffer=csv_path)
    except FileNotFoundError:
        importer_logger.log_info(message=f"CSV file at path: {csv_path} does not exist, check the config file.")


df = csv_meta_data_loader()


def read_images_with_pil(*, id_list: list, image_format: str = ".png") -> torch.Tensor:
    return torch.stack([
        PREPROCESSOR(
            Image.open(CONFIG["data_absolute_path"] + CONFIG["train_image_data_path"] + image_id + image_format))
        for image_id in id_list
    ])


def read_images_with_cv2(id_list: list, image_format: str = ".png"):
    return torch.stack([
        PREPROCESSOR(
            cv2.imread(CONFIG["data_absolute_path"] + CONFIG["train_image_data_path"] + image_id + image_format))
        for image_id in id_list
    ])


def rle_annotation_decoder(rle_encoding: list, shape: tuple) -> np.ndarray:
    """
    This function decodes an rle encoded annotation and then returns a instance segmentation MASK.
    Args:
        rle_encoding: List of numbers ( start index position, frequency, start index position, frequency etc..)
        shape: Tuple object that holds the values HEIGHT AND WIDTH (in this order).

    Returns: Masked numpy array

    """
    annotation_mask = np.zeros(shape=shape[0] * shape[1], dtype=np.uint8)
    starts, lengths = [np.asarray(x, dtype=int) for x in (rle_encoding[0:][::2], rle_encoding[1:][::2])]
    ends = starts + lengths - 1
    for start, end in zip(starts, ends):
        annotation_mask[start:end] = 1
    return annotation_mask.reshape(shape)



id_0 = df["id"][0]
masked_df = df[df["id"] == id_0]
masks = masked_df["annotation"]
print(masks.shape)
masked_cell = np.stack([rle_annotation_decoder(rle_encoding=mask.split(), shape=(520, 704)) for mask in masks])
masked_cell = np.any(masked_cell == 1, axis=0)

plt.imshow(masked_cell)
plt.show()
