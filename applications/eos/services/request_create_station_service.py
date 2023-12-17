import logging
from gluon import current

if False:
    from gluon import *

    request = current.request
    response = current.response
    session = current.session
    cache = current.cache
    T = current.T
    db = current.db

from applications.eos.modules import const


class RequestCreateStationService:
    def __init__(self, db, T):
        self.T = T
        self.current = current
        self.db = db

    def handle_approve(self, request_create_station, reason):
        # create station data
        new_station_id = self.db.stations.insert(
            address=request_create_station.address,
            agents_id=request_create_station.agents_id,
            area_id=request_create_station.area_id,
            contact_point=request_create_station.contact_point,
            data_folder=request_create_station.data_folder,
            data_server=request_create_station.data_server,
            data_server_port=request_create_station.data_server_port,
            data_server_public=request_create_station.data_server_public,
            data_source=request_create_station.data_source,
            description=request_create_station.description,
            email=request_create_station.email,
            file_mapping=request_create_station.file_mapping,
            file_mapping_desc=request_create_station.file_mapping_desc,
            frequency_receiving_data=request_create_station.frequency_receiving_data,
            ftp_connection_status=request_create_station.ftp_connection_status,
            ftp_id=request_create_station.ftp_id,
            interval_scan=request_create_station.interval_scan,
            is_public=request_create_station.is_public,
            is_public_data_type=request_create_station.is_public_data_type,
            is_qi=request_create_station.is_qi,
            last_file_content=request_create_station.last_file_content,
            last_file_name=request_create_station.last_file_name,
            last_file_path=request_create_station.last_file_path,
            last_qty_adjusting=request_create_station.last_qty_adjusting,
            last_qty_error=request_create_station.last_qty_error,
            last_qty_exceed=request_create_station.last_qty_exceed,
            last_qty_good=request_create_station.last_qty_good,
            last_time=request_create_station.last_time,
            latitude=request_create_station.latitude,
            longitude=request_create_station.longitude,
            logger_id=request_create_station.logger_id,
            mqtt_client_id=request_create_station.mqtt_client_id,
            mqtt_pwd=request_create_station.mqtt_pwd,
            mqtt_usr=request_create_station.mqtt_usr,
            off_time=request_create_station.off_time,
            order_in_area=request_create_station.order_in_area,
            order_no=request_create_station.order_no,
            path_format=request_create_station.path_format,
            phone=request_create_station.phone,
            province_id=request_create_station.province_id,
            pwd=request_create_station.pwd,
            qi=request_create_station.qi,
            qi_adjsut_time=request_create_station.qi_adjsut_time,
            qi_adjust=request_create_station.qi_adjust,
            qi_time=request_create_station.qi_time,
            retry=request_create_station.retry,
            scan_failed=request_create_station.scan_failed,
            station_code=request_create_station.station_code,
            station_id=request_create_station.station_id,
            station_name=request_create_station.station_name,
        )
        # update decimal id for station
        station = self.db.stations(new_station_id)
        station.update_record(station_id=new_station_id)

        map_create_request_station_equipment_id_to_equipment = self.handle_clone_equipment(request_create_station.id,
                                                                                           new_station_id)
        self.handle_clone_dataloger_and_command(request_create_station.id, new_station_id)
        self.handle_clone_alarm(request_create_station.id, new_station_id)
        self.handle_clone_camera_links(request_create_station.id, new_station_id)
        self.handle_clone_stations_send_data(request_create_station.id, new_station_id)
        self.handle_clone_station_indicator(request_create_station.id, new_station_id,
                                            map_create_request_station_equipment_id_to_equipment)
        self.handle_clone_data_hour_lastest(request_create_station.id, new_station_id)
        self.handle_clone_data_month_lastest(request_create_station.id, new_station_id)
        self.handle_clone_data_day_lastest(request_create_station.id, new_station_id)
        self.handle_clone_data_lastest(request_create_station.id, new_station_id)
        self.handle_clone_last_data_files(request_create_station.id, new_station_id)
        self.handle_clone_data_aqi_hour_lastest(request_create_station.id, new_station_id)
        self.handle_clone_data_aqi_24h_lastest(request_create_station.id, new_station_id)
        self.handle_clone_qcvn_station_kind(request_create_station.id, new_station_id)

        # update request_create_station
        request_create_station.update_record(approve_status=const.REQUEST_CREATE_STATION_APPROVED_STATUS,
                                             approve_reason=reason, station_id=new_station_id)

    def handle_reject(self, request_create_station, reason):
        request_create_station.update_record(approve_status=const.REQUEST_CREATE_STATION_REJECTED_STATUS,
                                             approve_reason=reason)

    def handle_clone_equipment(self, request_create_station_id, new_station_id):
        request_create_station_equipments = self.db(
            self.db.request_create_station_equipments.request_create_station_id == request_create_station_id).select()
        if not request_create_station_equipments:
            return
        list_equipments = []
        for item in request_create_station_equipments:
            item_dict = item.as_dict()
            del item_dict["request_create_station_id"]
            item_dict['station_id'] = new_station_id
            list_equipments.append(item_dict)
        new_ids = self.db.equipments.bulk_insert(list_equipments)
        map_create_request_station_equipment_id_to_equipment = {}
        for i in range(len(request_create_station_equipments)):
            map_create_request_station_equipment_id_to_equipment[request_create_station_equipments[i].id] = new_ids[i]
        return map_create_request_station_equipment_id_to_equipment

    def handle_clone_dataloger_and_command(self, request_create_station_id, new_station_id):
        request_create_station_data_loggers = self.db(
            self.db.request_create_station_datalogger.request_create_station_id == request_create_station_id).select()
        if request_create_station_data_loggers:
            list_data_logger = []
            for item in request_create_station_data_loggers:
                item_dict = item.as_dict()
                del item_dict["request_create_station_id"]
                item_dict['station_id'] = new_station_id
                list_data_logger.append(item_dict)
            self.db.datalogger.bulk_insert(list_data_logger)

        request_create_station_data_logger_commands = self.db(
            self.db.request_create_station_datalogger_command.request_create_station_id == request_create_station_id).select()
        if request_create_station_data_logger_commands:
            list_data_logger_command = []
            for item in request_create_station_data_logger_commands:
                item_dict = item.as_dict()
                del item_dict["request_create_station_id"]
                item_dict['station_id'] = new_station_id
                list_data_logger_command.append(item_dict)
            self.db.datalogger_command.bulk_insert(list_data_logger_command)
        return

    def handle_clone_alarm(self, request_create_station_id, new_station_id):
        request_create_station_alarms = self.db(
            self.db.request_create_station_alarm.request_create_station_id == request_create_station_id).select()
        if not request_create_station_alarms:
            return
        list_station_alarm = []
        for item in request_create_station_alarms:
            item_dict = item.as_dict()
            del item_dict["request_create_station_id"]
            item_dict['station_id'] = new_station_id
            list_station_alarm.append(item_dict)
        self.db.station_alarm.bulk_insert(list_station_alarm)
        return

    def handle_clone_camera_links(self, request_create_station_id, new_station_id):
        request_create_station_camera_links = self.db(
            self.db.request_create_station_camera_links.request_create_station_id == request_create_station_id).select()
        if not request_create_station_camera_links:
            return
        list_camera_links = []
        for item in request_create_station_camera_links:
            item_dict = item.as_dict()
            del item_dict["request_create_station_id"]
            item_dict['station_id'] = new_station_id
            list_camera_links.append(item_dict)
        self.db.camera_links.bulk_insert(list_camera_links)
        return

    def handle_clone_stations_send_data(self, request_create_station_id, new_station_id):
        request_create_station_send_data = self.db(
            self.db.request_create_station_send_data.request_create_station_id == request_create_station_id).select()
        if not request_create_station_send_data:
            return
        list_station_send_data = []
        for item in request_create_station_send_data:
            item_dict = item.as_dict()
            del item_dict["request_create_station_id"]
            item_dict['station_id'] = new_station_id
            list_station_send_data.append(item_dict)
        self.db.stations_send_data.bulk_insert(list_station_send_data)
        return

    def handle_clone_station_indicator(self, request_create_station_id, new_station_id,
                                       request_create_station_equipment_id_to_equipment_id):
        request_create_station_indicator = self.db(
            self.db.request_create_station_indicator.request_create_station_id == request_create_station_id).select()
        if not request_create_station_indicator:
            return
        list_station_indicator = []
        for item in request_create_station_indicator:
            item_dict = item.as_dict()
            del item_dict["request_create_station_id"]
            item_dict['station_id'] = new_station_id
            request_create_station_equipment_id = item_dict['equipment_id']
            if request_create_station_equipment_id_to_equipment_id is not None:
                item_dict['equipment_id'] = request_create_station_equipment_id_to_equipment_id.get(
                    request_create_station_equipment_id)
            list_station_indicator.append(item_dict)
        self.db.station_indicator.bulk_insert(list_station_indicator)
        return

    def handle_clone_data_hour_lastest(self, request_create_station_id, new_station_id):
        request_create_station_data_hour_lastest = self.db(
            self.db.request_create_station_data_hour_lastest.request_create_station_id == request_create_station_id).select()
        if not request_create_station_data_hour_lastest:
            return
        list_data = []
        for item in request_create_station_data_hour_lastest:
            item_dict = item.as_dict()
            del item_dict["request_create_station_id"]
            item_dict['station_id'] = new_station_id
            list_data.append(item_dict)
        self.db.data_hour_lastest.bulk_insert(list_data)
        return

    def handle_clone_data_month_lastest(self, request_create_station_id, new_station_id):
        request_create_station_data_month_lastest = self.db(
            self.db.request_create_station_data_month_lastest.request_create_station_id == request_create_station_id).select()
        if not request_create_station_data_month_lastest:
            return
        list_data = []
        for item in request_create_station_data_month_lastest:
            item_dict = item.as_dict()
            del item_dict["request_create_station_id"]
            item_dict['station_id'] = new_station_id
            list_data.append(item_dict)
        self.db.data_month_lastest.bulk_insert(list_data)
        return

    def handle_clone_data_day_lastest(self, request_create_station_id, new_station_id):
        request_create_station_data_day_lastest = self.db(
            self.db.request_create_station_data_day_lastest.request_create_station_id == request_create_station_id).select()
        if not request_create_station_data_day_lastest:
            return
        list_data = []
        for item in request_create_station_data_day_lastest:
            item_dict = item.as_dict()
            del item_dict["request_create_station_id"]
            item_dict['station_id'] = new_station_id
            list_data.append(item_dict)
        self.db.data_day_lastest.bulk_insert(list_data)
        return

    def handle_clone_data_lastest(self, request_create_station_id, new_station_id):
        request_create_station_data_lastest = self.db(
            self.db.request_create_station_data_lastest.request_create_station_id == request_create_station_id).select()
        if not request_create_station_data_lastest:
            return
        list_data = []
        for item in request_create_station_data_lastest:
            item_dict = item.as_dict()
            del item_dict["request_create_station_id"]
            item_dict['station_id'] = new_station_id
            list_data.append(item_dict)
        self.db.data_lastest.bulk_insert(list_data)
        return

    def handle_clone_last_data_files(self, request_create_station_id, new_station_id):
        request_create_station_last_data_files = self.db(
            self.db.request_create_station_last_data_files.request_create_station_id == request_create_station_id).select()
        if not request_create_station_last_data_files:
            return
        list_data = []
        for item in request_create_station_last_data_files:
            item_dict = item.as_dict()
            del item_dict["request_create_station_id"]
            item_dict['station_id'] = new_station_id
            list_data.append(item_dict)
        self.db.last_data_files.bulk_insert(list_data)
        return

    def handle_clone_data_aqi_hour_lastest(self, request_create_station_id, new_station_id):
        request_create_station_data_aqi_hour_lastest = self.db(
            self.db.request_create_station_data_aqi_hour_lastest.request_create_station_id == request_create_station_id).select()
        if not request_create_station_data_aqi_hour_lastest:
            return
        list_data = []
        for item in request_create_station_data_aqi_hour_lastest:
            item_dict = item.as_dict()
            del item_dict["request_create_station_id"]
            item_dict['station_id'] = new_station_id
            list_data.append(item_dict)
        self.db.data_aqi_hour_lastest.bulk_insert(list_data)
        return

    def handle_clone_data_aqi_24h_lastest(self, request_create_station_id, new_station_id):
        request_create_station_data_aqi_24h_lastest = self.db(
            self.db.request_create_station_data_aqi_24h_lastest.request_create_station_id == request_create_station_id).select()
        if not request_create_station_data_aqi_24h_lastest:
            return
        list_data = []
        for item in request_create_station_data_aqi_24h_lastest:
            item_dict = item.as_dict()
            del item_dict["request_create_station_id"]
            item_dict['station_id'] = new_station_id
            list_data.append(item_dict)
        self.db.data_aqi_24h_lastest.bulk_insert(list_data)
        return

    def handle_clone_qcvn_station_kind(self, request_create_station_id, new_station_id):
        request_create_station_qcvn_station_kind = self.db(
            self.db.request_create_station_qcvn_station_kind.request_create_station_id == request_create_station_id).select()
        if not request_create_station_qcvn_station_kind:
            return
        list_data = []
        for item in request_create_station_qcvn_station_kind:
            item_dict = item.as_dict()
            del item_dict["request_create_station_id"]
            item_dict['station_id'] = new_station_id
            list_data.append(item_dict)
        self.db.qcvn_station_kind.bulk_insert(list_data)
        return
