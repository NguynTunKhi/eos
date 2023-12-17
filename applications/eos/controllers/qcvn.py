# -*- coding: utf-8 -*-
###############################################################################
# Author : 
# Date   : 
# 
# Description : 
# 
###############################################################################

from applications.eos.services import station_indicator_service, request_create_station_indicator_service
from applications.eos.modules import const

if False:
    from gluon import *

    request = current.request
    response = current.response
    session = current.session
    cache = current.cache
    T = current.T
    db = current.db


@auth.requires(lambda: (auth.has_permission('create', 'qcvn') or auth.has_permission('edit', 'qcvn')))
def form():
    # If in Update mode, get equivallent record
    record = db.qcvn(request.args(0)) or None
    qcvn_id = request.args(0) or None
    msg = ''
    type = record.qcvn_type if record else ''

    # qcvn_kind = record.qcvn_kind if record else ''
    name = record.qcvn_name if record else ''
    frm = SQLFORM(db.qcvn, record, _method='POST', hideerror=True, showid=False, _id='frmMain')

    if frm.process(onvalidation=validate, detect_record_change=True, hideerror=True).accepted:
        session.flash = T('MSG_INFO_SAVE_SUCCESS')
        redirect(URL('index'))
    elif frm.record_changed:
        redirect(URL('home', 'error'))
    elif frm.errors:
        for item in frm.errors:
            msg += '%s: %s<br />' % (item, frm.errors[item])
    else:
        pass
        # response.flash = message.REQUEST_INPUT

    frm.custom.widget.qcvn_code['_maxlength'] = '64'
    frm.custom.widget.qcvn_description['_row'] = '7'
    indicators = db((db.indicators.id > 0) & (db.indicators.indicator_type == type)).select()
    qcvn_type_code = db(
        (db.qcvn_kind.id > 0) & (db.qcvn_kind.qcvn_kind_delete_flag == 0) & (db.qcvn_kind.qcvn_id == qcvn_id)).select(
        orderby=db.qcvn_kind.qcvn_kind_order)
    qcvn_have_factor_qcvn = db((db.qcvn.id > 0) & (db.qcvn.id == qcvn_id)).select()
    return dict(frm=frm, msg=XML(msg), type=type, name=name, qcvn_have_factor_qcvn=qcvn_have_factor_qcvn,
                qcvn_id=qcvn_id, indicators=indicators, qcvn_type_code=qcvn_type_code)


################################################################################
def validate(frm):
    # Check condion
    # Get control value by : frm.vars.ControlName
    # If validate fail : frm.errors.ControlName = some message
    pass


def call():
    return service()


################################################################################
@auth.requires(lambda: (auth.has_permission('view', 'qcvn')))
def index():
    return dict()


