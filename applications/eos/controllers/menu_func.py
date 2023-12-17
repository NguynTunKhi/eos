# -*- coding: utf-8 -*-
###############################################################################
# Author : 
# Date   : 
# 
# Description : 
# 
###############################################################################

def validate(form):
    if form.vars.parent_id == 1:
        form.vars.code = form.vars.name
    else:
        parent = db.menu_func(form.vars.parent_id)
        form.vars.code = parent.code + "|" + form.vars.name

    # If the menu_func table exists a record that is not deleted and has the code field equals new code,
    # a error is occurred
    menu_func_record = db(db.menu_func.code == form.vars.code).select()
    if len(menu_func_record) > 0:
        form.errors.code = "Error"
    else:
        db.menu_func.insert(**dict(form.vars))

################################################################################
@decor.requires_permission('Administration|menu_func|menu_func_form')
def menu_func_form():
    form = SQLFORM(db.menu_func,
                   _method = 'POST',
                   showid = False,
                   submit_button = T('BTN_SUBMIT'),
                   deletable = False)
    
    form.custom.widget.name['_style'] = "width:95%"
    form.custom.widget.name['_onchange'] = "setCode()"
    form.custom.widget.description['_style'] = "width:95%"
    form.custom.widget.code['_readonly'] = True
    form.custom.widget.code['_style'] = "width:95%"
    
    if form.validate(onvalidation = validate, hideerror = True):
        pass
    elif form.errors:
        if form.errors.code == "Error":
            val.add_to_validation_summary(T('ERR_FUNC_CODE'))
        else:
            val.add_to_validation_summary(T('ERR_INVALID_VALUE'))
    
    return dict(form = form)

################################################################################
def get_menu_func():
    records = db(db.menu_func.id > 0).select(db.menu_func.id, db.menu_func.name, orderby = db.menu_func.id) or None
    if records == None : return
    
    # Remove all items of dropdownlist        
    str = "$('#menu_func_parent_id').find('option').remove();"
    
    # Add new items to dropdownlist
    for row in records:
        str += "$('#menu_func_parent_id').append(new Option('" + row.name + "','" + '%s'%row.id + "', false, false));"

    return str    

################################################################################
def call():
    return service()

################################################################################
@service.json
def menu_func_json(*args, **kwargs):
    import json
    
    #get records all of menu_func table
    menu_functions = db(db.menu_func.id > 0).select(orderby = db.menu_func.id)
    nodes = []

    for record in menu_functions:
        node = {'id': str(record.id),
                'parent': str(record.parent_id) if record.parent_id else '#',
                'text': record.name,
                'state' : { 'opened' : True }
               }
        nodes.append(node)
        
    return nodes

################################################################################
def del_menu_func():
    id = request.vars.id
    db(db.menu_func.id == id).delete()
    return ""

################################################################################
def rename_menu_func():
    id = request.vars.id
    new_name = request.vars.new_name
    current_record = db.menu_func(id)
    
    if current_record.parent_id == 0:
        db(db.menu_func.id == id).update(name = new_name, code = new_name) # Update current record
    else:
        new_code = db.menu_func(current_record.parent_id).code + "|" + new_name
        
        # Get all records in the menu_func table that has code equals new code
        # If any record in this has del_flag is False, an error is occurred,
        # else they are deleted from the table
        other_records = db((db.menu_func.id != id) & (db.menu_func.code == new_code)).select()
        if len(other_records) > 0:
            for record in other_records:
                del db.menu_func[record.id]

        db(db.menu_func.id == id).update(name = new_name, code = new_code) # Update current record

    # Update all records that is child nodes of current record
    childs = db((db.menu_func.parent_id == current_record) & (db.menu_func.del_flag == False)).select()
    for child in childs:
        child.update_record(code = new_code + "|" + child.name)
    
    return ""
