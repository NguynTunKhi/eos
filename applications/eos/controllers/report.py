# -*- coding: utf-8 -*-
###############################################################################
# Author : 
# Date   : 
# 
# Description : 
# 
###############################################################################

from reportlab.lib.enums import TA_JUSTIFY, TA_LEFT, TA_CENTER, TA_RIGHT
from reportlab.lib.pagesizes import cm
from applications.eos.modules.eos import const_controller as cc, const_action as ca
from applications.eos.modules import common
from w2pex import date_util

################################################################################
def call():
    return service()

def download(): 
    return response.stream(request.vars.file)
