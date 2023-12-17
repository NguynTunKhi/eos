from applications.eos.exception import http
from applications.eos.enums import request_station


class ApproveRequestIndicator:
    def __init__(self, request_sync_station_id, action, reason):
        self.request_sync_station_id = request_sync_station_id
        self.action = action
        self.reason = reason

    def validate(self):
        if self.action not in request_station.RequestStationApproveAction().arr():
            return False, http.HttpException(
                message='Invalid Approve Action',
                http_code=400,
            )
        else:
            return True, None


class RequestListRequestSyncStation:
    def __init__(self, keyword, station_type, page, page_size, approve_status):
        # type:(str, int|None, int, int, int|None) -> None

        self.keyword = keyword
        self.station_type = station_type
        self.page = page
        self.page_size = page_size
        self.approve_status = approve_status


class ResponseListRequestSyncStation:
    def __init__(self, page, page_size, total, data):
        self.page = page
        self.page_size = page_size
        self.total = total
        self.data = data
