import pandas as pd
from inspec_ai._datasets.utils import _get_dataset_from_plain_url


def room_occupancy() -> pd.DataFrame:
    """Prepares an experimental time series dataset for room occupancy detection (binary classification).

    The original dataset is hosted on the UCI Machine Learning Repository. If it is not int the .out folder, downloads it.

    Returns: An experimental time series dataset for room occupancy detection

    """
    url = "https://archive.ics.uci.edu/ml/machine-learning-databases/00357/occupancy_data.zip"

    _get_dataset_from_plain_url(url, "occupancy_data")
    df = pd.read_csv(".out/occupancy_data/datatraining.txt")
    df["date"] = pd.to_datetime(df["date"])

    return df
