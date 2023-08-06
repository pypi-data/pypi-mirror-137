# Dimemsions GBQ Schema Utility

CLI to retrieve SQL schema information about the [Dimensions on Google BigQuery](https://console.cloud.google.com/bigquery?p=dimensions-ai&page=project) dataset. 

**NOTE** This is the same documentation available from https://docs.dimensions.ai/bigquery/data-sources.html - only it's retrieving from the BigQuery database itself. 


## Requirements 

* Python 
* Personal Google account credentials set up in your local machine. The [BigQueryLAB](https://bigquery-lab.dimensions.ai/tutorials/01-connection/#option-2-using-a-local-jupyter-and-your-personal-credentials) has a tutorial showing how to do that. 

## Examples

* `dimschema publications .` : show all fields from the Publications table

* `dimschema ids` : show fields containing the string 'ids' 

* `dimschema datasets ids` : show fields containing the string 'ids', only in the Datasets table


## Development

```
$ mkvirtualenv dimschema
$ pip install --editable .
```

See https://stackoverflow.com/questions/30306099/pip-install-editable-vs-python-setup-py-develop

