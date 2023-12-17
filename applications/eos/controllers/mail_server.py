# -*- coding: utf-8 -*-
###############################################################################
# Author :
# Date   :
#
# Description :
#
###############################################################################


@auth.requires(lambda: (auth.has_permission('view', 'mail_server')))
def form():
    # If in Update mode, get equivallent record
    msg = ''
    record = db(db.mail_server.id > 0).select().first()
    frm = SQLFORM(db.mail_server, record, _method='POST', hideerror=True, showid=False, _id='frmMain')
    password = record.sender_email_password if record else ''

    if frm.process(onvalidation=validate, detect_record_change=True, hideerror=True).accepted:
        session.flash = T('MSG_INFO_SAVE_SUCCESS')
        redirect(URL('form'))
    elif frm.record_changed:
        redirect(URL('home', 'error'))
    elif frm.errors:
        for item in frm.errors:
            msg += '%s<br />' % (frm.errors[item])
    else:
        pass
        # response.flash = message.REQUEST_INPUT
    return dict(frm = frm, msg = XML(msg), password=password)


################################################################################
def validate(frm):
    # Check condion
    # Get control value by : frm.vars.ControlName
    # If validate fail : frm.errors.ControlName = some message
    pass


def call():
    return service()
