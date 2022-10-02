import csv
import os


class Split:
    def __init__(
        self,
        csv_file: str,
        train_ratio: float,
        validate_ratio: float = None,
        shuffle=False,
        ignore_header=True,
    ) -> None:
        if train_ratio < 0 or train_ratio > 1:
            raise ValueError("Train ratio should be between 0 and 1")
        if validate_ratio is not None and (validate_ratio < 0 or validate_ratio > 1):
            raise ValueError("Validate ratio should be between 0 and 1")

        self.csv = csv_file
        self.train_ratio = train_ratio
        self.csv_header = None
        self.validate_ratio = (
            1 - train_ratio if validate_ratio is None else validate_ratio
        )
        if self.validate_ratio + self.train_ratio > 1:
            raise ValueError("Train and validate ratio should be less than 1")

        self.test_ratio = (
            1 - train_ratio - validate_ratio if validate_ratio is not None else None
        )

        self.csv_data = []

        with open(self.csv, mode="r",  encoding="utf-8") as file:
            csvFile = csv.reader(file)
            self.csv_data = [lines for lines in csvFile]
            if ignore_header:
                self.csv_header = self.csv_data[0]
                self.csv_data = self.csv_data[1:]

        if shuffle:
            import random

            random.shuffle(self.csv_data)

        train_half = int(len(self.csv_data) * self.train_ratio)
        self.train_set = self.csv_data[:train_half]

        other_set = self.csv_data[train_half:]
        if self.test_ratio is not None:
            validate_half = int(len(self.csv_data) * self.validate_ratio)
            self.validate_set = other_set[:validate_half]
            self.test_set = other_set[validate_half:]
        else:
            self.validate_set = other_set
            self.test_set = []

    def _csv_write(
        self, csv_data: list, type: str, path: str = None, postfix: str = None
    ) -> None:
        filename = type
        if postfix is not None:
            filename += "_" + postfix
        filename += ".csv"
        _path = filename
        if path is not None:
            _path = os.path.join(path, filename)

        with open(_path, "w",  encoding="utf-8") as csvfile:
            filewriter = csv.writer(
                csvfile, delimiter=",", quotechar="|", quoting=csv.QUOTE_MINIMAL
            )
            if self.csv_header is not None:
                filewriter.writerow(self.csv_header)
            filewriter.writerows(csv_data)
            print("Saved {} set to {}".format(type, _path))

    def csv_write(self, path=None, postfix=None):
        if len(self.train_set):
            self._csv_write(self.train_set, "train", path, postfix)
        if len(self.validate_set):
            self._csv_write(self.validate_set, "validate", path, postfix)
        if len(self.test_set):
            self._csv_write(self.test_set, "test", path, postfix)
