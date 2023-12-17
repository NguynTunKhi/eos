# coding=utf-8
# encoding: utf-8
# encoding=utf8
from datetime import datetime
import logging

from bson.objectid import ObjectId

from applications.eos.adapters import eos_tw
from applications.eos.exception import http
from applications.eos.enums import request_station as request_station_enums
from applications.eos.package import request_sync_station_pack
from applications.eos.common import condition_tree
from applications.eos.modules import common
from applications.eos.modules import const as common_const

from gluon import current

if False:
    from gluon import *

    request = current.request
    response = current.response
    session = current.session
    cache = current.cache
    T = current.T
    db = current.db


class RequestSyncStationService:
    def __init__(self, mongo_client, T):
        self.mongo_client = mongo_client
        self.T = T
        self.current = current

    def list_request_sync_stations(self, request_pack  # type: request_sync_station_pack.RequestListRequestSyncStation
                                   ):
        condition = condition_tree.ExpressionTree(None)
        if request_pack.keyword:
            condition.And(
                condition_tree.ExpressionTree(None).Or(
                    {
                        "station_name": {"$regex": request_pack.keyword},
                    },
                    {
                        "station_code": {"$regex": request_pack.keyword},
                    },
                    {
                        "last_file_name": {"$regex": request_pack.keyword},
                    }
                )
            )
        if request_pack.approve_status is not None:
            condition.And({
                "approve_status": request_pack.approve_status
            })
        if request_pack.station_type is not None:
            condition.And({
                "station_type": request_pack.station_type
            })

        docs = self.mongo_client.request_sync_stations.find(condition.dict). \
            sort("_id", -1).skip((request_pack.page - 1) * request_pack.page_size). \
            limit(request_pack.page_size)
        count = docs.count()
        request_sync_stations = []
        station_type = dict()
        for item in common.get_station_types():
            station_type[str(item['value'])] = item['name']
        for doc in docs:
            request_sync_stations.append(self.doc_to_request_sync_station(doc, station_type))

        return request_sync_station_pack.ResponseListRequestSyncStation(page=request_pack.page,
                                                                        page_size=request_pack.page_size, total=count,
                                                                        data=request_sync_stations)

    def approve_request_sync_station(self, request_pack  # type: request_sync_station_pack.ApproveRequestIndicator
                                     ):
        valid, ex = request_pack.validate()
        if not valid:
            raise ex
        request_sync_station, valid, ex = self.validate_approve_sync_station_pack(request_pack)
        if not valid:
            raise ex

        if request_pack.action == request_station_enums.RequestStationApproveAction.APPROVE:
            self.handle_approve(request_sync_station, request_pack)
        elif request_pack.action == request_station_enums.RequestStationApproveAction.REJECT:
            self.handle_reject(request_sync_station, request_pack)
        return

    def handle_approve(self, request_sync_station, request_pack):
        station = self.request_sync_station_to_station(request_sync_station)
        request_sync_station_decimal_id = str(int(str(request_pack.request_sync_station_id), 16))
        ## check station exists
        if 'station_code' in station:
            check_exists = self.mongo_client.stations.find_one({
                'station_code': station["station_code"]
            })
            if check_exists is not None:
                station["_id"] = str(check_exists['_id'])
                station_id = str(int(str(check_exists['_id']), 16))
                self.update(station)

                request_sync_station_indicator_docs = self.mongo_client.request_sync_station_indicator.find({
                    'request_sync_station_id': request_sync_station_decimal_id
                })

                self.mongo_client.station_indicator.delete_many({
                    'station_id': station_id
                })
                for doc in request_sync_station_indicator_docs:
                    if '_id' in doc:
                        doc.pop('_id')
                    if 'id' in doc:
                        doc.pop('id')
                    if 'request_sync_station_id' in doc:
                        doc.pop('request_sync_station_id')
                    doc['station_id'] = str(int(str(check_exists['_id']), 16))
                    self.mongo_client.station_indicator.insert(doc)

                request_sync_station_qcvn_station_kinds = self.mongo_client.request_sync_station_qcvn_station_kind.find(
                    {
                        'request_sync_station_id': request_sync_station_decimal_id
                    })

                self.mongo_client.qcvn_station_kind.delete_many(
                    {
                        'station_id': request_sync_station_decimal_id
                    })
                for doc in request_sync_station_qcvn_station_kinds:
                    if '_id' in doc:
                        doc.pop('_id')
                    if 'id' in doc:
                        doc.pop('id')
                    if 'request_sync_station_id' in doc:
                        doc.pop('request_sync_station_id')
                    doc['station_id'] = str(int(str(check_exists['_id']), 16))
                    self.mongo_client.qcvn_station_kind.insert(doc)

                self.update_request_sync_station(request_sync_station["id"], {
                    "approve_status": request_station_enums.RequestStationApproveStatus.APPROVED,
                    "station_id": check_exists['_id'],
                    "reason": request_pack.reason
                })
                return

        new_station_id = self.create_station(station)
        logging.info("create success new station %s when handle approve request_sync_station: %s", new_station_id,
                     request_sync_station["id"])
        self.update_request_sync_station(request_sync_station["id"], {
            "approve_status": request_station_enums.RequestStationApproveStatus.APPROVED,
            "station_id": new_station_id,
            "reason": request_pack.reason
        })

        logging.info("update success request_sync_station when handle approve request_sync_station: %s",
                     request_sync_station["id"])
        request_sync_station_indicator_docs = self.mongo_client.request_sync_station_indicator.find({
            'request_sync_station_id': request_sync_station_decimal_id
        })
        for doc in request_sync_station_indicator_docs:
            if '_id' in doc:
                doc.pop('_id')
            if 'id' in doc:
                doc.pop('id')
            if 'request_sync_station_id' in doc:
                doc.pop('request_sync_station_id')
            doc['station_id'] = str(int(str(new_station_id), 16))
            self.mongo_client.station_indicator.insert(doc)

        request_sync_station_qcvn_station_kinds = self.mongo_client.request_sync_station_qcvn_station_kind.find({
            'request_sync_station_id': request_sync_station_decimal_id
        })

        for doc in request_sync_station_qcvn_station_kinds:
            if '_id' in doc:
                doc.pop('_id')
            if 'id' in doc:
                doc.pop('id')
            if 'request_sync_station_id' in doc:
                doc.pop('request_sync_station_id')
            doc['station_id'] = str(int(str(new_station_id), 16))
            self.mongo_client.qcvn_station_kind.insert(doc)

    def handle_reject(self, request_sync_station, request_pack):
        self.update_request_sync_station(request_sync_station["id"], {
            "approve_status": request_station_enums.RequestStationApproveStatus.REJECTED,
            "reason": request_pack.reason
        })
        logging.info("update success request_sync_station when handle reject request_sync_station: %s",
                     request_sync_station["id"])

    def update(self, station):
        station.pop("_id")
        updatedata = {
            "$set": station,
        }
        new_station_id = self.mongo_client.stations.update_one({"station_code": station['station_code']}, updatedata)
        return new_station_id

    def create_station(self, station):
        new_station_id = self.mongo_client.stations.insert(station)
        station_id = str(int(str(new_station_id), 16))
        self.mongo_client.stations.update_one(
            {"_id": new_station_id},
            {
                "$set": {
                    "station_id": station_id,
                    "last_time": datetime.now(),
                },
            }
        )
        return new_station_id

    def validate_approve_sync_station_pack(self, request_pack  # type: request_sync_station_pack.ApproveRequestIndicator
                                           ):
        doc = self.mongo_client.request_sync_stations.find_one({"_id": ObjectId(request_pack.request_sync_station_id)})
        if not doc:
            return None, False, http.HttpException(
                message=self.T('Missing id for get request sync station'),
                http_code=400,
            )
        station_type = dict()
        for item in common.get_station_types():
            station_type[str(item['value'])] = item['name']

        request_sync_station = self.doc_to_request_sync_station(doc, station_type)
        if request_sync_station["approve_status"] == request_station_enums.RequestStationApproveStatus.APPROVED:
            return request_sync_station, False, http.HttpException(
                message=self.T('Can not approve approved request station'),
                http_code=400,
            )
        if request_sync_station["approve_status"] == request_station_enums.RequestStationApproveStatus.REJECTED:
            return request_sync_station, False, http.HttpException(
                message=self.T('Can not approve rejected request station'),
                http_code=400,
            )
        return request_sync_station, True, None

    def create_request_sync_created_stations(self, request_stations  # type: [dict]
                                             ):
        models = self.request_sync_created_stations_to_models(request_stations)
        inserted_ids = {}
        for model in models:
            station_indicators = None
            if 'station_indicators' in model:
                station_indicators = model['station_indicators']
                model.pop('station_indicators')

            qcvn_station_kinds = None
            if 'qcvn_station_kinds' in model:
                qcvn_station_kinds = model['qcvn_station_kinds']
                model.pop('qcvn_station_kinds')

            station_id = model['id']
            model.pop('id')
            new_id = self.mongo_client.request_sync_stations.insert(model)
            notity = {
                "title": model["station_name"] + " được yêu cầu đồng bộ",
                "notify_level": 1,
                "send_type": 0,
                "content": model["station_name"] + " được yêu cầu đồng bộ",
                "notify_time": datetime.now(),
            }
            id = self.mongo_client.notifications.insert(notity)
            inserted_ids[station_id] = str(new_id)
            self.mongo_client.request_sync_stations.update_one(
                {"_id": new_id},
                {
                    "$set": {
                        'request_sync_station_id': str(int(str(new_id), 16))
                    },
                }
            )

            if station_indicators:
                self.handle_station_indicators_for_request_sync_created_stations(station_indicators, new_id,
                                                                                 qcvn_station_kinds)
            data_server = ''
            username = ''
            if 'username' in model:
                username = model['username']
            if 'data_server' in model:
                data_server = model['data_server']

            if data_server:
                doc = self.mongo_client.ftp_management.find_one({'ftp_ip': data_server})
                if doc:
                    ftp_id = str(int(str(doc['_id']), 16))
                    self.mongo_client.request_sync_stations.update_one(
                        {"_id": new_id},
                        {
                            "$set": {
                                'ftp_id': ftp_id
                            },
                        }
                    )

        return inserted_ids

    def get_request_sync_stations_approve_status(self, request_sync_station_ids):
        request_sync_station_object_ids = []
        for id in request_sync_station_ids:
            request_sync_station_object_ids.append(ObjectId(id))
        docs = self.mongo_client.request_sync_stations.find({"_id": {
            '$in': request_sync_station_object_ids,
        }})
        if docs is None:
            return []
        res = {}
        for doc in docs:
            doc_res = {}
            if 'approve_status' in doc:
                doc_res['approve_status'] = doc['approve_status']
            if 'reason' in doc:
                doc_res['reason'] = doc['reason']
            res[str(doc['_id'])] = doc_res
        return res

    def get_request_sync_stations_approve_status_from_local_dp(self, tw_request_sync_station_ids):
        res, err = eos_tw.TWAPI().get_request_sync_stations_approve_status(tw_request_sync_station_ids)
        if err is not None:
            logging.error("got error when call to tw api ti get request sync station status with list id:" + ''.join(
                [str(x) for x in tw_request_sync_station_ids]))
            return res, err
        if len(res['data']) > 0:
            return res['data'], None
        return [], None

    def handle_station_indicators_for_request_sync_created_stations(self, station_indicators,
                                                                    new_request_sync_station_id, qcvn_station_kinds):
        for station_indicator in station_indicators:
            if 'indicator' not in station_indicator:
                continue
            indicator = station_indicator['indicator']
            doc = self.mongo_client.indicators.find_one({"indicator": indicator['indicator']})
            if doc is None:
                continue
            indicator_id = int(str(doc['_id']), 16)
            station_indicator['indicator_id'] = str(indicator_id)
            station_indicator.pop('indicator')
            station_indicator.pop('station_id')
            station_indicator['request_sync_station_id'] = str(int(str(new_request_sync_station_id), 16))
            if '_id' in station_indicator:
                station_indicator.pop('_id')
            new_id = self.mongo_client.request_sync_station_indicator.insert(station_indicator)
            print(new_id)

        for qcvn_station_kind in qcvn_station_kinds:
            qcvn_station_kind.pop('station_id')
            qcvn_station_kind['request_sync_station_id'] = str(int(str(new_request_sync_station_id), 16))
            if '_id' in qcvn_station_kind:
                qcvn_station_kind.pop('_id')
            new_id = self.mongo_client.request_sync_station_qcvn_station_kind.insert(qcvn_station_kind)
            print(new_id)

    def request_sync_created_stations_to_models(self, request_stations):
        models = []
        for request_station in request_stations:
            request_station.pop('is_synced')
            request_station['station_id'] = None
            request_station['approve_status'] = request_station_enums.RequestStationApproveStatus.WAITING
            try:
                if 'last_time' in request_station and request_station['last_time']:
                    last_time = datetime.strptime(request_station['last_time'].split(".")[0],
                                                  "%Y-%m-%d %H:%M:%S")
                    request_station['last_time'] = last_time
                if 'qi_adjsut_time' in request_station and request_station['qi_adjsut_time']:
                    qi_adjsut_time = datetime.strptime(request_station['qi_adjsut_time'].split(".")[0],
                                                       "%Y-%m-%d %H:%M:%S")
                    request_station['qi_adjsut_time'] = qi_adjsut_time
                if 'off_time' in request_station and request_station['off_time']:
                    off_time = datetime.strptime(request_station['off_time'].split(".")[0],
                                                 "%Y-%m-%d %H:%M:%S")
                    request_station['off_time'] = off_time
                if 'qi_time' in request_station and request_station['qi_time']:
                    qi_time = datetime.strptime(request_station['qi_time'].split(".")[0], "%Y-%m-%d %H:%M:%S")
                    request_station['qi_time'] = qi_time

                if 'period_ra' in request_station and request_station['period_ra']:
                    period_ra = datetime.strptime(request_station['period_ra'].split(".")[0], "%Y-%m-%d %H:%M:%S")
                    request_station['period_ra'] = period_ra

                if 'verification_deadline' in request_station and request_station['verification_deadline']:
                    period_ra = datetime.strptime(request_station['verification_deadline'].split(".")[0],
                                                  "%Y-%m-%d %H:%M:%S")
                    request_station['verification_deadline'] = period_ra

                if 'send_data' in request_station and request_station['send_data']:
                    send_data = request_station['send_data']
                    if 'ftp_user' in send_data and send_data['ftp_user']:
                        request_station['username'] = send_data['ftp_user']
                    if 'ftp_password' in send_data and send_data['ftp_password']:
                        request_station['pwd'] = send_data['ftp_password']
                    if 'ftp_ip' in send_data and send_data['ftp_ip']:
                        request_station['data_server'] = send_data['ftp_ip']
                    if 'ftp_port' in send_data and send_data['ftp_port']:
                        request_station['data_server_port'] = send_data['ftp_port']

            except ValueError as v:
                request_station['last_time'] = None
                request_station['qi_adjsut_time'] = None
                request_station['off_time'] = None
                request_station['qi_time'] = None
            if 'send_data' in request_station:
                request_station.pop('send_data')
            request_station['agents_id'] = ''
            if 'agent_name' in request_station:
                doc = self.mongo_client.agents.find_one({'agent_name': request_station['agent_name']})
                if doc:
                    request_station['agents_id'] = str(int(str(doc['_id']), 16))
                    request_station['agent_name'] = doc['agent_name']
                else:
                    request_station['agent_name'] = ''
            request_station['area_ids'] = []
            if 'area_names' in request_station:
                docs = self.mongo_client.areas.find({'area_name': {'$in': request_station['area_names']}})
                area_names = []
                area_ids = []
                for doc in docs:
                    area_ids.append(str(int(str(doc['_id']), 16)))
                    area_names.append(doc['area_name'])
                request_station['area_names'] = area_names
                request_station['area_ids'] = area_ids
            models.append(request_station)
        return models

    # sync_created_stations_local_dp method to sync created station, call on local dp
    def sync_created_stations_local_dp(self, station_ids,  # type: []
                                       ):
        stations, valid, err = self.validate_and_transform_sync_creation_stations(station_ids)
        if not valid:
            raise err
        stations = self.bind_station_indicator(stations)
        self.bind_qcvn_kind(stations)
        self.bind_agent_to_stations(stations)
        self.bind_areas_to_stations(stations)

        twapi = eos_tw.TWAPI()
        response_body, err = twapi.sync_created_station(stations)

        if err:
            logging.error("error when sync_created_station: " + err)
            raise http.HttpException(
                message=err,
                http_code=500,
            )
        else:
            data = response_body['data']
            for station_id, request_sync_id in data.iteritems():
                self.update_station(station_id, {
                    'is_synced': True,
                    'tw_request_sync_station_id': request_sync_id
                })

        return response_body

    def bind_agent_to_stations(self, stations):
        agents_ids = []
        for station in stations:
            if 'agents_id' in station and station['agents_id']:
                agents_ids.append(ObjectId(decimal_to_hex(int(station['agents_id']))))
        docs = self.mongo_client.agents.find({"_id": {'$in': agents_ids}})
        mp_agent_name = {}
        for doc in docs:
            mp_agent_name[str(doc['_id'])] = doc['agent_name']

        for station in stations:
            if 'agents_id' in station and station['agents_id']:
                if str(decimal_to_hex(int(station['agents_id']))).lower() in mp_agent_name:
                    station['agent_name'] = mp_agent_name[str(decimal_to_hex(int(station['agents_id']))).lower()]

    def bind_areas_to_stations(self, stations):
        area_object_ids = []
        for station in stations:
            if 'area_ids' in station:
                area_ids = station['area_ids']
                for area_id in area_ids:
                    area_object_ids.append(ObjectId(decimal_to_hex(int(area_id))))
        mp_area_name = {}
        if len(area_object_ids) != 0:
            docs = self.mongo_client.areas.find({"_id": {'$in': area_object_ids}})
            for doc in docs:
                mp_area_name[str(doc['_id'])] = doc['area_name']
        for station in stations:
            if 'area_ids' in station:
                area_ids = station['area_ids']
                area_names = []
                for area_id in area_ids:
                    if str(decimal_to_hex(int(area_id))).lower() in mp_area_name:
                        area_names.append(mp_area_name[str(decimal_to_hex(int(area_id))).lower()])
                station['area_names'] = area_names

    def bind_station_indicator(self, stations):
        station_decimal_ids = []
        for station in stations:
            station_decimal_ids.append(get_str_decimal_station_id(station))
        station_indicator_docs = self.mongo_client.station_indicator.find({"station_id": {'$in': station_decimal_ids}})
        indicator_decimal_ids = []
        indicator_hex_ids = []
        clone_station_indicator_docs = []
        for station_indicator in station_indicator_docs:
            clone_station_indicator_docs.append(station_indicator)
            if station_indicator['indicator_id']:
                indicator_id = station_indicator['indicator_id']
                indicator_decimal_ids.append(indicator_id)
                indicator_hex_ids.append(ObjectId(decimal_to_hex(int(indicator_id))))

        indicator_docs = self.mongo_client.indicators.find({"_id": {
            '$in': indicator_hex_ids,
        }})
        map_indicator = {}
        for indicator in indicator_docs:
            indicator_decimal_id = str(int(str(indicator['_id']), 16))
            map_indicator[indicator_decimal_id] = indicator

        map_station_indicator = {}
        for station_indicator in clone_station_indicator_docs:
            if 'status' in station_indicator and station_indicator['status'] != common_const.SI_STATUS['IN_USE'][
                'value']:
                continue
            if station_indicator['station_id'] not in map_station_indicator:
                map_station_indicator[station_indicator['station_id']] = []
            if station_indicator['indicator_id'] in map_indicator:
                station_indicator['indicator'] = map_indicator[station_indicator['indicator_id']]
            map_station_indicator[station_indicator['station_id']].append(station_indicator)

        for station in stations:
            if get_str_decimal_station_id(station) in map_station_indicator:
                station['station_indicators'] = map_station_indicator[get_str_decimal_station_id(station)]

        return stations

    def bind_qcvn_kind(self, stations):
        station_decimal_ids = []
        for station in stations:
            station_decimal_ids.append(get_str_decimal_station_id(station))
        qcvn_station_kinds = self.mongo_client.qcvn_station_kind.find({"station_id": {'$in': station_decimal_ids}})
        clone_qcvn_station_kinds = dict()
        for qcvn_station_kind in qcvn_station_kinds:
            if not clone_qcvn_station_kinds.has_key(str(qcvn_station_kind['station_id'])):
                clone_qcvn_station_kinds[str(qcvn_station_kind['station_id'])] = [qcvn_station_kind]
            else:
                clone_qcvn_station_kinds[str(qcvn_station_kind['station_id'])].append(qcvn_station_kind)

        for station in stations:
            if clone_qcvn_station_kinds is not None and \
                    get_str_decimal_station_id(station) in clone_qcvn_station_kinds:
                station['qcvn_station_kinds'] = clone_qcvn_station_kinds[get_str_decimal_station_id(station)]

        return stations

    def update_stations(self, station_ids, set_update_fields):
        list_object_ids = []
        for item in station_ids:
            list_object_ids.append(ObjectId(item))
        self.mongo_client.stations.update_many(
            {
                "_id": {
                    "$in": list_object_ids,
                },
            },
            {
                "$set": set_update_fields,
            }
        )

    def update_station(self, station_id, set_update_fields):
        self.mongo_client.stations.update_one(
            {
                "_id": ObjectId(station_id),
            },
            {
                "$set": set_update_fields,
            }
        )

    def update_request_sync_station(self, request_sync_station_id, set_update_fields):
        self.mongo_client.request_sync_stations.update_one(
            {"_id": ObjectId(request_sync_station_id)},
            {
                "$set": set_update_fields,
            }
        )

    def validate_and_transform_sync_creation_stations(self, station_ids):
        station_obj_ids = []
        station_str_decimal_ids = []
        for station_id in station_ids:
            station_obj_ids.append(ObjectId(station_id))
            station_decimal_id = int(station_id, 16)
            station_str_decimal_ids.append(str(station_decimal_id))
        docs = self.mongo_client.stations.find({"_id": {'$in': station_obj_ids}})
        if docs.count() != len(station_obj_ids):
            return None, False, http.HttpException(
                message=self.T('Not Found'),
                http_code=400,
            )
        # synced_list = []
        stations = []
        for doc in docs:
            stations.append(self.doc_to_station(doc))
        # for station in stations:
        #     if station['is_synced']:
        #         synced_list.append(station['station_name'])
        # used to block sync synced station, but allowing for now
        # if len(synced_list) != 0:
        #     return None, False, http.HttpException(
        #         message=self.T('Station %(synced_list)s is synced', dict(synced_list=synced_list)),
        #         http_code=400,
        #     )

        # get send data
        send_datas = self.mongo_client.stations_send_data.find({"station_id": {'$in': station_str_decimal_ids}})
        map_station_id_to_send_data = {}
        for send_data in send_datas:
            map_station_id_to_send_data[send_data['station_id']] = send_data
        for station in stations:
            if str(int(station['id'], 16)) in map_station_id_to_send_data:
                send_data = map_station_id_to_send_data[str(int(station['id'], 16))]
                station['send_data'] = send_data
        # get indicator data

        return stations, True, None

    def request_sync_station_to_station(self, request_station):
        station = request_station.copy()
        station.pop("approve_status")
        station.pop("station_id")
        station.pop("id")
        return station

    def doc_to_request_sync_station(self, row, station_types):
        request_sync_station = self.doc_to_station(row)
        request_sync_station.pop('is_synced')
        approve_status = ''
        if 'approve_status' in row:
            approve_status = row['approve_status']
        station_id = None
        station_id_decimal = None
        if 'station_id' in row and row['station_id']:
            station_id = str(row['station_id'])
            station_id_decimal = str(int(station_id, 16))
        reason = ''
        if 'reason' in row:
            reason = row['reason']
        request_sync_station['approve_status'] = approve_status
        request_sync_station['station_id'] = station_id
        request_sync_station['station_id_decimal'] = station_id_decimal
        request_sync_station['reason'] = reason
        request_sync_station['str_station_type'] = station_types[str(request_sync_station["station_type"])]

        if 'request_sync_station_id' in row:
            request_sync_station['request_sync_station_id'] = row['request_sync_station_id']

        return request_sync_station

    def doc_to_station(self, row):
        area_ids = []
        if 'area_ids' in row:
            area_ids = row['area_ids']
        agents_id = ''
        if 'agents_id' in row:
            agents_id = row['agents_id']
        address = ''
        if "address" in row:
            address = row["address"]
        contact_point = ''
        if "contact_point" in row:
            contact_point = row["contact_point"]
        data_folder = ''
        if "data_folder" in row:
            data_folder = row["data_folder"]
        data_server = ''
        if "data_server" in row:
            data_server = "ftp.envisoft.gov.vn"
        data_server_port = ''
        if "data_server_port" in row:
            data_server_port = "21"
        data_server_public = ''
        if "data_server_public" in row:
            data_server_public = row["data_server_public"]
        data_source = ''
        if "data_source" in row:
            data_source = row["data_source"]
        description = ''
        if "description" in row:
            description = row["description"]
        email = ''
        if "email" in row:
            email = row["email"]
        file_mapping = ''
        if "file_mapping" in row:
            file_mapping = row["file_mapping"]
        file_mapping_desc = ''
        if "file_mapping_desc" in row:
            file_mapping_desc = row["file_mapping_desc"]
        frequency_receiving_data = None
        if "frequency_receiving_data" in row:
            frequency_receiving_data = row["frequency_receiving_data"]
        ftp_connection_status = False
        if "ftp_connection_status" in row:
            ftp_connection_status = row["ftp_connection_status"]
        interval_scan = None
        if "interval_scan" in row:
            interval_scan = row["interval_scan"]
        is_public = False
        if "is_public" in row:
            is_public = row["is_public"]
        is_public_data_type = None
        if "is_public_data_type" in row:
            is_public_data_type = row["is_public_data_type"]
        is_qi = None
        if "is_qi" in row:
            is_qi = row["is_qi"]
        last_file_content = ''
        if "last_file_content" in row:
            last_file_content = row["last_file_content"]
        last_file_name = ''
        if "last_file_name" in row:
            last_file_name = row["last_file_name"]
        last_file_path = ''
        if "last_file_path" in row:
            last_file_path = row["last_file_path"]
        last_qty_adjusting = None
        if "last_qty_adjusting" in row:
            last_qty_adjusting = row["last_qty_adjusting"]
        last_qty_error = None
        if "last_qty_error" in row:
            last_qty_error = row["last_qty_error"]
        last_qty_exceed = None
        if "last_qty_exceed" in row:
            last_qty_exceed = row["last_qty_exceed"]
        last_qty_good = None
        if "last_qty_good" in row:
            last_qty_good = row["last_qty_good"]
        last_time = None
        if "last_time" in row and row["last_time"]:
            last_time = row["last_time"]
        latitude = None
        if "latitude" in row:
            latitude = row["latitude"]
        longitude = None
        if "longitude" in row:
            longitude = row["longitude"]
        logger_id = ''
        if "logger_id" in row:
            logger_id = row["logger_id"]
        mqtt_client_id = ''
        if "mqtt_client_id" in row:
            mqtt_client_id = row["mqtt_client_id"]
        off_time = None
        if "off_time" in row and row["off_time"]:
            off_time = row["off_time"]
        order_in_area = None
        if "order_in_area" in row:
            order_in_area = row["order_in_area"]
        order_no = None
        if "order_no" in row:
            order_no = row["order_no"]
        path_format = None
        if "path_format" in row:
            path_format = row["path_format"]
        phone = ''
        if "phone" in row:
            phone = row["phone"]
        qi = None
        if "qi" in row:
            qi = row["qi"]
        qi_adjsut_time = None
        if "qi_adjsut_time" in row:
            qi_adjsut_time = row["qi_adjsut_time"]
        qi_adjust = None
        if "qi_adjust" in row:
            qi_adjust = row["qi_adjust"]
        qi_time = None
        if "qi_time" in row:
            qi_time = row["qi_time"]
        qty_adjusting = None
        if "qty_adjusting" in row:
            qty_adjusting = row["qty_adjusting"]
        qty_error = None
        if "qty_error" in row:
            qty_error = row["qty_error"]
        qty_exceed = None
        if "qty_exceed" in row:
            qty_exceed = row["qty_exceed"]
        qty_good = None
        if "qty_good" in row:
            qty_good = row["qty_good"]
        retry = None
        if "retry" in row:
            retry = row["retry"]
        scan_failed = None
        if "scan_failed" in row:
            scan_failed = row["scan_failed"]
        station_code = ''
        if "station_code" in row:
            station_code = row["station_code"]
        station_name = ''
        if "station_name" in row and row["station_name"]:
            station_name = row["station_name"]
        station_type = None
        if "station_type" in row:
            station_type = row["station_type"]
        status = None
        if "status" in row:
            status = row["status"]
        time_count_offline = None
        if "time_count_offline" in row:
            time_count_offline = row["time_count_offline"]
        transfer_type = None
        if "transfer_type" in row:
            transfer_type = row["transfer_type"]
        username = None
        if "username" in row:
            username = row["username"]
        is_synced = False
        if 'is_synced' in row:
            is_synced = row['is_synced']
        pwd = None
        if 'pwd' in row:
            pwd = row['pwd']
        ftp_id = None
        if 'ftp_id' in row:
            ftp_id = row['ftp_id']

        period_ra = None
        if 'period_ra' in row:
            period_ra = row['period_ra']

        career = None
        if 'career' in row:
            career = row['career']
        implement_agency_ra = None
        if 'implement_agency_ra' in row:
            implement_agency_ra = row['implement_agency_ra']
        contact_info = None
        if 'contact_info' in row:
            contact_info = row['contact_info']
        verification_deadline = None
        if 'verification_deadline' in row:
            verification_deadline = row['verification_deadline']
        country_code = None
        if 'country_code' in row:
            country_code = row['country_code']
        return {
            'country_code': country_code,
            'verification_deadline': verification_deadline,
            'contact_info': contact_info,
            'implement_agency_ra': implement_agency_ra,
            'career': career,
            'id': str(row["_id"]),
            'agents_id': agents_id,
            'area_ids': area_ids,
            'address': address,
            'contact_point': contact_point,
            'data_folder': data_folder,
            'data_server': data_server,
            'data_server_port': data_server_port,
            'data_server_public': data_server_public,
            'data_source': data_source,
            'description': description,
            'email': email,
            'file_mapping': file_mapping,
            'file_mapping_desc': file_mapping_desc,
            'frequency_receiving_data': frequency_receiving_data,
            'ftp_connection_status': ftp_connection_status,
            'interval_scan': interval_scan,
            'is_public': is_public,
            'is_public_data_type': is_public_data_type,
            'is_qi': is_qi,
            'last_file_content': last_file_content,
            'last_file_name': last_file_name,
            'last_file_path': last_file_path,
            'last_qty_adjusting': last_qty_adjusting,
            'last_qty_error': last_qty_error,
            'last_qty_exceed': last_qty_exceed,
            'last_qty_good': last_qty_good,
            'last_time': last_time,
            'latitude': latitude,
            'longitude': longitude,
            'logger_id': logger_id,
            'mqtt_client_id': mqtt_client_id,
            'off_time': off_time,
            'order_in_area': order_in_area,
            'order_no': order_no,
            'path_format': path_format,
            'phone': phone,
            'qi': qi,
            'qi_adjsut_time': qi_adjsut_time,
            'qi_adjust': qi_adjust,
            'qi_time': qi_time,
            'qty_adjusting': qty_adjusting,
            'qty_error': qty_error,
            'qty_exceed': qty_exceed,
            'qty_good': qty_good,
            'retry': retry,
            'scan_failed': scan_failed,
            'station_code': station_code,
            'station_name': station_name,
            'station_type': station_type,
            'status': status,
            'time_count_offline': time_count_offline,
            'transfer_type': transfer_type,
            'username': username,
            'is_synced': is_synced,
            'pwd': pwd,
            'ftp_id': ftp_id,
            'period_ra': period_ra,
        }


def get_str_decimal_station_id(station):
    if 'station_id' in station and station['station_id']:
        return station['station_id']
    str_hex_id = ''
    if '_id' in station and station['_id']:
        str_hex_id = station['_id']
    if 'id' in station and station['id']:
        str_hex_id = station['id']
    if str_hex_id == '':
        return str_hex_id
    return str(int(str_hex_id, 16))


conversion_table = {
    0: '0',
    1: '1',
    2: '2',
    3: '3',
    4: '4',
    5: '5',
    6: '6',
    7: '7',
    8: '8',
    9: '9',
    10: 'A',
    11: 'B',
    12: 'C',
    13: 'D',
    14: 'E',
    15: 'F'}


def decimal_to_hex(decimal):
    if (decimal <= 0):
        return ''
    remainder = decimal % 16
    return decimal_to_hex(decimal // 16) + conversion_table[remainder]
