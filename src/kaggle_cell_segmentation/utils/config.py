import yaml
import os
from kaggle_cell_segmentation.utils.custom_logger import *
import datetime


def get_root_path() -> str:
    """
    This function returns the root directory absolute path dynamically depending on the current working directory
    which is usually either src OR test.
    Args:
        work_dir (str): Current working source directory

    Returns (str): Project root absolute path.

    """
    work_dir = "src" if "src" in os.getcwd() else "test"
    return os.getcwd().split(work_dir)[0]


config_logger = CustomLogger.construct_logger(name="CONFIG",
                                              log_file_path=get_root_path() + "logs/CONFIG.log",
                                              logger_level=20)


def read_yaml(*, root_path: str, config_path: str = "properties/dev.yaml") -> Union[dict, None]:
    """
    This function reads a yaml file based on a given root_path and CONFIG file path.
    Args:
        root_path (str): Absolute root path of the project.
        config_path (str): Relative path of CONFIG file location.

    Returns (str): Dictionary with CONFIG key / value pairs.

    """
    try:
        with open(root_path + config_path, mode="r") as stream:
            try:
                return yaml.safe_load(stream=stream)
            except yaml.YAMLError as e:
                config_logger.log_info(message=f"At {datetime.datetime.now()} error {e} occurred.")

    except FileNotFoundError as e:
        config_logger.log_info(message=f"At {datetime.datetime.now()} error {e} occurred.")
