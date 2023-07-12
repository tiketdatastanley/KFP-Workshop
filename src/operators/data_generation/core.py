from typing import Dict, Any

from src.common.logger import create_logger
from src.common.bigquery import Bigquery
from src.common.constant import Path, DataArtifact
from src.common.utility import read_query_from_file


class DataGenerator:
    def __init__(self, config: Dict[str, Any]):
        self.bq = Bigquery(config)
        self.logger = create_logger("workshop:DataGenerator")

    def __call__(self, callback=None):
        query_exec_dst = [
            (Path.QUERY_TRAIN, DataArtifact.DATA_TRAIN),
            (Path.QUERY_VAL, DataArtifact.DATA_VAL),
            (Path.QUERY_TEST, DataArtifact.DATA_TEST),
        ]

        for query_path, dst in query_exec_dst:
            self.logger.info(f"Executing {query_path}")
            query = read_query_from_file(query_path)
            df = self.bq.query_to_df(query)
            df.to_parquet(dst, index=False)
