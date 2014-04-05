#!/usr/bin/env python2

from greshunkel.build import main
from greshunkel.context import BASE_CONTEXT, build_doc_context, build_blog_context
import argparse

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Build the OlegDB website.')
    parser.add_argument('include_dir', type=str,
        help='The location of the OlegDB header files.')
    args = parser.parse_args()
    context = build_doc_context(args.include_dir, BASE_CONTEXT)
    context = build_blog_context(context)
    main(context)
