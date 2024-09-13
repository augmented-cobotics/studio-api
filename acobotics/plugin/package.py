import argparse
import base64
import yaml
import os
import re

import compileall

from . import Plugin
from ..api import Robot, Manufacturer

from zipfile import ZipFile

def dir_path(string):
    if os.path.isdir(string):
        return string
    else:
        raise NotADirectoryError(string)
    
parser = argparse.ArgumentParser(description='Process some integers.')
parser.add_argument('directory', type=dir_path, help='The directory containing the plugin.yml file')

def validate_plugin(input):
    assets_dir = os.path.join(input, "assets")
    plugin_file = os.path.join(input, "plugin.yml")
    
    if not os.path.exists(plugin_file):
        raise FileNotFoundError("Could not find 'plugin.yml' in the specified directory")

    with open(plugin_file, 'r') as f:
        plugin_raw = yaml.safe_load(f)

    # logo
    
    logo_file = os.path.join(assets_dir, plugin_raw['logo'])
    if not os.path.exists(logo_file):
        raise FileNotFoundError("Could not find plugin logo in the assets")
        

    mfs_dir = os.path.join(input, "manufacturers")
    
    manufacturers = []
    mfs_dir = os.path.join(input, "manufacturers")
    
    if os.path.isdir(mfs_dir):
        for mfs_entry in os.scandir(mfs_dir):
            if not mfs_entry.is_dir():
                continue
            
            mfs_file = os.path.join(mfs_entry.path, "manufacturer.yml")
            with open(mfs_file, 'r') as f:
                mfs_raw = yaml.safe_load(f)

            robots_paths = mfs_raw['robots']

            # robots
            robots = []
            for robot_path in robots_paths:
                robot_path = os.path.join(mfs_entry.path, robot_path)

                with open(robot_path, 'r') as f:
                    robot_raw = yaml.safe_load(f)

                avatar_file = os.path.join(assets_dir, robot_raw['avatar'])
                if not os.path.exists(avatar_file):
                    raise FileNotFoundError(f"Robot '{robot_raw['id']}' has an invalid avatar")

                banner_file = os.path.join(assets_dir, robot_raw['banner'])
                if not os.path.exists(banner_file):
                    raise FileNotFoundError(f"Robot '{robot_raw['id']}' has an invalid avatar")

                robot = Robot(**robot_raw)
                robots.append(robot)
            
            mfs_raw['robots'] = robots

            logo_file = os.path.join(assets_dir, mfs_raw['logo'])
            with open(logo_file, "rb") as f:
                mfs_raw['logo'] = base64.b64encode(f.read()).decode('ascii')

            mfs = Manufacturer(**mfs_raw)

            manufacturers.append(mfs)

    plugin = Plugin(**plugin_raw, manufacturers=manufacturers) 
    return plugin
        

def run():
    args = parser.parse_args()
    input = args.directory
    
    plugin = validate_plugin(input)
    output_file = os.path.join(input, f'{plugin.id}.acsp')
    
    ignored_extensions = [ '.acsp', '.py' ]
    ignored_files = [ '.env', ]
    ignored_dirs = [ '.vscode', '__pycache__' ]
    
    compileall.compile_dir(input, legacy=True)
        
    with ZipFile(output_file, 'w') as zip:
        def process_folder(path):
            for file in os.listdir(path):
                file_path = os.path.join(path, file)
                
                if os.path.isdir(file_path):
                    if file in ignored_dirs:
                        continue
                    
                    process_folder(file_path)
                    continue
                
                filename, ext = os.path.splitext(file)
                if filename in ignored_files:
                    continue
                
                if ext in ignored_extensions:
                    continue
                    
                zip.write(file_path, file_path)
                
                if ext == '.pyc':
                    os.remove(file_path)
   
        process_folder(input)

if __name__ == '__main__':
    run()