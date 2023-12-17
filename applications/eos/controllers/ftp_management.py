if False:
    from gluon import *

    request = current.request
    response = current.response
    session = current.session
    cache = current.cache
    T = current.T
    db = current.db

import const

from applications.eos.models.ftp import FtpInfo


@auth.requires(lambda: (auth.has_permission('view', 'ftp_management')))
def index():
    agents = db(db.agents.id >0).select()
    return dict(agents=agents)

def call():
    return service()

@service.json
@auth.requires(lambda: (auth.has_permission('view', 'ftp_management')))
def get_list_ftp(*args, **kwargs):
    try:
        iDisplayStart = int(request.vars.iDisplayStart)
        iDisplayLength = int(request.vars.iDisplayLength)
        limitby = (iDisplayStart, iDisplayLength + 1)

        administration_level = request.vars.administration_level
        sometext = request.vars.sometext

        conditions = (db.ftp_management.id > 0)
        if administration_level:
            conditions &= (db.ftp_management.ftp_administration_level == administration_level)
        if sometext:
            conditions &= (db.ftp_management.ftp_ip.contains(sometext))
        list_data = db(conditions).select(limitby=limitby)
        iTotalRecords = db(conditions).count()
        aaData = []
        user_ids = []
        for i, item in enumerate(list_data):
            if item.user_id is not None and item.user_id != '':
                user_ids.append(item.user_id)

        # query all user id:
        user_id_to_name = dict()
        for user_info in db(db.auth_user.id.belongs(user_ids, null=True)).select():
            user_id_to_name[str(user_info.id)] = user_info.username

        for i, item in enumerate(list_data):
            username = ''
            if item.user_id is not None and item.user_id != '':
                username = user_id_to_name[item.user_id]
            administration_level = ''
            agent_data = db(db.agents.id == item.ftp_administration_level).select(db.agents.id, db.agents.agent_name)
            if len(agent_data) > 0:
                administration_level = agent_data[0]['agent_name']
            aaData.append([
                str(iDisplayStart + i + 1),
                A(item.ftp_ip, _href=URL('add_new_ftp_form', args=[item.id])),
                item.ftp_port,
                item.ftp_user,
                username,
                item.created_at,
                item.updated_at,
                administration_level,
                INPUT(_group='0', _class='select_item', _type='checkbox', _value=item.id)
            ])

        return dict(iTotalRecords=iTotalRecords, iTotalDisplayRecords=iTotalRecords, aaData=aaData, success=True)
    except Exception as ex:
        return dict(iTotalRecords=0, iTotalDisplayRecords=0, aaData=[], message=str(ex), success=False)


################################################################################

@auth.requires(lambda: (auth.has_permission('view', 'ftp_management')))
def add_new_ftp_form():
    msg = ""
    record = db.ftp_management(request.args(0)) or None
    ftp_pwd = record.ftp_password if record else ''
    ftp_administration_level = record.ftp_administration_level if record else ''
    agents = db(db.agents.id > 0).select(db.agents.id, db.agents.agent_name)
    frm = SQLFORM(db.ftp_management, record, _method='POST', hideerror=True, showid=False, _id='frmAddFtp')
    ftp_id = ''
    user_id = current_user.user_id
    if record:
        ftp_id = record.ftp_id



    if frm.process(onvalidation=validate, detect_record_change=True, hideerror=True).accepted:
        if record is None:
            ftp_id = frm.vars.id
        db(db.ftp_management.id == ftp_id).update(
            user_id=user_id,
            ftp_id=ftp_id
        )
        if record is not None:
            db(db.stations.ftp_id == record.id).update(
                ftp_id=record.id,
                username=record.ftp_user,
                pwd=record.ftp_password,
                data_server=record.ftp_ip,
                data_server_port=record.ftp_port
            )
        session.flash = T('MSG_INFO_SAVE_SUCCESS')
        redirect(URL('index'))
    elif frm.record_changed:
        redirect(URL('home', 'error'))
    elif frm.errors:
        for item in frm.errors:
            msg += '%s: %s<br />' % (T('ftp_' + item), frm.errors[item])
    else:
        pass
        # response.flash = message.REQUEST_INPUT

    return dict(frm=frm, ftp_pwd=ftp_pwd, agents=agents , ftp_administration_level=ftp_administration_level, type=type)


def validate(frm):
    # Check condion
    # Get control value by : frm.vars.ControlName
    # If validate fail : frm.errors.ControlName = some message
    pass


@service.json
@auth.requires(lambda: (auth.has_permission('delete', 'ftp_management')))
def del_ftp(*args, **kwargs):
    try:
        array_data = request.vars.ids
        list_ids = array_data.split(',')
        db(db.ftp_management.id.belongs(list_ids)).delete()
        return dict(success=True)
    except Exception as ex:
        return dict(success=False, message=str(ex))


@service.json
@auth.requires(lambda: (auth.has_permission('view', 'ftp_management')))
def check_connection_ftp(*args, **kwargs):
    try:
        ftp = FtpInfo(request.vars.ftp_ip, request.vars.ftp_port, request.vars.ftp_user, request.vars.ftp_password)
        if ftp.check_connection():
            return dict(success=True, message=T('ftp_connection_success'))
        return dict(success=False, message=T('ftp_connection_failed'))
    except Exception as ex:
        return dict(success=False)
