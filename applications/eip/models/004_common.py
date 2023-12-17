# -*- coding: utf-8 -*-
###############################################################################
# Author : 
# Date   : 
# 
# Description : 
# 
###############################################################################
from gluon import current

logger = app.get_logger()
action_handler = app.get_action_handler()
action_handler.attach(current.response)
decor = app.get_decorator()
controller_requires_login = app.controller_requires_login
widgets = app.get_bootstrap_widgets()
val = app.get_validation()
val.set_error_label(T('MSG_ERR'))
val.set_mode(1)

# Objects to be used in modules are stored in 'current'
current.db = db
current.logger = logger
current.myconf = myconf



# -------------------------------------------------------------------------
# configure email
# -------------------------------------------------------------------------
mail = auth.settings.mailer
mail.settings.server = 'logging' if request.is_local else myconf.get('smtp.server')
mail.settings.sender = myconf.get('smtp.sender')
mail.settings.login = myconf.get('smtp.login')
mail.settings.tls = myconf.get('smtp.tls') or False
mail.settings.ssl = myconf.get('smtp.ssl') or False


datetime_format_vn = str(T('%H:%M %d/%m/%Y'))
date_format_js = str(T('Y-m-d'))
full_date_format = str(T('%Y-%m-%d %H:%M:%S'))
full_date_format_2 = str(T('%Y/%m/%d %H:%M:%S'))
full_date_format_js = str(T('%Y-%m-%d %H:%M:%S-js'))
full_date_format_js_2 = str(T('%Y/%m/%d %H:%M:%S-js'))
    
