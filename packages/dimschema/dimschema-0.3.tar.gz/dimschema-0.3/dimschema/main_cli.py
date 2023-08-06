#!/usr/bin/python
# -*- coding: utf-8 -*-

import click
from tabulate import tabulate

from .VERSION import *
from .core.queries import *
from .core.fmanager import *



@click.command()
@click.argument('args', nargs=-1)
@click.option('--tables', is_flag=True, help='Show table names')
@click.option('--refresh', is_flag=True, help='Refresh the local cache')
@click.option('--prompt', is_flag=True, help='Enter a SQL query (experimental)')
@click.option('--init', is_flag=True, help='Init the config folder with the GBQ info etc..')
@click.pass_context
def main_cli(ctx, args=None, init=False, tables=False, refresh=False, prompt=False):
    """Helper to print GBQ schema information. Pass '.' to show all fields.
    
    $ dimschema <OPT:table-name> <field-pattern> 
    """
    click.secho("Dimensions GBQ schema-helper (" + VERSION + ")", dim=True)

    config = ConfigManager()

    if init:
        config.init_config_folder(force=True)
        return

    config.init_config_folder()
    
    gbq = BigQueryManager(config)

    if tables:
        print(tabulate(gbq.tables_list(), showindex="false", headers="keys", tablefmt='simple'))
        return

    if refresh:
        click.secho("Refreshing GBQ..", fg="red")
        df = gbq.get_fields_list_from_cache(refresh_cache=True)
        return

    if prompt:
        click.secho("Enter a SQL query (experimental). Enter an empty line to run. Syntax sugar: 'dim.'='dimensions-ai.data_analytics.'", fg="red")

        sentinel = '' # ends when this string is seen
        contents = []
        for line in iter(input, sentinel):
            contents.append(line)

        sql = " ".join(contents)
        click.secho("... running GBQ query", dim=True)
        df = gbq.any_query(sql)
        # disable_numparse=True => avoid scientific notation in large numbers
        print(tabulate(df, showindex="false", headers="keys", tablefmt='grid', disable_numparse=True))
        return

    if args:

        if len(args) > 1:
            # first arg a table name
            table, searchterm = args[0], args[1]
        else:
            searchterm, table = args[0], None

        if searchterm == ".":
            searchterm = None

        if table and table not in VALID_TABLE_NAMES:
            click.secho("Table name not valid. Use --tables to verify.", fg="red")
            return

        df = gbq.get_fields_list_from_cache(table=table, pattern=searchterm)
        print(tabulate(df, showindex="false", headers="keys",  tablefmt='simple')) 
        print("=====")
        print("Total fields: ", len(df))
        return

    click.echo(ctx.get_help())
    return



if __name__ == '__main__':
    main_cli()
