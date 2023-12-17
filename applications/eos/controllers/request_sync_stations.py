import json
from applications.eos.services.request_sync_station_service import *
from applications.eos.common import response as http_response
from applications.eos.middleware import basic_auth
from applications.eos.package import request_sync_station_pack
from applications.eos.repo.ftp_repo import FtpRepo
from applications.eos.common import my_const

if False:
    from gluon import *

    request = current.request
    response = current.response
    session = current.session
    cache = current.cache
    T = current.T
    pydb = pydb
    db = current.db
    auth = current.auth


def call():
    return service()


# API for local dp
# sync_created_stations_local_dp api for local dp call to sync created station(on local dp) to tw
@service.json
@auth.requires(lambda: (auth.has_permission('create', 'request_sync_stations')))
def sync_created_stations_local_dp(*args, **kwargs):
    try:
        array_data = request.vars.ids
        list_ids_int = array_data.split(',')
        list_ids_hex = []
        for item in list_ids_int:
            station_id_hex = format(int(item), "02X")
            list_ids_hex.append(station_id_hex)
        response_body = RequestSyncStationService(mongo_client=pydb, T=T).sync_created_stations_local_dp(list_ids_hex)
        return response_body
    except http.HttpException as ex:
        return http_response.Response(
            code=ex.http_code,
            message=ex.message,
            data=None,
        ).to_dict()


# API for tw

## Internal API
# create_sync_station_request api with basic auth deploy on tw for local dp call to create sync_station_request
@request.wsgi.middleware(basic_auth.BasicAuthMiddleware)
def create_sync_station_request():
    response.headers['Content-Type'] = 'application/json'
    try:
        try:
            request_body_str = json.loads(request.body.read())
            request_body_object = json.loads(request_body_str)
            map_ids = RequestSyncStationService(pydb, T).create_request_sync_created_stations(request_body_object)
            return json.dumps(http_response.Response(
                code=200,
                message='success',
                data=map_ids,
            ).to_dict())
        except TypeError as ex:
            return json.dumps(http_response.Response(
                code=400,
                message="parse request fail: " + ex.__str__(),
                data=None,
            ).to_dict())
    except http.HttpException as ex:
        return json.dumps(http_response.Response(
            code=ex.http_code,
            message=ex.message,
            data=None,
        ).to_dict())

# get_request_sync_stations_approve_status api with basic auth deploy on tw for local dp call to get approve status and reason
@request.wsgi.middleware(basic_auth.BasicAuthMiddleware)
def get_request_sync_stations_approve_status():
    response.headers['Content-Type'] = 'application/json'
    try:
        try:
            request_body_str = json.loads(request.body.read())
            request_body_object = json.loads(request_body_str)
            map_ids = RequestSyncStationService(pydb, T).get_request_sync_stations_approve_status(request_body_object)
            return json.dumps(http_response.Response(
                code=200,
                message='success',
                data=map_ids,
            ).to_dict())
        except TypeError as ex:
            return json.dumps(http_response.Response(
                code=400,
                message="parse request fail: " + ex.__str__(),
                data=None,
            ).to_dict())
    except http.HttpException as ex:
        return json.dumps(http_response.Response(
            code=ex.http_code,
            message=ex.message,
            data=None,
        ).to_dict())


## App API

def index():
    return dict()


@service.json
@auth.requires(lambda: (auth.has_permission('approve', 'request_sync_stations')))
# For approve/reject request sync station
def approve_request_sync_station(*args, **kwargs):
    try:
        try:
            request_sync_station_id = request.vars.request_sync_station_id
            approve_action = request.vars.approve_action
            reason = request.vars.reason
            request_pack = request_sync_station_pack.ApproveRequestIndicator(request_sync_station_id,
                                                                             int(approve_action), reason)
        except TypeError as ex:
            return json.dumps(http_response.Response(
                code=400,
                message="parse request fail: " + ex.__str__(),
                data=None,
            ).to_dict())
        RequestSyncStationService(pydb, T).approve_request_sync_station(request_pack)
        return http_response.Response(
            code=200,
            message='success',
            data=None
        ).to_dict()
    except http.HttpException as ex:
        return http_response.Response(
            code=ex.http_code,
            message=ex.message,
            data=None,
        ).to_dict()


