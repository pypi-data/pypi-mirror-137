"""
Dimcli general purpose utilities for working with data. 
NOTE: these functions are attached to the top level ``dimcli.utils`` module. So you can import them as follows:

>>> from dimcli.utils import *

"""



import click
import sys
import subprocess
import os
import re
import webbrowser
from itertools import islice


def save2File(contents, filename, path):
    """Save string contents to a file, creating the file if it doesn't exist.

    NOTE Not generalized much, so use at your own risk.


    Parameters
    ----------
    contents: str
        File contents
    filename: str
        Name of the file.
    path: str
        Full path of the file to save. If not existing, it gets created.
    
    Returns
    -------
    str
        The file path with format  "file://..."

    """
    if not os.path.exists(path):
        os.makedirs(path)
    filename = os.path.join(path, filename)
    f = open(filename, 'wb')
    f.write(contents.encode())  # python will convert \n to os.linesep
    f.close()  # you can omit in most cases as the destructor will call it
    url = "file://" + filename
    return url





def open_multi_platform(fpath):
    """Open a file using the native OS tools, taking care of platform differences. 

    Supports win, macos and linux.
    """
    click.secho("Opening `%s` ..." % fpath)
    if sys.platform == 'win32':
        subprocess.Popen(['start', fpath], shell=True)

    elif sys.platform == 'darwin':
        subprocess.Popen(['open', fpath])

    else:
        try:
            subprocess.Popen(['xdg-open', fpath])
        except OSError:
            print("Couldnt find suitable opener for %s" % fpath)



def exists_key_in_dicts_list(dict_list, key):
    """From a list of dicts, checks if a certain key is in one of the dicts in the list.

    See also https://stackoverflow.com/questions/14790980/how-can-i-check-if-key-exists-in-list-of-dicts-in-python

    Parameters
    ----------
    dict_list: list 
        A list of dictionaries.
    key: obj 
        The obj to be found in dict keys

    Returns
    -------
    Dict or None

    """
    # return next((i for i,d in enumerate(dict_list) if key in d), None)
    return next((d for i,d in enumerate(dict_list) if key in d), None)





# https://gist.github.com/zdavkeos/1098474

def walk_up(bottom):
    """Mimic os.walk, but walk 'up' instead of down the directory tree

    Example
    -------
    #print all files and directories
    # directly above the current one
    >>> for i in walk_up(os.curdir):
    >>>    print(i)

    # look for a TAGS file above the
    # current directory
    >>> for c,d,f in walk_up(os.curdir):
    >>>    if 'TAGS' in f:
    >>>        print(c)
    >>>        break
    """

    bottom = os.path.realpath(bottom)

    #get files in current dir
    try:
        names = os.listdir(bottom)
    except Exception as e:
        print(e)
        return


    dirs, nondirs = [], []
    for name in names:
        if os.path.isdir(os.path.join(bottom, name)):
            dirs.append(name)
        else:
            nondirs.append(name)

    yield bottom, dirs, nondirs

    new_path = os.path.realpath(os.path.join(bottom, '..'))
    
    # see if we are at the top
    if new_path == bottom:
        return

    for x in walk_up(new_path):
        yield x



def printDebug(text, mystyle="", err=True, **kwargs):
    """Wrapper around click.secho() for printing in colors with various defaults.

    :kwargs = you can do printDebug("s", bold=True)

    2018-12-06: by default print to standard error stderr (err=True)
    https://click.palletsprojects.com/en/5.x/api/#click.echo
    This means that the output is ok with `less` and when piped to other commands (or files)

    Styling output:
    <http://click.pocoo.org/5/api/#click.style>
    Styles a text with ANSI styles and returns the new string. By default the styling is self contained which means that at the end of the string a reset code is issued. This can be prevented by passing reset=False.

    This works also with inner click styles eg

    ```python
    uri, title = "http://example.com", "My ontology"
    printDebug(click.style("[%d]" % 1, fg='blue') +
               click.style(uri + " ==> ", fg='black') +
               click.style(title, fg='red'))
    ```

    Or even with Colorama

    ```
    from colorama import Fore, Style

    printDebug(Fore.BLUE + Style.BRIGHT + "[%d]" % 1 + 
            Style.RESET_ALL + uri + " ==> " + Fore.RED + title + 
            Style.RESET_ALL)
    ```


    Examples:

    click.echo(click.style('Hello World!', fg='green'))
    click.echo(click.style('ATTENTION!', blink=True))
    click.echo(click.style('Some things', reverse=True, fg='cyan'))
    Supported color names:

    black (might be a gray)
    red
    green
    yellow (might be an orange)
    blue
    magenta
    cyan
    white (might be light gray)
    reset (reset the color code only)
    New in version 2.0.

    Parameters:
    text – the string to style with ansi codes.
    fg – if provided this will become the foreground color.
    bg – if provided this will become the background color.
    bold – if provided this will enable or disable bold mode.
    dim – if provided this will enable or disable dim mode. This is badly supported.
    underline – if provided this will enable or disable underline.
    blink – if provided this will enable or disable blinking.
    reverse – if provided this will enable or disable inverse rendering (foreground becomes background and the other way round).
    reset – by default a reset-all code is added at the end of the string which means that styles do not carry over. This can be disabled to compose styles.

    """

    if mystyle == "comment":
        click.secho(text, dim=True, err=err)
    elif mystyle == "important":
        click.secho(text, bold=True, err=err)
    elif mystyle == "normal":
        click.secho(text, reset=True, err=err)
    elif mystyle == "red" or mystyle == "error":
        click.secho(text, fg='red', err=err)
    elif mystyle == "green":
        click.secho(text, fg='green', err=err)
    else:
        click.secho(text, err=err, **kwargs)




def printInfo(text, mystyle="", **kwargs):
    """Wrapper around printDebug for printing ALWAYS to stdout
    This means that the output can be grepped etc..
    NOTE this output will be picked up by pipes etc..

    Fixes https://github.com/lambdamusic/Ontospy/issues/76
    """
    printDebug(text, mystyle, False, **kwargs)