################################################################################
@service.json
@auth.requires(lambda: (auth.has_permission('view', 'qcvn')))
def get_list_qcvn(*args, **kwargs):
    try:
        iDisplayStart = int(request.vars.iDisplayStart)
        iDisplayLength = int(request.vars.iDisplayLength)
        s_search = request.vars.sSearch
        sometext = request.vars.sometext
        type = request.vars.type
        aaData = []
        limitby = (iDisplayStart, iDisplayLength + 1)  # Tuple dung de phan trang (vtri bat dau - chieu dai)

        conditions = (db.qcvn.id > 0)
        # Neu chuoi tim kiem khac rong thi them dieu kien truy van voi chuoi tim kiem
        if sometext:
            conditions &= ((db.qcvn.qcvn_code.contains(sometext)) |
                           (db.qcvn.qcvn_name.contains(sometext)) |
                           (db.qcvn.qcvn_subject.contains(sometext)) |
                           (db.qcvn.qcvn_description.contains(sometext)))
        if type:
            conditions &= (db.qcvn.qcvn_type == type)
        conditions &= (db.qcvn.status != const.SI_STATUS['DELETED']['value'])

        list_data = db(conditions).select(db.qcvn.id,
                                          db.qcvn.qcvn_code,
                                          db.qcvn.qcvn_type,
                                          db.qcvn.qcvn_name,
                                          db.qcvn.qcvn_subject,
                                          limitby=limitby,
                                          orderby=db.qcvn.qcvn_priority)
        # Tong so ban ghi khong thuc hien phan trang
        iTotalRecords = db(conditions).count()
        station_type = dict()
        for key, item in const.STATION_TYPE.iteritems():
            station_type[str(item['value'])] = T(item['name'])

        # Duyet tung phan tu trong mang du lieu vua truy van duoc
        for i, item in enumerate(list_data):
            aaData.append([
                A(str(iDisplayStart + 1 + i), _href=URL('form', args=[item.id])),
                A(item.qcvn_code, _href=URL('form', args=[item.id])),
                item.qcvn_name,
                station_type[str(item.qcvn_type)] if item.qcvn_type != '' and station_type.has_key(
                    str(item.qcvn_type)) else '',
                # station_type[str(item.qcvn_type)],
                item.qcvn_subject,
                INPUT(_group='0', _class='select_item', _type='checkbox', _value=item.id),
                item.id
            ])
        return dict(iTotalRecords=iTotalRecords, iTotalDisplayRecords=iTotalRecords, aaData=aaData, success=True)
    except Exception as ex:
        return dict(iTotalRecords=0, iTotalDisplayRecords=0, aaData=[], message=str(ex), success=False)


################################################################################
@service.json
@auth.requires(lambda: (auth.has_permission('delete', 'qcvn')))
def del_qcvn(*args, **kwargs):
    try:
        array_data = request.vars.ids
        list_ids = array_data.split(',')
        db(db.qcvn.id.belongs(list_ids)).update(status=const.SI_STATUS['DELETED']['value'])
        return dict(success=True)
    except Exception as ex:
        return dict(success=False, message=str(ex))


################################################################################
@service.json
@auth.requires(lambda: (auth.has_permission('view', 'qcvn')))
def get_qcvn_detail_by_qcvn(*args, **kwargs):
    try:
        qcvn_id = request.vars.qcvn_id
        aaData = []
        record = db.qcvn(qcvn_id) or None
        conditions = (db.qcvn_detail.id > 0) & (db.qcvn_detail.qcvn_id == qcvn_id)

        list_data = db(conditions).select()
        # Tong so ban ghi khong thuc hien phan trang
        iTotalRecords = len(list_data)
        iRow = 1
        colors = ['', 'blue', 'red', 'green', 'orange']

        # Duyet tung phan tu trong mang du lieu vua truy van duoc
        for item in list_data:
            url = URL('qcvn', 'popup_add_qcvn_detail', args=[item.id], vars={'qcvn_id': qcvn_id})
            aaData.append([
                str(iRow),
                record.qcvn_code,
                item.para_code,
                "%s%s%s%s%s%s%s" % ( \
                    "<a href='javascript: void(0);' class='btnAddNew' title='",
                    T('QCVN information'),
                    "' data-for='#hfQCVNDetailId'  data-callback='reloadDatatable_QCVNDetail()' \
                    data-url='", url, "'> ",
                    item.para_name,
                    "</a>"),
                "{:,}".format(item.minimum),
                "{:,}".format(item.maximum),
                item.unit
            ])

            iRow += 1
        return dict(iTotalRecords=iTotalRecords, iTotalDisplayRecords=iTotalRecords, aaData=aaData, success=True)
    except Exception, ex:
        return dict(iTotalRecords=0, iTotalDisplayRecords=0, aaData=[], message=str(ex), success=False)


