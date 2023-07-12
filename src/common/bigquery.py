from google.cloud import bigquery


class Bigquery:
    def __init__(self, config):
        self.client = bigquery.Client(config["bigquery"]["billing_project"])

    def execute_query(self, query: str):
        job = self.client.query(query)
        job.result()

    def query_to_df(self, query: str):
        job = self.client.query(query)
        return job.result().to_arrow().to_pandas()

    def add_df_to_bq(self, df, table: str):
        job_config = bigquery.job.LoadJobConfig()
        job_config.write_disposition = bigquery.WriteDisposition.WRITE_APPEND
        job = self.client.load_table_from_dataframe(df, table, job_config=job_config)
