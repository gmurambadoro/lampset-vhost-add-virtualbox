#!/usr/bin/python3

import argparse
import os.path as path
import os
import shutil

"""
This script is used to create and activate an Apache2 vhost file.
This file needs to run with privileges because it makes changes apache2 system folders
Usage:
    vhost-new.py -h
"""

WEB_ROOT = '/var/www/'
WORK_FOLDER = '/tmp/'
APACHE_SITES_FOLDER = '/etc/apache2/sites-available/'


# todo: use php fpm

def is_granted(msg_prompt: str) -> bool:
    resp = prompt(msg_prompt=msg_prompt, accept_empty=False, max_retries=3)

    return resp.strip().lower() in ['y']


def prompt(msg_prompt: str, accept_empty: bool, max_retries: int = None) -> str:
    if not max_retries:
        max_retries = 3

    for _ in range(0, max_retries):
        resp = input(msg_prompt).strip()

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

php_versions = ['5.6', '7.1', '7.2', '7.3', '7.4']
php_version = None

if args.interactive:
    print("""
Welcome to Apache2 VHost File Generation Tool.
Version: 1.0.0    
Notes: This tool allows you to create and activate an Apache2 vhost file for a development or testing domain.
    """)
    domain = prompt('Domain name - e.g. example.com: ', False)
    dir_name = prompt(f'Web Directory [{WEB_ROOT}{domain}]: ', True) or domain
    no_localhost = not (prompt(
        msg_prompt=f'Do you want to append .localhost to the domain [{domain}.localhost] (y|N): ',
        accept_empty=False).strip().lower() == 'y')

    override = prompt(
        msg_prompt='Do yo want to overwrite existing configuration if it exists? (y|N): ',
        accept_empty=False).lower() == 'y'

    if is_granted('Do you have PHP-FPM enabled?'):
        php_version = prompt('Enter your PHP Version e.g. 7.2, 7.4 [7.4]: ', accept_empty=False, max_retries=3) or '7.4'

        if not php_version:
            raise RuntimeError('Please select a valid PHP version: ' + str(php_versions))
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
    domain += '.localhost'

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
    
    {PHP_FPM}

    ErrorLog /var/log/apache2/{DOMAIN}_error.log
    CustomLog /var/log/apache2/{DOMAIN}_access.log combined
</VirtualHost>
""".strip().replace('{DOMAIN}', domain).replace('{DIR}', dir_name)

php_fpm = """
    <FilesMatch \.php$>
        # For Apache version 2.4.10 and above, use SetHandler to run PHP as a fastCGI process server
        SetHandler "proxy:unix:/run/php/php{PHP_VER}-fpm.sock|fcgi://localhost"
    </FilesMatch>
""".replace('{PHP_VER}', php_version or 'PHP_VERSION_NOT_SET')

vhost_str = vhost_str.replace('{PHP_FPM}', php_fpm if php_version else '')

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

os.system('cat ' + vhost_conf_dest)

print()

