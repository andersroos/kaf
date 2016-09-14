#!/usr/bin/env python3

import argparse
import sys
import importlib.util
import os


try:
    import kaf
except:
    sys.path.append(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'py'))
    import kaf


def build(dir):
    to_build = []
    for root, dirs, files in os.walk(dir):
        dirs[::] = [d for d in dirs if d not in ['node_modules', '.git']]
        
        for fil in files:
            filename = os.path.relpath(os.path.join(root, fil), dir)
            for regex, builder in kaf.rules:
                if regex.match(filename):
                    to_build.append((filename, builder))

    for filename, builder in to_build:
        builder.build(filename)
        

def main():

    parser = argparse.ArgumentParser()
    
    parser.add_argument('--file', '-f', dest="file", default=None,
                        help="Specify the kaf file to use, if not specified the current path will"
                        " be searched upwards for kaf.py and the first one found will"
                        " be used.")
    parser.add_argument('--watch', '-w', dest="watch", default=False, action='store_true',
                        help="Watch all instead of building all.")
                        
    args = parser.parse_args()

    if args.file:
        defs_filename = args.file
    else:
        dir = pwd = os.getcwd()
        while True:
            filename = os.path.join(dir, "kaf.py")
            if os.access(filename, os.R_OK):
                defs_filename = filename
                break
            if dir == '/':
                print("Could not find kaf.py in '%s' or above, bailing." % pwd, file=sys.stderr)
                return 1
            
            dir = os.path.dirname(dir)

    # Import the user's kaf.py.

    spec = importlib.util.spec_from_file_location("defs", filename)
    defs = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(defs)

    # Build
        
    defs_dir = os.path.dirname(filename)

    if args.watch:
        watch(defs_dir)
    else:
        build(defs_dir)
    
    
if __name__ == '__main__':
    sys.exit(main())
