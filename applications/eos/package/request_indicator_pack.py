from applications.eos.exception import http
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
    from gluon import current

    T = current.T


class CreateRequestIndicator:
    def __init__(self, indicator, indicator_type, description, unit, source_name, order_no):
        self.order_no = order_no
        self.source_name = source_name
        self.unit = unit
        self.description = description
        self.indicator = indicator
        self.indicator_type = indicator_type

    def validate(self):
        if self.indicator is None or len(self.indicator.lstrip()) == 0:
            return False, http.HttpException(message="Indicator name can not empty", http_code=400)
        if self.indicator_type is None or self.indicator_type < 0 or self.indicator_type > 4:
            return False, http.HttpException(message="Indicator type must > 0 and < 5", http_code=400)
        if self.source_name is None or len(self.source_name.lstrip()) == 0:
            return False, http.HttpException(message="Indicator name can not empty", http_code=400)
        if self.order_no is None or self.order_no <= 0:
            return False, http.HttpException(message="OrderNo must > 0", http_code=400)
        return True, None


class UpdateRequestIndicator:
    def __init__(self, id, indicator, indicator_type, description, unit, source_name, order_no):
        self.id = id
        self.order_no = order_no
        self.source_name = source_name
        self.unit = unit
        self.description = description
        self.indicator = indicator
        self.indicator_type = indicator_type

    def validate(self):
        if self.indicator is None or len(self.indicator.lstrip()) == 0:
            return False, http.HttpException(message="Indicator name can not empty", http_code=400)
        if self.indicator_type is None or self.indicator_type < 0 or self.indicator_type > 4:
            return False, http.HttpException(message="Indicator type must > 0 and < 5", http_code=400)
        if self.source_name is None or len(self.source_name.lstrip()) == 0:
            return False, http.HttpException(message="Indicator name can not empty", http_code=400)
        if self.order_no is None or self.order_no <= 0:
            return False, http.HttpException(message="OrderNo must > 0", http_code=400)
        return True, None


class ApproveRequestIndicator:
    def __init__(self, request_indicator_id, action, reason):
        self.request_indicator_id = request_indicator_id
        self.action = action
        self.reason = reason

    def validate(self):
        if self.action not in request_indicator.RequestIndicatorApproveAction().arr():
            return False, http.HttpException(
                message='Invalid Approve Action',
                http_code=400,
            )
        else:
            return True, None


class RequestListRequestIndicator:
    def __init__(self, keyword, indicator_type, page, page_size, approve_status):
        # type:(str, int|None, int, int, int|None) -> None

        self.keyword = keyword
        self.indicator_type = indicator_type
        self.page = page
        self.page_size = page_size
        self.approve_status= approve_status


class ResponseListRequestIndicator:
    def __init__(self, page, page_size, total, data):
        self.page = page
        self.page_size = page_size
        self.total = total
        self.data = data
