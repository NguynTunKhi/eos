# -*- coding: utf-8 -*-
###############################################################################
# Author : 
# Date   : 
# 
# Description : 
# 
###############################################################################

@decor.requires_permission('delete_any_table')
def call():
    return service()

@service.json
def delete(*args, **kwargs):
    import json
    try:
        table_name = request.args[2]
        list_ids = request.vars.id.split(',')
        db(db[table_name].id.belongs(list_ids)).update(del_flag = True)
        return dict(success = True)
    except Exception as ex:
        return dict(success = False, message = str(ex))
