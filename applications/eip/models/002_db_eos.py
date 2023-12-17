from applications.eos.modules import const, common
import datetime
from applications.eos.modules.plugin_ckeditor import CKEditor
ckeditor = CKEditor(db)

## if SSL/HTTPS is properly configured and you want all HTTP requests to be redirected to HTTPS, uncomment the line below:
# request.requires_https()

### Constant ###
station_type_value = []
station_type_disp = []
for key, item in common.sort_dict_const_by_value(const.STATION_TYPE):
    station_type_value.append(item['value'])
    station_type_disp.append(T(item['name']))

si_status_value = []
si_status_disp = []
for key, item in common.sort_dict_const_by_value(const.SI_STATUS):
    si_status_value.append(item['value'])
    si_status_disp.append(T(item['name']))

alarm_level_value = []
alarm_level_disp = []
for key, item in common.sort_dict_const_by_value(const.ALARM_LEVEL):
    alarm_level_value.append(item['value'])
    alarm_level_disp.append(T(item['name']))

alarm_log_level_value = []
alarm_log_level_disp = []
for key, item in common.sort_dict_const_by_value(const.ALARM_LOG_LEVEL):
    alarm_log_level_value.append(item['value'])
    alarm_log_level_disp.append(T(item['name']))

station_status_value = []
station_status_disp = []
station_status_color = []
for key, item in common.sort_dict_const_by_value(const.STATION_STATUS):
    station_status_value.append(item['value'])
    station_status_disp.append(T(item['name']))
    station_status_color.append(item['color'])

adjustment_type_value = []
adjustment_type_disp = []
for key, item in common.sort_dict_const_by_value(const.ADJUSTMENT_TYPE):
    adjustment_type_value.append(item['value'])
    adjustment_type_disp.append(T(item['name']))
adjustment_type_value.reverse()
adjustment_type_disp.reverse()

adjustment_status_value = []
adjustment_status_disp = []
for key, item in common.sort_dict_const_by_value(const.ADJUSTMENT_STATUS):
    adjustment_status_value.append(item['value'])
    adjustment_status_disp.append(T(item['name']))

sensor_trouble_history_status_value = []
sensor_trouble_history_status_disp = []
for key, item in common.sort_dict_const_by_value(const.SENSOR_STATUS):
    sensor_trouble_history_status_value.append(item['value'])
    sensor_trouble_history_status_disp.append(T(item['name']))

################################################################################
db.define_table('areas',
                Field('area_code', 'string', notnull=True),
                Field('area_name', 'string', notnull=True),
                Field('order_no', 'integer', default=0),
                Field('description', 'text'),
                )

################################################################################
db.define_table('provinces',
                Field('province_code', 'string', notnull=True, length=8),
                Field('province_name', 'string', notnull=True, length=32),
                Field('order_no', 'integer', default=0),
                Field('default', 'boolean', default=0),
                )
db.provinces.province_code.requires = [IS_NOT_EMPTY(), IS_NOT_IN_DB(db, db.provinces.province_code,
                                                                    error_message=T('Value is existed!'))]
db.provinces.province_name.requires = [IS_NOT_EMPTY(), IS_NOT_IN_DB(db, db.provinces.province_name,
                                                                    error_message=T('Value is existed!'))]

################################################################################
db.define_table('station_types',
                Field('code', 'string', length=16),
                Field('station_type', 'string', notnull=True, length=32),
                Field('station_type_english', 'string', length=32),
                Field('icon', 'upload'),
                Field('color', 'string', default='#ffffff'),
                Field('order', 'integer', default=0),
                )

################################################################################
db.define_table('alarm_levels',
                Field('station_type', 'integer', notnull=True, default=0),
                Field('level_name', 'integer', notnull=True),
                Field('color', 'string'),
                )
db.alarm_levels.station_type.requires = IS_IN_SET(station_type_value, station_type_disp)
db.alarm_levels.level_name.requires = IS_IN_SET([0, 1, 2, 3, 4],
                                                [T('Severe contemination'), T('High contemination'), T('Contemination'),
                                                 T('Slight contemination'), T('No data')])

################################################################################
db.define_table('agents',
                Field('agent_code', 'string', length=16, default=''),
                Field('agent_name', 'string', notnull=True, length=128),
                Field('manage_agent', 'string', notnull=True, default=''),
                Field('description', 'text', length=512),
                Field('longitude', 'double'),
                Field('latitude', 'double'),
                Field('province_id', 'string'),
                Field('area_id', 'string'),
                Field('order_number', 'integer', default=0),
                Field('address', 'string', length=256),
                Field('status', 'integer', default=0),
                Field('contact_point', 'string', length=128),
                Field('phone', 'string', length=64),  # dt cua nguoi dai dien agent
                Field('email', 'string', length=128),

                Field('data_server', 'string'),  # IP / link den server chua du lieu cua agent
                Field('data_server_port', 'string', default=21),
                Field('username', 'string'),
                Field('pwd', 'string'),
                Field('directory_format', 'string'),
                Field('file_format', 'string'),
                )
db.agents.agent_code.requires = [IS_NOT_EMPTY(),
                                 IS_NOT_IN_DB(db, db.agents.agent_code, error_message=T('Value is existed!'))]
db.agents.agent_name.requires = [IS_NOT_EMPTY(),
                                 IS_NOT_IN_DB(db, db.agents.agent_name, error_message=T('Value is existed!'))]
db.agents.longitude.requires = IS_NULL_OR(IS_DECIMAL_IN_RANGE(7, 24))
db.agents.latitude.requires = IS_NULL_OR(IS_DECIMAL_IN_RANGE(100, 112))
db.agents.province_id.requires = IS_IN_DB(db, db.provinces.id, db.provinces.province_name)
db.agents.area_id.requires = IS_NULL_OR(IS_IN_DB(db, db.areas.id, db.areas.area_name))

