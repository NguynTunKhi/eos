# -*- coding: utf-8 -*-
###############################################################################
# Author : 
# Date   : 
# 
# Description : 
# 
###############################################################################


@auth.requires(lambda: (auth.has_permission('create', 'datalogger') or auth.has_permission('edit', 'datalogger')))
def form():
    # If in Update mode, get equivallent record
    record = db.datalogger(request.args(0)) or None
    logger_id = request.args(0) or None
    msg = ''
    name = record.logger_name if record else ''
    logger_ids = request.vars.logger_id
    station_id = record.station_id if record else ''
    count_logger_id = db(db.adjustments.station_id == station_id).count(db.adjustments.logger_id != '')
    frm = SQLFORM(db.datalogger, record, _method='POST', hideerror=True, showid=False, _id='frmMain')

    if frm.process(onvalidation=validate, detect_record_change=True, hideerror=True).accepted:
        if count_logger_id > 0:
            db(db.adjustments.station_id == station_id).update(logger_id=logger_ids)
        session.flash = T('MSG_INFO_SAVE_SUCCESS')
        redirect(URL('index'))
    elif frm.record_changed:
        redirect(URL('home', 'error'))
    elif frm.errors:
        for item in frm.errors:
            msg += '%s: %s<br />' % (item, frm.errors[item])
    else:
        pass

    stations = db(db.stations.id > 0).select(db.stations.id, db.stations.station_name)

    return dict(frm=frm, msg=XML(msg), type=type, name=name,
                logger_id=logger_id, stations=stations, station_id=station_id)


################################################################################
def validate(frm):
    # Check condion
    # Get control value by : frm.vars.ControlName
    # If validate fail : frm.errors.ControlName = some message
    pass


def call():
    return service()


################################################################################
@auth.requires(lambda: (auth.has_permission('view', 'datalogger')))
def index():
    return dict()


################################################################################
@service.json
@auth.requires(lambda: (auth.has_permission('view', 'datalogger')))
def get_list_datalogger(*args, **kwargs):
    iDisplayStart = int(request.vars.iDisplayStart)
    iDisplayLength = int(request.vars.iDisplayLength)
    s_search = request.vars.sSearch
    sometext = request.vars.sometext
    aaData = []
    limitby = (iDisplayStart, iDisplayLength + 1)  # Tuple dung de phan trang (vtri bat dau - chieu dai)

    conditions = (db.datalogger.id > 0)

    conditions &= (db.datalogger.logger_id is not None)

    # Neu chuoi tim kiem khac rong thi them dieu kien truy van voi chuoi tim kiem
    if sometext:
        conditions &= ((db.datalogger.logger_id.contains(sometext)) |
                       (db.datalogger.logger_name.contains(sometext)) |
                       (db.datalogger.logger_note.contains(sometext)))

    list_data = db(conditions).select(db.datalogger.id,
                                      db.datalogger.logger_id,
                                      db.datalogger.logger_name,
                                      db.datalogger.logger_note,
                                      db.datalogger.station_id,
                                      limitby=limitby,
                                      orderby=db.datalogger.logger_id)
    # Tong so ban ghi khong thuc hien phan trang
    iTotalRecords = db(conditions).count()
    station_type = dict()
    for key, item in const.STATION_TYPE.iteritems():
        station_type[str(item['value'])] = T(item['name'])

    # Duyet tung phan tu trong mang du lieu vua truy van duoc
    for i, item in enumerate(list_data):
        station_id = item.station_id
        station = db(db.stations.id == station_id).select(db.stations.station_name)
        if len(station) > 0:
            aaData.append([
                A(str(iDisplayStart + 1 + i), _href=URL('form', args=[item.id])),
                A(str(item['logger_id']), _href=URL('form', args=[item.id])),
                item.logger_name,
                item.logger_note,
                station[0].station_name,
                INPUT(_group='0', _class='select_item', _type='checkbox', _value=item.id),
                item.id
            ])
    return dict(iTotalRecords=iTotalRecords, iTotalDisplayRecords=iTotalRecords, aaData=aaData, success=True)


################################################################################
@service.json
@auth.requires(lambda: (auth.has_permission('delete', 'datalogger')))
def del_qcvn(*args, **kwargs):
    try:
        array_data = request.vars.ids
        list_ids = array_data.split(',')
        db(db.datalogger.id.belongs(list_ids)).delete()
        return dict(success=True)
    except Exception as ex:
        return dict(success=False, message=str(ex))


