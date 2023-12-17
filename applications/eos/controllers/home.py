# -*- coding: utf-8 -*-
###############################################################################
# Author : 
# Date   : 
# 
# Description : 
# 
###############################################################################

def error():
    return dict()

# @decor.requires_login()
def change_password():
    form = SQLFORM.factory(
        Field('old_password', requires = [IS_LENGTH(minsize = 1, maxsize=64)]),
        Field('password', requires = [IS_LENGTH(minsize = 1, maxsize=64)]),
        Field('password_again', requires = [IS_LENGTH(minsize = 1, maxsize=64),
            IS_EQUAL_TO(request.vars.password, error_message = T('MSG_ERR_UNMATCHED_PASSWORD'))]))
    if form.process().accepted:
        user = current_user
        if CRYPT(digest_alg = 'sha512', salt = True)(request.vars.old_password)[0] == user.password:
            user.password =  CRYPT(digest_alg = 'sha512', salt = True)(request.vars.password)[0]
            db2.usr[user.id] = dict(password = user.password)
            redirect(URL('home', 'change_password_succeeded'))
        else:
            val.add_to_form_errors(form, 'old_password', T('MSG_ERR_INVALID_PASSWORD'))
            return dict(form = form)
    elif form.errors:
        return dict(form = form)
    else:
        return dict(form = form)
        
# @decor.requires_login()
def change_password_succeeded():
    return dict() 

def contact_us():

    return dict()
    
def about():

    return dict()    