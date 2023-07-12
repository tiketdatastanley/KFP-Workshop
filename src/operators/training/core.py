import pandas as pd

from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score

from src.common.constant import DataArtifact


class Trainer:
    def __init__(self, config):
        self.features = config["features"]
        self.label_column = config["label_column"]

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
        X_train, X_val, y_train, y_val = self.__load_dataset()

        model = RandomForestClassifier(random_state=42)
        model.fit(X_train, y_train)

        y_pred = model.predict(X_val)
        metrics = {"accuracy": accuracy_score(y_val, y_pred)}

        if callback_model:
            callback_model(model)

        if callback_metrics:
            callback_metrics(metrics)

        return model