################################################################################
@service.json
@auth.requires(lambda: (auth.has_permission('view', 'datalogger')))
def get_qcvn_detail_by_qcvn(*args, **kwargs):
    try:
        iDisplayStart = int(request.vars.iDisplayStart)  # Vi tri bat dau lay du lieu
        iDisplayLength = int(request.vars.iDisplayLength)  # So luong ban ghi se lay toi da
        station_id = request.vars.station_id  # Chuoi tim kiem nhap tu form

        aaData = []  # Du lieu json se tra ve
        limitby = (iDisplayStart, iDisplayLength + 1)  # Tuple dung de phan trang (vtri bat dau - chieu dai)
        conditions = (db.datalogger_command.id > 0)
        if station_id:
            conditions &= (db.datalogger_command.station_id == station_id)
        list_data = db(conditions).select(db.datalogger_command.id,
                                          db.datalogger_command.command_id,
                                          db.datalogger_command.command_name,
                                          db.datalogger_command.command_content,
                                          db.datalogger_command.status,
                                          limitby=limitby,
                                          orderby=~db.datalogger_command.id)
        # Tong so ban ghi khong thuc hien phan trang
        iTotalRecords = db(conditions).count()
        print("hungdx")
        print(iTotalRecords)
        indicator_dict = common.get_indicator_dict()

        # List kind
        rowsKind = db(db.datalogger_command.id > 0).select()
        resKind = {}
        for item in rowsKind:
            resKind[str(item.id)] = item.id
        # Thu tu ban ghi
        iRow = iDisplayStart + 1

        # Duyet tung phan tu trong mang du lieu vua truy van duoc
        for item in list_data:
            print(item.command_content)
            listA = [
                str(iRow),
                item.command_id,
                item.command_name,
                item.command_content,
                # item.qcvn_const_area_value,
                INPUT(_group='1', _class='select_item', _type='checkbox', _value=item.id),
                item.id,
            ]
            aaData.append(listA)
            iRow += 1
        return dict(iTotalRecords=iTotalRecords, iTotalDisplayRecords=iTotalRecords, aaData=aaData, success=True)
    except Exception as ex:
        return dict(iTotalRecords=0, iTotalDisplayRecords=0, aaData=[], message=str(ex), success=False)


################################################################################
@service.json
@auth.requires(lambda: (auth.has_permission('view', 'datalogger')))
def get_qcvn_detail_by_qcvnCode(*args, **kwargs):
    try:
        iDisplayStart = int(request.vars.iDisplayStart)  # Vi tri bat dau lay du lieu
        iDisplayLength = int(request.vars.iDisplayLength)  # So luong ban ghi se lay toi da
        station_id = request.vars.station_id  # Chuoi tim kiem nhap tu form

        aaData = []  # Du lieu json se tra ve
        limitby = (iDisplayStart, iDisplayLength + 1)  # Tuple dung de phan trang (vtri bat dau - chieu dai)
        conditions = (db.datalogger_command.id > 0)
        if station_id:
            conditions &= (db.datalogger_command.station_id == station_id)
        list_data = db(conditions).select(db.datalogger_command.id,
                                          db.datalogger_command.command_id,
                                          db.datalogger_command.command_name,
                                          db.datalogger_command.command_content,
                                          db.datalogger_command.status,
                                          limitby=limitby,
                                          orderby=~db.datalogger_command.id)
        # Tong so ban ghi khong thuc hien phan trang
        iTotalRecords = db(conditions).count()

        indicator_dict = common.get_indicator_dict()

        # List kind
        rowsKind = db(db.datalogger_command.id > 0).select()
        resKind = {}
        for item in rowsKind:
            resKind[str(item.id)] = item.id

        # qcvn_kind_dict = common.get_qcvn_kind_dict()
        # print(res)
        # Thu tu ban ghi
        iRow = iDisplayStart + 1

        # Duyet tung phan tu trong mang du lieu vua truy van duoc
        for item in list_data:
            listA = [
                str(iRow),
                item.command_id,
                item.command_name,
                item.command_content,
                # item.qcvn_const_area_value,
                INPUT(_group='1', _class='select_item', _type='checkbox', _value=item.id),
                item.id,
            ]
            aaData.append(listA)
            iRow += 1
        return dict(iTotalRecords=iTotalRecords, iTotalDisplayRecords=iTotalRecords, aaData=aaData, success=True)
    except Exception as ex:
        return dict(iTotalRecords=0, iTotalDisplayRecords=0, aaData=[], message=str(ex), success=False)


################################################################################

