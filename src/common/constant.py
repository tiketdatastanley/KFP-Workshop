import os


class Folder:
    RESOURCE = "resources"
    DATA = "data"


class Path:
    CONFIG = os.path.join(Folder.RESOURCE, "config.yml")
    QUERY_TRAIN = os.path.join(Folder.RESOURCE, "query_train.sql")
    QUERY_VAL = os.path.join(Folder.RESOURCE, "query_val.sql")
    QUERY_TEST = os.path.join(Folder.RESOURCE, "query_test.sql")


class DataArtifact:
    DATA_TRAIN = os.path.join(Folder.DATA, "train.parquet")
    DATA_VAL = os.path.join(Folder.DATA, "val.parquet")
    DATA_TEST = os.path.join(Folder.DATA, "test.parquet")
