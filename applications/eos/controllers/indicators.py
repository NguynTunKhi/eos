import json
from applications.eos.middleware import basic_auth
from applications.eos.services import indicator_service
from applications.eos.common import response as http_response


if False:
    from gluon import *
    request = current.request
    response = current.response
    session = current.session
    cache = current.cache
    T = current.T
    pydb = pydb



@auth.requires(lambda: (auth.has_permission('create', 'indicators') or auth.has_permission('edit', 'indicators')))
def form():
    # If in Update mode, get equivallent record
    record = db.indicators(request.args(0)) or None
    station_id = request.args(0) or None
    msg = ''

    frm = SQLFORM(db.indicators, record, _method='POST', hideerror=True, showid=False, _id='frmMain')

    if frm.process(onvalidation=validate, detect_record_change=True, hideerror=True).accepted:
        if record:
            if record.order_no is None:
                record.update_record(order_no=0)
        session.flash = T('MSG_INFO_SAVE_SUCCESS')
        redirect(URL('index'))
    elif frm.record_changed:
        redirect(URL('home', 'error'))
    elif frm.errors:
        for item in frm.errors:
            msg += '%s: %s<br />' % (T(item), frm.errors[item])
    else:
        pass
        # response.flash = message.REQUEST_INPUT

    return dict(frm=frm, msg=XML(msg), station_id=station_id)


################################################################################
def validate(frm):
    # Check condion
    # Get control value by : frm.vars.ControlName
    # If validate fail : frm.errors.ControlName = some message
    indicator = frm.vars.indicator
    indicator_type = frm.vars.indicator_type
    id = request.args(0) or None
    is_exist = db((db.indicators.id != id) & (db.indicators.indicator == indicator) & (
            db.indicators.indicator_type == indicator_type)).count()

    if is_exist:
        frm.errors.indicator = T('This indicator is already existed!')

    pass


def call():
    return service()


################################################################################
def index():
    return dict()


################################################################################
@service.json
@auth.requires(lambda: (auth.has_permission('view', 'indicators')))
def get_list_indicators(*args, **kwargs):
    import json
    try:
        iDisplayStart = int(request.vars.iDisplayStart)  # Vi tri bat dau lay du lieu
        iDisplayLength = int(request.vars.iDisplayLength)  # So luong ban ghi se lay toi da
        limitby = (iDisplayStart, iDisplayLength + 1)  # Tuple dung de phan trang (vtri bat dau - chieu dai)

        s_search = request.vars.sSearch
        type = request.vars.type
        sometext = request.vars.sometext
        aaData = []

        conditions = (db.indicators.id > 0)
        # Neu chuoi tim kiem khac rong thi them dieu kien truy van voi chuoi tim kiem
        if sometext:
            conditions &= (db.indicators.indicator.contains(sometext) |
                           db.indicators.source_name.contains(sometext) |
                           db.indicators.unit.contains(sometext))
        if type:
            conditions &= (db.indicators.indicator_type == type)

        list_data = db(conditions).select(db.indicators.id,
                                          db.indicators.indicator,
                                          db.indicators.indicator_type,
                                          db.indicators.unit,
                                          db.indicators.tendency_value,
                                          db.indicators.preparing_value,
                                          db.indicators.exceed_value,
                                          db.indicators.order_no,
                                          orderby=~db.indicators.order_no,
                                          limitby=limitby)
        # Tong so ban ghi khong thuc hien phan trang
        iTotalRecords = db(conditions).count()
        iRow = iDisplayStart + 1
        indicator_type = dict(db.indicators.indicator_type.requires.options())

        # Duyet tung phan tu trong mang du lieu vua truy van duoc
        for i, item in enumerate(list_data):
            # id = str(item.id) + "xxx"
            aaData.append([
                str(iRow),
                A(item.indicator, _href=URL('form', args=[item.id])),
                indicator_type.get(str(item.indicator_type)),
                # item.source_name,
                item.unit,
                item.order_no,
                # SPAN(item.tendency_value, _style="background:#99CC00; color:white", _class="badge"),
                # SPAN(item.preparing_value, _style="background:#FF9900; color:white", _class="badge"),
                # SPAN(item.exceed_value, _style="background:#FF0000; color:white", _class="badge"),
                # INPUT(_group = '0', _class = 'select_item', _type = 'checkbox', _value = item.id),
                # item.id,
                '<div data-toggle="tooltip" data-placement="left" title="Xóa thông số" data-original-title="Xóa thông số" > <i class ="fa fa-trash fa-white" style="color:red;font-size: 1.1em;cursor:pointer" onclick="handleDelete(this)" id="' + str(
                    item.id) + '" > </i></div>'
                ,
            ])
            iRow += 1

        return dict(iTotalRecords=iTotalRecords, iTotalDisplayRecords=iTotalRecords, aaData=aaData, success=True)
    except Exception, ex:
        return dict(iTotalRecords=0, iTotalDisplayRecords=0, aaData=[], message=str(ex), success=False)


