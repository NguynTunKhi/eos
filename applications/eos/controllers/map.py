# -*- coding: utf-8 -*-

################################################################################
# @decor.requires_login()
@auth.requires(lambda: (auth.has_permission('view', 'map')))
def index():
    
    return dict()