################################################################################
db.define_table('stations',
                Field('station_code', 'string', notnull=True, length=64, default=''),
                Field('station_name', 'string', notnull=True, length=128),
                Field('station_type', 'integer', notnull=True, default=0),
                Field('description', 'text', length=512),
                Field('longitude', 'double', notnull=True),
                Field('latitude', 'double', notnull=True, required=True),
                Field('agents_id', 'string'),
                Field('province_id', 'string', notnull=True),
                Field('area_id', 'string'),
                Field('area_ids', 'list:string'),
                Field('order_in_area', 'integer', default=0),
                Field('address', 'string', length=128),
                Field('status', 'integer', default=0),
                Field('off_time', 'datetime'),
                Field('contact_point', 'string'),
                Field('phone', 'string'),  # dt cua nguoi dai dien station
                Field('email', 'string'),
                Field('retry', 'integer', default=5),  # So nguong scan, neu vuot nguong coi nhu tram In-active
                Field('interval_scan', 'integer', default=5),
                Field('data_server', 'string'),  # IP / link den server chua du lieu cua station
                Field('data_server_port', 'string', default=21),
                Field('data_folder', 'string'),
                Field('username', 'string'),
                Field('pwd', 'string'),
                Field('is_qi', 'boolean', default=True),  # Neu tram do chi so AQI/WQI thi = True
                Field('qi', 'double'),  # Quality index (display on map)
                Field('qi_adjust', 'double'),  # Quality index (display on map)
                Field('qi_time', 'datetime'),
                Field('qi_adjsut_time', 'datetime'),
                Field('scan_failed', 'integer', default=0),  # Luu so lan da scan data nhung that bai
                Field('file_mapping', 'string'),
                Field('file_mapping_desc', 'text'),
                Field('logger_id', 'string', notnull=True),
                Field('is_public', 'boolean', default=False),
                Field('is_public_data_type', 'integer', default=const.DATA_TYPE['APPROVED']['value']),
                Field('path_format', 'integer', default=0),  # Luu so lan da scan data nhung that bai
                Field('frequency_receiving_data', 'integer', notnull=True, default=5), #tan suat nhan du lieu tinh theo phut
                Field('time_count_offline', 'integer', notnull=True, default=15), #time count offline
                Field('ftp_connection_status', 'boolean', notnull=True, default=True),
                Field('order_no', 'integer', default=0),
                Field('contact_info', 'string'),
                Field('verification_deadline', 'string'),
                Field('country_code', 'string'),
                Field('period_ra', 'date'),
                Field('implement_agency_ra', 'string'),
                Field('station_pictures', 'list:upload'),
                )
db.stations.station_type.requires = IS_IN_SET(station_type_value, station_type_disp)
db.stations.station_code.requires = [IS_NOT_EMPTY(),
                                     IS_NOT_IN_DB(db, db.stations.station_code, error_message=T('Value is existed!'))]
db.stations.station_name.requires = [IS_NOT_EMPTY(),
                                     IS_NOT_IN_DB(db, db.stations.station_name, error_message=T('Value is existed!'))]
db.stations.longitude.requires = [IS_NOT_EMPTY(), IS_DECIMAL_IN_RANGE(100, 112)]
db.stations.latitude.requires = [IS_NOT_EMPTY(), IS_DECIMAL_IN_RANGE(7, 24)]
db.stations.province_id.requires = IS_IN_DB(db, db.provinces.id, db.provinces.province_name)
db.stations.area_id.requires = IS_NULL_OR(IS_IN_DB(db, db.areas.id, db.areas.area_name))
db.stations.status.requires = IS_IN_SET(station_status_value, station_status_disp)
db.stations.agents_id.requires = IS_NULL_OR(IS_IN_DB(db, db.agents.id, db.agents.agent_name))
db.stations.path_format.requires = IS_IN_SET([0, 1, 2, 3, 4], [T('Stations path format 1'),
                                                                  T('Stations path format 2'),
                                                                  T('Stations path format 3'),
                                                                  T('Stations path format 4'),
                                                                  T('Stations path format 5')])

################################################################################
db.define_table('station_role',  # Luu station thuoc group/role nao
                Field('station_id', 'string', notnull=True),
                Field('role_id', 'string', notnull=True),
                )

################################################################################
db.define_table('indicators',
                Field('indicator', 'string', notnull=True),  # For display
                Field('source_name', 'string', notnull=True),  # Ten trong file source (txt)
                Field('indicator_type', 'integer'),
                Field('tendency_value', 'double', notnull=True, default=0),
                Field('preparing_value', 'double', notnull=True, default=0),
                Field('exceed_value', 'double', notnull=True, default=0),
                Field('unit', 'string'),
                )
db.indicators.indicator_type.requires = IS_IN_SET(station_type_value, station_type_disp)

db.define_table('aqi_indicators',  # Bang master luu cac gtri quy chuan de tinh ra cac gtri AQI cu the
                Field('indicator_id', 'string', notnull=True),
                Field('indicator', 'string', notnull=True),
                Field('qc_1h', 'double'),
                Field('qc_3h', 'double'),
                Field('qc_24h', 'double'),
                Field('qc_1y', 'double'),
                )

db.define_table('aqi_data_hour',
                Field('station_id', 'string', notnull=True),
                Field('get_time', 'datetime', notnull=True),
                Field('data', 'json'),  # Gtri AQI chinh duoc luu trong key = 'aqi'
                )

db.define_table('aqi_data_24h',
                Field('station_id', 'string', notnull=True),
                Field('get_time', 'datetime', notnull=True),
                Field('data_24h', 'json'),  # la gtri trung binh cua 24h trong ngay
                Field('data_1d', 'json'),  # la gtri MAX(AQI_24h, AQI_1h) trong ngay
                )

########################################################################################################################

db.define_table('aqi_data_adjust_hour',  # Luu du lieu adjust, tinh aqi adjust theo gio
                Field('station_id', 'string', notnull=True),
                Field('get_time', 'datetime', notnull=True),
                Field('data', 'json'),  # Gtri AQI chinh duoc luu trong key = 'aqi'
                )