@service.json
def get_list_qcvn_details(*args, **kwargs):
    try:
        qcvn_id = request.vars.qcvn_id  # Chuoi tim kiem nhap tu form
        # Get all QCVN detail
        qcvn_details = db(db.datalogger_command.qcvn_id == qcvn_id).select(db.datalogger_command.id,
                                                                           db.datalogger_command.indicator_id,
                                                                           db.datalogger_command.qcvn_type_code,
                                                                           db.datalogger_command.qcvn_min_value,
                                                                           db.datalogger_command.qcvn_max_value,
                                                                           db.datalogger_command.qcvn_const_area_value)
        for i in range(len(qcvn_details)):
            qcvn_details[i].id = str(qcvn_details[i].id)

        return dict(qcvn_details=qcvn_details, success=True)
    except Exception as ex:
        return dict(message=str(ex), success=False)


################################################################################
@service.json
def get_qcvn_detail(*args, **kwargs):
    try:
        id = request.vars.id
        qcvn_detail = db.datalogger_command(id) or None
        return dict(qcvn_detail=qcvn_detail, success=True)
    except Exception as ex:
        return dict(message=str(ex), success=False)


################################################################################
@service.json
@auth.requires(lambda: (auth.has_permission('create', 'datalogger')))
def link_indicator_to_qcvn(*args, **kwargs):
    try:
        qcvn_id = request.vars.qcvn_id
        qcvn_name = request.vars.qcvn_name
        qcvn_code = request.vars.qcvn_code
        qcvn_type_code = request.vars.qcvn_type_code
        qcvn_min_value = request.vars.qcvn_min_value
        qcvn_max_value = request.vars.qcvn_max_value
        qcvn_const_area_value = request.vars.qcvn_const_area_value
        indicator_id = request.vars.indicator
        tendency = request.vars.tendency
        preparing = request.vars.preparing
        exceed = request.vars.exceed
        indicator = db.indicators(indicator_id) or None
        qcvn = db.datalogger(qcvn_id) or None
        if not qcvn:
            return dict(success=False, message=T('QCVN is not existed!'))
        qcvn_type = qcvn.qcvn_type or const.STATION_TYPE['WASTE_WATER']['value']
        if not indicator:
            return dict(success=False, message=T('Indicator is not existed!'))
        unit = indicator.unit
        conditions = ((db.datalogger_command.qcvn_id == qcvn_id) &
                      (db.datalogger_command.indicator_id == indicator_id) &
                      (db.datalogger_command.qcvn_type == qcvn_type))
        existed = db(conditions).count(db.datalogger_command.id)
        if existed:
            return dict(success=False, message=T('Indicator is existed!'))
        db.datalogger_command.insert(qcvn_id=qcvn_id, qcvn_name=qcvn_name, qcvn_type=qcvn_type, qcvn_code=qcvn_code,
                                     qcvn_min_value=qcvn_min_value, qcvn_max_value=qcvn_max_value,
                                     qcvn_type_code=qcvn_type_code, qcvn_const_area_value=qcvn_const_area_value,
                                     indicator_id=indicator_id, tendency_value=tendency, preparing_value=preparing,
                                     exceed_value=exceed, unit=unit)
        return dict(success=True)
    except Exception as ex:
        return dict(success=False, message=str(ex))


################################################################################
# # @decor.requires_login()
@auth.requires(lambda: (auth.has_permission('view', 'datalogger')))
def popup_add_qcvn_detail():
    record = db.datalogger_command(request.args(0)) or None
    qcvn_id = request.vars.qcvn_id

    frm = SQLFORM(db.datalogger_command, record, _method='POST', hideerror=True, showid=False)
    frm.custom.widget.description['_rows'] = '4'

    if qcvn_id:
        db.datalogger_command.qcvn_id.requires = IS_IN_DB(db(db.datalogger.id == qcvn_id), db.datalogger.id,
                                                          db.datalogger.qcvn_name)
    return dict(frm=frm, qcvn_id=qcvn_id)


################################################################################
@service.json
@auth.requires(lambda: (auth.has_permission('create', 'datalogger') or auth.has_permission('edit', 'datalogger')))
def ajax_save_qcvn_detail(*args, **kwargs):
    try:
        # convert date manually 
        if not request.vars.id:
            db.datalogger_command.insert(**dict(request.vars))
        else:
            db(db.datalogger_command.id == request.vars.id).update(**dict(request.vars))

        return dict(success=True)
    except Exception as ex:
        logger.error(str(ex))
        return dict(success=False, message=str(ex))
