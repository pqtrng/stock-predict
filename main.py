import os.path

import yfinance as yf
import pandas as pd
from feature import generate_feature, normalize_data
DATA_PATH = "data.csv"

START_DATE = "1990-01-01"
END_DATE = "2023-06-30"

def get_data(start_date:str, end_date:str):
    try:
        ticker = yf.Ticker("^IXIC")
        data = ticker.history(start=start_date, end=end_date)
        data.to_csv(f"{start_date}_{end_date}_{DATA_PATH}")
    except Exception as e:
        print("Error downloading data:", e)

if __name__ == "__main__":
    file_name = f"{START_DATE}_{END_DATE}_{DATA_PATH}"
    if not os.path.exists(file_name):
        print("Data file not found. Downloading data ...")
        get_data(START_DATE, END_DATE)
    else:
        print("Data file found. Skipping download.")

    raw_data = pd.read_csv(file_name, index_col='Date')
    data = generate_feature(raw_data)

    start_train = START_DATE
    end_train = "2022-12-31"
    start_test = "2023-01-01"
    end_test = END_DATE

    data_train = data.loc[start_train:end_train]
    X_train = data_train.drop('close', axis=1).values
    y_train = data_train['close'].values
    print(X_train.shape)
    print(y_train.shape)

    data_test = data.loc[start_test:end_test]
    X_test = data_test.drop('close', axis=1).values
    y_test = data_test['close'].values
    print(X_test.shape)

    X_scaled_train = normalize_data(X_train)
    X_scaled_test = normalize_data(X_test)