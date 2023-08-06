import os.path
import os
import sys
import pandas as pd
import click

# from ..utils.misc_utils import walk_up


USER_DIR = os.path.expanduser("~/.dimensions/dimschema/")

USER_GBQ_CACHE_FILE_NAME = "gbq_cache.csv"
USER_GBQ_CACHE_FILE_PATH = os.path.expanduser(USER_DIR + USER_GBQ_CACHE_FILE_NAME)




def init_cache_folder(_dir):
    """
    Create the folder where json and csv exports are stored
    """
    if not os.path.exists(_dir):
        click.secho("First time running.. Creating cache folder.. ", fg='red')
        os.mkdir(_dir)
        click.secho(f"Done: {_dir}", fg='green')


def get_storage_file(group="gbq"):
    """Get the global cache file. 
    # @TODO support for multiple groups
    """

    if group == "gbq":
        if os.path.exists(USER_GBQ_CACHE_FILE_PATH):
            return USER_GBQ_CACHE_FILE_PATH
    return None


def read_storage_file(group="gbq"):
    """
    read cached data
    """

    fpath = USER_GBQ_CACHE_FILE_PATH
    if fpath:
        df = pd.read_csv(fpath)
        return df


def save_storage_file(df, group="gbq"):
    """
    save to json
    """

    fpath = USER_GBQ_CACHE_FILE_PATH
    if fpath:
        df.to_csv(fpath, index=False)
        click.secho(f"Cached rows: {len(df)}", fg="green")
        return True
    
    click.secho(f"Caching failed", fg="red")

