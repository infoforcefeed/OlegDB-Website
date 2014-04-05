#!/usr/bin/env python2

from greshunkel.build import build_doc_context, main
import argparse

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Build the OlegDB website.')
    parser.add_argument('include_dir', type=str,
        help='The location of the OlegDB header files.')
    args = parser.parse_args()
    build_doc_context(args.include_dir)
    main()
