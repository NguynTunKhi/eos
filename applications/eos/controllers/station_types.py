# -*- coding: utf-8 -*-
###############################################################################
# Author : 
# Date   : 
# 
# Description : 
# 
###############################################################################

@auth.requires(lambda: (auth.has_permission('create', 'station_types') or auth.has_permission('edit', 'master_station_type')))
def form():
    # If in Update mode, get equivallent record
    record = db.station_types(request.args(0)) or None
    msg = ''
    code = request.vars.code
    station_type_1 = request.vars.station_type
    station_type_english = request.vars.station_type_english
    qi_type = request.vars.qi_type
    order = request.vars.order
    color = request.vars.color
    icon = request.vars.icon
    can_update = True
    station_type = db((db.station_types.code == code) & (db.station_types.del_flag == True)).select().first()
    station_code = db((db.station_types.code == code) & (db.station_types.del_flag == False)).select().first()
    frm = SQLFORM(db.station_types, record, _method = 'POST', hideerror = True, showid = False, _id = 'frmMain')

    if not station_code or can_update:
        if station_type:
            db(db.station_types.code == code).update(del_flag=False, station_type=station_type_1, station_type_english=station_type_english,
                                                     qi_type=qi_type, order=order, color=color, icon=icon)
            session.flash = T('MSG_INFO_SAVE_SUCCESS')
            redirect(URL('index'))
        else:
            if frm.process(onvalidation = validate, detect_record_change = True, hideerror = True).accepted:
                session.flash = T('MSG_INFO_SAVE_SUCCESS')
                redirect(URL('index'))
            elif frm.record_changed:
                redirect(URL('home', 'error'))
            elif frm.errors:
                for item in frm.errors:
                    # if not station_type and item == 'code':
                    #     msg += T('Code used')
                    # else:
                    msg += '%s: %s<br />' %(item, frm.errors[item])
            else:
                pass
    else:
        msg += T('Code used')

    frm.custom.widget.code['_maxlength'] = '16'
    frm.custom.widget.station_type['_maxlength'] = '32'
    
    return dict(frm = frm, msg = XML(msg))

################################################################################
def validate(frm):
    #Check condion
    #Get control value by : frm.vars.ControlName
    #If validate fail : frm.errors.ControlName = some message
    pass

def call():
    return service()

################################################################################
def index():
    return locals()

################################################################################
@service.json
@auth.requires(lambda: (auth.has_permission('view', 'station_types')))
def get_list_station_types(*args, **kwargs):
    try:
        aaData = [] # Du lieu json se tra ve
        conditions = ((db.station_types.id > 0) & (db.station_types.del_flag != True))
        list_data = db(conditions).select(  db.station_types.id, 
                                            db.station_types.code,
                                            db.station_types.qi_type,
                                            db.station_types.station_type,
                                            db.station_types.station_type_english,
                                            db.station_types.color,
                                            orderby = ~db.station_types.order)
        iTotalRecords = len(list_data)
        qi_type = ''
        # Duyet tung phan tu trong mang du lieu vua truy van duoc
        for i, item in enumerate(list_data):
            if item.qi_type == 0:
                qi_type = T('NOT_QI')
            elif item.qi_type == 1:
                qi_type = T('CAL_AQI')
            elif item.qi_type == 2:
                qi_type = T('CAL_WQI')
            aaData.append([
                str(i + 1),
                A(item.station_type, _href = URL('form', args = [item.id])),
                A(item.station_type_english, _href=URL('form', args=[item.id])) if item.station_type_english is not None
                else A(T("Don't have english name"), _href=URL('form', args=[item.id])),
                item.code,
                qi_type,
                item.color,
                INPUT(_group = '0', _class = 'select_item', _type = 'checkbox', _value = item.id),
                item.id,
            ])

        return dict(iTotalRecords = iTotalRecords, iTotalDisplayRecords = iTotalRecords, aaData = aaData, success = True)
    except Exception, ex:
        return dict(iTotalRecords = 0, iTotalDisplayRecords = 0, aaData = [], message = str(ex), success = False)
        
################################################################################
@service.json
@auth.requires(lambda: (auth.has_permission('delete', 'station_types')))
def delete_station_type(*args, **kwargs):
    try:
        array_data = request.vars.ids
        list_ids = array_data.split(',')
        db(db.station_types.id.belongs(list_ids)).update(del_flag = True)
        return dict(success = True)
    except Exception as ex:
        return dict(success = False, message = str(ex))