########################################################################################################################
db.define_table('aqi_data_adjust_24h',  # Luu du lieu  adjust, tinh aqi adjust theo 24 gio
                Field('station_id', 'string', notnull=True),
                Field('get_time', 'datetime', notnull=True),
                Field('data_24h', 'json'),  # la gtri trung binh cua 24h trong ngay
                Field('data_1d', 'json'),  # la gtri MAX(AQI_24h, AQI_1h) trong ngay
                )

db.define_table('wqi_data_hour',
                Field('station_id', 'string', notnull=True),
                Field('get_time', 'datetime', notnull=True),
                Field('data', 'json'),  # Gtri WQI chinh duoc luu trong key = 'wqi'
                )

db.define_table('wqi_data_adjust_hour',
                Field('station_id', 'string', notnull=True),
                Field('get_time', 'datetime', notnull=True),
                Field('data', 'json'),  # Gtri WQI chinh duoc luu trong key = 'wqi'
                )

db.define_table('app_settings',
                Field('app_id', 'string', notnull=True),
                Field('current_version', 'string', notnull=True),
                Field('must_update', 'integer'),  # la gtri trung binh cua 24h trong ngay
                Field('message_update', 'string'),  # la gtri MAX(WQI_24h, WQI_1h) trong ngay
                Field('link_api_header', 'string'),
                Field('change_value_common_setting', 'string'),
                )

################################################################################
db.define_table('equipments',
                Field('station_id', 'string', notnull=True),
                Field('station_type', 'integer'),
                Field('equipment', 'string', notnull=True),
                Field('brandname', 'string'),
                Field('start_date', 'date'),  # Ngay bat dau chay
                Field('warranty_start', 'date'),  # del capacity, model
                Field('warranty_end', 'date'),
                Field('implement_date', 'date'),
                Field('produce_date', 'date'),
                Field('lrv', 'double'),
                Field('urv', 'double'),
                Field('provider', 'string'),
                Field('series', 'string'),
                Field('made_in', 'string'),
                Field('status', 'integer', default=0),
                Field('description', 'text')
                )
db.equipments.station_id.requires = IS_IN_DB(db, db.stations.id, db.stations.station_name)
db.equipments.station_type.requires = IS_IN_SET(station_type_value, station_type_disp)
db.equipments.status.requires = IS_IN_SET([0, 1, 2, 3, 4],
                                          [T('Not in use'), T('In use'), T('Failing'), T('Maintenance'),
                                           T('Need replace')])

################################################################################
db.define_table('camera_links',
                Field('station_type', 'integer', notnull=True, default=0),
                Field('station_id', 'string', notnull=True),
                Field('station_name', 'string'),
                Field('order_no', 'integer', default=0),
                Field('is_visible', 'boolean', default=True),
                Field('camera_source', 'string', notnull=True, length=128),
                Field('description', 'string', length=512),
                )
db.camera_links.station_type.requires = IS_IN_SET(station_type_value, station_type_disp)

################################################################################
db.define_table('station_indicator',
                Field('station_id', 'string', notnull=True),
                Field('station_name', 'string', notnull=True),
                Field('station_type', 'integer', notnull=True),
                Field('indicator_id', 'string', notnull=True),
                Field('tendency_value', 'double', notnull=True, default=0),
                Field('preparing_value', 'double', notnull=True, default=0),
                Field('exceed_value', 'double', notnull=True, default=0),
                Field('unit', 'string', notnull=True, default=''),
                Field('qcvn_id', 'string'),
                Field('qcvn_code', 'string'),
                Field('qcvn_detail_id', 'string'),
                Field('qcvn_detail_type_code', 'string'),
                Field('qcvn_detail_min_value', 'double'),
                Field('qcvn_detail_max_value', 'double'),
                Field('qcvn_detail_const_area_value', 'double'),
                Field('equipment_id', 'string'),  # Mot thiet bi luu dc nhieu thong so
                Field('equipment_name', 'string'),
                Field('equipment_urv', 'double'),
                Field('equipment_lrv', 'double'),
                Field('mapping_name', 'string'),
                Field('convert_rate', 'double', default=1),
                Field('status', 'integer', default=const.SI_STATUS['IN_USE']['value']),

                Field('is_public', 'boolean', default=False),
                Field('equal0', 'boolean', default=False),
                Field('negative_value', 'boolean', default=False),
                Field('out_of_range', 'boolean', default=False),
                Field('out_of_range_min', 'double'),
                Field('out_of_range_max', 'double'),
                Field('equipment_adjust', 'boolean', default=False),  # Todo : chua clear req
                Field('equipment_status', 'boolean', default=False),  # Todo : chua clear req
                Field('continous_equal', 'boolean', default=False),
                Field('continous_equal_value', 'integer'),
                Field('continous_times', 'integer', default=0),
                Field('is_calc_qi', 'boolean', default=False),
                Field('extraordinary_value_check', 'boolean', default=False),
                Field('extraordinary_value', 'integer', default=0),
                Field('compare_value_check', 'boolean', default=False),
                Field('compare_value', 'string'),
                Field('coefficient_data', 'double', default=0),
                Field('parameter_value', 'string'),
                )
db.station_indicator.station_type.requires = IS_IN_SET(station_type_value, station_type_disp)
db.station_indicator.status.requires = IS_IN_SET(si_status_value, si_status_disp)

