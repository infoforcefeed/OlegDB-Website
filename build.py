#!/usr/bin/env python3

from greshunkel.build import main
from greshunkel.context import BASE_CONTEXT, build_doc_context, build_blog_context

if __name__ == '__main__':
    context = build_doc_context(BASE_CONTEXT)
    context = build_blog_context(context)
    main(context)
