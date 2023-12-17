# -*- coding: utf-8 -*-
###############################################################################
# Author : 
# Date   : 
# 
# Description : 
# 
###############################################################################


@auth.requires(lambda: (auth.has_permission('view', 'owner_information')))
def form():
    # If in Update mode, get equivallent record
    msg = ''
    record = db(db.manager_owner_information.id > 0).select().first()
    frm = SQLFORM(db.manager_owner_information, record, _method='POST', hideerror=True, showid=False, _id='frmMain')

    if frm.process(onvalidation=validate, detect_record_change=True, hideerror=True).accepted:
        data = db(db.manager_owner_information.id > 0).select().first()
        session.ownerName = unicode(data.name, "utf-8")
        session.ownerDivision = unicode(data.division, "utf-8")
        session.perThousand = data.perThousand
        session.decimal = data.decimal
        session.flash = T('MSG_INFO_SAVE_SUCCESS')
        redirect(URL('form'))
    elif frm.record_changed:
        redirect(URL('home', 'error'))
    elif frm.errors:
        for item in frm.errors:
            msg += '%s: %s<br />' % (T('provinces_' + item), frm.errors[item])
    else:
        pass
        # response.flash = message.REQUEST_INPUT
    return dict(frm = frm, msg = XML(msg))


################################################################################
def validate(frm):
    # Check condion
    # Get control value by : frm.vars.ControlName
    # If validate fail : frm.errors.ControlName = some message
    pass


def call():
    return service()



################################################################################
@service.json
def get_logo(*args, **kwargs):
    try:
        logo_db = db(db.manager_owner_information.id>0).select()
        for i in logo_db:
            if (i.logo == '' or i.logo == None):
                logo = IMG(_src="%s" % URL('static', 'images', args='logo_xam.png'),
                           _style="height:50px; width:auto; padding-left: 40px;")
            else:
                logo = IMG(_src="%s" % URL('default', 'download', args=[i.logo]),
                           _style="height:50px; width:auto; padding-left: 40px;") if i.logo else ''

        return dict(success=True,
                    logo=logo)
    except Exception, ex:
        return dict(message=str(ex), success=False)

########################################################################
@service.json
def get_logo_login(*args, **kwargs):
    try:
        logo_db = db(db.manager_owner_information).select() 
        for i in logo_db:
            if (i.logo == '' or i.logo == None): 
                logo_login1 = IMG(_src="%s" % URL('static', 'images', args='logo.png'),
                               _style="height:150px; width:auto;")
            else:
                logo_login1 = IMG(_src="%s" % URL('default', 'download', args=[i.logo]),
                               _style="height:150px; width:auto;") if i.logo else ''
        return dict(success=True, logo_login=logo_login1)
    except Exception, ex: 
            return dict(message=str(ex), success=False)