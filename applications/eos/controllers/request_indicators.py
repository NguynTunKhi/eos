import json
from applications.eos.middleware import basic_auth
from applications.eos.services import request_indicator_service
from applications.eos.package import request_indicator_pack
from applications.eos.exception import http
from applications.eos.common import response as http_response
from applications.eos.enums import request_indicator

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

auth.settings.allow_basic_login = True


def call():
    return service()


# For API version

# create_request_indicator api with basic auth deploy on tw for local dp call to create request indicator
@request.wsgi.middleware(basic_auth.BasicAuthMiddleware)
def create_request_indicator():
    response.headers['Content-Type'] = 'application/json'
    try:
        try:
            data = json.loads(request.body.read())
            req = request_indicator_pack.CreateRequestIndicator(**data)
        except TypeError as ex:
            return json.dumps(http_response.Response(
                code=400,
                message="parse request fail: " + ex.__str__(),
                data=None,
            ).to_dict())
        idx = request_indicator_service.RequestIndicatorService(pydb, current.T).create_request_indicator(
            request_pack=req)
        return json.dumps(http_response.Response(
            code=200,
            message='success',
            data={
                'id': idx,
            }
        ).to_dict())
    except http.HttpException as ex:
        return json.dumps(http_response.Response(
            code=ex.http_code,
            message=ex.message,
            data=None,
        ).to_dict())
    # except Exception as ex:
    #     return json.dumps(http_response.Response(
    #         code=500,
    #         message='internal server error',
    #         data=None,
    #     ).__dict__)


# list_request_indicators api with basic auth deploy on tw for local dp call to list request indicators
@request.wsgi.middleware(basic_auth.BasicAuthMiddleware)
def list_request_indicators():
    response.headers['Content-Type'] = 'application/json'
    try:
        params = request.get_vars
        keyword = params['keyword']
        indicator_type_raw = params['indicator_type']
        indicator_type = None
        if indicator_type_raw is not None:
            indicator_type = int(indicator_type_raw)
        page_raw = params['page']
        page = 0
        if page_raw:
            page = int(page_raw)
        page_size_raw = params['page_size']
        page_size = 10
        if page_size_raw:
            page_size = int(page_size_raw)
        approve_status_raw = params['approve_status']
        if approve_status_raw is None or approve_status_raw == "":
            approve_status = None
        else:
            approve_status = int(approve_status_raw)
        req = request_indicator_pack.RequestListRequestIndicator(keyword=keyword, indicator_type=indicator_type,
                                                                 page=page,
                                                                 page_size=page_size, approve_status=approve_status)
        resp = request_indicator_service.RequestIndicatorService(pydb, current.T).list_request_indicators(
            request_pack=req)
        return json.dumps(http_response.Response(
            code=200,
            message='success',
            data=resp.data,
            total=resp.total,
            page=resp.page,
            page_size=resp.page_size,
        ).to_dict())
    except ValueError as ex:
        return json.dumps(http_response.Response(
            code=400,
            message=ex.__str__(),
            data=None,
        ).to_dict())


# list_request_indicators api with basic auth deploy on tw for local dp call to update request indicator
@request.wsgi.middleware(basic_auth.BasicAuthMiddleware)
def update_request_indicator():
    response.headers['Content-Type'] = 'application/json'
    try:
        try:
            request_indicator_id = request.env.path_info.split("/")[4]
            data = json.loads(request.body.read())
            req = request_indicator_pack.UpdateRequestIndicator(request_indicator_id, **data)
        except TypeError as ex:
            return json.dumps(http_response.Response(
                code=400,
                message="parse request fail: " + ex.__str__(),
                data=None,
            ).to_dict())
        request_indicator_service.RequestIndicatorService(pydb, current.T).update_request_indicator(request_pack=req)
        return json.dumps(http_response.Response(
            code=200,
            message='success',
            data=None
        ).to_dict())
    except http.HttpException as ex:
        return json.dumps(http_response.Response(
            code=ex.http_code,
            message=ex.message,
            data=None,
        ).to_dict())


# get_request_indicator api with basic auth deploy on tw for local dp call to get a request indicator
@request.wsgi.middleware(basic_auth.BasicAuthMiddleware)
def get_request_indicator():
    response.headers['Content-Type'] = 'application/json'
    try:
        try:
            request_indicator_id = request.env.path_info.split("/")[4]
        except TypeError as ex:
            return json.dumps(http_response.Response(
                code=400,
                message="parse request fail: " + ex.__str__(),
                data=None,
            ).to_dict())
        data = request_indicator_service.RequestIndicatorService(pydb, current.T).get_request_indicator(
            request_indicator_id)
        return json.dumps(http_response.Response(
            code=200,
            message='success',
            data=data
        ).to_dict())
    except http.HttpException as ex:
        return json.dumps(http_response.Response(
            code=ex.http_code,
            message=ex.message,
            data=None,
        ).to_dict())


# For app TW version

# index_tw for index page tw
def index_tw():
    return dict()