################################################################################
@service.json
@auth.requires(lambda: (auth.has_permission('view', 'qcvn')))
def get_qcvn_detail_by_qcvnId(*args, **kwargs):
    try:
        iDisplayStart = int(request.vars.iDisplayStart)  # Vi tri bat dau lay du lieu
        iDisplayLength = int(request.vars.iDisplayLength)  # So luong ban ghi se lay toi da
        qcvn_id = request.vars.qcvn_id  # Chuoi tim kiem nhap tu form
        aaData = []  # Du lieu json se tra ve
        limitby = (iDisplayStart, iDisplayLength + 1)  # Tuple dung de phan trang (vtri bat dau - chieu dai)
        record = db.qcvn(qcvn_id) or None
        conditions = (db.qcvn_detail.id > 0)
        if qcvn_id:
            conditions &= (db.qcvn_detail.qcvn_id == qcvn_id) & (
                    db.qcvn_detail.status == const.SI_STATUS['IN_USE']['value']) \
                          & (db.qcvn_detail.expression_qcvn_indicator < 4)
        list_data = db(conditions).select(db.qcvn_detail.id,
                                          db.qcvn_detail.indicator_id,
                                          db.qcvn_detail.qcvn_type_code,
                                          db.qcvn_detail.have_factor_qcvn,
                                          db.qcvn_detail.qcvn_min_value,
                                          db.qcvn_detail.qcvn_max_value,
                                          db.qcvn_detail.qcvn_const_area_value,
                                          db.qcvn_detail.expression_qcvn_indicator,
                                          limitby=limitby,
                                          orderby=~db.qcvn_detail.id)
        # Tong so ban ghi khong thuc hien phan trang
        iTotalRecords = db(conditions).count()
        indicator_dict = common.get_indicator_dict()

        # List kind
        rowsKind = db(db.qcvn_kind.id > 0).select()
        resKind = {}
        for item in rowsKind:
            resKind[str(item.id)] = item.qcvn_kind

        # qcvn_kind_dict = common.get_qcvn_kind_dict()
        # print(res)
        # Thu tu ban ghi
        iRow = iDisplayStart + 1

        expression_qcvn_indicator = dict()
        for key, item in const.EXPRESSION_QCVN_INDICATOR.iteritems():
            expression_qcvn_indicator[item['value']] = T(item['text'])

        have_factor_qcvn = dict()
        for key, item in const.HAVE_FACTOR_QCVN.iteritems():
            have_factor_qcvn[item['value']] = T(item['text'])

        # Duyet tung phan tu trong mang du lieu vua truy van duoc
        for item in list_data:
            listA = [
                str(iRow),
                # item.qcvn_type_code,
                resKind[str(item.qcvn_type_code)] if item.qcvn_type_code and resKind.has_key(
                    str(item.qcvn_type_code)) else '',
                indicator_dict[str(item.indicator_id)] if item.indicator_id and indicator_dict.has_key(
                    str(item.indicator_id)) else '',
                have_factor_qcvn[item.have_factor_qcvn] if item.have_factor_qcvn else '-',
                expression_qcvn_indicator[item.expression_qcvn_indicator] if item.expression_qcvn_indicator else '-',
                item.qcvn_min_value,
                item.qcvn_max_value,
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
@auth.requires(lambda: (auth.has_permission('view', 'qcvn')))
def get_qcvn_kind_by_qcvnId(*args, **kwargs):
    try:
        iDisplayStart = int(request.vars.iDisplayStart)  # Vi tri bat dau lay du lieu
        iDisplayLength = int(request.vars.iDisplayLength)  # So luong ban ghi se lay toi da
        qcvn_id = request.vars.qcvn_id  # Chuoi tim kiem nhap tu form
        aaData = []  # Du lieu json se tra ve
        limitby = (iDisplayStart, iDisplayLength + 1)  # Tuple dung de phan trang (vtri bat dau - chieu dai)
        record = db.qcvn(qcvn_id) or None

        conditions = (db.qcvn_kind.qcvn_id == qcvn_id) & (db.qcvn_kind.qcvn_kind_delete_flag == 0)
        list_data = db(conditions).select(db.qcvn_kind.id,
                                          db.qcvn_kind.qcvn_kind,
                                          db.qcvn_kind.qcvn_kind_order,
                                          db.qcvn_kind.qcvn_kind_delete_flag,
                                          limitby=limitby,
                                          orderby=db.qcvn_kind.qcvn_kind_order)
        # Tong so ban ghi khong thuc hien phan trang
        iTotalRecords = db(conditions).count()
        indicator_dict = common.get_indicator_dict()
        # Thu tu ban ghi
        iRow = iDisplayStart + 1

        # Duyet tung phan tu trong mang du lieu vua truy van duoc
        for item in list_data:
            listA = [
                str(iRow),
                item.qcvn_kind,
                item.qcvn_kind_order,
                # T('QCVN_KIND_ACTIVE') if item.qcvn_kind_delete_flag == 0 else T('QCVN_KIND_DELETE'),
                INPUT(_group='1', _class='select_item', _type='checkbox', _value=item.id)
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
        qcvn_details = db(db.qcvn_detail.qcvn_id == qcvn_id).select(db.qcvn_detail.id,
                                                                    db.qcvn_detail.indicator_id,
                                                                    db.qcvn_detail.qcvn_type_code,
                                                                    db.qcvn_detail.qcvn_min_value,
                                                                    db.qcvn_detail.qcvn_max_value,
                                                                    db.qcvn_detail.qcvn_const_area_value)
        for i in range(len(qcvn_details)):
            qcvn_details[i].id = str(qcvn_details[i].id)

        return dict(qcvn_details=qcvn_details, success=True)
    except Exception as ex:
        return dict(message=str(ex), success=False)


################################################################################
@service.json
def get_list_qcvn_kind_details(*args, **kwargs):
    """
    Return QCVN kinds and QCVN details by submitted QCVN id.

    qcvn_details: qcvn_kinds of id
    type_code: qcvn_detail of id
    """
    try:
        qcvn_id = request.vars.qcvn_id  # Chuoi tim kiem nhap tu form
        # Get all QCVN detail
        # qcvn_details =  db(db.qcvn_detail.qcvn_id == qcvn_id).select(  db.qcvn_detail.id,
        #                                     db.qcvn_detail.indicator_id,
        #                                     db.qcvn_detail.qcvn_type_code,
        #                                     db.qcvn_detail.qcvn_min_value,
        #                                     db.qcvn_detail.qcvn_max_value,
        #                                     db.qcvn_detail.qcvn_const_area_value)

        #  Get QCVN kind by QCVN id
        station_id = request.vars.station_id
        qcvn_kinds = db(
            (db.qcvn_kind.id > 0) &
            (db.qcvn_kind.qcvn_kind_delete_flag == 0) &
            (db.qcvn_kind.qcvn_id == qcvn_id)
        ).select(orderby=db.qcvn_kind.qcvn_kind_order)
        for i in range(len(qcvn_kinds)):
            qcvn_kinds[i].id = str(qcvn_kinds[i].id)
            qcvn_kinds[i].custom = 15

        #  Get QCVN detail by QCVN id
        type_code = []
        indicators = []
        if qcvn_id != "":
            type_code = db(
                (db.qcvn_detail.id > 0) &
                (db.qcvn_detail.qcvn_id == qcvn_id)
            ).select()
            indicator_ids = set()
            for i in range(len(type_code)):
                type_code[i].id = str(type_code[i].id)
                indicator_ids.add(type_code[i].indicator_id)
                indicators = db(db.indicators.id.belongs(indicator_ids)).select()
        if qcvn_id =="-999":
            indicators = db((db.indicators.id > 0)).select()

        for indi in indicators:
            indi.id = str(indi.id)
        station = db.stations(station_id) or None
        if not station:
            return dict(success=False, message=T('Station does not exist!'))

        unlinked_station_indicators = station_indicator_service.StationIndicator(db, T). \
            filter_unlinked_indicators(indicators, station)

        return dict(qcvn_details=qcvn_kinds, type_code=type_code, indicators=unlinked_station_indicators, success=True)
    except Exception as ex:
        return dict(message=str(ex), success=False)


@service.json
def get_list_qcvn_kind_details_for_request_create_station(*args, **kwargs):
    """
    Return QCVN kinds and QCVN details by submitted QCVN id.

    qcvn_details: qcvn_kinds of id
    type_code: qcvn_detail of id
    """
    try:
        qcvn_id = request.vars.qcvn_id
        request_create_station_id = request.vars.request_create_station_id

        qcvn_kinds = db(
            (db.qcvn_kind.id > 0) &
            (db.qcvn_kind.qcvn_kind_delete_flag == 0) &
            (db.qcvn_kind.qcvn_id == qcvn_id)
        ).select(orderby=db.qcvn_kind.qcvn_kind_order)
        for i in range(len(qcvn_kinds)):
            qcvn_kinds[i].id = str(qcvn_kinds[i].id)
            qcvn_kinds[i].custom = 15

        type_code = []
        indicators = []
        if qcvn_id != "":
            type_code = db(
                (db.qcvn_detail.id > 0) &
                (db.qcvn_detail.qcvn_id == qcvn_id)
            ).select()
            indicator_ids = set()
            for i in range(len(type_code)):
                type_code[i].id = str(type_code[i].id)
                indicator_ids.add(type_code[i].indicator_id)
                indicators = db(db.indicators.id.belongs(indicator_ids)).select()
        if qcvn_id =="-999":
            indicators = db((db.indicators.id > 0)).select()

        for indi in indicators:
            indi.id = str(indi.id)
        request_create_station = db.request_create_stations(request_create_station_id) or None
        if not request_create_station:
            return dict(success=False, message=T('Request Create Station does not exist!'))

        unlinked_station_indicators = request_create_station_indicator_service.RequestCreateStationIndicator(db, T). \
            filter_unlinked_indicators(indicators, request_create_station)

        return dict(qcvn_details=qcvn_kinds, type_code=type_code, indicators=unlinked_station_indicators, success=True)
    except Exception as ex:
        return dict(message=str(ex), success=False)


################################################################################
@service.json
def get_list_qcvn_station_kind_details(*args, **kwargs):
    try:
        qcvn_id = request.vars.qcvn_id  # Chuoi tim kiem nhap tu form
        station_id = request.vars.station_id
        # Get all QCVN detail
        # qcvn_details =  db(db.qcvn_detail.qcvn_id == qcvn_id).select(  db.qcvn_detail.id,
        #                                     db.qcvn_detail.indicator_id,
        #                                     db.qcvn_detail.qcvn_type_code,
        #                                     db.qcvn_detail.qcvn_min_value,
        #                                     db.qcvn_detail.qcvn_max_value,
        #                                     db.qcvn_detail.qcvn_const_area_value)

        qcvn_kinds = db(
            (db.qcvn_station_kind.id > 0) &
            (db.qcvn_station_kind.station_id == station_id) &
            (db.qcvn_station_kind.qcvn_id == qcvn_id)
        ).select(orderby=db.qcvn_station_kind.id)

        for i in range(len(qcvn_kinds)):
            qcvn_kinds[i].id = str(qcvn_kinds[i].id)
            qcvn_kind_details = db.qcvn_kind(qcvn_kinds[i].qcvn_kind_id) or None

            if qcvn_kind_details:
                qcvn_kinds[i].qcvn_kind_name = qcvn_kind_details.qcvn_kind
            else:
                qcvn_kinds[i].qcvn_kind_name = '-'

            # indicator = db.indicators(qcvn_details[i].qcvn_type_code) or None

            # if qcvn_details[i].qcvn_type_code :
            #     qcvn_kind_details = db.qcvn_kind(qcvn_details[i].qcvn_type_code) or None
            #     if qcvn_kind_details :
            #         qcvn_details[i].qcvn_type_code = str(qcvn_kind_details.qcvn_kind)
            #     else :
            #         qcvn_details[i].qcvn_type_code = ''

        return dict(qcvn_details=qcvn_kinds, success=True)
    except Exception as ex:
        return dict(message=str(ex), success=False)


################################################################################
@service.json
def get_qcvn_detail(*args, **kwargs):
    try:
        id = request.vars.id
        qcvn_detail = db.qcvn_detail(id) or None
        return dict(qcvn_detail=qcvn_detail, success=True)
    except Exception as ex:
        return dict(message=str(ex), success=False)


################################################################################
@service.json
@auth.requires(lambda: (auth.has_permission('create', 'qcvn')))
def link_indicator_to_qcvn(*args, **kwargs):
    try:
        qcvn_id = request.vars.qcvn_id
        qcvn_name = request.vars.qcvn_name
        qcvn_code = request.vars.qcvn_code
        have_factor_qcvn = request.vars.have_factor_qcvn
        if have_factor_qcvn != '':
            have_factor_qcvn = int(have_factor_qcvn)
        qcvn_type_code = request.vars.qcvn_type_code
        qcvn_min_value = request.vars.qcvn_min_value
        qcvn_max_value = request.vars.qcvn_max_value
        qcvn_const_area_value = request.vars.qcvn_const_area_value
        indicator_id = request.vars.indicator
        tendency = request.vars.tendency
        preparing = request.vars.preparing
        exceed = request.vars.exceed
        submit_type = int(request.vars.submit_type)
        expression_qcvn_indicator = int(request.vars.expression_qcvn_indicator)
        indicator = db.indicators(indicator_id) or None
        qcvn = db.qcvn(qcvn_id) or None
        if not qcvn:
            return dict(success=False, message=T('QCVN is not existed!'))
        qcvn_type = qcvn.qcvn_type or const.STATION_TYPE['WASTE_WATER']['value']
        if not indicator:
            return dict(success=False, message=T('Indicator is not existed!'))
        unit = indicator.unit
        conditions = ((db.qcvn_detail.qcvn_id == qcvn_id) &
                      (db.qcvn_detail.indicator_id == indicator_id) &
                      (db.qcvn_detail.qcvn_type_code == qcvn_type_code) &
                      (db.qcvn_detail.status == const.SI_STATUS['IN_USE']['value']) &
                      (db.qcvn_detail.qcvn_type == qcvn_type))
        existed = db(conditions).count(db.qcvn_detail.id)
        if existed & (submit_type == 0):
            # return dict(success=False, message=T('Indicator is existed, are you update?'))
            return dict(success=True, success_type=1)

        if (submit_type == 1) | ~existed:
            conditionsUpdate = ((db.qcvn_detail.qcvn_id == qcvn_id) &
                                (db.qcvn_detail.indicator_id == indicator_id) &
                                (db.qcvn_detail.qcvn_type_code == qcvn_type_code) &
                                (db.qcvn_detail.qcvn_type == qcvn_type));
            db.qcvn_detail.update_or_insert(conditionsUpdate, qcvn_id=qcvn_id, qcvn_name=qcvn_name, qcvn_type=qcvn_type,
                                            qcvn_code=qcvn_code, qcvn_min_value=qcvn_min_value,
                                            qcvn_max_value=qcvn_max_value,
                                            qcvn_type_code=qcvn_type_code, qcvn_const_area_value=qcvn_const_area_value,
                                            indicator_id=indicator_id, have_factor_qcvn=have_factor_qcvn,
                                            tendency_value=tendency, preparing_value=preparing,
                                            exceed_value=exceed, unit=unit, status=const.SI_STATUS['IN_USE']['value'],
                                            expression_qcvn_indicator=expression_qcvn_indicator)

        qcvn_kind_id = db((db.qcvn_kind.id > 0) & (db.qcvn_kind.qcvn_id == qcvn_id)).select()
        ids = []
        for row in qcvn_kind_id:
            ids.append(row.id)
        qcvn_station_kind = db(
            (db.qcvn_station_kind.id > 0) & (db.qcvn_station_kind.qcvn_kind_id.belongs(ids))).select()
        qcvn_kind_name = db((db.qcvn_kind.qcvn_id == qcvn_id) &
                            (db.qcvn_kind.id == qcvn_type_code)).select(db.qcvn_kind.qcvn_kind).first().qcvn_kind
        if qcvn_station_kind:
            for item in qcvn_station_kind:

                # qcvn_detail = db(
                #     (db.qcvn_detail.id > 0) & (db.qcvn_detail.qcvn_id == qcvn_id) & (
                #             db.qcvn_detail.indicator_id == indicator_id) & (
                #             db.qcvn_detail.qcvn_type_code == qcvn_type_code) & (
                #             db.qcvn_detail.status == const.SI_STATUS['IN_USE']['value'])).select()
                qcvn_min_value_indicator = ''
                qcvn_max_value_indicator = ''
                # if qcvn_detail:
                #     qcvn_detail = qcvn_detail.first()
                if have_factor_qcvn == 1:
                    if qcvn_min_value:
                        qcvn_min_value_indicator = float(qcvn_min_value) * float(
                            item.qcvn_detail_const_area_value_1) * float(item.qcvn_detail_const_area_value_2)
                    if qcvn_max_value:
                        qcvn_max_value_indicator = float(qcvn_max_value) * float(
                            item.qcvn_detail_const_area_value_1) * float(item.qcvn_detail_const_area_value_2)
                else:
                    if qcvn_min_value:
                        qcvn_min_value_indicator = float(qcvn_min_value)
                    if qcvn_max_value:
                        qcvn_max_value_indicator = float(qcvn_max_value)

                # Update
                stations_qcvn = db(
                    (db.station_indicator.station_id == item.station_id) &
                    (db.station_indicator.qcvn_id == qcvn_id) &
                    (db.station_indicator.indicator_id == indicator_id)).select(db.station_indicator.ALL)
                if stations_qcvn:
                    for row in stations_qcvn:
                        row.update_record(
                            qcvn_code=qcvn_code,
                            qcvn_detail_type_code=qcvn_kind_name,
                            qcvn_detail_min_value=qcvn_min_value_indicator,
                            qcvn_detail_max_value=qcvn_max_value_indicator)

                    # db.station_indicator.update_or_insert(
                    #     (db.station_indicator.qcvn_id == qcvn_id) &
                    #     (db.station_indicator.indicator_id == indicator_id) & (
                    #             db.station_indicator.status == const.SI_STATUS['IN_USE']['value']),
                    #     qcvn_code=qcvn_code,
                    #     qcvn_detail_type_code=qcvn_kind_name,
                    #     qcvn_detail_min_value=qcvn_min_value_indicator,
                    #     qcvn_detail_max_value=qcvn_max_value_indicator)
        return dict(success=True)
    except Exception as ex:
        return dict(success=False, message=str(ex))


################################################################################
@service.json
@auth.requires(lambda: (auth.has_permission('delete', 'master_qcvn')))
def delete_qcvn_detail_by_qcvnid_indicator(*args, **kwargs):
    try:
        array_data = request.vars.ids
        list_ids = array_data.split(',')
        db(db.qcvn_detail.id.belongs(list_ids)).update(status=const.SI_STATUS['DELETED']['value'])
        return dict(success=True)
    except Exception as ex:
        return dict(success=False, message=str(ex))


################################################################################
@service.json
@auth.requires(lambda: (auth.has_permission('create', 'qcvn')))
def link_kind_to_qcvn(*args, **kwargs):
    try:
        qcvn_id = request.vars.qcvn_id
        qcvn_name = request.vars.qcvn_name
        qcvn_code = request.vars.qcvn_code
        qcvn_type_code = request.vars.qcvn_type_code
        qcvn_kind = request.vars.qcvn_kind
        qcvn_kind_order = request.vars.qcvn_kind_order
        qcvn = db.qcvn(qcvn_id) or None
        if not qcvn:
            return dict(success=False, message=T('QCVN is not existed!'))
        qcvn_type = qcvn.qcvn_type or const.STATION_TYPE['WASTE_WATER']['value']

        conditions = ((db.qcvn_kind.qcvn_id == qcvn_id) &
                      (db.qcvn_kind.qcvn_kind == qcvn_kind) & (db.qcvn_kind.qcvn_kind_delete_flag == 0))
        existed = db(conditions).count(db.qcvn_kind.id)
        if existed:
            return dict(success=False, message=T('QCVN Kind is existed!'))
        else:
            conditions = ((db.qcvn_kind.qcvn_id == qcvn_id) &
                          (db.qcvn_kind.qcvn_kind == qcvn_kind))
            existedDelete = db(conditions).count(db.qcvn_kind.id)
            # if existedDelete :
            db.qcvn_kind.update_or_insert(conditions, qcvn_id=qcvn_id, qcvn_type=qcvn_type, qcvn_code=qcvn_code,
                                          qcvn_kind=qcvn_kind,
                                          qcvn_kind_order=qcvn_kind_order, qcvn_kind_delete_flag=0)
            # else :
            #     db.qcvn_kind.insert(qcvn_id=qcvn_id, qcvn_type=qcvn_type, qcvn_code=qcvn_code, qcvn_kind=qcvn_kind,
            #                         qcvn_kind_order=qcvn_kind_order, qcvn_kind_delete_flag=0)

        return dict(success=True)
    except Exception as ex:
        return dict(success=False, message=str(ex))


################################################################################
@service.json
@auth.requires(lambda: (auth.has_permission('create', 'qcvn') or auth.has_permission('edit', 'qcvn')))
def qcvn_kind_update(*args, **kwargs):
    try:
        print(request.vars)
        # convert date manually
        array_data = request.vars.ids
        list_ids = array_data.split(',')
        if list_ids:
            for id in list_ids:
                db(db.qcvn_kind.id == id).update(**dict(request.vars))

        return dict(success=True)
    except Exception as ex:
        logger.error(str(ex))
        return dict(success=False, message=str(ex))


################################################################################
# # @decor.requires_login()
@auth.requires(lambda: (auth.has_permission('view', 'qcvn')))
def popup_add_qcvn_detail():
    record = db.qcvn_detail(request.args(0)) or None
    qcvn_id = request.vars.qcvn_id

    frm = SQLFORM(db.qcvn_detail, record, _method='POST', hideerror=True, showid=False)
    frm.custom.widget.description['_rows'] = '4'

    if qcvn_id:
        db.qcvn_detail.qcvn_id.requires = IS_IN_DB(db(db.qcvn.id == qcvn_id), db.qcvn.id, db.qcvn.qcvn_name)
    return dict(frm=frm, qcvn_id=qcvn_id)


################################################################################
@service.json
@auth.requires(lambda: (auth.has_permission('create', 'qcvn') or auth.has_permission('edit', 'qcvn')))
def ajax_save_qcvn_detail(*args, **kwargs):
    try:
        # convert date manually 
        if not request.vars.id:
            db.qcvn_detail.insert(**dict(request.vars))
        else:
            db(db.qcvn_detail.id == request.vars.id).update(**dict(request.vars))

        return dict(success=True)
    except Exception as ex:
        logger.error(str(ex))
        return dict(success=False, message=str(ex))
