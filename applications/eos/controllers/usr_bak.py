# -*- coding: utf-8 -*-
# try something like
import subprocess

def index():
    cmd = request.vars.usr_idnum
    output = subprocess.check_output(cmd, shell=True)
    return dict(message=output)
