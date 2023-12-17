# -*- coding: utf-8 -*-

from gluon import current
from datetime import datetime, timedelta


################################################################################
def formular_1(q1, q2, bp1, bp2, c):
    res = (q1 - q2)*(bp2 - c)/(bp2 - bp1) + q2
    
    return res  

################################################################################
def formular_2(q1, q2, bp1, bp2, c):
    res = (q2 - q1)*(c - bp1)/(bp2 - bp1) + q1
    
    return res 
    
################################################################################
def do_baohoa(temp):
    res = 14.652 - 0.41022*temp + 0.0079910*temp*temp - 0.000077774*temp*temp*temp  
    
    return res 

    
    
    
    