@service.json
@auth.requires(lambda: (auth.has_permission('view', 'request_indicators')))
def get_list_request_indicators(*args, **kwargs):
    try:
        idisplay_start = int(request.vars.iDisplayStart)
        idisplay_length = int(request.vars.iDisplayLength)
        limit_by = (idisplay_start, idisplay_length + 1)
        approve_status_raw = request.vars.approve_status
        if approve_status_raw == "":
            approve_status = None
        else:
            approve_status = int(approve_status_raw)

        i_type = request.vars.type
        some_text = request.vars.sometext
        data = []

        conditions = (db.request_indicators.id > 0)
        if some_text:
            conditions &= (db.request_indicators.indicator.contains(some_text) |
                           db.request_indicators.source_name.contains(some_text) |
                           db.request_indicators.unit.contains(some_text))
        if i_type:
            conditions &= (db.request_indicators.indicator_type == i_type)
        if approve_status is not None:
            conditions &= (db.request_indicators.approve_status == approve_status)

        list_data = db(conditions).select(db.request_indicators.ALL,
                                          orderby=~db.request_indicators.order_no,
                                          limitby=limit_by)

        i_total_records = db(conditions).count()
        i_row = idisplay_start + 1
        indicator_type = dict(db.request_indicators.indicator_type.requires.options())

        for i, item in enumerate(list_data):
            i_tag = A(I())
            if auth.has_permission('approve', 'request_indicators') and \
                    item.approve_status == request_indicator.RequestIndicatorApproveStatus.WAITING:
                i_tag = A(I(_class="fa fa-edit", _onClick="showApproveModal('" + str(item.id) + "')"))
            data.append([
                str(i_row),
                A(item.indicator, _href=URL('form', args=[item.id])),
                indicator_type.get(str(item.indicator_type)),
                item.unit,
                item.source_name,
                item.order_no,
                item.description,
                item.approve_status,
                item.reason,
                i_tag,
            ])
            i_row += 1

        return dict(iTotalRecords=i_total_records, iTotalDisplayRecords=i_total_records, aaData=data, success=True)
    except Exception as ex:
        return dict(iTotalRecords=0, iTotalDisplayRecords=0, aaData=[], message=str(ex), success=False)


@service.json
@auth.requires(lambda: (auth.has_permission('approve', 'request_indicators')))
# For approve/reject request indicator
def approve_request_indicator(*args, **kwargs):
    try:
        try:
            request_indicator_id = request.vars.request_indicator_id
            approve_action = request.vars.approve_action
            reason = request.vars.reason
            request_indicator_id_int = int(request_indicator_id)
            request_indicator_id_hex = format(request_indicator_id_int, "02X")
            req = request_indicator_pack.ApproveRequestIndicator(request_indicator_id_hex,
                                                                 int(approve_action),
                                                                 reason)
        except TypeError as ex:
            return json.dumps(http_response.Response(
                code=400,
                message="parse request fail: " + ex.__str__(),
                data=None,
            ).to_dict())
        request_indicator_service.RequestIndicatorService(pydb, current.T).approve_request_indicator(req)
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


# For app LOCAL DP version

# index_local_dp for index page local_dp
def index_local_dp():
    return dict()


@service.json
@auth.requires(lambda: (auth.has_permission('view', 'request_indicators')))
def list_request_indicator_local_dp(*args, **kwargs):
    idisplay_start = int(request.vars.iDisplayStart)
    idisplay_length = int(request.vars.iDisplayLength)
    page = int(idisplay_start / idisplay_length) + 1
    page_size = idisplay_length

    approve_status_raw = request.vars.approve_status
    if approve_status_raw == "":
        approve_status = None
    else:
        approve_status = int(approve_status_raw)
    i_type = request.vars.type
    some_text = request.vars.sometext

    req = request_indicator_pack.RequestListRequestIndicator(keyword=some_text, indicator_type=i_type,
                                                             page=page,
                                                             page_size=page_size, approve_status=approve_status)
    try:
        response_body = request_indicator_service.RequestIndicatorService(pydb,
                                                                          current.T).list_request_indicators_local_dp(
            request_pack=req)
        return response_body
    except http.HttpException as ex:
        return http_response.Response(
            code=ex.http_code,
            message=ex.message,
            data=None
        ).to_dict()


@service.json
@auth.requires(lambda: (auth.has_permission('view', 'request_indicators')))
def get_request_indicator_local_dp(*args, **kwargs):
    try:
        request_indicator_id = request.env.path_info.split("/")[6]
        response_body = request_indicator_service.RequestIndicatorService(pydb,
                                                                          current.T).get_request_indicators_local_dp(
            request_indicator_id)
        return response_body
    except http.HttpException as ex:
        return http_response.Response(
            code=ex.http_code,
            message=ex.message,
            data=None,
        ).to_dict()


@service.json
@auth.requires(lambda: (auth.has_permission('edit', 'request_indicators')))
def update_request_indicator_local_dp(*args, **kwargs):
    response.headers['Content-Type'] = 'application/json'
    try:
        try:
            request_indicator_id = request.env.path_info.split("/")[6]
            data = json.loads(request.body.read())
            req = request_indicator_pack.UpdateRequestIndicator(request_indicator_id, **data)
        except TypeError as ex:
            return json.dumps(http_response.Response(
                code=400,
                message="parse request fail: " + ex.__str__(),
                data=None,
            ).to_dict())
        response_body = request_indicator_service.RequestIndicatorService(pydb,
                                                                          current.T).update_request_indicator_local_dp(
            request_pack=req)
        return response_body
    except http.HttpException as ex:
        return http_response.Response(
            code=ex.http_code,
            message=ex.message,
            data=None,
        ).to_dict()


@service.json
@auth.requires(lambda: (auth.has_permission('create', 'request_indicators')))
def create_request_indicator_local_dp(*args, **kwargs):
    response.headers['Content-Type'] = 'application/json'
    try:
        try:
            data = json.loads(request.body.read())
            req = request_indicator_pack.CreateRequestIndicator(**data)
        except TypeError as ex:
            return json.dumps(http_response.Response(
                code=400,
                message="parse request fail: " + ex.__str__(),
                data=None,
            ).to_dict())
        response_body = request_indicator_service.RequestIndicatorService(pydb,
                                                                          current.T).create_request_indicator_local_dp(
            request_pack=req)
        return response_body
    except http.HttpException as ex:
        return http_response.Response(
            code=ex.http_code,
            message=ex.message,
            data=None,
        ).to_dict()
