#!/usr/bin/python3

import argparse
import os.path as path
import os
import shutil

"""
This script is used to create and activate an apache2 vhost file.
This file needs to run with privileges because it makes changes apache2 system folders
Usage:
    vhost-new.py -h
"""

WEB_ROOT = '/var/www/'
WORK_FOLDER = '/tmp/'
APACHE_SITES_FOLDER = '/etc/apache2/sites-available/'

# todo: use php fpm


def get_keyboard_input(prompt: str, accept_empty: bool, retries: int = None) -> str:
    if not retries:
        retries = 3

    for _ in range(0, retries):
        resp = input(prompt).strip()

        if resp:
            return resp

        if accept_empty:
            return resp

    raise RuntimeError(f'No input provided!!')


parser = argparse.ArgumentParser()

parser.add_argument('--interactive',
                    required=False,
                    help='Get the commands from user input',
                    action='store_true')

parser.add_argument('--domain', required=False,
                    help="The name of the domain e.g. test.com. The suffix *.localhost will be appended "
                         "automatically")

parser.add_argument('--dir',
                    required=False,
                    help="The path to the document_root. "
                         "You can specify an absolute url or a path relative to the Apache "
                         "web_root folder {WEB_ROOT}".replace('{WEB_ROOT}', WEB_ROOT))

parser.add_argument('--no-localhost',
                    required=False,
                    help="Specify this flag if you do not want *.localhost to "
                         "be appended automatically to the domain. However, "
                         "you will need to add this domain to "
                         "/etc/hosts file yourself", action="store_true")

parser.add_argument('--override', required=False, action='store_true',
                    help='Override a vhost if the configuration file already exists.')

args = parser.parse_args()

if args.interactive:
    domain = get_keyboard_input('Domain e.g. example.com: ', False)
    dir_name = get_keyboard_input(f'Web Directory [{WEB_ROOT}{domain}]: ', True) or domain
    no_localhost = get_keyboard_input(
        prompt=f'Do you want to append .localhost to the domain [{domain}.localhost] (y|N):',
        accept_empty=False).lower() == 'y'

    override = get_keyboard_input(
        prompt='Do yo want to overwrite existing configuration if it exists? (y|N): ',
        accept_empty=False).lower() == 'y'
else:
    domain = args.domain
    dir_name = args.dir
    no_localhost = args.no_localhost
    override = args.override

    if dir_name is None:
        dir_name = domain

if not dir_name:
    raise RuntimeError(f'Empty document directory!!!')

# check if dir_name exists
if not path.exists(dir_name):
    dir_name = path.join(WEB_ROOT, dir_name)

if not path.exists(dir_name):
    raise FileNotFoundError('The path does not exist: %s' % dir_name)

# create the actual domain name
if not no_localhost:
    domain = domain + '.localhost'

# create the working folder
if not path.exists(WORK_FOLDER):
    os.mkdir(WORK_FOLDER)

vhost_str = """
<VirtualHost *:80>
    ServerName {DOMAIN}

    DocumentRoot {DIR}
    <Directory {DIR}>
        AllowOverride All
        Order Allow,Deny
        Allow from All
    </Directory>

    ErrorLog /var/log/apache2/{DOMAIN}_error.log
    CustomLog /var/log/apache2/{DOMAIN}_access.log combined
</VirtualHost>
""".strip().replace('{DOMAIN}', domain).replace('{DIR}', dir_name)

vhost_conf_src = path.join(WORK_FOLDER, domain + ".conf")

with open(vhost_conf_src, 'w') as file:
    file.write(vhost_str)

# create the destination path to store the config
vhost_conf_dest = path.join(APACHE_SITES_FOLDER, path.basename(vhost_conf_src))

if path.exists(vhost_conf_dest):
    if override:
        os.system('sudo rm %s' % vhost_conf_dest)
    else:
        raise Exception('The file `%s` already exists.' % vhost_conf_dest)

os.system('sudo cp %s %s' % (vhost_conf_src, vhost_conf_dest))

# activate the site
os.system('sudo a2ensite %s' % path.basename(vhost_conf_dest))

# restart apache 2
os.system('sudo systemctl reload apache2')