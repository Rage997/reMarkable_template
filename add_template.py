# Little python3 script to add a template to the remarkable using SSH connection

import subprocess
import json
import sys
import argparse
import getpass
import pexpect
from pexpect import pxssh
import os
from utils import effortless_scp, yer_or_no

# reMarkable IP. If the connection is not through usb you need to change it
rm_ip='10.11.99.1'

parser = argparse.ArgumentParser(description='A python script to copy a template to the reMarkable')
parser.add_argument( 'template', action = 'store', type = str, help = 'The template to copy.' )
args = parser.parse_args( )
template = args.template

filename = sys.argv[1].split('/')[-1]
if not os.path.isfile(filename):
    print(filename + ' does not exist')
    raise FileNotFoundError

name = filename.split('.')[0]
# path to the templates on the reMarkable
templates_path = '/usr/share/remarkable/templates/'
password = getpass.getpass()

# Template description. ref: https://remarkablewiki.com/tips/templates
description = {
  "name": name,
  "filename": name,
  "iconCode": "\ue9db",
  "landscape": "false", 
  "categories": [
    "Life/organize"
  ]
}
# print('Template description: ', json.dumps(description))


# # We need to add a description of the template to templates.json (see: https://remarkablewiki.com/tips/templates)
# # the easiest way is to copy it locally, add it using python, and then copy it back
# 1) Copy templates.json from reMarkable to the machine
try:
    effortless_scp('root@'+rm_ip+':'+templates_path+'templates.json', '.', password)
except Exception as e:
    print('The ssh connection could not be enstablished! Is the reMarkable awake? Is the password correct?')
    sys.exit(1)

# 2) Add new template description
# read the json and append new entry describing the new template
with open('templates.json', 'r') as json_file:
    data = json.load(json_file)

filenames_list = [template['filename'] for template in data['templates']]
if filename in filenames_list or name in filenames_list:
    print('This template is already present in the reMarkable!')
    sys.exit(0)
else:
    data['templates'].append(description)

with open('templates.json', 'w') as json_file:
    json.dump(data, json_file, indent=4, sort_keys=True)

# 3) copy templates.json back
try:
    effortless_scp('templates.json',  'root@'+rm_ip+':'+templates_path, password)
except RuntimeError as e:
    print('An error occured copying back templates.json to reMarkable.')
    sys.exit(1)

# 4) Copy the template to reMarkable
try:
    effortless_scp(template, 'root@'+rm_ip+':'+templates_path, password)
except RuntimeError as e:
    print('An error occured copying the template to reMarkable.')

print('To see the new template you need to restart the reMarkable. Do you want to do it now?')

if yer_or_no():
    print('Rebooting reMarkable.')
    try:
        s = pxssh.pxssh()
        s.login(rm_ip, 'root', password)
        s.sendline('systemctl restart xochitl')
        s.prompt()
        s.close()
    except pxssh.ExceptionPxssh as e:
        print("SSH failed on login. Please, restart the reMarkable manually.")
        print(e)

print('Done! Enjoy your new template.')