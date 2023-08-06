import os.path
import os
import sys
import pandas as pd
import click
import configparser

from .utils import *




USER_DIR = os.path.expanduser("~/.dimensions/dimschema/")

USER_CONFIG_FILE_NAME = "dimschema.ini"
USER_CONFIG_FILE_PATH = os.path.expanduser(USER_DIR + USER_CONFIG_FILE_NAME)

USER_GBQ_CACHE_FILE_NAME = "gbq_cache.csv"
USER_GBQ_CACHE_FILE_PATH = os.path.expanduser(USER_DIR + USER_GBQ_CACHE_FILE_NAME)



###
#
# INIT file helpers 
#
#
###



class ConfigManager(object):
    """
    Helper class containing methods for the init files
    """

    def __init__(self):
        pass


    def init_config_folder(self, user_dir=USER_DIR, user_config_file=USER_CONFIG_FILE_PATH, force=False):
        """Create the config folder/file unless existing. 
        If it exists, backup and create new one.
        """

        if not os.path.exists(user_dir):
            click.secho("First time running.. Creating cache folder.. ", fg='red')
            os.mkdir(user_dir)
            click.secho(f"Done: {user_dir}", fg='green')

        if not os.path.exists(user_config_file) or force:

            if os.path.exists(user_config_file):
                click.secho("Looks like you have already setup a config file: `%s`." % user_config_file, fg="red")
                if click.confirm("Overwrite?"):
                    pass
                else:
                    click.secho("Goodbye")
                    return False

            section = "[gbq]" # default for now
            gbqproject = click.prompt('Please enter the GBQ project name for accessing Dimensions: (e.g. "ds-data-solutions-gbq")')
            
            if not gbqproject:
                click.secho("Goodbye")
                return False

            f= open(user_config_file,"w+")
            f.write(section + "\n")
            f.write("project=" + gbqproject + "\n")
            f.close()
            click.secho(
                "Created %s" % user_config_file, dim=True
            )

    def get_gbq_project(self):
        """
        get the GBQ project name
        """

        section_value = self._read_init_file(section_name="gbq")
        try:
            return section_value["project"]
        except:
            click.secho("GBQ project setting not found." , fg="red")
            raise


    def _read_init_file(self, section_name):
        """
        parse the credentials file / generic inner method
        """

        config = configparser.ConfigParser()
        try:
            config.read(USER_CONFIG_FILE_PATH)
        except:
            printDebug(f"ERROR: `{USER_CONFIG_FILE_NAME}` credentials file not found." , fg="red")
            sys.exit(0)
        # we have a good config file

        try:
            section_value = config[section_name]
        except:
            printDebug(f"ERROR: Credentials file `{USER_CONFIG_FILE_NAME}` does not contain settings for: '{section_name}''", fg="red")
            printDebug(f"Available sections are:")
            for x in config.sections():
                printDebug("'%s'" % x)
            sys.exit(0)
        return section_value



    # 
    # GBQ Cache file helpers
    #


    def get_storage_file(self, group="gbq"):
        """Get the global cache file. 
        # @TODO support for multiple groups
        """

        if group == "gbq":
            if os.path.exists(USER_GBQ_CACHE_FILE_PATH):
                return USER_GBQ_CACHE_FILE_PATH
        return None


    def read_storage_file(self, group="gbq"):
        """
        read cached data
        """

        fpath = USER_GBQ_CACHE_FILE_PATH
        if fpath:
            df = pd.read_csv(fpath)
            return df


    def save_storage_file(self, df, group="gbq"):
        """
        save to json
        """

        fpath = USER_GBQ_CACHE_FILE_PATH
        if fpath:
            df.to_csv(fpath, index=False)
            click.secho(f"Cached rows: {len(df)}", fg="green")
            return True
        
        click.secho(f"Caching failed", fg="red")

