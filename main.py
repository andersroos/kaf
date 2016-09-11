#!/usr/bin/env python3

import argparse
import sys
import importlib.util
import os

def main():

    parser = argparse.ArgumentParser()
    
    parser.add_argument('--list', '-l', dest="list", action='store_true', default=False,
                        help="List targets.")
    parser.add_argument('--file', '-f', dest="file", default=None,
                        help="Specify the kaf file to use, if not specified the current path will"
                        " be searched upwards for kaf.py and the first one found will"
                        " be used.")

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

    # Make sure kaf can be imported, not sure this is needed properly released.
    
    try:
        import kaf
    except:
        sys.path.append(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'py'))

    # Import the user's kaf.py.

    spec = importlib.util.spec_from_file_location("defs", filename)
    defs = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(defs)

    # Build the target.

    if args.list:

        print("depend")
        print("build")
        print("test")
        print("package/install")
        print("deploy/install")
    
    
    
if __name__ == '__main__':
    sys.exit(main())