################################################################################
db.define_table('station_alarm',  # Cac tram khi co cac loai alarm thi bao cho ai, bang cach gi
                Field('station_id', 'string', notnull=True),
                Field('station_name', 'string', notnull=True),
                Field('station_type', 'string', notnull=True),
                Field('tendency_method_email', 'boolean', default=False),  # Gui email
                Field('preparing_method_email', 'boolean', default=False),
                Field('exceed_method_email', 'boolean', default=False),
                Field('tendency_method_sms', 'boolean', default=False),  # Gui SMS
                Field('preparing_method_sms', 'boolean', default=False),
                Field('exceed_method_sms', 'boolean', default=False),
                Field('tendency_phone_list', 'string'),  # Danh sach SDT gui SMS
                Field('preparing_phone_list', 'string'),
                Field('exceed_phone_list', 'string'),
                Field('tendency_email_list', 'string'),  # Danh sach email gui msg
                Field('preparing_email_list', 'string'),
                Field('exceed_email_list', 'string'),
                Field('tendency_msg', 'text'),  # Noi dung MSG gui di
                Field('preparing_msg', 'text'),
                Field('exceed_msg', 'text'),
                Field('exceed_emails_header', 'text'),
                )

################################################################################
db.define_table('alarm_logs',  # Ve co ban luu cac MESSAGE alarm setting in master
                Field('station_id', 'string', notnull=True),
                Field('station_name', 'string', notnull=True),
                Field('alarm_datetime', 'datetime', notnull=True, default=request.now),
                Field('content', 'text', notnull=True),
                Field('alarm_level', 'integer', notnull=True, default=0),
                Field('alarm_type', 'integer', notnull=True, default=0),
                Field('alarm_to', 'text', notnull=True),
                Field('alarm_to_phone', 'string', notnull=True),
                Field('status', 'integer', notnull=True, default=0),
                Field('send_sms', 'boolean', default=False),
                )
db.alarm_logs.station_id.requires = IS_IN_DB(db, db.stations.id, db.stations.station_name)
db.alarm_logs.alarm_level.requires = IS_IN_SET(alarm_log_level_value, alarm_log_level_disp)
db.alarm_logs.status.requires = IS_IN_SET([0, 1, 2, 3], [T('Not solve yet'), T('Checking'), T('Solving'), T('Solved')])
db.alarm_logs.alarm_type.requires = IS_IN_SET([0, 1], [T('Station alarm'), T('Indicator alarm')])

################################################################################
db.define_table('data_min_collect',  # Luu tong hop cac ban ghi data_min theo thang
                Field('station_id', 'string', notnull=True),
                Field('year', 'integer', notnull=True, default=0),
                Field('month', 'integer', notnull=True, default=0),
                Field('total', 'integer', notnull=True, default=0),
                Field('exceed', 'integer', notnull=False, default=0),
                )
db.data_min_collect.station_id.requires = IS_IN_DB(db, db.stations.id, db.stations.station_name)

################################################################################
db.define_table('commands',  # Mot command chi cho 1 station
                Field('station_id', 'string', notnull=True),  # Nguoi dung create cac command va luu o bang nay
                Field('station_name', 'string', notnull=True),
                Field('station_type', 'integer', notnull=True),
                Field('title', 'string', notnull=True),
                Field('command', 'string', notnull=True),
                Field('equipment_id', 'string', notnull=False),
                Field('bottle', 'integer', default=0),
                Field('created_date', 'date', default=request.now),
                Field('logger_id', 'string'),
                Field('status', 'integer', default=1, zero=1),
                Field('is_process', 'integer', default=0),
                Field('send_data_logger_time', 'integer', default=0),
                Field('datalogger_transaction_id', 'string'),
                )
db.commands.station_type.requires = IS_IN_SET(station_type_value, station_type_disp)
db.commands.status.requires = IS_IN_SET([0, 1], [T('CMD_waiting'), T('CMD_now')])
db.commands.is_process.requires = IS_IN_SET([0, 1], [T('CMD_unfulfilled'), T('CMD_complete')])
# db.commands.equipment_id.requires = IS_IN_DB(db, db.equipments.id, db.equipments.equipment)

################################################################################
db.define_table('commands_schedule',  # Lich chay cua cac command se luu o bang nay
                Field('command_id', 'string', notnull=True),
                Field('station_id', 'string', notnull=True),
                Field('station_name', 'string', notnull=True),
                Field('title', 'string', notnull=True),
                Field('issue_datetime', 'datetime', notnull=True, default=request.now),  # Ngay tao command
                Field('execute_datetime', 'datetime'),  # Ngay chay command
                Field('status', 'integer', notnull=True, default=0),
                Field('is_set_by_schedule', 'boolean', notnull=True, default=False),
                # Command nay duoc issue truc tiep hay tao qua man hinh schedule
                )
db.commands_schedule.status.requires = IS_IN_SET([0, 1, 2], [T('Not run'), T('Running'), T('Finished')])

################################################################################
db.define_table('command_results',  # Ket qua cua cac lan chay command se luu o bang nay
                Field('command_schedule_id', 'string', notnull=True),
                Field('command_id', 'string', notnull=True),
                Field('station_id', 'string', notnull=True),
                Field('station_name', 'string', notnull=True),
                Field('title', 'string', notnull=True),
                Field('issue_datetime', 'datetime', notnull=True, default=request.now),
                Field('results', 'json'),  # List cac chi so do dc
                )

################# Todo : bang nay sau xoa ###############################################################
db.define_table('command_schedule',
                Field('command_id', 'string', notnull=True),
                Field('start_time', 'datetime', notnull=True, default=request.now),
                Field('end_time', 'datetime', notnull=True),
                Field('inteval', 'integer', notnull=True),
                Field('repeat', 'integer', notnull=True),
                # -1 : ko repeate, 0 : theo phut, 1 : theo gio, 2 : theo ngay, 3 : theo tuan, 4 : theo thang
                )
db.command_schedule.repeat.requires = IS_IN_SET([-1, 0, 1, 2, 3, 4],
                                                [T('No repeat'), T('Minutely'), T('Hourly'), T('Daily'), T('Weekly'),
                                                 T('Monthly')])

################################################################################
db.define_table('last_data_files',
                Field('filename', 'string', notnull=True),
                Field('lasttime', 'datetime', notnull=True),
                Field('station_id', 'string', notnull=True),
                Field('station_name', 'string')
                )

