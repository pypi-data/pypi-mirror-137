import os
from collections import namedtuple
from pathlib import Path
from tempfile import NamedTemporaryFile
from urllib.parse import urlsplit, urlunsplit

import numpy as np
import pandas as pd
import sklearn.datasets as skdata
from google.cloud import storage
from google.cloud.exceptions import NotFound
from torch.utils.data import Dataset

TrainValTest = namedtuple("TrainValTest", ["trainset", "valset", "testset"])


def build_url(scheme, netloc, path):
    return urlunsplit((scheme, netloc, str(path), "", ""))


class DataNotFoundError(Exception):
    def __init__(self, path):
        super().__init__(f"Data not found at {path}")
        self.path = path

    def __repr__(self):
        return f"Data not found at {self.path}"


class BinDataset(Dataset):
    def __init__(self, X, Y):
        super().__init__()
        if X.shape[0] != Y.shape[0]:
            raise ValueError("X and Y must have the same number of samples.")
        self._X = X
        self._Y = Y

    def __getitem__(self, idx):
        return (self._X[idx], self._Y[idx])

    def __len__(self):
        return self._X.shape[0]

    @classmethod
    def generate(
        cls,
        n_samples,
        train_split=0.7,
        val_split=0.2,
        test_split=0.1,
        n_features=20,
        n_informative=10,
        n_redundant=7,
        n_repeated=3,
        flip_y=0.05,  # larger values will make classification hard
        class_sep=0.5,  # larger values will make classification easy
        random_state=10,
    ):
        X, Y = skdata.make_classification(
            n_samples=n_samples,
            n_features=n_features,
            n_informative=n_informative,
            n_redundant=n_redundant,
            n_repeated=n_repeated,
            n_classes=2,
            flip_y=flip_y,
            class_sep=class_sep,
            random_state=random_state,
        )
        X = X.astype(np.float32)
        Y = Y.astype(np.int8)

        splits = (train_split, val_split, test_split)
        test_size = np.floor(n_samples * (splits[2] / sum(splits))).astype(np.int)
        val_size = np.floor(n_samples * (splits[1] / sum(splits))).astype(np.int)
        train_size = n_samples - val_size - test_size

        if test_size:
            test_slice = slice(0, test_size)
            testset = cls(X[test_slice], Y[test_slice])
        else:
            testset = None

        if val_size:
            val_slice = slice(test_size, test_size + val_size)
            valset = cls(X[val_slice], Y[val_slice])
        else:
            valset = None

        if train_size:
            train_slice = slice(test_size + val_size, n_samples)
            trainset = cls(X[train_slice], Y[train_slice])
        else:
            trainset = None

        return TrainValTest(trainset=trainset, valset=valset, testset=testset)

    @classmethod
    def _load(cls, dataroot, filenames):
        datasets = []

        # dataroot is in the form scheme://netloc/path (path includes the leading /)
        flds = urlsplit(dataroot)
        if flds.scheme == "file":
            # file:///path/to/directory
            # ignore netloc
            for filename in filenames:
                path = Path(flds.path) / filename
                try:
                    dataset = cls._tensorify(path)
                    datasets.append(dataset)
                except FileNotFoundError:
                    raise DataNotFoundError(path)
        elif flds.scheme == "gs":
            # gs://bucket/prefix
            bucket = flds.netloc
            prefix = Path(flds.path).relative_to("/")  # get rid of the leading /
            for filename in filenames:
                blobname = str(prefix / filename)
                try:
                    dataset = cls._load_from_gcp(bucket, blobname)
                    datasets.append(dataset)
                except NotFound:
                    raise DataNotFoundError(f"gs://{bucket}/{blobname}")
        else:
            raise ValueError(
                f"Unsupported scheme {flds.scheme}! Use either file:// or gcp://."
            )

        return datasets

    @classmethod
    def load_train_val_single(cls, dataroot):
        return cls._load(dataroot, ["train.csv", "val.csv"])

    @classmethod
    def load_test_single(cls, dataroot):
        return cls._load(dataroot, ["test.csv"])[0]

    @classmethod
    def load_train_val_partitioned(cls, dataroot, part_nums):
        train_filenames = [f"train_part_{i:02d}.csv" for i in part_nums]
        val_filenames = [f"val_part_{i:02d}.csv" for i in part_nums]
        return cls._load(dataroot, train_filenames), cls._load(dataroot, val_filenames)

    @classmethod
    def load_test_partitioned(cls, dataroot, part_nums):
        filenames = [f"test_{i:02d}.csv" for i in part_nums]
        return cls._load(dataroot, filenames)

    @classmethod
    def _load_from_gcp(cls, bucket, blobname):
        client = storage.Client()
        bucket = client.bucket(bucket)
        blob = bucket.blob(blobname)
        with NamedTemporaryFile("wb", delete=False) as f:
            blob.download_to_file(f)
        dataset = cls._tensorify(f.name)
        os.remove(f.name)
        return dataset

    @classmethod
    def _tensorify(cls, path):
        data = pd.read_csv(path).values
        X = data[:, :-1].astype(np.float32)
        Y = data[:, -1].astype(np.int8)
        return cls(X, Y)

    def _to_csv(self, fd):
        n_features = self[0][0].shape[0]
        feature_names = [f"f{i}" for i in range(1, n_features + 1)] + ["y"]
        header = ",".join(feature_names)
        print(header, file=fd)
        for x, y in self:
            row = ",".join([str(x_i.item()) for x_i in x])
            row += f",{y}"
            print(row, file=fd)

    def _save_to_file(self, path):
        if path.exists():
            raise ValueError(f"{path} already exists! Delete before reusing this path.")
        os.makedirs(path.parent, exist_ok=True)
        with open(path, "wt") as f:
            self._to_csv(f)

    def _save_to_gcp(self, bucket, blobname):
        client = storage.Client()
        bucket = client.bucket(bucket)
        blob = bucket.blob(blobname)
        with NamedTemporaryFile("wt", delete=False) as f:
            self._to_csv(f)
        blob.upload_from_filename(f.name)
        os.remove(f.name)

    def save(self, path):
        path = urlsplit(path)
        if path.scheme == "file":
            self._save_to_file(Path(path.path))
        elif path.scheme == "gs":
            self._save_to_gcp(
                bucket=path.netloc, blobname=str(Path(path.path).relative_to("/"))
            )
        else:
            raise ValueError(
                f"Unsupported scheme {path.scheme}! Use either file:// or gcp://."
            )
        return self

    def partition(self, n_parts, drop_last=False):
        part_len = len(self) // n_parts
        parts_indexes = _partition(list(range(len(self))), part_len, drop_last)
        parted_datasets = []
        for part_indexes in parts_indexes:
            part_X = self._X[part_indexes]
            part_Y = self._Y[part_indexes]
            parted_ds = BinDataset(part_X, part_Y)
            parted_datasets.append(parted_ds)
        return parted_datasets

    @classmethod
    def remove(cls, *paths):
        for orig_path in paths:
            path = urlsplit(orig_path)
            if path.scheme == "file":
                cls._remove_file(Path(path.path))
            elif path.scheme == "gs":
                cls._remove_gcp(
                    bucket=path.netloc, blobname=str(Path(path.path).relative_to("/")),
                )
            else:
                raise ValueError(
                    f"Unsupported scheme {path.scheme}! Use either file:// or gcp://."
                )

    @classmethod
    def _remove_file(cls, path):
        if path.exists():
            os.remove(path)

    @classmethod
    def _remove_gcp(cls, bucket, blobname):
        client = storage.Client()
        bucket = client.bucket(bucket)
        blob = bucket.blob(blobname)
        if blob.exists():
            blob.delete()


def _partition(xs, size, drop_last):
    if len(xs) < size:
        return [] if drop_last else [xs]

    if len(xs) == size:
        return [xs]

    return [xs[:size]] + _partition(xs[size:], size, drop_last)
