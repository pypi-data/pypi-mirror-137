import pandas as pd
from inspec_ai._datasets.utils import _get_dataset_from_kaggle


def delhi_climate() -> pd.DataFrame:
    """Prepares a daily time series of the New Delhi weather, comprising 4 variables: meantemp,
    humidity, wind_speed, and meanpressure.

    The original datasets are hosted on kaggle. If they are not present in the .out folder, invokes the kaggle api to download them.
    You should ensure that your credentials are properly set, following the kaggle api doc: https://github.com/Kaggle/kaggle-api.

    Returns: A daily time series of the New Delhi weather

    """
    data_name = "daily-climate-time-series-data"

    _get_dataset_from_kaggle(data_name=data_name, is_competition=False, author="sumanthvrao")

    raw_train_df = pd.read_csv(f".out/{data_name}/DailyDelhiClimateTrain.csv")
    raw_test_df = pd.read_csv(f".out/{data_name}/DailyDelhiClimateTest.csv")

    df = raw_train_df.iloc[:-1, :].append(raw_test_df).reset_index(drop=True)  # The last row of the train df is also the first of the test df.

    df["date"] = pd.to_datetime(df["date"])

    return df
