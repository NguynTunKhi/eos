# -*- coding: utf-8 -*-
###############################################################################
# Author : 
# Date   : 
# 
# Description : 
# 
###############################################################################
from gluon.custom_import import track_changes
# Check if loaded modules have changed these modules will be reload
track_changes(True)

from gluon.tools import PluginManager, Service, Auth
plugins = PluginManager()
service = Service()

from w2pex.util import ThreadSafe
# Dictionary contains keys - global variables
global_dict = cache.ram('my_thread_safe_object', lambda: ThreadSafe(), ThreadSafe.forever)

from appbase import AppUtil
app = AppUtil.get_instance()
# config = app.get_config()

# -------------------------------------------------------------------------
# once in production, remove reload=True to gain full speed
# -------------------------------------------------------------------------
from gluon.contrib.appconfig import AppConfig
myconf = AppConfig(reload = True)

# current_language = 'vn'
T.is_writable = True
if not session.lang:
    session.lang = 'vn'
T.force(session.lang)