# For list request sync station
@service.json
@auth.requires(lambda: (auth.has_permission('view', 'request_sync_stations')))
def list_request_sync_stations(*args, **kwargs):
    response.headers['Content-Type'] = 'application/json'
    try:
        try:
            i_type = request.vars.type
            int_i_type = None
            if i_type != '':
                int_i_type = int(i_type)
            idisplay_start = int(request.vars.iDisplayStart)
            idisplay_length = int(request.vars.iDisplayLength)
            page = int(idisplay_start / idisplay_length) + 1
            page_size = idisplay_length

            approve_status_raw = request.vars.approve_status
            if approve_status_raw == "":
                approve_status = None
            else:
                approve_status = int(approve_status_raw)
            some_text = request.vars.sometext
            request_pack = request_sync_station_pack.RequestListRequestSyncStation(keyword=some_text,
                                                                                   station_type=int_i_type,
                                                                                   page=page,
                                                                                   page_size=page_size,
                                                                                   approve_status=approve_status)
        except TypeError as ex:
            return json.dumps(http_response.Response(
                code=400,
                message="parse request fail: " + ex.__str__(),
                data=None,
            ).to_dict())
        resp = RequestSyncStationService(pydb, T).list_request_sync_stations(request_pack)
        return http_response.Response(
            code=200,
            message='success',
            data=resp.data,
            total=resp.total,
            page=resp.page,
            page_size=resp.page_size,
        ).to_dict()
    except http.HttpException as ex:
        return http_response.Response(
            code=ex.http_code,
            message=ex.message,
            data=None,
        ).to_dict()


@auth.requires(
    lambda: (auth.has_permission('view', 'request_sync_stations') or auth.has_permission('approve', 'request_sync_stations')))