################################################################################
db.define_table('data_lastest',  # De luu cac du lieu cua tram moi nhat
                Field('station_id', 'string', notnull=True),
                Field('get_time', 'datetime', notnull=True),
                Field('is_exceed', 'boolean', default=False),  # De danh dau cac record co du lieu vuot nguong
                Field('data', 'json'),  # Truong nay luu dict cac chi so {ten chi so : gtri)
                Field('data_status', 'json'),  # Truong nay luu dict cac chi so {ten chi so : gtri)
                )

################################################################################
db.define_table('data_adjust',  # Luu nhung du lieu do nguoi dung chinh sua
                Field('station_id', 'string', notnull=True),
                Field('get_time', 'datetime', notnull=True),
                Field('is_exceed', 'boolean', default=False),
                # Cho vao de khop du lieu giua cac bang, thuc chat k dung den
                Field('data', 'json'),
                Field('is_approved', 'boolean', default=False),
                Field('del_flag', 'boolean', default=False),
                )
################################################################################
db.define_table('data_hour_adjust',  # Luu du lieu goc, tinh trung binh theo gio
                Field('station_id', 'string', notnull=True),
                Field('get_time', 'datetime', notnull=True),
                Field('data', 'json'),
                )

################################################################################
db.define_table('data_day_adjust',  # Luu du lieu goc, tinh trung binh theo gio
                Field('station_id', 'string', notnull=True),
                Field('get_time', 'date', notnull=True),
                Field('data', 'json'),
                Field('data_min', 'json'),
                Field('data_max', 'json'),
                Field('data_min_time', 'json'),
                Field('data_max_time', 'json'),
                )

################################################################################
db.define_table('data_mon_adjust',  # Luu du lieu goc, tinh trung binh theo thang
                Field('station_id', 'string', notnull=True),
                Field('get_time', 'date', notnull=True),
                Field('data', 'json'),
                Field('data_min', 'json'),
                Field('data_max', 'json'),
                Field('data_min_time', 'json'),
                Field('data_max_time', 'json'),
                )
################################################################################
db.define_table('data_approve',  # Luu nhung du lieu do nguoi dung chinh sua
                Field('station_id', 'string', notnull=True),
                Field('get_time', 'datetime', notnull=True),
                Field('is_exceed', 'boolean', default=False),
                # Cho vao de khop du lieu giua cac bang, thuc chat k dung den
                Field('data', 'json'),
                )

################################################################################
db.define_table('data_alarm',  # Luu nhung du lieu bi canh bao
                Field('station_id', 'string', notnull=True),
                Field('get_time', 'datetime', notnull=True),
                Field('alarm_level', 'integer', notnull=True),
                Field('data', 'json'),
                Field('data_status', 'json'),
                Field('file_name', 'string'),
                Field('path_file', 'string'),
                Field('file_content', 'string'),
                )
db.data_alarm.alarm_level.requires = IS_IN_SET(alarm_level_value, alarm_level_disp)
db.data_alarm.station_id.requires = IS_IN_DB(db, db.stations.id, db.stations.station_name)

################################################################################
db.define_table('data_min',
                Field('station_id', 'string', notnull=True),
                Field('get_time', 'datetime', notnull=True),
                Field('is_exceed', 'boolean', default=False),  # De danh dau cac record co du lieu vuot nguong
                Field('data', 'json'),  # Truong nay luu dict cac chi so {ten chi so : gtri)
                Field('data_status', 'json'),  # Truong nay luu dict cac chi so {ten chi so : gtri)
                Field('file_name', 'string', notnull=True),  # Truong nay luu dict cac chi so {ten chi so : gtri)
                Field('file_content', 'string'),  # Luu tru txt file trong ftp
                Field('path_file', 'string'),  # Luu tru đường dẫn txt file trong ftp
                )
db.define_table('station_indicator_exceed',  # Luu du lieu vượt qui chuẩn
                Field('station_id', 'string', notnull=True),
                Field('indicator_id', 'string', notnull=True),
                Field('station_indicator_id', 'string', notnull=True),
                Field('indicator_name', 'string'),
                Field('value', 'double'),
                Field('unit', 'string'),
                Field('unit_convert_rate', 'integer', notnull=True, default=1),
                Field('get_time', 'datetime', notnull=True),
                Field('status', 'integer', notnull=True, default=0), # 0: đang đo, 1 = Hiệu chuẩn, 2 = lỗi thiết bị
                Field('is_exceed', 'boolean', default=False), # Có vượt QCVN hay không, False = Không, True = Có
                Field('station_qcvn_min', 'double'),
                Field('station_qcvn_max', 'double'),
                Field('file_name', 'string', notnull=True),  # Truong nay luu dict cac chi so {ten chi so : gtri)
                Field('path_file', 'string'),  # Luu tru đường dẫn txt file trong ftp
                Field('file_content', 'string'),  # Luu tru txt file trong ftp
                )
################################################################################
db.define_table('data_hour',
                Field('station_id', 'string', notnull=True),
                Field('get_time', 'datetime', notnull=True),
                Field('data', 'json'),
                )

################################################################################
db.define_table('data_day',
                Field('station_id', 'string', notnull=True),
                Field('get_time', 'date', notnull=True),
                Field('data', 'json'),
                Field('data_min', 'json'),
                Field('data_max', 'json'),
                Field('data_min_time', 'json'),
                Field('data_max_time', 'json'),
                )

################################################################################
db.define_table('data_mon',
                Field('station_id', 'string', notnull=True),
                Field('get_time', 'date', notnull=True),
                Field('data', 'json'),
                Field('data_min', 'json'),
                Field('data_max', 'json'),
                Field('data_min_time', 'json'),
                Field('data_max_time', 'json'),
                )

