import json
import logging
import os

import requests

from applications.eos.enums import auth
from applications.eos.package import request_indicator_pack


class TWAPI:
    def __init__(self):
        self.basic_auth_user = os.getenv(auth.ENV_TW_USER_BASIC_AUTH_API)
        self.basic_auth_password = os.getenv(auth.ENV_TW_PASSWORD_BASIC_AUTH_API)
        self.host = os.getenv(auth.ENV_TW_HOST)

    # get_list_request_indicators call to eos tw and response returned request_indicators and err_msg
    def get_list_request_indicators(self, request_pack  # type: request_indicator_pack.RequestListRequestIndicator
                                    ):
        api_endpoint = self.host + '/eos/request_indicators/list_request_indicators'
        params = {
            'page': request_pack.page,
            'page_size': request_pack.page_size,
        }
        if request_pack.indicator_type:
            params['indicator_type'] = request_pack.indicator_type

        if request_pack.keyword:
            params['keyword'] = request_pack.keyword
        if request_pack.approve_status is not None:
            params['approve_status'] = request_pack.approve_status

        resp = requests.get(url=api_endpoint, params=params, auth=(self.basic_auth_user, self.basic_auth_password))
        response_body, err = self.extract_response(resp)
        return response_body, err

    def get_request_indicator_by_id(self, request_indicator_id  # type: str
                                    ):
        api_endpoint = self.host + '/eos/request_indicators/get_request_indicator/' + request_indicator_id
        resp = requests.get(url=api_endpoint, auth=(self.basic_auth_user, self.basic_auth_password))
        response_body, err = self.extract_response(resp)
        return response_body, err

    def update_request_indicator(self, request_pack  # type: request_indicator_pack.UpdateRequestIndicator
                                 ):
        api_endpoint = self.host + '/eos/request_indicators/update_request_indicator/' + request_pack.id
        resp = requests.post(url=api_endpoint, json={
            "order_no": request_pack.order_no,
            "source_name": request_pack.source_name,
            "unit": request_pack.unit,
            "description": request_pack.description,
            "indicator": request_pack.indicator,
            "indicator_type": request_pack.indicator_type,
        }, auth=(self.basic_auth_user, self.basic_auth_password))
        response_body, err = self.extract_response(resp)
        return response_body, err

    def create_request_indicator(self, request_pack  # type: request_indicator_pack.CreateRequestIndicator
                                 ):
        api_endpoint = self.host + '/eos/request_indicators/create_request_indicator'
        resp = requests.post(url=api_endpoint, json={
            "order_no": request_pack.order_no,
            "source_name": request_pack.source_name,
            "unit": request_pack.unit,
            "description": request_pack.description,
            "indicator": request_pack.indicator,
            "indicator_type": request_pack.indicator_type,
        }, auth=(self.basic_auth_user, self.basic_auth_password))
        response_body, err = self.extract_response(resp)
        return response_body, err

    def extract_response(self, resp):
        if resp.status_code != requests.codes.ok:
            err_msg = 'get error response from TWAPI with code: %s, body: %s' % (resp.status_code, resp.content)
            return None, err_msg
        json_response = resp.json()
        if 'meta' in json_response:
            meta = json_response['meta']
            if 'code' in meta:
                code = meta['code']
                if code != 200:
                    err_msg = 'get error response from TWAPI with code: %s, meta_code: %s, body:%s' % (
                        resp.status_code, code, resp.content)
                    return json_response, err_msg
                else:
                    return json_response, None
            else:
                err_msg = 'get error response from TWAPI with code: %s, body:%s' % (resp.status_code, resp.content)
                return None, err_msg
        else:
            err_msg = 'get error response from TWAPI with code: %s, body:%s' % (resp.status_code, resp.content)
            return None, err_msg

    def sync_created_station(self, stations):
        api_endpoint = self.host + '/eos/request_sync_stations/create_sync_station_request'
        json_str = json.dumps(stations, default=str)
        resp = requests.post(url=api_endpoint, json=json_str, auth=(self.basic_auth_user, self.basic_auth_password))
        response_body, err = self.extract_response(resp)
        return response_body, err

    def get_request_sync_stations_approve_status(self, tw_request_sync_station_ids):
        api_endpoint = self.host + '/eos/request_sync_stations/get_request_sync_stations_approve_status'
        json_str = json.dumps(tw_request_sync_station_ids, default=str)
        resp = requests.post(url=api_endpoint, json=json_str, auth=(self.basic_auth_user, self.basic_auth_password))
        response_body, err = self.extract_response(resp)
        return response_body, err

