# Adds a template to the remarkable
import subprocess
import json
import sys
import argparse
from pexpect import pxssh
import getpass # prompts user for passwrod without echoing

parser = argparse.ArgumentParser(description='A python script to copy a template to the reMarkable')
parser.add_argument( 'template', action = 'store', type = str, help = 'The template to copy.' )
args = parser.parse_args( )
template = args.template

#  add help Usage: python add_template.py <template_path>'

filename = sys.argv[1].split('/')[-1]
name = filename.split('.')[0]
# rm_ip=10.11.99.1
rm_ip='192.168.1.186'
# Template description
description = {
  "name": name,
  "filename": filename,
  "iconCode": "\ue9db",
  "landscape": "false", 
  "categories": [
    "Life/organize"
  ]
}

templates_path = '/usr/share/remarkable/templates/'

password = getpass.getpass()

# # We need to add a description of the template to templates.json (see: https://remarkablewiki.com/tips/templates)
# # the easiest way is to copy it locally, add it using python, and then copy it back
# 1) Copy templates.json from reMarkable to the machine
try:
    subprocess.run(['scp', 'root@'+rm_ip+':'+templates_path+'templates.json', '.'])
except subprocess.CalledProcessError as grepexc:   
    print("Error:", grepexc.returncode, grepexc.output)

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
subprocess.run(['scp',  'templates.json',  'root@'+rm_ip+':'+templates_path])

# 4) Copy the template to reMarkable
subprocess.run(['scp', template, 'root@'+rm_ip+':'+templates_path])

print('Done! Enjoy your new template')