################################################################################
#hungdx add table to calculator data hour find lost issue 30
db.define_table('data_hour_lastest',
                Field('station_id', 'string', notnull=True),
                Field('last_time', 'datetime', notnull=True),
                )
db.define_table('data_day_lastest',
                Field('station_id', 'string', notnull=True),
                Field('last_time', 'datetime', notnull=True),
                )
db.define_table('data_month_lastest',
                Field('station_id', 'string', notnull=True),
                Field('last_time', 'datetime', notnull=True),
                )
################################################################################
db.define_table('notifications',
                Field('title', 'string', notnull=True),
                Field('sender', 'string', notnull=True),
                Field('receivers', 'list:string', notnull=True),
                Field('content', 'text'),
                Field('send_type', 'integer', notnull=True, default=0),
                Field('is_read', 'boolean', notnull=True, default='False'),
                Field('notify_level', 'integer', notnull=True, default=0),
                Field('notify_time', 'datetime', notnull=True, default=request.now)
                )
db.notifications.send_type.requires = IS_IN_SET([0, 1, 2], [T('System message'), T('Email'), T('SMS')])
db.notifications.notify_level.requires = IS_IN_SET([0, 1, 2], [T('Info'), T('Warning'), T('Error')])

################################################################################
db.define_table('settings',
                Field('lack_data_value', 'string'),
                Field('paging', 'string'),
                Field('server_input_ip', 'string'),
                Field('server_input_port', 'string'),
                Field('server_output_ip', 'string'),
                Field('online_refresh_timing', 'integer'),
                Field('get_data_interval', 'integer'),
                Field('recent_notification_day', 'integer', default=3),
                Field('recent_alarm_day', 'integer', default=3),
                )
db.settings.lack_data_value.requires = IS_IN_SET(['0', 'null'])

################################################################################
db.define_table('area_station',
                Field('area_id', 'string', notnull=True),
                Field('area_name', 'string', notnull=True),
                Field('order_no', 'integer', default=0),
                Field('station_id', 'string', notnull=True),
                Field('station_name', 'string', notnull=True),
                Field('station_type', 'string', notnull=True),
                )
################################################################################
db.define_table('station_off_log',
                Field('station_id', 'string', notnull=True),
                Field('station_name', 'string', notnull=True),
                Field('province_id', 'string', notnull=True),
                Field('station_type', 'integer', notnull=True),
                Field('start_off', 'datetime', notnull=True),
                Field('end_off', 'datetime'),
                Field('duration', 'integer', default=0),  # seconds
                )
db.station_off_log.station_type.requires = IS_IN_SET(station_type_value, station_type_disp)

################################################################################
db.define_table('command_log',
                Field('command', 'string', notnull=True),
                Field('command_date', 'datetime', notnull=True),
                )

################################################################################
db.define_table('adjustments',
                Field('station_id', 'string', notnull=True),
                Field('station_name', 'string', notnull=True),
                Field('created_by', 'string', notnull=True,
                      default=str(session.auth.user.id) if session.auth and hasattr(session.auth,
                                                                                    'user') and session.auth.user else ''),
                Field('created_date', 'date', notnull=True, default=request.now),
                Field('submit_to', 'string'),
                Field('from_date', 'datetime', notnull=True),
                Field('to_date', 'datetime', notnull=True),
                Field('title', 'string', notnull=True, length=256),
                Field('content', 'text'),
                Field('adjustment_type', 'integer', notnull=True, default=1),
                Field('status', 'integer', notnull=True, default=0),
                Field('logger_id', 'string'),
                Field('indicator_id', 'string', notnull=True, length=256),
                Field('indicator_name', 'string', notnull=True, length=256),
                Field('indicator_value_1', 'double'),
                Field('indicator_value_2', 'double'),
                Field('tolerance_value', 'double'),
                Field('is_process', 'integer', notnull=False, default=0),
                Field('datalogger_transaction_id', 'string'),
                )
db.adjustments.status.requires = IS_IN_SET(adjustment_status_value, adjustment_status_disp)
db.adjustments.adjustment_type.requires = IS_IN_SET(adjustment_type_value, adjustment_type_disp)
db.adjustments.submit_to.requires = IS_NULL_OR(IS_IN_DB(db, db.auth_user.id, db.auth_user._format))
db.adjustments.station_id.requires = IS_IN_DB(db, db.stations.id, db.stations.station_name)


def radioboxes(field, value):
    items = [DIV(INPUT(_type='radio', _id='%s_%s' % (field.name, key), _value=key, _name=field.name, value=value),
                 LABEL(name, _for='%s_%s' % (field.name, key)), _class='radio col-sm-6 col-md-4 col-lg-4')
             for key, name in field.requires.options() if key]
    return DIV(*items)


################################################################################
db.define_table('qcvn',  # Quy chuẩn kỹ thuật quốc gia, ký hiệu là QCVN
                Field('qcvn_code', 'string', notnull=True),
                Field('qcvn_type', 'integer', notnull=True, default=0),
                Field('qcvn_const_value', 'integer', notnull=True, default=0, widget=radioboxes,
                      requires=IS_IN_SET({1: T('LBL_CONST_VALUE_YES'), 2: T('LBL_CONST_VALUE_NO')}, sort=False)),
                Field('qcvn_type_compare', 'integer', notnull=True, default=0, widget=radioboxes,
                      requires=IS_IN_SET({0: T('LBL_PARA_VALUE'), 1: T('LBL_AV_PARA_VALUE')}, sort=False)),
                Field('qcvn_name', 'string', notnull=True, length=256),
                Field('qcvn_subject', 'string', length=256),
                Field('qcvn_description', 'text'),
                Field('qcvn_priority', 'integer', notnull=True, default=0),
                Field('status', 'integer', default=const.SI_STATUS['IN_USE']['value']),
                )
db.qcvn.qcvn_type.requires = IS_IN_SET(station_type_value, station_type_disp)

