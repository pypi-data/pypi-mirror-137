import pandas as pd

from inspec_ai._datasets.utils import _get_dataset_from_kaggle


def food_sales() -> pd.DataFrame:
    """Prepares a grouped time series of food sales, comprising 1437 food items over about 5 years and a half.

    The data is an extract from the m5 forecasting competition, hosted on kaggle. If the original datasets
    are not present in the .out folder, invokes the kaggle api to download them. You should ensure that
    your credentials are properly set, following the kaggle api doc: https://github.com/Kaggle/kaggle-api.

    Returns: A grouped time series of food sales, comprising 1437 food items over about 5 years and a half.

    """
    _get_dataset_from_kaggle(data_name="m5-forecasting-accuracy", is_competition=True)

    raw_sales_df = pd.read_csv(".out/m5-forecasting-accuracy/sales_train_evaluation.csv")
    calendar_df = pd.read_csv(".out/m5-forecasting-accuracy/calendar.csv")

    temp_sales_df = _clean_m5_forecasting_accuracy_food(raw_sales_df)
    clean_df = _replace_day_indicator_with_calendar_date(temp_sales_df, calendar_df).rename(columns={"item_id": "product", "dept_id": "department"})

    return clean_df


def _clean_m5_forecasting_accuracy_food(raw_df):
    sliced_df = raw_df.loc[(raw_df["store_id"] == "CA_1") & (raw_df["cat_id"] == "FOODS"), :].drop(columns=["store_id", "state_id", "cat_id", "id"])

    number_of_days = len(sliced_df.columns[sliced_df.columns.str[:2] == "d_"])

    # The next few lines reshape the df from wide to long
    date_slices_to_concat = []

    for i in range(1, number_of_days + 1):  # TODO: Optimize this, it's like 1950 iterations long
        date_slice = sliced_df.loc[:, ["item_id", "dept_id", f"d_{i}"]]
        date_slice.rename(columns={f"d_{i}": "sales"}, inplace=True)
        date_slice["d"] = f"d_{i}"
        date_slices_to_concat.append(date_slice)

    clean_df = pd.concat(date_slices_to_concat, axis=0)

    return clean_df


def _replace_day_indicator_with_calendar_date(clean_df, calendar_df):
    merged_df = pd.merge(left=clean_df, right=calendar_df[["date", "d"]], on="d", how="left")
    merged_df["date"] = pd.to_datetime(merged_df["date"])
    merged_df.drop(columns="d", inplace=True)

    return merged_df
