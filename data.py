"""Load the most recent data export and filter to a cube type."""

import json
from datetime import datetime
from glob import glob

import pandas as pd


def load(cube_type="333"):
    """Load the most recent data export and filter to a cube type."""

    # Find the most recent data export in the data directory.
    files = glob("data/cubedesk_data_*.txt")

    # The filenames have the format `cubedesk_data_DD_MM_YYYY_HH_MM_SS.txt`.
    def key(file: str):
        return datetime.strptime(
            file.replace("data/cubedesk_data_", "").replace(".txt", ""),
            "%d_%m_%Y_%H_%M_%S",
        )

    files = sorted(files, key=key, reverse=True)

    with open(files[0], encoding="utf-8") as data:
        df = pd.DataFrame.from_dict(json.load(data)["solves"])

        # Filter to a cube type.
        df = df[df["cube_type"] == cube_type]

        df = df[["started_at", "time"]]

        df = df.sort_values(by="started_at")

        return df


def remove_outliers(series: pd.Series):
    """
    Remove outliers from a series:

    - If the series has less than 3 elements, don't remove any elements.
    - If the series has 5 elements, remove the first and last element.
    - Otherwise, remove 5% of the elements from the start and end of the series.
    """

    if len(series) < 3:
        return series

    if len(series) == 5:
        row = 1

    else:
        row = int(len(series) * (5 / 100))

    if row == 0:
        return series

    return series.sort_values().iloc[row:-row].copy()