################################################################################
db.define_table('qcvn_kind',  # Loại tiêu chuẩn
                Field('qcvn_id', 'string', notnull=True),
                Field('qcvn_code', 'string', notnull=True, length=255),  # MÃ QCVN
                Field('qcvn_type', 'integer', notnull=True),
                Field('qcvn_kind', 'string', notnull=True),
                Field('qcvn_kind_order', 'integer', notnull=False, default=0),
                Field('qcvn_kind_delete_flag', 'integer', notnull=True, default=0),
                )

################################################################################
db.define_table('qcvn_detail',  # Giá trị giới hạn các thông số QCVN
                Field('qcvn_id', 'string', notnull=True),
                Field('qcvn_code', 'string', notnull=True, length=255),  # MÃ QCVN
                Field('qcvn_type', 'integer', notnull=True),
                Field('indicator_id', 'string', notnull=True),
                Field('have_factor_qcvn', 'integer', default=const.HAVE_FACTOR_QCVN['YES']['value']),
                Field('tendency_value', 'double', notnull=True, default=0),
                Field('preparing_value', 'double', notnull=True, default=0),
                Field('exceed_value', 'double', notnull=True, default=0),
                Field('qcvn_min_value', 'double', default=0),
                Field('qcvn_max_value', 'double', notnull=True, default=0),
                Field('qcvn_const_area_value', 'double', notnull=False, default=0),
                Field('qcvn_type_code', 'string', notnull=True),
                Field('unit', 'string', notnull=True, default=''),
                Field('status', 'integer', default=const.SI_STATUS['IN_USE']['value']),
                Field('expression_qcvn_indicator', 'integer', default=const.EXPRESSION_QCVN_INDICATOR['EXPRESSION_1']['value']),
                )
db.qcvn_detail.qcvn_id.requires = IS_IN_DB(db, db.qcvn.id, db.qcvn.qcvn_code)
db.qcvn_detail.qcvn_type.requires = IS_IN_SET(station_type_value, station_type_disp)

################################################################################
db.define_table('qcvn_station_kind',  # Man hinh Tram > QCVN
                Field('qcvn_id', 'string', notnull=True),
                Field('station_id', 'string', notnull=True),
                Field('station_name', 'string', notnull=True),
                Field('qcvn_kind_id', 'string', notnull=True),
                Field('qcvn_detail_const_area_value_1', 'double'),
                Field('qcvn_detail_const_area_value_2', 'double'),
                Field('station_type', 'integer', notnull=True),
                Field('status', 'integer', default=const.SI_STATUS['IN_USE']['value']),
                )
# db.qcvn_station_kind.qcvn_id.requires = IS_IN_DB(db, db.qcvn.id)


################################################################################
db.define_table('agent_details',
                Field('agent_id', 'string', notnull=True),
                Field('agent_name', 'string', notnull=True, length=128),
                Field('agent_detail_id', 'string', notnull=True),
                Field('agent_detail_name', 'string', notnull=True, length=128),
                Field('data_server', 'string'),
                Field('data_server_port', 'string'),
                Field('directory_format', 'string'),
                Field('file_format', 'string'),
                Field('username', 'string'),
                Field('pwd', 'string'),
                )

################################################################################
db.define_table('agent_station',
                Field('agent_id', 'string', notnull=True),
                Field('agent_name', 'string', notnull=True),
                Field('order_no', 'integer', default=0),
                Field('station_id', 'string', notnull=True),
                Field('station_name', 'string', notnull=True),
                Field('station_type', 'string', notnull=True),
                )

################################################################################
db.define_table('ftp_send_receive',
                Field('send_agent_id', 'string', notnull=True),
                Field('send_agent_name', 'string', notnull=True),
                Field('receive_agent_id', 'string', notnull=True),
                Field('receive_agent_name', 'string', notnull=True),
                Field('file_name', 'string', notnull=True),
                Field('send_time', 'datetime', notnull=True, default=request.now),
                Field('status', 'integer', notnull=True, default=1),
                Field('alarm_status', 'boolean', default=False),  # False : chua gui canh bao, True : da gui canh bao
                Field('archive_status', 'boolean', default=False),  # False : chua luu, True : da luu
                )
db.ftp_send_receive.status.requires = IS_IN_SET([1, 2, 3, 4, 5], [T('Sent successful'),
                                                                  T('Failed to connect FTP'),
                                                                  T('Transmission error'),
                                                                  T('File format invalid'),
                                                                  T('File blank')])

################################################################################
db.define_table('stations_send_data',
                Field('station_id', 'string', notnull=True),
                Field('status', 'integer', notnull=True, default=1),
                Field('time_send_data', 'integer', notnull=True),
                Field('from_date', 'datetime', notnull=True, default=request.now),
                Field('file_format', 'string'),
                Field('file_name', 'string'),
                Field('file_format', 'string'),
                Field('ftp_path', 'string', notnull=True),
                Field('ftp_ip', 'string', notnull=True, length=128),
                Field('ftp_port', 'integer', notnull=True, default=21),
                Field('ftp_user', 'string', notnull=True),
                Field('ftp_password', 'string', notnull=True),
                Field('send_success', 'integer', notnull=True, default=0),
                Field('failed_reason', 'string', notnull=True, default=''),
                Field('ftp_connected', 'integer', notnull=True, default=0),
                )
db.stations_send_data.status.requires = IS_IN_SET([0, 1], [T('Sent successful'), T('Failed to connect FTP')])

################################################################################
db.define_table('datalogger',  # Datalogger
                Field('logger_id', 'string', notnull=True),
                Field('station_id', 'string', notnull=True),
                Field('station_name', 'string', notnull=True, default=''),
                Field('logger_name', 'string', notnull=True, length=256),
                Field('logger_note', 'text')
                )
db.datalogger.logger_id.requires = [IS_NOT_EMPTY()]
db.datalogger.logger_name.requires = [IS_NOT_EMPTY()]
db.datalogger.station_id.requires = IS_IN_DB(db, db.stations.id, db.stations.station_name)

