#!/usr/bin/python
# -*- coding: utf-8 -*-


from google.cloud import bigquery
import os 
import pandas as pd
import click

# https://docs.dimensions.ai/bigquery/data-sources.html
VALID_TABLE_NAMES = [
		"publications", "grants", "clinical_trials", "grid", "datasets", "patents", "researchers", "policy_documents", "reports"
		]


class BigQueryManager(object):
	"""
	Helper class containing methods for GBQ queries
	"""

	def __init__(self, config_instance):
		GCP_PROJECT_ID = config_instance.get_gbq_project()
		self.client = bigquery.Client(project=GCP_PROJECT_ID)
		self.config = config_instance


	def get_fields_list_from_cache(self, table=None, pattern=None, refresh_cache=False):
		"""Full fields list 

		"""
		if not self.config.get_storage_file():
			# recreate if not existing
			refresh_cache = True

		if refresh_cache:
			df = self.get_fields_list() 
			self.config.save_storage_file(df, "gbq")

		else:
			df = self.config.read_storage_file("gbq")

		if table:
			df = df[df['table_name'].str.contains(table)]
		if pattern:
			df = df[df['field_path'].str.contains(pattern)]

		# shorten the data type info
		df['data_type'] = df['data_type'].apply(lambda x: x.split("<")[0])
		return df.sort_values(["table_name", "field_path"])



	def get_fields_list(self):
		"""Full fields list 

			SELECT *
			FROM
			dimensions-ai.data_analytics.INFORMATION_SCHEMA.COLUMN_FIELD_PATHS
		"""

		query_job = self.client.query(f"""
			SELECT
			table_name, field_path, data_type
			FROM
			dimensions-ai.data_analytics.INFORMATION_SCHEMA.COLUMN_FIELD_PATHS
			""")

		df = query_job.to_dataframe() 
		return df



	def tables_list(self):
		"""List of tables
		https://cloud.google.com/bigquery/docs/information-schema-tables
		"""
		query_job = self.client.query(f"""
			SELECT table_catalog, table_schema, table_name, table_type, creation_time
			FROM dimensions-ai.data_analytics.INFORMATION_SCHEMA.TABLES;
			""")

		results = query_job.to_dataframe() 
		return results


	def any_query(self, q):
		"""Run any query
		"""
		q = q.replace("dim.", "dimensions-ai.data_analytics.")

		query_job = self.client.query(q)

		results = query_job.to_dataframe() 
		return results


	def test_query(self):
		"""

		"""
		query_job = self.client.query("""
		SELECT
			id,
			title,
			ARRAY_LENGTH(authors) as authors_count,
			CAST(altmetrics.score as INT64) as altmetric_score
		FROM
			`dimensions-ai.data_analytics.publications`
		WHERE
			year = 2020 AND 'grid.4991.5' in UNNEST(research_orgs)
		ORDER BY
			altmetrics.score desc
		LIMIT 5""")

		results = query_job.result()  # Waits for job to complete.

		for row in results:
			print("{} : {} : {}".format(row.id, row.authors_count, row.altmetric_score))
			print("----\nDone")
			


