"""
Lahman baseball datasets module.
"""
import os
import tempfile
from typing import Optional, Tuple, List
from zipfile import ZipFile
from glob import glob

import pandas as pd
import requests
from tqdm import tqdm


class LahmanDatasets:
    """
    This class downloads the Lahman CSV files containing baseball statistics
    and loads them into Pandas datasets. About 43 MB of data will be downloaded.
    """

    def __init__(self):
        self.__url = "https://github.com/chadwickbureau/baseballdatabank/archive/master.zip"
        self.__target_filename = os.path.join(tempfile.gettempdir(), "master.zip")
        self.__extract_folder = os.path.join(tempfile.gettempdir(), "lahman_csv")
        self.__zip_file: Optional[ZipFile] = None
        self.__dataframes_lookup: List[Tuple[str, pd.DataFrame]] = []

    def __getitem__(self, item):
        dfs = [tup[1] for tup in self.__dataframes_lookup if tup[0] == item]

        if len(dfs) == 1:
            return dfs[0]

        return None

    @property
    def dataframe_names(self):
        """
        Returns the list of data frame names. Each data frame corresponds
        to a CSV file in the Lahman database.
        :return: The list of data frame names.
        """
        return [tup[0] for tup in self.__dataframes_lookup]

    def load(self) -> None:
        """
        Loads the Lahman baseball datasets.
        """
        self.__download(self.__target_filename)
        self.__extract_zip_files()
        self.__create_datasets()

    def __download(self, target_filename: str) -> None:
        result = requests.get(self.__url, stream=True)

        with open(target_filename, "wb") as file:
            for chunk in tqdm(result.iter_content(chunk_size=1000000)):
                tqdm.write(f"{self.__url} => Downloading chunk...")
                file.write(chunk)

        # pylint: disable=consider-using-with
        self.__zip_file = ZipFile(target_filename, "r")

    def __extract_zip_files(self):
        if not os.path.exists(self.__extract_folder):
            os.makedirs(self.__extract_folder)

        self.__zip_file.extractall(self.__extract_folder)

    def __create_datasets(self):
        csv_files = glob(os.path.join(
            self.__extract_folder,
            "baseballdatabank-master",
            "core",
            "*.csv"))

        for file in csv_files:
            data_frame = pd.read_csv(file)
            df_name = os.path.splitext(file)[0].split("\\")[-1]
            self.__dataframes_lookup.append((df_name, data_frame))
