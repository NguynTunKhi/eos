# -*- coding: utf-8 -*-
################################################################################
# Author: 
# Date: 
#
# Description : 
#
################################################################################

response.logo = A(B('web',SPAN(2),'py'),XML('&trade;&nbsp;'), _class='brand', _href='http://www.web2py.com/')
response.title = request.application.replace('_',' ').title()
response.subtitle = ''
response.meta.author = 'Your Name <you@example.com>'
response.meta.keywords = 'web2py, python, waste water, environment'
response.meta.generator = 'Web2py Web Framework'
response.google_analytics_id = None
from applications.eip.models.js_languages import vn
response.js_string = vn.JS_LANGUAGES

################################################################################
def get_js_string(lang):
    return  ''


################################################################################
def get_function_codes():
    if current_user:
        codes = set()

        # conditions = ((db.func.id > 0) &
                      # (db.func.id == db.permission.func_id) &
                      # (db.permission.role_id == db.membership.role_id) &
                      # (db.membership.user_id == str(current_user.id)))
        
        # functions = db(conditions).select(db.func.code)
        # for function in functions:
            # codes.add(function.code)
            
        # funcs = db(db.func.id > 0).select(db.func.id, db.func.code)
        funcs = db(db.func.id > 0).select()
        permissions = db(db.permission.id > 0).select(db.permission.func_id, db.permission.role_id)
        memberships = db(db.membership.user_id == str(current_user.id)).select(db.membership.role_id)
        
        for func in funcs:
            for permission in permissions:
                for membership in memberships:
                    if func.id == permission.func_id and permission.role_id == membership.role_id:
                        codes.add(func.code)
        return codes

################################################################################
def get_menu_codes():
    if current_user:
        db = current.db
        menu_codes = set()
        return menu_codes   # do da fix menu o layout_master
        
        ################################################
        # Get all codes of the menu_func table that current user has permission
        ################################################
        conditions = ((db.menu_func.id > 0) &
                      (db.menu_func.id == db.menu_permission.menu_func_id) &
                      (db.menu_permission.role_id == db.membership.role_id) &
                      (db.membership.user_id == str(current_user.id)))
        all_menu_funcs = db(conditions).select(db.menu_func.code, distinct = True)

        ################################################
        # Analyse each string code as follows:
        # "P1|P2|P3|CHIL" => list ["P1", "P1|P2", "P1|P2|P3", "P1|P2|P3"|CHIL"]
        # If list[i] doesn't exist in menu_codes, it is added
        ################################################
        for menu_func in all_menu_funcs:
            node_array = menu_func.code.split('|')
            length_node_array = len(node_array)
            parent = node_array[0]
            
            if parent not in menu_codes:
                menu_codes.add(parent)
            
            for index in range(1, length_node_array):
                parent = parent + "|" + node_array[index]
                if parent not in menu_codes:
                    menu_codes.add(parent)

        return menu_codes

################################################################################
def has_function_code(code):
    if current_user:
        if 'admin' in current_user.roles or code in current_user.function_codes:
            return True
    return False

################################################################################
def has_menu_code(code):
    if current_user:
        # if ('admin' in current_user.roles) or (code in current_user.menu_codes):
        if 'admin' in current_user.roles:
            return True
    return False
    
################################################################################
def get_menu_html():
    return
    

