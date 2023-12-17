# @auth.requires()
from applications.eos.modules import const
import re


def call():
    return service()


def to_snake_case(str):
    str = str.replace(" ", "")
    s1 = re.sub('(.)([A-Z][a-z]+)', r'\1_\2', str)
    return re.sub('([a-z0-9])([A-Z])', r'\1_\2', s1).lower()

def convert_name_stations_type(str):
    str = str.split('(')
    return str[0].lower()

def get_list_api():
    query = (db.station_types.code == 4) | (db.station_types.code == 1)
    rows = db(query).select(db.station_types.ALL)
    api_list = []
    host = request.env.http_host
    for row in rows:
        # {'name': 'Danh sach tram theo thanh phan moi truong', 'type': 'POST',
        #      'url': 'https:hagiang.deahan-si.com/eos/call/json/sharing-station'}
        api_list.append(dict(name=T('Danh sách các trạm quan trắc tự động ') + T(convert_name_stations_type(row['station_type'])),
                             key=to_snake_case(row['station_type'] + "Station"),
                             url='http://{}/eos/api_led/call/json/stations?station_type={}'.format(host, row['code']),
                             type='POST'
                             ))
        api_list.append(dict(name=T('Thông tin chi tiết trạm quan trắc tự động ') + T(convert_name_stations_type(row['station_type'])),
                             key='detail_stations' + row['code'],
                             url='http://{}/eos/api_led/call/json/data_info_stations?station_type={}'.format(host, row['code']),
                             type='POST'
                             ))
    api_list.append(
        dict(name=T('Chỉ số AQI'), key="aqi_ngay", type='POST',
             url='http://{}/eos/api_led/call/json/aqi_day'.
             format(host)))
    api_list.append(
        dict(name=T('Dịch vụ chia sẻ số liệu trung bình 1 giờ trạm tự động nước mặt'), key="data_1h", type='POST',
             url='http://{}/eos/api_led/call/json/idh_data?data_type=2'.
             format(host)))
    api_list.append(
        dict(name=T('Dịch vụ chia sẻ số liệu trung bình ngày trạm tự động nước mặt'), key="data_1d", type='POST',
             url='http://{}/eos/api_led/call/json/idh_data?data_type=1'.
             format(host)))
    api_list.append(
        dict(name=T('Dịch vụ chia sẻ số liệu trung bình tháng trạm tự động nước mặt'), key="data_1m", type='POST',
             url='http://{}/eos/api_led/call/json/idh_data?data_type=0'.
             format(host)))
    return api_list


@service.json
def ajax_get_list_api(*args, **kwargs):
    try:
        iDisplayStart = 0  # int(request.vars.iDisplayStart)
        aaData = []
        list_data = get_list_api()
        # Tong so ban ghi khong thuc hien phan trang
        iTotalRecords = len(list_data)

        # Duyet tung phan tu trong mang du lieu vua truy van duoc
        for i, item in enumerate(list_data):
            aaData.append([
                str(iDisplayStart + 1 + i),
                item['name'],
                item['type'],
                item['url'],
                item['key']
            ])
        return dict(iTotalRecords=iTotalRecords, iTotalDisplayRecords=iTotalRecords, aaData=aaData, success=True)
    except Exception as ex:
        return dict(iTotalRecords=0, iTotalDisplayRecords=0, aaData=[], message=str(ex), success=False)


def sharing_api():
    return dict()


def authentication_api():
    rows = db(db.auth_user.id > 0).select(db.auth_user._id, db.auth_user.username)

    return dict(
        array_user=list(rows)
    )


@service.json
def ajax_get_authen_api(*args, **kwargs):
    try:
        iDisplayStart = 0  # int(request.vars.iDisplayStart)
        aaData = []
        list_data = get_list_api()
        # Tong so ban ghi khong thuc hien phan trang
        iTotalRecords = len(list_data)

        # Duyet tung phan tu trong mang du lieu vua truy van duoc
        for i, item in enumerate(list_data):
            aaData.append([
                str(iDisplayStart + 1 + i),
                item['name'],
                item['type'],
                item['url'],
                item['key'],
            ])
        return dict(iTotalRecords=iTotalRecords, iTotalDisplayRecords=iTotalRecords, aaData=aaData, success=True)
    except Exception as ex:
        return dict(iTotalRecords=0, iTotalDisplayRecords=0, aaData=[], message=str(ex), success=False)


def list_sharing():
    return dict()


@service.json
def get_api_share_by_user_id(*args, **kwargs):
    token = None
    try:
        user_id = request.vars.user_id
        user = db(db.auth_user.id == user_id).select(db.auth_user.ALL).first()
        # token = user_id
        if user_id:
            data = db(db.sharing_api.user_id == user_id).select(db.sharing_api.ALL).first()
            if data:
                if data.list_authen:
                    data['list_authen'] = '{}'.format(data['list_authen']).split(';')
                    data['id'] = str(data['id'])
                    return dict(success=True, data=data)
            else:
                from datetime import datetime, timedelta
                from applications.eos.modules import const
                from gluon.tools import prettydate
                import json
                from gluon.tools import AuthJWT
                import ast
                from applications.eos.modules.custom_auth import CustomAuth
                auth_share = CustomAuth(db, host_names=myconf.get('host.names'))
                auth_share.user = user
                myjwt = AuthJWT(auth_share, secret_key='secret@259', expiration=60 * 60 * 24 * 365 * 3)
                token = myjwt.jwt_token_manager()
                json_object = json.loads(token)
                token = json_object['token']
                # db.login_user.insert(user_id=auth.user_id, confirm_2fa=False, token=json_object['token'],
                #                      is_admin=is_admin)

        return dict(success=True, data=dict(token=token, list_authen=[]))
    except Exception as ex:
        return dict(success=False, message=ex.message)


@service.json
def putting_data(*args, **kwargs):
    try:
        data = dict()
        for k in request.vars:
            if k in ['list_authen', 'user_id', 'token', 'department_name']:
                data[k] = request.vars[k]
        if data.has_key('list_authen') and data['list_authen']:
            data['list_authen'] = str(data['list_authen'])
        db.sharing_api.update_or_insert(db.sharing_api.user_id == data['user_id'], **data)
        db.token_user.insert(user_id=data['user_id'], token=data['token'])
        db.commit()
        return dict(record=data, success=True)
    except Exception as ex:
        return dict(mesage=str(ex), success=False)

@service.json
def get_detail(*args, **kwargs):
    try:
        service_key = request.vars.service_key
        data_full = get_list_api()
        record = filter(lambda i: i['key'] == service_key, data_full)
        return dict(data=record, success=True)
    except Exception as ex:
        return dict(message=str(ex), success=False)
