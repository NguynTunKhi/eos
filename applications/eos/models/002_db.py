# -*- coding: utf-8 -*-

## if SSL/HTTPS is properly configured and you want all HTTP requests to be redirected to HTTPS, uncomment the line below:
# request.requires_https()

import os, sys

response.generic_patterns = ['*'] if request.is_local else []

##########################################################################
db.define_table('func',
    Field('func_code', length = 64, notnull = True, unique = True, required = True,
          requires = [IS_LENGTH(minsize = 1, maxsize = 64),
                      IS_MATCH('[\w\.\-_|]+', strict = True),
                      IS_LOWER(),
                      IS_NOT_IN_DB(db, 'func.func_code')]),
    Field('func_name', length = 128),
    Field('parent_code', length=64))

# CKEDITOR



