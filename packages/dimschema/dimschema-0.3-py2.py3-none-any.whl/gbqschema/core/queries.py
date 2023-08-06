#!/usr/bin/python
# -*- coding: utf-8 -*-


from google.cloud import bigquery
import os 
import pandas as pd
import click

#
from ..settings import *
client = bigquery.Client(project=GBQ_PROJECT)

from .storage import *

def tables_list():
	"""List of tables
	https://cloud.google.com/bigquery/docs/information-schema-tables
	"""
	query_job = client.query(f"""
		SELECT * 
		FROM dimensions-ai.data_analytics.INFORMATION_SCHEMA.TABLES;
		""")

	results = query_job.to_dataframe() 
	return results


def fields_list_all():
	"""Full fields list 

		SELECT *
		FROM
		dimensions-ai.data_analytics.INFORMATION_SCHEMA.COLUMN_FIELD_PATHS
	"""

	query_job = client.query(f"""
		SELECT
		table_name, field_path, data_type
		FROM
		dimensions-ai.data_analytics.INFORMATION_SCHEMA.COLUMN_FIELD_PATHS
		""")

	df = query_job.to_dataframe() 
	return df



def fields_list(table=None, pattern=None, refresh_cache=False):
	"""Full fields list 

		SELECT *
		FROM
		dimensions-ai.data_analytics.INFORMATION_SCHEMA.COLUMN_FIELD_PATHS
	"""
	if not get_storage_file():
		# recreate if not existing
		refresh_cache = True

	if refresh_cache:
		df = fields_list_all() 
		save_storage_file(df, "gbq")

	else:
		df = read_storage_file("gbq")

	if table:
		df = df[df['table_name'].str.contains(table)]
	if pattern:
		df = df[df['field_path'].str.contains(pattern)]

	# shorten the data type info
	df['data_type'] = df['data_type'].apply(lambda x: x.split("<")[0])
	return df.sort_values(["table_name", "field_path"])




def query_results_summary(GBQ_TABLE):
	"""Summary of data in the GBQ table we created"""

	client = bigquery.Client(project=GBQ_PROJECT)
	query_job = client.query(f"""
		SELECT COUNT(distinct id) as tot_ids, topic, variant
		FROM `{GBQ_PROJECT}.{GBQ_TABLE}`  
		GROUP BY topic, variant
		ORDER BY topic
		""")

	results = query_job.to_dataframe() 
	return results




def test_query():
	"""

	"""
	client = bigquery.Client(project=GBQ_PROJECT)
	query_job = client.query("""
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
		