################################################################################
db.define_table('datalogger_command',  #Lệnh của dataloger
                Field('command_id', 'string', notnull=True),
                Field('command_name', 'string', notnull=True, length=255),
                Field('station_id', 'string', notnull=True),
                Field('command_content', 'string'),
                Field('status', 'integer', notnull=True, default=0),
                )

################################################################################
db.define_table('equipments_status_history',
                Field('station_id', 'string', notnull=True),
                Field('status', 'integer', default=0),
                Field('equipment_id', 'string'),  # Mot thiet bi luu dc nhieu thong so
                Field('get_time', 'datetime', notnull=True),
                )

db.define_table('manager_stations',  #Lệnh của dataloger
                Field('station_id', 'string', notnull=True),
                Field('user_id', 'string', notnull=True),
                )

db.define_table('manager_owner_information',  #Thông tin cơ quan chủ quản
                Field('name', 'string', notnull=True , default = "Trung tâm Quan trắc Môi Trường Miền Bắc"),
                Field('division', 'string', notnull=True , default = "Tổng Cục Môi Trường"),
                Field('logo', 'upload'),
                )

db.define_table('sensor_trouble_history',
                Field('station_id', 'string', notnull=True),
                Field('station_indicator_id', 'string'),
                Field('indicator_id', 'string'),
                Field('equipment_id', 'string'),  # Mot thiet bi luu dc nhieu thong so
                Field('value', 'float'),
                Field('unit', 'string'),
                Field('status', 'integer'),
                Field('get_time', 'datetime'),
                Field('indicator_name', 'string'),
                Field('file_name', 'string'),
                Field('indicator_name', 'string'), # Ten chi so
                Field('is_db_defined', 'integer', notnull=True, default=1),
                # 1 = Thong so chua co txt, có trong khai báo trạm; 0 = thong so da co trong txt, không có khai báo trong trạm
                Field('file_content', 'string'),
                Field('path_file', 'string'),
                )
db.sensor_trouble_history.status.requires = IS_IN_SET(sensor_trouble_history_status_value, sensor_trouble_history_status_disp)

db.define_table('station_trouble_definition',  # Luu tru tinh hinh khai bao indicator trong he thong
                Field('station_id', 'string', notnull=True),
                Field('station_indicator_id', 'string'),
                Field('indicator_id', 'string'),
                Field('indicator_name', 'string', notnull=True),
                Field('value', 'float'),
                Field('unit', 'string'),
                Field('status', 'integer'),
                Field('is_db_defined', 'integer', notnull=True, default=1),
                # 1 = Thong so chua co txt, có trong khai báo trạm; 0 = thong so da co trong txt, không có khai báo trong trạm
                Field('get_time', 'datetime', notnull=True, default=request.now),
                Field('file_name', 'string', notnull=True),
                Field('file_content', 'string'),
                Field('path_file', 'string'),
                )

if db(db.manager_owner_information.id > 0).count() == 0:
    db.manager_owner_information.insert()
################################################################################
db.define_table('manager_stations_history',  #Lịch sử quản lý trạm
                Field('station_id', 'string', notnull=True),
                Field('station_name', 'string', notnull=False),
                Field('action', 'string', notnull=True),
                Field('username', 'string', notnull=True),
                Field('description', 'string', notnull=False),
                Field('update_time', 'datetime', notnull=True),
                )


########################################################################################################################
db.define_table('data_wqi_hour_lastest',
                Field('station_id', 'string', notnull=True),
                Field('last_time', 'datetime', notnull=True),
                )

db.define_table('data_adjust_wqi_hour_lastest',
                Field('station_id', 'string', notnull=True),
                Field('last_time', 'datetime', notnull=True),
                )
# SEND EMAIL CONFIG
# SENDER_EMAIL = 'hd.envisoft@gmail.com'
# MAIL_SERVER = 'smtp.gmail.com'
# MAIL_SENDER_PASSWORD = 'ttqtduan!$2019'
# MAIL_SERVER_PORT = 587
########################################################################################################################
db.define_table('mail_server',  # Luu du lieu goc, tinh trung binh theo thang
                Field('mail_server', 'string', notnull=True, default='smtp.gmail.com'),
                Field('mail_server_port', 'integer', notnull=True, default=587),
                Field('sender_email', 'string', notnull=True, default='hd.envisoft@gmail.com'),
                Field('sender_email_password', 'string', notnull=True, default='ttqtduan!$2019'),
                )
if db(db.mail_server.id > 0).count() == 0:
    db.mail_server.insert()
################################################################################

#
db.define_table('eip_config',
                Field('name', 'string', notnull=True , default = "eip_config"),
                Field('waste_water_is_public', 'boolean', default=True),
                Field('surface_water_is_public', 'boolean', default=True),
                Field('stack_emission_is_public', 'boolean', default=True),
                Field('ambient_air_is_public', 'boolean', default=True),
                Field('time_public', 'integer', default=3)
                )

db.define_table('eip_faq',
                Field('title', 'string', notnull=True , default = "[FAQ]"),
                Field('content', 'text', widget=ckeditor.widget),
                Field('created_time', 'datetime', default=request.now, writable=False,readable=False, update=request.now),
                )

db.define_table('data_hour_status_history',
                Field('config', 'json', notnull=True),
                Field('data', 'json'),
                Field('time', 'datetime', notnull=True),
                )


db.define_table('manager_careers',
                Field('career_name', 'string'),
                Field('career_code', 'string', unique=True),
                Field('career_description', 'string'),
                Field('created_at', 'datetime', default=request.now, writable=False, readable=True),
                Field('updated_at', 'datetime', default=request.now, writable=False, readable=True,update=request.now),
                )

db.manager_careers.career_code.requires = [IS_NOT_EMPTY(), IS_NOT_IN_DB(db, db.manager_careers.career_code,
                                                                    error_message=T('Value is existed!'))]