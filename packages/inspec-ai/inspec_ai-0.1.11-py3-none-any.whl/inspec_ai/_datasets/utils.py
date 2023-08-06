import os
import urllib.request
import warnings
import zipfile
from pathlib import Path


def _get_dataset_from_kaggle(data_name: str, is_competition: bool, author: str = ""):
    """Download Kaggle dataset if it is not in .out.

    If you are unsure how to fill the arguments of the function, you find the information in the pre-made Kaggle api
    command that should be accessible from the dataset's page on Kaggle.

    Args:
        data_name: Name of the dataset (or competition)
        is_competition: The kaggle API command is not the same if the dataset comes from a competition, so there is a need to specify it here.
        author: If it is not a competition, you need to provide the dataset's author username.

    """
    if not author and not is_competition:
        raise ValueError("You need to provide the author if the dataset is not from a competition.")

    if os.path.isdir(f".out/{data_name}"):
        return

    if is_competition:
        api_command = f"competitions download -c {data_name}"
    else:
        api_command = f"datasets download -d {author}/{data_name}"

    os.system("kaggle " + api_command)

    with zipfile.ZipFile(f"{data_name}.zip", "r") as zip_reader:
        zip_reader.extractall(f".out/{data_name}")

    os.remove(f"{data_name}.zip")

    warnings.warn(
        "The requested dataset is downloaded from kaggle, so you need to set your credentials following the kaggle api doc: "
        + "https://github.com/Kaggle/kaggle-api."
    )


def _get_dataset_from_plain_url(url: str, data_name: str):
    extension = "." + url.split(".")[-1]
    destination_directory = Path(".out") / data_name
    file_path = destination_directory / (data_name + extension)

    if os.path.isdir(destination_directory):
        return

    os.makedirs(destination_directory)

    with urllib.request.urlopen(url) as http_get, open(file_path, "wb") as file_writer:
        response = http_get.read()
        file_writer.write(response)

    if extension == ".zip":
        with zipfile.ZipFile(file_path, "r") as zip_reader:
            zip_reader.extractall(destination_directory)

        os.remove(file_path)
