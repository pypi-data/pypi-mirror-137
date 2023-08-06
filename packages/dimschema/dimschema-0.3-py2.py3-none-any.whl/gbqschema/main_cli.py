#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys
import os
import click
from tabulate import tabulate

from .VERSION import *
from .core.queries import *
from .core.storage import *

# hardcoded
VALID_TABLE_NAMES = ["publications", "grants", "clinical_trials", "grid", "datasets", "patents", "researchers"]

@click.command()
@click.argument('args', nargs=-1)
@click.option('--tables', is_flag=True, help='Show table names')
@click.option('--refresh', is_flag=True, help='Refresh the local cache')
@click.pass_context
def main_cli(ctx, args=None, tables=False, refresh=False):
    """Helper to print GBQ schema information. Pass '.' to show all fields.
    
    $ gbqschema <field> <OPT:table>
    """
    click.secho("GBQschema helper (" + VERSION + ")", dim=True)

    init_cache_folder(USER_DIR)

    if tables:
        print(tabulate(tables_list(), showindex="false", headers="keys", tablefmt='simple'))
        return

    if refresh:
        click.secho("Refreshing GBQ..", fg="red")
        df = fields_list(refresh_cache=True)
        return

    if args:

        if len(args) > 1:
            # first arg a table name
            searchterm, table = args[0], args[1]
        else:
            searchterm, table = args[0], None

        if searchterm == ".":
            searchterm = None

        if table and table not in VALID_TABLE_NAMES:
            click.secho("Table name not valid. Use --tables to verify.", fg="red")
            return

        df = fields_list(table=table, pattern=searchterm)
        print(tabulate(df, showindex="false", headers="keys",  tablefmt='simple')) 
        print("=====")
        print("Total fields: ", len(df))
        return

    click.echo(ctx.get_help())
    return



if __name__ == '__main__':
    main_cli()
