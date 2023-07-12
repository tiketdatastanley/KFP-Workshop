import pandas as pd

from sklearn.metrics import accuracy_score

from src.common.constant import DataArtifact


class Evaluator:
    def __init__(self, model, config):
        self.model = model
        self.features = config["features"]
        self.label_column = config["label_column"]

    def __load_test(self):
        df_test = pd.read_parquet(DataArtifact.DATA_TEST)
        X_test = df_test[self.features]
        y_test = df_test[self.label_column]
        return X_test, y_test

    def __call__(self, callback_metrics=None):
        X_test, y_test = self.__load_test()
        y_pred = self.model.predict(X_test)

        metrics = {"accuracy": accuracy_score(y_test, y_pred)}

        if callback_metrics:
            callback_metrics(metrics)

        return metrics
