import pandas as pd
from inspec_ai._datasets.utils import _get_dataset_from_kaggle


def covid_variants() -> pd.DataFrame:
    """Prepares a hierarchical grouped time series of the share of covid cases by variant in different countries.

    The original dataset is hosted - *and often updated* - on kaggle. If they are not present in the .out folder, invokes the kaggle api to download them.
    You should ensure that your credentials are properly set, following the kaggle api doc: https://github.com/Kaggle/kaggle-api.

    Returns: A hierarchical grouped time series of the share of covid cases by variant

    """
    data_name = "omicron-covid19-variant-daily-cases"
    _get_dataset_from_kaggle(data_name=data_name, is_competition=False, author="yamqwe")

    df = pd.read_csv(f".out/{data_name}/covid-variants.csv")

    df.drop(columns=["num_sequences", "num_sequences_total"], inplace=True)

    df.rename(
        columns={"location": "country", "perc_sequences": "share_of_cases"},
        inplace=True,
    )

    df["date"] = pd.to_datetime(df["date"])

    return df