def form():
    db = current.db
    ftp_repo = FtpRepo(db)
    province = ""
    data_request_sync_station_id = request.args(0)
    record = db.request_sync_stations(data_request_sync_station_id) or None
    request_sync_station_id = request.args(0) or None
    type = record.station_type if record else ''
    name = record.station_name if record else ''
    implement_agency_ra = record.implement_agency_ra if record else ''
    period_ra = record.period_ra if record else ''

    ftp_list = ftp_repo.get_all(auth)
    pwd = record.pwd if record else ''
    mqtt_pwd = record.mqtt_pwd if record else ''
    ftp_last_file_name_res = record.last_file_name if record else ''
    ftp_folder_path_res = record.data_folder if record else ''
    ftp_id_res = record.ftp_id if record else ''
    str_area_names = ""
    if record.area_names:
        str_area_names = ', '.join([str(x) for x in record.area_names])
    i_area_names = INPUT(_class='form-control', _type='text', _name='area_names', _value=str_area_names, value=str_area_names)

    code = request.vars.station_code
    msg = ''
    frm = SQLFORM(db.request_sync_stations, record, _method='POST', hideerror=True, showid=False, _id='frmMain')

    indicators, qcvns, equipments, alarm, qcvn_station_kind, qcvn_station_kind_list_by_qcvn, \
        qcvn_const_value_by_qcvn, datalogger, datalogger_command_list, data_send = [], [], []   , [], [], [], [], [], [], []
    # Get Station alarm info
    list_status_data_send = []
    current_send_status = 0
    curent_send_name = ''
    agents = db(db.agents.id > 0).select()
    if request_sync_station_id:
        # Get all indicators to fill in dropdown
        # indicators = db((db.indicators.id > 0) & (db.indicators.indicator_type == type)).select()
        # Get all QCVN to fill in dropdown
        station_type = record.station_type
        qcvns = db((db.qcvn.id > 0) & (db.qcvn.qcvn_type == record.station_type)).select(db.qcvn.id, db.qcvn.qcvn_code,
                                                                                         db.qcvn.qcvn_const_value)

    # all_records = db().select(db.request_sync_station_indicator.ALL)
    #
    # for record in all_records:
    #     # Do something with the record
    #     print(record)

    res_ftp_folder_path = ""
    if request_sync_station_id:
        folder_path = ["NuocThai", "NuocMat", "NuocNgam", "KhiThai", "KhongKhi"]
        if record.station_code != "" or record.station_code != None:
            res_ftp_folder_path = "/".join(["", folder_path[record.station_type], record.station_code])
        else:
            res_ftp_folder_path = "/".join(["", folder_path[record.station_type]])
    province = db.provinces(db.provinces.id == record.province_id)
    provinces = dict()
    if os.getenv(my_const.APP_SIDE) == my_const.APP_SIDE_LOCAL_DP:
        provinces = db(db.provinces.default == 1).select()
    else:
        provinces = db(db.provinces.id > 0).select()
    res = dict(frm=frm, msg=XML(msg),
               request_sync_station_id=request_sync_station_id,
               pwd=pwd,
               mqtt_pwd='' if mqtt_pwd is None else mqtt_pwd,
               type=type,
               name=name,
               code=code,
               i_area_names=i_area_names,
               implement_agency_ra=implement_agency_ra,
               period_ra=period_ra,
               indicators=indicators,
               equipments=equipments,
               qcvns=qcvns,
               qcvn_station_kind=qcvn_station_kind,
               qcvn_station_kind_list_by_qcvn=qcvn_station_kind_list_by_qcvn,
               qcvn_const_value_by_qcvn=qcvn_const_value_by_qcvn,
               datalogger=datalogger,
               type_datalogger=const.TYPE_SAMPLING,
               datalogger_command_list=datalogger_command_list,
               data_send=None,
               list_status_data_send=list_status_data_send,
               current_send_status=current_send_status,
               curent_send_name=curent_send_name,
               send_file_name=None,
               alarm=alarm,
               ftp_list=ftp_list,
               ftp_id_res=ftp_id_res,
               ftp_last_file_name_res=ftp_last_file_name_res,
               ftp_folder_path_res=ftp_folder_path_res,
               res_ftp_folder_path=res_ftp_folder_path,
               agents=agents,
               provinces=provinces,
               province=province,
               )
    return res

