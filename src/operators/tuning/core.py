import os
import json
from tempfile import TemporaryDirectory

import pandas as pd

from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import ParameterGrid
from sklearn.metrics import accuracy_score

from src.common.constant import DataArtifact


class Tuning:
    def __init__(self, config):
        self.features = config["features"]
        self.label_column = config["label_column"]
        self.fixed_params = config["fixed_params"]
        self.tuned_params = config["tuned_params"]

    def __load_dataset(self):
        df_train = pd.read_parquet(DataArtifact.DATA_TRAIN)
        df_val = pd.read_parquet(DataArtifact.DATA_VAL)

        X_train = df_train[self.features]
        X_val = df_val[self.features]

        y_train = df_train[self.label_column]
        y_val = df_val[self.label_column]

        return X_train, X_val, y_train, y_val

    def __call__(
        self, callback_model=None, callback_artifact=None, callback_metrics=None
    ):
        result = []
        X_train, X_val, y_train, y_val = self.__load_dataset()

        combinations = ParameterGrid(self.tuned_params)

        for tuned_params in combinations:
            params = {**self.fixed_params, **tuned_params}
            model = RandomForestClassifier(**params)
            model.fit(X_train, y_train)

            y_pred = model.predict(X_val)
            accuracy = accuracy_score(y_val, y_pred)

            result.append({"params": json.dumps(params), "accuracy": accuracy})

        result_df = pd.DataFrame(result)
        result_df = result_df.sort_values(by="accuracy", ascending=False)
        result_df = result_df.reset_index(drop=True)
        result_df["rank"] = range(result_df.shape[0])

        if callback_artifact:
            with TemporaryDirectory() as tmpdir:
                result_df.to_csv(os.path.join(tmpdir, "summary.csv"))
                callback_artifact(tmpdir)

        return result_df
