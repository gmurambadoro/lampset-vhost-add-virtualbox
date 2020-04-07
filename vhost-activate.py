#!/usr/bin/python3

import argparse
import os.path as path
import os

"""
This script is used to create and activate an apache2 vhost file.
Usage:
    vhost-activate --domain test --dir test --localhost
"""

WEB_ROOT = '/var/www/'

parser = argparse.ArgumentParser()
parser.add_argument('domain', help="The name of the domain e.g. test.com. The suffix *.localhost will be appended "
                                   "automatically")
parser.add_argument('--dir', required=False, help="The path to the document_root. "
                                                  "You can specify an absolute url or a path "
                    "relative to the Apache web_root folder {WEB_ROOT}".replace('{WEB_ROOT}', WEB_ROOT))
parser.add_argument('--no-localhost', required=False, help="Specify this flag if you do not want *.localhost to "
                    "be appended automatically to the domain. However, you will need to add this domain to "
                    "/etc/hosts file yourself")

args = parser.parse_args()

domain = getattr(args, 'domain')
dir_name = getattr(args, 'dir')
no_localhost = getattr(args, 'no_localhost')

if dir_name is None:
    dir_name = domain

# check if dir_name exists
if not path.exists(dir_name):
    dir_name = path.join(WEB_ROOT, dir_name)

if not path.exists(dir_name):
    raise FileNotFoundError('The path does not exist: %s' % dir_name)

# create the actual domain name
if not int(no_localhost or '0'):
    domain = domain + '.localhost'

print(domain, no_localhost)