#################################################################
@service.json
@auth.requires(lambda: (auth.has_permission('view', 'indicators')))
def get_indicator_info(*args, **kwargs):
    try:
        indicator_id = request.vars.indicator_id
        qcvn_kind_id = request.vars.qcvn_kind_id
        qcvn_id = request.vars.qcvn_id
        cons_1, cons_2 = 0, 0
        try:
            if request.vars.cons_1:
                cons_1 = float(request.vars.cons_1)
            if request.vars.cons_2:
                cons_2 = float(request.vars.cons_2)
            pass
        except:
            pass

        tendency = preparing = exceed = ''
        qcvn_min_value_indicator = qcvn_max_value_indicator = ''
        indicator = db.indicators(indicator_id)
        qcvn_detail = []
        if indicator:
            tendency_value = indicator.tendency_value
            preparing_value = indicator.preparing_value
            exceed_value = indicator.exceed_value
            source_name = indicator.source_name

            qcvn_detail = db(
                (db.qcvn_detail.id > 0) & (db.qcvn_detail.qcvn_id == qcvn_id) & (
                        db.qcvn_detail.indicator_id == indicator_id) & (
                        db.qcvn_detail.qcvn_type_code == qcvn_kind_id) & (
                        db.qcvn_detail.status == const.SI_STATUS['IN_USE']['value'])).select()

            if qcvn_detail:
                qcvn_detail = qcvn_detail.first()
                print(qcvn_detail)
                if qcvn_detail.have_factor_qcvn == 1:
                    if qcvn_detail.qcvn_min_value:
                        qcvn_min_value_indicator = float(qcvn_detail.qcvn_min_value) * cons_1 * cons_2
                    if qcvn_detail.qcvn_max_value:
                        qcvn_max_value_indicator = float(qcvn_detail.qcvn_max_value) * cons_1 * cons_2
                else:
                    if qcvn_detail.qcvn_min_value:
                        qcvn_min_value_indicator = float(qcvn_detail.qcvn_min_value)
                    if qcvn_detail.qcvn_max_value:
                        qcvn_max_value_indicator = float(qcvn_detail.qcvn_max_value)

        return dict(success=True, tendency_value=tendency_value, preparing_value=preparing_value,
                    exceed_value=exceed_value, source_name=source_name, qcvn_detail=qcvn_detail,
                    qcvn_min_value_indicator=qcvn_min_value_indicator,
                    qcvn_max_value_indicator=qcvn_max_value_indicator)
    except Exception as ex:
        return dict(success=False, message=str(ex))


@service.json
def delete_indicator(*args, **kwargs):
    id = request.vars.id
    check_exist = db(db.station_indicator.indicator_id == id).select(db.station_indicator._id)
    if (check_exist):
        return dict(success=True, data=True)
    else:
        db(db.indicators._id==id).delete()
        return dict(success=True, data=False)


# For API version

# list_indicators_id_gt api with basic auth deploy on tw for elt sync indicator local dp call to get list indicator
# with greater
# than request id
#
# @service.json
# @request.wsgi.middleware(basic_auth.BasicAuthMiddleware)
# def list_indicators_id_gt():
#     response.headers['Content-Type'] = 'application/json'
#     try:
#         params = request.get_vars
#         indicator_id = params['indicator_id']
#         if indicator_id is None or indicator_id == "":
#             return json.dumps(http_response.Response(
#                 code=400,
#                 message=T('invalid request'),
#                 data=None,
#             ).to_dict())
#         data = indicator_service.IndicatorService(pydb, current.T).get_indicators_id_gt(id=indicator_id)
#         return json.dumps(http_response.Response(
#             code=200,
#             message='success',
#             data=data,
#         ).to_dict())
#     except ValueError as ex:
#         return json.dumps(http_response.Response(
#             code=400,
#             message=ex.__str__(),
#             data=None,
#         ).to_dict())
