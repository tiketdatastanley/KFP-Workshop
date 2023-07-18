import os
import json
from tempfile import TemporaryDirectory

import pandas as pd

from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score

from src.common.constant import DataArtifact


def select_best_parameters(df):
    """
    df: dataframe from tuning step
      params: "JSON str"
      accuracy: float
      rank: int
    """

    if df.shape[0] == 0:
        return {}
    return json.loads(df.iloc[0]["params"])


class Trainer:
    def __init__(self, config, parameters):
        self.features = config["features"]
        self.label_column = config["label_column"]
        self.parameters = parameters

    def __load_dataset(self):
        df_train = pd.read_parquet(DataArtifact.DATA_TRAIN)
        df_val = pd.read_parquet(DataArtifact.DATA_VAL)
        df_combined = pd.concat([df_train, df_val])

        X_train = df_combined[self.features]
        y_train = df_combined[self.label_column]

        return X_train, y_train

    def __call__(
        self,
        callback_params=None,
        callback_model=None,
        callback_artifact=None,
        callback_metrics=None,
    ):
        X_train, y_train = self.__load_dataset()

        model = RandomForestClassifier(random_state=42)
        model.fit(X_train, y_train)

        y_pred = model.predict(X_train)
        metrics = {"accuracy": accuracy_score(y_train, y_pred)}

        feature_importance = {
            ft: v for ft, v in zip(self.features, model.feature_importances_)
        }

        if callback_params:
            callback_params(self.parameters)

        if callback_model:
            callback_model(model)

        if callback_artifact:
            with TemporaryDirectory() as tmpdir:
                path = os.path.join(tmpdir, "feature_importance.json")
                with open(path, "w") as fp:
                    json.dump(feature_importance, fp)
                callback_artifact(tmpdir)

        if callback_metrics:
            callback_metrics(metrics)

        return model, feature_importance
