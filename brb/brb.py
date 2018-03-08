#!/usr/bin/env python
from __future__ import print_function

from pkg_resources import Requirement, resource_filename
from os.path import exists as path_exists
import logging
import lasio
import yaml
import argparse
import sys

__author__ = 'Software Innovation Bergen, Statoil ASA'
__version__ = '0.1.0'

def _standardize_columns(df, conf):
    """Replaces column names in df that has a corresponding default value in
    the config

    Parameters
    -----------
    df   : pandas.DataFrame
    conf : dict{}
           Default values given alternative names
           e.g. {'Default': 'Alt1','Alt2'}
    Returns
    df : pandas.DataFrame
    """
    conf = {i: k for k,v in conf.items() for i in v}
    df.columns = [conf.get(k, k) for k in df.columns]

    return df

def _sluggify(token):
    return token.replace('/', '!').replace(' ', '_')


def wellname(las):
    return las.header['Well']['WELL'].value


def write(outname, df, keys):
    if path_exists(outname):
        exit('File %s exists, will not overwrite.' % outname)
    index_name = df.index.name  # the index column is not a regular column
    if index_name in keys:
        keys = [k for k in keys if k != index_name]
    for k in keys:
        if k not in df:
            logging.warn('No such column %s' % k)
    keys = [k for k in keys if k in df]
    df[keys].to_csv(outname)
    print('wrote %d rows to %s' % (len(df), outname))


def main():
    parser = argparse.ArgumentParser(prog = sys.argv[0],
             description = 'brb las file canonizer '
             'brb is a command for reading a las file, canonizing the well '
             'name according to NPD standards, and export a selection of '
             'canonically named columns.')

    parser.add_argument('input',
                        type=str,
                        help='Input file')

    parser.add_argument('--verbose',
                        '-v',
                        action='store_true',
                        help='verbose output')

    parser.add_argument('--headers',
                        nargs='+',
                        default=[],
                        type=str,
                        help='Header names. The headers follows in a '
                        'space-separated list, e.g.: "--headers RMS GR')

    args = parser.parse_args(args = sys.argv[1:])

    if not path_exists(args.input):
        exit('No such file or directory "%s"' % fname)
    fname = args.input
    keys = args.headers

    try:
        with open(fname, 'r') as f_:
            las = lasio.read(f_)
    except Exception as err:
        exit('Unable to read las file "%s". %s' % (fname, str(err)))

    try:
        name = _sluggify(wellname(las))
    except:
        logging.warn('Unable to fetch wellname')
        name = fname

    conf = None
    try:
        filename = resource_filename(Requirement.parse("brb"),
                              "brb/share/brb_default_header_names.yml")
        with open(filename, 'r') as _f:
            conf = yaml.load(_f)
    except Exception as err:
        logging.warn('Could not read config file: {}'.format(err))

    df = las.df()
    if conf:
        df = _standardize_columns(df, conf)
    write(name + '.csv', df, keys)