@service.json
@auth.requires(lambda: (auth.has_permission('view', 'indicators')))
def get_list_indicators_for_request_sync_station(*args, **kwargs):
    try:
        # db = current.db
        iDisplayStart = int(request.vars.iDisplayStart)
        request_sync_station_id = request.vars.request_sync_station_id
        aaData = []
        view_only = request.vars.view_only
        conditions = (db.request_sync_station_indicator.id > 0)
        if request_sync_station_id:
            conditions &= (db.request_sync_station_indicator.request_sync_station_id == request_sync_station_id)
        list_data = db(conditions).select(db.request_sync_station_indicator.id,
                                          db.request_sync_station_indicator.indicator_id,
                                          db.request_sync_station_indicator.tendency_value,
                                          db.request_sync_station_indicator.preparing_value,
                                          db.request_sync_station_indicator.exceed_value,
                                          db.request_sync_station_indicator.qcvn_code,
                                          db.request_sync_station_indicator.qcvn_detail_type_code,
                                          db.request_sync_station_indicator.qcvn_detail_min_value,
                                          db.request_sync_station_indicator.qcvn_detail_max_value,
                                          db.request_sync_station_indicator.qcvn_detail_const_area_value,
                                          db.request_sync_station_indicator.equipment_name,
                                          db.request_sync_station_indicator.equipment_lrv,
                                          db.request_sync_station_indicator.equipment_urv,
                                          db.request_sync_station_indicator.mapping_name,
                                          db.request_sync_station_indicator.convert_rate,
                                          db.request_sync_station_indicator.status,db.request_sync_station_indicator.qcvn_id, db.request_sync_station_indicator.qcvn_kind_id,)
        iTotalRecords = db(conditions).count()
        indicator_dict = common.get_indicator_dict()
        status = dict(db.request_sync_station_indicator.status.requires.options())
        iRow = iDisplayStart + 1

        for item in list_data:
            if (item.qcvn_detail_type_code is not None) & (item.qcvn_detail_type_code != '-- Chọn loại --') \
                    & (item.qcvn_detail_type_code != '---'):
                text = item.qcvn_detail_type_code
            else:
                text = '---'
            indicator = db.indicators(item.indicator_id) or None

            qcvn_id = ""
            qcvn_kind_id = ""
            conditions_kind = (db.request_sync_station_qcvn_station_kind.request_sync_station_id == request_sync_station_id)
            if 'qcvn_id' in item and  item.qcvn_id != "" or item.qcvn_id is not None:
                qcvn_id = str(item.qcvn_id)
                conditions_kind &= (db.request_sync_station_qcvn_station_kind.qcvn_id == item.qcvn_id)
            if 'qcvn_kind_id' in item and  item.qcvn_kind_id != "" or item.qcvn_kind_id is not None:
                qcvn_kind_id = str(item.qcvn_kind_id)
                conditions_kind &= (db.request_sync_station_qcvn_station_kind.qcvn_kind_id == item.qcvn_kind_id)

            qcvn_station_kind = db.request_sync_station_qcvn_station_kind(conditions_kind) or None

            qcvn_detail_const_area_value_1 = 0
            qcvn_detail_const_area_value_2 = 0
            qcvn_detail_const_area_value_3 = 0
            if qcvn_station_kind:
                qcvn_detail_const_area_value_1 = qcvn_station_kind.qcvn_detail_const_area_value_1 if qcvn_station_kind.qcvn_detail_const_area_value_1 else None
                qcvn_detail_const_area_value_2 = qcvn_station_kind.qcvn_detail_const_area_value_2 if qcvn_station_kind.qcvn_detail_const_area_value_2 else None
                qcvn_detail_const_area_value_3 = qcvn_station_kind.qcvn_detail_const_area_value_3 if qcvn_station_kind.qcvn_detail_const_area_value_3 else None


            listA = [
                str(iRow),  # A(str(iRow), _href = URL('form', args = [item.id])),
                indicator.indicator + '(' + indicator.unit + ')',
                item.mapping_name,
                "{:,}".format(item.convert_rate) if item.convert_rate else 1,
                # "{0:.4f}".format(item.tendency_value),
                # "{0:.4f}".format( item.preparing_value),
                # "{0:.4f}".format(item.exceed_value),
                item.equipment_name,
                item.equipment_lrv,
                item.equipment_urv,
                item.qcvn_code,
                qcvn_detail_const_area_value_1,
                qcvn_detail_const_area_value_2,
                qcvn_detail_const_area_value_3,
                TD(text, _class="qcvn_detail_type_code", _value=str(item.qcvn_detail_type_code)),
                round(item.qcvn_detail_min_value, 6) if item.qcvn_detail_min_value else None,
                round(item.qcvn_detail_max_value, 6) if item.qcvn_detail_max_value else None,
                # item.qcvn_detail_const_area_value,
                status[str(item.status)] if item.status else '',
                # A(I(_class='fa fa-edit'), data={'url': '/eos/stations/popup_edit_thong_so?station_id='+station_id+'&qcvn_id='+qcvn_id +'&qcvn_kind_id='+qcvn_kind_id +'&station_indicator_id='+ str(idd)}, _class="edit_thong_so_btn btnAddNew", _href="javascript: {};")
                A(I())
            ]
            if not view_only:
                listA.append(INPUT(_group='1', _class='select_item', _type='checkbox', _value=item.id))
            listA.append(item.id)

            aaData.append(listA)
            iRow += 1
        return dict(iTotalRecords=iTotalRecords, iTotalDisplayRecords=iTotalRecords, aaData=aaData, success=True)
    except Exception as ex:
        return dict(iTotalRecords=0, iTotalDisplayRecords=0, aaData=[], message=str(ex), success=False)
