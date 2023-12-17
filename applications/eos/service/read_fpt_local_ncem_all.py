import ftplib
import math

from pydal import DAL, Field
from threading import Thread
import os
import traceback
import datetime

# from StringIO import StringIO

# Find the best implementation available on this platform
try:
    from cStringIO import StringIO
except:
    from StringIO import StringIO

import time

import logging
from logging.handlers import RotatingFileHandler
from logging import handlers
import sys

db = DAL('mongodb://tuan:tuan@localhost/eos', pool_size=100) # Server tinh
# db = DAL('mongodb://tuan:tuan@localhost/eos', pool_size=300) # Server TW

# db = DAL('mongodb://tuan:tuan@113.160.218.8/eos', pool_size=50) # Ha Noi
# db = DAL('mongodb://tuan:tuan@113.160.218.8/eos', pool_size=20) # Nam Dinh
# db = DAL('mongodb://tuan:tuan@103.88.113.229/eos', pool_size=200)  # NCEM

# db = DAL('mongodb://tuan:tuan@103.88.113.229/eos') # NCEM
# db = DAL('mongodb://tuan:tuan@113.160.218.8/eos') # Nam Dinh
# db = DAL('mongodb://tuan:tuan@113.160.218.8/eos') # Ha Noi

ftp_session_pool = {}

LOGGER_LEVEL_FOR_COMMON = logging.DEBUG
# LOGGER_LEVEL_FOR_COMMON = logging.INFO

# LOGGER_LEVEL_FOR_STATION = logging.INFO

LOGGER_LEVEL_FOR_STATION = logging.DEBUG

# LOGGER_NAME = 'nd_envi_log_' # Nam Dinh

LOGGER_NAME = 'envi_log_'  # NCEM

LOGGER_STATION_FOLDER = 'log_all'

LOGGER_COMMON_FOLDER = 'log_common'

LOGGER_MAX_SIZE = (1048576 * 10)

LOGGER_BACKUP_COUNT = 2


################################################################################
def getLogger(station_id, logger_folder, logger_name, logger_max_size, backup_count, logger_level):
    # log_station_dir = os.getcwd() + os.sep + str(station_id)

    log_station_dir = os.getcwd() + os.sep + logger_folder

    log_file_name = logger_name + str(station_id) + '.log'

    try:
        if not os.path.exists(log_station_dir):
            os.makedirs(log_station_dir)
            # print log_station_dir
    except Exception as ex:
        # print ("Creation of the directory %s failed" % log_station_dir)
        log_station_dir = os.getcwd()

    tmp_logger = logging.getLogger(str(station_id))

    LOG_FILENAME = log_station_dir + os.sep + log_file_name

    # print "LOG_FILENAME", LOG_FILENAME

    # tmp_logger.setLevel(logging.INFO)
    tmp_logger.setLevel(logger_level)
    # tmp_logger.setLevel(logging.ERROR)
    # tmp_logger.setLevel(logging.FATAL)

    # format = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
    # format = logging.Formatter(
    #     "[%(filename)s:%(lineno)s - %(funcName)10s() ] %(asctime)s - %(name)s - %(levelname)s - %(message)s")

    format = logging.Formatter(
        "[%(filename)s:%(lineno)s - %(funcName)10s() ] %(asctime)s - %(levelname)s - %(message)s")

    stream_handler = logging.StreamHandler(sys.stdout)
    stream_handler.setFormatter(format)
    tmp_logger.addHandler(stream_handler)

    rotating_file_handler = handlers.RotatingFileHandler(LOG_FILENAME, maxBytes=logger_max_size,
                                                         backupCount=backup_count)
    rotating_file_handler.setFormatter(format)
    tmp_logger.addHandler(rotating_file_handler)
    return tmp_logger


logger = getLogger("all", LOGGER_COMMON_FOLDER, LOGGER_NAME, LOGGER_MAX_SIZE, LOGGER_BACKUP_COUNT,
                   LOGGER_LEVEL_FOR_COMMON)

SI_STATUS = {  # Station indicator status
    'IN_USE': {'value': 1, 'name': 'In use'},
    'DELETED': {'value': 2, 'name': 'Deleted'},
    'SENSOR_ERROR': {'value': 3, 'name': 'Sensor error'},
    'ADJUSTMENT_INDICATOR': {'value': 4, 'name': 'Adjustments'},
}

STATION_TYPE = {
    'WASTE_WATER': {'value': 0, 'name': 'Waste water', 'image': 'waste_water2.png'},
    'SURFACE_WATER': {'value': 1, 'name': 'Surface water', 'image': 'surface_water2.png'},
    'UNDERGROUND_WATER': {'value': 2, 'name': 'Underground water', 'image': 'underground_water2.png'},
    'STACK_EMISSION': {'value': 3, 'name': 'Stack emission', 'image': 'stack_emission.png'},
    'AMBIENT_AIR': {'value': 4, 'name': 'Ambient air', 'image': 'ambient_air2.png'},
}

STATION_TYPE = {
    'WASTE_WATER': {'value': 0, 'name': 'Waste water', 'image': 'waste_water2.png'},
    'SURFACE_WATER': {'value': 1, 'name': 'Surface water', 'image': 'surface_water2.png'},
    'UNDERGROUND_WATER': {'value': 2, 'name': 'Underground water', 'image': 'underground_water2.png'},
    'STACK_EMISSION': {'value': 3, 'name': 'Stack emission', 'image': 'stack_emission.png'},
    'AMBIENT_AIR': {'value': 4, 'name': 'Ambient air', 'image': 'ambient_air2.png'},
}

EXPRESSION_QCVN_INDICATOR = {
    'EXPRESSION_1': {'value': 1, 'text': 'qcvn_indecator<=max'},
    'EXPRESSION_2': {'value': 2, 'text': 'qcvn_indecator<max'},
    'EXPRESSION_3': {'value': 3, 'text': 'min<qcvn_indecator<max'},
    'EXPRESSION_4': {'value': 4, 'text': 'min<qcvn_indecator<=max'},
    'EXPRESSION_5': {'value': 5, 'text': 'min<=qcvn_indecator<max'},
}

STATION_STATUS = {
    'GOOD': {'value': 0, 'name': 'Good', 'color': '#1dce6c', 'icon': 'fa fa-circle'},  # fa fa-spinner fa-spin
    # 'TENDENCY': {'value': 1, 'name': 'Tendency', 'color': '#F1D748', 'icon': 'fa fa-circle'},
    'TENDENCY': {'value': 1, 'name': 'Good', 'color': '#1dce6c', 'icon': 'fa fa-circle'},
    # 'PREPARING': {'value': 2, 'name': 'Preparing', 'color': '#F08432', 'icon': 'fa fa-circle'},
    'PREPARING': {'value': 2, 'name': 'Good', 'color': '#1dce6c', 'icon': 'fa fa-circle'},
    'EXCEED': {'value': 3, 'name': 'Exceed', 'color': '#EA3223', 'icon': 'fa fa-circle'},
    'OFFLINE': {'value': 4, 'name': 'Offline', 'color': '#999999', 'icon': 'fa fa-stop'},
    'ADJUSTING': {'value': 5, 'name': 'Adjusting', 'color': 'purple', 'icon': 'fa fa-pause'},
    'ERROR': {'value': 6, 'name': 'Sensor error', 'color': 'red', 'icon': 'fa fa-times-circle-o'},
}

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

# hungdx add table to calculator data hour find lost issue 30
################################################################################
db.define_table('data_hour',
                Field('station_id', 'string', notnull=True),
                Field('get_time', 'datetime', notnull=True),
                Field('data', 'json'),
                )

db.define_table('data_hour_lastest',
                Field('station_id', 'string', notnull=True),
                Field('last_time', 'datetime', notnull=True),
                )

################################################################################
# hungdx add table to calculator data hour find lost issue 30

db.define_table('data_day_lastest',
                Field('station_id', 'string', notnull=True),
                Field('last_time', 'datetime', notnull=True),
                )

################################################################################
db.define_table('data_min',
                Field('station_id', 'string', notnull=True),
                Field('get_time', 'datetime', notnull=True),
                Field('is_exceed', 'boolean', default=False),  # De danh dau cac record co du lieu vuot nguong
                Field('data', 'json'),  # Truong nay luu dict cac chi so {ten chi so : gtri)
                )
# {
#     "_id" : ObjectId("5c16851b9dc6d656686ecbdb"),
#     "get_time" : ISODate("2018-12-17T00:00:31.000+0000"),
#     "data" : {
#         "DO" : 8.01,
#         "Temp" : 31.14,
#         "EC" : 454.92,
#         "ORP" : 255.46,
#         "pH" : 7.77,
#         "TSS" : 3.75
#     },
#     "orgin_data" : {
#         "DO" : {'value': 8.01, 'status': 0, 'unit'='m3'},
#         "Temp" : {'value': 8.01, 'status': 0, 'unit'='m3'},
#         "ORP" : {'value': 8.01, 'status': 0, 'unit'='m3'},
#         "pH" : {'value': 8.01, 'status': 0, 'unit'='m3'},
#         "TSS" : {'value': 8.01, 'status': 0, 'unit'='m3'},
#         "EC" : {'value': 8.01, 'status': 0, 'unit'='m3'},
#     },
#     "station_id" : "28494690359734869565924903870"
# }
################################################################################
db.define_table('data_month_lastest',
                Field('station_id', 'string', notnull=True),
                Field('last_time', 'datetime', notnull=True),
                )
################################################################################
db.define_table('provinces',
                Field('province_code', 'string', notnull=True, length=8),
                Field('province_name', 'string', notnull=True, length=32),
                Field('order_no', 'integer', default=0),
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

db.define_table('equipments_status_history',
                Field('station_id', 'string', notnull=True),
                Field('status', 'integer', default=0),
                Field('equipment_id', 'string'),  # Mot thiet bi luu dc nhieu thong so
                Field('get_time', 'datetime', notnull=True),
                )
################################################################################
db.define_table('data_min_collect',  # Luu tong hop cac ban ghi data_min theo thang
                Field('station_id', 'string', notnull=True),
                Field('year', 'integer', notnull=True, default=0),
                Field('month', 'integer', notnull=True, default=0),
                Field('total', 'integer', notnull=True, default=0),
                Field('exceed', 'integer', notnull=False, default=0),
                )
################################################################################
db.define_table('alarm_levels',
                Field('station_type', 'integer', notnull=True, default=0),
                Field('level_name', 'integer', notnull=True),
                Field('color', 'string'),
                )

################################################################################
db.define_table('data_alarm',  # Luu nhung du lieu bi canh bao
                Field('station_id', 'string', notnull=True),
                Field('get_time', 'datetime', notnull=True),
                Field('alarm_level', 'integer', notnull=True),
                Field('data', 'json'),
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
                Field('qi_time', 'datetime'),
                Field('scan_failed', 'integer', default=0),  # Luu so lan da scan data nhung that bai
                Field('file_mapping', 'string'),
                Field('file_mapping_desc', 'text'),
                Field('logger_id', 'string', notnull=True),
                Field('is_public', 'boolean', default=False),
                Field('path_format', 'integer', default=0),  # Luu so lan da scan data nhung that bai
                Field('frequency_receiving_data', 'integer', default=0),  # Luu so lan da scan data nhung that bai
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

################################################################################
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
                Field('status', 'integer', default=SI_STATUS['IN_USE']['value']),

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
                )

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
                )

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
                )

################################################################################
db.define_table('station_types',
                Field('code', 'string', length=16),
                Field('station_type', 'string', notnull=True, length=32),
                Field('icon', 'upload'),
                Field('color', 'string', default='#ffffff'),
                Field('order', 'integer', default=0),
                )


################################################################################
class FTPConnection(object):
    def __init__(self, server, port, username, password, second_limit):
        self.server = server
        self.username = username
        self.password = password
        self.second_limit = second_limit
        self.port = port

    def __enter__(self):
        self.ftp = ftplib.FTP(self.server)
        self.ftp.connect('ftp.cem.gov.vn', self.port, self.second_limit)  # TriNT: Khi chay thay, thi phai rem
        self.ftp.login(self.username, self.password)
        return self

    def __exit__(self, type, value, traceback):
        self.ftp.quit()

    def writeserverfile(self, serverpath, filename, path):
        self.ftp.cwd(serverpath)
        self.ftp.storlines('STOR ' + filename, open(path, 'r'))


################################################################################
# Using multihtreading to keep a large FTP transfer alive via the control socket.

def downloadFile(ip, port, time_out, filename, folder):
    # login
    # ftp = FTP(myhost,myuser,passw)

    ftp = ftplib.FTP(ip)
    ftp.connect(ip, port, time_out)

    ftp.set_debuglevel(2)

    sock = ftp.transfercmd('RETR ' + filename)

    def background():
        f = open(folder + filename, 'wb')
        while True:
            block = sock.recv(1024 * 1024)
            if not block:
                break
            f.write(block)
        sock.close()

    # t = threading.Thread(target=background)
    t = Thread(target=background)
    t.start()

    while t.is_alive():
        t.join(60)
        # This command does not affect anything at all. It performs no action other than having the server send an OK reply.
        # This command is used to keep connections with servers "alive" (connected) while nothing is being done.
        ftp.voidcmd('NOOP')


################################################################################
'''
    Batch chay 10p/lan
    Tinh toan du lieu cho bang 'data_min_collect'
'''


def calc_data_min_collect(year=0, month=0):
    try:
        logger.info('Start calculate data min collect')
        today = datetime.datetime.now()
        if not year:
            year = today.year
        if not month:
            month = today.month

        field = [
            db.stations.id,
            db.stations.station_code
        ]
        conditions = (db.stations.id > 0)
        rows = db(conditions).select(*field)

        first_date_in_this_month = '%s%s01000000' % ('%0.4d' % year, '%0.2d' % month)
        first_date_in_this_month = datetime.datetime.strptime(first_date_in_this_month, '%Y%m%d%H%M%S')
        next_month = month + 1
        next_year = year
        if next_month > 12:
            next_month = 1
            next_year += 1
        first_date_in_next_month = '%s%s01000000' % ('%0.4d' % next_year, '%0.2d' % next_month)
        first_date_in_next_month = datetime.datetime.strptime(first_date_in_next_month, '%Y%m%d%H%M%S')

        for row in rows:
            station_id = str(row.id)
            ############ total
            conditions2 = (db.data_min.get_time >= first_date_in_this_month)
            conditions2 &= (db.data_min.get_time < first_date_in_next_month)
            conditions2 &= (db.data_min.station_id == station_id)
            total = db(conditions2).count(db.data_min.id)

            ############ exceed
            conditions4 = (db.data_min.get_time >= first_date_in_this_month)
            conditions4 &= (db.data_min.get_time < first_date_in_next_month)
            conditions4 &= (db.data_min.is_exceed == True)
            conditions4 &= (db.data_min.station_id == station_id)
            exceed = db(conditions4).count(db.data_min.id)

            conditions3 = (db.data_min_collect.station_id == station_id)
            conditions3 &= (db.data_min_collect.year == year)
            conditions3 &= (db.data_min_collect.month == month)
            db.data_min_collect.update_or_insert(conditions3,
                                                 station_id=station_id,
                                                 year=year,
                                                 month=month,
                                                 total=total,
                                                 exceed=exceed,
                                                 )

        db.commit()
    except Exception as ex:
        logger.error(str(ex))
    finally:
        logger.info('End calculate data min collect')

    return


################################################################################
# hungdx fix lost data  add return last_time
def get_lastest_files_dict_new():
    try:
        rows = db(db.last_data_files.id > 0).select(
            db.last_data_files.filename,
            db.last_data_files.station_id,
            db.last_data_files.lasttime,
        )
        res = {}
        last_time = {}
        for item in rows:
            res[str(item.station_id)] = item.filename
            last_time[str(item.station_id)] = item.lasttime
        return res, last_time
    except Exception as ex:
        traceback.print_exc()
        # logger.error('get_lastest_files_dict_new --> Exception = %s', ex.message)
        return [], []


################################################################################

# hungdx fix lost data  add return last_time
def get_lastest_files_dict_new_by_station_id(station_id):
    try:
        rows = db(db.last_data_files.station_id == station_id).select(
            db.last_data_files.filename,
            db.last_data_files.station_id,
            db.last_data_files.lasttime,
        )
        res = {}
        last_time = {}
        for item in rows:
            res[str(item.station_id)] = item.filename
            last_time[str(item.station_id)] = item.lasttime
        return res, last_time
    except Exception as ex:
        traceback.print_exc()
        # logger.error('station_id --> Exception = %s', station_id)
        # logger.error('get_lastest_files_dict_new_by_station_id -->Exception = %s', ex.message)
        return [], []


################################################################################
def get_lastest_files_dict():
    rows = db(db.last_data_files.id > 0).select(
        db.last_data_files.filename,
        db.last_data_files.station_id,
    )
    res = {}
    for item in rows:
        res[str(item.station_id)] = item.filename
    return res


################################################################################
def get_lastest_files_by_id(station_id):
    rows = db(db.last_data_files.id == station_id).select(
        db.last_data_files.filename,
        db.last_data_files.station_id,
    )
    res = {}
    for item in rows:
        res[str(item.station_id)] = item.filename
    return res


################################################################################
def get_usr_dict():
    rows = db(db.auth_user.id > 0).select(db.auth_user.id, db.auth_user.fullname, db.auth_user.image)
    res_name = {}
    res_avatar = {}

    for item in rows:
        res_name[str(item.id)] = item.fullname
        res_avatar[str(item.id)] = item.image

    return res_name, res_avatar


################################################################################
def get_group_dict():
    rows = db(db.auth_group.id > 0).select()
    res = {}
    for item in rows:
        res[str(item.id)] = item.role

    return res


################################################################################
def get_province_dict():
    provinces = db(db.provinces.id > 0).select()
    res = {}
    for item in provinces:
        res[str(item.id)] = item.province_name

    return res


################################################################################
def get_province_have_station():
    ret = dict()

    stations = db(db.stations.id > 0).select(db.stations.province_id)
    province_ids = [station.province_id for station in stations]

    provinces = db(db.provinces.id.belongs(province_ids)).select()

    for row in provinces:
        ret[str(row.id)] = row.as_dict()
    return ret


################################################################################
'''
Get station_indicator by station_id or station_type
Return dict with format: {indicator_id: row.as_dict()}
'''


def get_station_indicator_by_station(station_id='', station_type=''):
    try:
        si_dict = dict()
        conditions = (db.station_indicator.id > 0)
        conditions &= (db.station_indicator.status == SI_STATUS['IN_USE']['value'])
        if station_type:
            db.station_indicator.station_type == station_type
        if station_id:
            db.station_indicator.station_id == station_id
        rows = db(conditions).select(db.station_indicator.ALL)
        for row in rows:
            si_dict[str(row.indicator_id)] = row.as_dict()
        return si_dict
    except Exception as ex:
        traceback.print_exc()
        # logger.error('station_id --> Exception = %s', station_id)
        # logger.error('get_station_indicator_by_station --> Exception = %s', ex.message)
        return dict()


################################################################################
def get_station_off_log():
    # hungdx fix lost data  add return last_time
    return_rows = []

    try:
        rows = db(db.station_off_log.id > 0).select(
            db.station_off_log.id,
            db.station_off_log.station_id,
            db.station_off_log.station_name,
            db.station_off_log.start_off,
            db.station_off_log.end_off,
        )
        # res = {}
        for row in rows:
            # res[str(item.station_id)] = item.filename
            # last_time[str(item.station_id)] = item.lasttime
            if not row.end_off:
                return_rows.append(row)
                # res[str(row.station_id)] = {
                #     'id': str(row.id),
                #     'station_id': str(row.station_id),
                #     'station_name': str(row.station_name),
                #     'start_off': str(row.start_off),
                #     # 'end_off': str(row.id),
                # }
        return return_rows
    except Exception as ex:
        traceback.print_exc()
        # logger.error('get_station_off_log --> Exception = %s', ex.message)
        return []


################################################################################
################################################################################
def get_station_off_log_by_station_id(station_id):
    return_rows = []
    try:
        rows = db(db.station_off_log.station_id == station_id).select(
            db.station_off_log.id,
            db.station_off_log.station_id,
            db.station_off_log.station_name,
            db.station_off_log.start_off,
            db.station_off_log.end_off,
        )
        # res = {}
        for row in rows:
            if not row.end_off:
                return_rows.append(row)
        return return_rows
    except Exception as ex:
        traceback.print_exc()
        # logger.error('get_station_off_log_by_station_id--> Exception = %s', ex.message)
        return []


################################################################################
def get_last_time_by_station(station_id):
    try:
        row = db(db.last_data_files.station_id == station_id).select(db.last_data_files.lasttime)[0]
        return row.lasttime
    except Exception as ex:
        traceback.print_exc()
        # logger.info('get_last_time_by_station --> Have no lasttime with Exception = %s', ex.message)
        return None


################################################################################

'''
Get station_indicator by station_id or station_type
Return dict with format: {indicator_id: row.as_dict()}
'''


def get_station_indicator_by_station_2(station_indicator_rows, station_id=''):
    try:
        si_dict = dict()
        for row in station_indicator_rows:
            si_dict[str(row.indicator_id)] = row.as_dict()
        return si_dict
    except Exception as ex:
        traceback.print_exc()
        # logger.error('get_station_indicator_by_station_2 -->Exception = %s', ex.message)
        return dict()


################################################################################
'''
# Get indicator by station_id
station_indicators_rows: ROWS of station_indicator
indicators_rows: ROWS of indicators
Return ROWS of indicators
'''


def get_indicators_by_station_id(station_indicators_rows, indicators_rows, station_id=''):
    try:
        rows = []
        old_station_id = str(station_id)
        indicator_ids = []
        for si_row in station_indicators_rows:
            new_station_id = str(si_row.station_id)
            if new_station_id == old_station_id:
                indicator_id = str(si_row.indicator_id)
                indicator_ids.append(indicator_id)

        for i_row in indicators_rows:
            new_indicator_id = str(i_row.id)
            if new_indicator_id in indicator_ids:
                rows.append(i_row)
        return rows
    except Exception as ex:
        traceback.print_exc()
        # logger.error('station_id --> Exception = %s', station_id)
        # logger.error('get_indicators_by_station_id --> Exception = %s', ex.message)
        return []


################################################################################
# Get all indicator for station
# Return ROWS indicators
def get_indicator_station_info():
    try:

        # Get list indicator_id from mapping table
        conditions = (db.station_indicator.station_id > 0)
        conditions &= (db.station_indicator.status == SI_STATUS['IN_USE']['value'])
        # rows = db(conditions).select(db.station_indicator.indicator_id)
        rows = db(conditions).select(db.station_indicator.ALL)

        # Get list indicator_id used
        indicator_ids = []
        for row in rows:
            if row.indicator_id not in indicator_ids:
                indicator_ids.append(row.indicator_id)

        # Get indicator_dict {indicator_id : indicator_name}
        indicators = db(db.indicators.id.belongs(indicator_ids)).select(
            db.indicators.id,
            db.indicators.indicator
        )

        indicator_dict = {}
        for item in indicators:
            indicator_dict[str(item.id)] = item.indicator

        station_indicator_dict = {}
        for row in rows:
            if row.station_id not in station_indicator_dict:
                station_indicator_dict[row.station_id] = {}

            indicator = indicator_dict.get(row.indicator_id)
            if indicator:
                station_indicator_dict[row.station_id][indicator] = {
                    'id': str(row.id),
                    'equipment_id': row.equipment_id,
                    'equal0': row.equal0,
                    'negative_value': row.negative_value,
                    'out_of_range': row.out_of_range,
                    'out_of_range_min': row.out_of_range_min,
                    'out_of_range_max': row.out_of_range_max,
                    'continous_equal': row.continous_equal,
                    'continous_equal_value': row.continous_equal_value,
                    'continous_times': row.continous_times,
                    'mapping_name': row.mapping_name,
                    'convert_rate': row.convert_rate,
                    'qcvn_detail_max_value': row.qcvn_detail_max_value,
                    'qcvn_detail_min_value': row.qcvn_detail_min_value,
                    'indicator_id': row.indicator_id,
                }

        exceed_dict = {}
        preparing_dict = {}
        tendency_dict = {}

        for item in rows:
            # logger.info("item.indicator_id: %s", item.indicator_id)
            # indicator = indicator_dict.get(item.indicator_id).upper()  # ten chi so
            indicator = indicator_dict.get(item.indicator_id)

            if indicator:
                # logger.info("indicator: %s", indicator)
                indicator = indicator_dict.get(item.indicator_id).upper()  # ten chi so

                if item.station_id in exceed_dict:
                    exceed_dict[item.station_id][indicator] = item.exceed_value
                    preparing_dict[item.station_id][indicator] = item.preparing_value
                    tendency_dict[item.station_id][indicator] = item.tendency_value
                else:
                    exceed_dict[item.station_id] = {indicator: item.exceed_value}
                    preparing_dict[item.station_id] = {indicator: item.preparing_value}
                    tendency_dict[item.station_id] = {indicator: item.tendency_value}

        return station_indicator_dict, indicators, exceed_dict, preparing_dict, tendency_dict

    except Exception as ex:
        traceback.print_exc()
        # logger.error('get_indicator_station_info --> Exception = %s', ex.message)
        return [], [], [], [], []


################################################################################
# Get all indicator for station
# Return ROWS indicators
def get_indicator_station_info_by_station_id(station_id):
    try:

        # Get list indicator_id from mapping table
        conditions = (db.station_indicator.station_id == station_id)
        conditions &= (db.station_indicator.status == SI_STATUS['IN_USE']['value'])
        # rows = db(conditions).select(db.station_indicator.indicator_id)
        rows = db(conditions).select(db.station_indicator.ALL)

        # Get list indicator_id used
        indicator_ids = []
        for row in rows:
            if row.indicator_id not in indicator_ids:
                indicator_ids.append(row.indicator_id)

        # Get indicator_dict {indicator_id : indicator_name}
        indicators = db(db.indicators.id.belongs(indicator_ids)).select(
            db.indicators.id,
            db.indicators.indicator
        )

        indicator_dict = {}
        for item in indicators:
            indicator_dict[str(item.id)] = item.indicator

        station_indicator_dict = {}
        for row in rows:
            if row.station_id not in station_indicator_dict:
                station_indicator_dict[row.station_id] = {}

            indicator = indicator_dict.get(row.indicator_id)
            if indicator:
                station_indicator_dict[row.station_id][indicator] = {
                    'id': str(row.id),
                    'equipment_id': row.equipment_id,
                    'equal0': row.equal0,
                    'negative_value': row.negative_value,
                    'out_of_range': row.out_of_range,
                    'out_of_range_min': row.out_of_range_min,
                    'out_of_range_max': row.out_of_range_max,
                    'continous_equal': row.continous_equal,
                    'continous_equal_value': row.continous_equal_value,
                    'continous_times': row.continous_times,
                    'mapping_name': row.mapping_name,
                    'convert_rate': row.convert_rate,
                    'qcvn_detail_max_value': row.qcvn_detail_max_value,
                    'qcvn_detail_min_value': row.qcvn_detail_min_value,
                    'indicator_id': row.indicator_id,
                }

        exceed_dict = {}
        preparing_dict = {}
        tendency_dict = {}

        for item in rows:
            # logger.info("item.indicator_id: %s", item.indicator_id)
            # indicator = indicator_dict.get(item.indicator_id).upper()  # ten chi so
            indicator = indicator_dict.get(item.indicator_id)

            if indicator:
                # logger.info("indicator: %s", indicator)
                indicator = indicator_dict.get(item.indicator_id).upper()  # ten chi so

                if item.station_id in exceed_dict:
                    exceed_dict[item.station_id][indicator] = item.exceed_value
                    preparing_dict[item.station_id][indicator] = item.preparing_value
                    tendency_dict[item.station_id][indicator] = item.tendency_value
                else:
                    exceed_dict[item.station_id] = {indicator: item.exceed_value}
                    preparing_dict[item.station_id] = {indicator: item.preparing_value}
                    tendency_dict[item.station_id] = {indicator: item.tendency_value}

        return station_indicator_dict, indicators, exceed_dict, preparing_dict, tendency_dict

    except Exception as ex:
        traceback.print_exc()
        logger.error('get_indicator_station_info_by_station_id --> Exception = %s', station_id)
        logger.error('get_indicator_station_info_by_station_id --> Exception = %s', ex.message)
        return [], [], [], [], []


################################################################################
# Get all station_indicator
# Return ROWS station_indicator
# def get_station_indicator_value():
#     try:
#
#         # Get list indicator_id from mapping table
#         # conditions = (db.station_indicator.station_id > 0)
#         # conditions &= (db.station_indicator.indicator_id > 0)
#         conditions = (db.station_indicator.indicator_id > 0)
#         rows = db(conditions).select(db.station_indicator.ALL)
#         return rows
#     except Exception as ex:
#         return []

################################################################################
# Get color for indicator of Station
# si_dict: dict station_indicator {indicator_name: row.as_dict()}
# id: id of indicator
# value: value of indicator

def getColorByIndicator(si_dict, id, value):
    try:
        c = '#c9c9c9'
        if si_dict.has_key(id):
            data = si_dict[id]
            tendency = data['tendency_value']
            preparing = data['preparing_value']
            exceed = data['exceed_value']
            if value >= exceed:
                c = STATION_STATUS['EXCEED']['color']
            elif value >= preparing:
                c = STATION_STATUS['PREPARING']['color']
            elif value >= tendency:
                c = STATION_STATUS['TENDENCY']['color']
            else:
                c = STATION_STATUS['GOOD']['color']

        return c
    except Exception as ex:
        traceback.print_exc()
        # logger.error('getColorByIndicator -->Exception = %s', ex.message)
        return '#c9c9c9'


################################################################################
# Get latest data for station
# Return json data
def get_data_lastest_by_station(station_id):
    try:

        conditions = (db.data_lastest.station_id == station_id)
        if station_id == "":
            conditions = (db.data_lastest.station_id > 0)
        record = db(conditions).select(db.data_lastest.data).first()
        if record:
            return record.data
        return dict()
    except Exception as ex:
        traceback.print_exc()
        # logger.error('get_data_lastest_by_station --> Exception = %s', ex.message)
        return dict()


################################################################################
''' Get latest data for station
    Return json data, format {station_id :
                                {indicator : value, ...}
                             }
'''


################################################################################
def get_all_data_lastest():
    data_lastest_dict = {}
    try:

        conditions = (db.data_lastest.station_id > 0)
        rows = db(conditions).select(db.data_lastest.station_id, db.data_lastest.data)

        for item in rows:
            data_dict = {}
            for indicator in item.data:
                data_dict[indicator] = item.data[indicator]
            data_lastest_dict[item.station_id] = data_dict

        return data_lastest_dict
    except Exception as ex:
        traceback.print_exc()
        # logger.error('get_all_data_lastest-->Exception = %s', ex.message)
        return data_lastest_dict


################################################################################
def get_all_data_lastest_by_station_id(station_id):
    data_lastest_dict = {}
    try:

        conditions = (db.data_lastest.station_id == station_id)
        rows = db(conditions).select(db.data_lastest.station_id, db.data_lastest.data)

        for item in rows:
            data_dict = {}
            for indicator in item.data:
                data_dict[indicator] = item.data[indicator]
            data_lastest_dict[item.station_id] = data_dict

        return data_lastest_dict
    except Exception as ex:
        traceback.print_exc()
        # logger.error('get_all_data_lastest_by_station_id--> Exception = %s', ex.message)
        # logger.error("get_all_data_lastest: %s", ex.message)
        return data_lastest_dict


################################################################################
# Get latest data for station
# Return json data
def get_data_lastest_by_station_id(data_lastest_rows, station_id):
    try:
        for row in data_lastest_rows:
            if row.station_id == station_id:
                return row.data
        return dict()
    except Exception as ex:
        traceback.print_exc()
        # logger.error('station_id --> Exception = %s', station_id)
        # logger.error('get_data_lastest_by_station_id --> Exception = %s', ex.message)
        return dict()


################################################################################
# Get station info
# Return json data
def get_all_station_ftp_info():
    try:

        field = [
            db.stations.id,
            db.stations.station_code,
            db.stations.data_server,
            db.stations.data_server_port,
            db.stations.data_folder,
            db.stations.username,
            db.stations.pwd,
            db.stations.file_mapping,
            db.stations.scan_failed,
            db.stations.retry,
        ]
        conditions = (db.stations.id > 0)
        conditions &= (db.stations.station_code != None)
        conditions &= (db.stations.data_server != None)
        conditions &= (db.stations.data_folder != None)
        rows = db(conditions).select(*field)

        res_ip = {}
        res_data_folder = {}
        res_username = {}
        res_pwd = {}
        res_port = {}
        res_file_mapping = {}
        res_file_mapping2 = {}
        res_scan_failed = {}
        res_retry = {}

        for item in rows:
            res_ip[item.station_code] = item.data_server
            res_data_folder[item.station_code] = item.data_folder
            res_username[item.station_code] = item.username
            res_pwd[item.station_code] = item.pwd
            res_port[item.station_code] = item.data_server_port

            try:
                if item.scan_failed:
                    res_scan_failed[item.station_code] = item.scan_failed
                else:
                    res_scan_failed[item.station_code] = 0
            except:
                res_scan_failed[item.station_code] = 0

            res_retry[item.station_code] = item.retry
            res_file_mapping2[item.station_code] = item.retry

            try:
                if item.file_mapping:
                    res_file_mapping[item.station_code] = item.file_mapping
                else:
                    res_file_mapping[item.station_code] = None
            except:
                res_file_mapping[item.station_code] = None

            # if item.file_mapping:
            #     res_file_mapping[item.file_mapping] = str(item.id)

        return res_ip, res_data_folder, res_username, res_pwd, res_port, res_file_mapping, res_scan_failed, res_retry, res_file_mapping2
    except Exception as ex:
        traceback.print_exc()
        # logger.error('get_all_station_ftp_info --> Exception = %s', ex.message)
        return dict()


################################################################################
# Hungdx create new Return json data
def get_stations_ftp_load_update():
    try:

        field = [
            db.stations.id,
            db.stations.station_code,
            db.stations.data_server,
            db.stations.data_server_port,
            db.stations.data_folder,
            db.stations.username,
            db.stations.pwd,
            db.stations.file_mapping,
            db.stations.scan_failed,
            db.stations.retry,
            db.stations.path_format,
            db.stations.frequency_receiving_data,
        ]
        conditions = (db.stations.id > 0)
        conditions &= (db.stations.station_code is not None)
        conditions &= (db.stations.data_server is not None)
        conditions &= (db.stations.data_folder is not None)
        rows = db(conditions).select(*field)

        res_ip = {}
        res_data_folder = {}
        res_username = {}
        res_pwd = {}
        res_port = {}
        res_file_mapping = {}
        res_file_mapping2 = {}
        res_scan_failed = {}
        res_retry = {}
        res_format = {}
        res_frequency_receiving_data = {}

        for item in rows:
            res_ip[item.station_code] = item.data_server
            res_data_folder[item.station_code] = item.data_folder
            res_username[item.station_code] = item.username
            res_pwd[item.station_code] = item.pwd
            res_port[item.station_code] = item.data_server_port

            # res_scan_failed[item.station_code] = item.scan_failed

            try:
                if item.scan_failed:
                    res_scan_failed[item.station_code] = item.scan_failed
                else:
                    res_scan_failed[item.station_code] = 0
            except:
                res_scan_failed[item.station_code] = 0

            res_retry[item.station_code] = item.retry
            res_file_mapping2[item.station_code] = item.retry

            # res_file_mapping[item.station_code] = item.file_mapping # TriNT: Add 13/04/2019

            try:
                if item.file_mapping:
                    res_file_mapping[item.station_code] = item.file_mapping
                else:
                    res_file_mapping[item.station_code] = None
            except:
                res_file_mapping[item.station_code] = None

            # if item.file_mapping:
            #     logger.info("file_mapping = %s", item.file_mapping)  # TriNT: Add 13/04/2019
            #     # # res_file_mapping[item.file_mapping] = str(item.id) # Trint: delete
            #     # res_file_mapping[item.station_code] = str(item.file_mapping)  # Trint: add

            res_format[item.station_code] = item.path_format
            res_frequency_receiving_data[item.station_code] = item.frequency_receiving_data

        return res_ip, res_data_folder, res_username, res_pwd, res_port, res_file_mapping, res_scan_failed, \
               res_retry, res_file_mapping2, res_format, res_frequency_receiving_data
    except Exception as ex:
        traceback.print_exc()
        # logger.error('get_stations_ftp_load_update --> Exception = %s', ex.message)
        return dict()


################################################################################
# Hungdx create new Return json data
def get_stations_ftp_load_update_by_station_id(station_id):
    try:

        field = [
            db.stations.id,
            db.stations.station_code,
            db.stations.data_server,
            db.stations.data_server_port,
            db.stations.data_folder,
            db.stations.username,
            db.stations.pwd,
            db.stations.file_mapping,
            db.stations.scan_failed,
            db.stations.retry,
            db.stations.path_format,
            db.stations.frequency_receiving_data,
            db.stations.station_name,
        ]
        conditions = (db.stations.id == station_id)
        # conditions &= (db.stations.station_code is not None)
        # conditions &= (db.stations.data_server is not None)
        # conditions &= (db.stations.data_folder is not None)
        rows = db(conditions).select(*field)

        res_ip = {}
        res_data_folder = {}
        res_username = {}
        res_pwd = {}
        res_port = {}
        res_file_mapping = {}
        res_file_mapping2 = {}
        res_scan_failed = {}
        res_retry = {}
        res_format = {}
        res_frequency_receiving_data = {}
        res_station_name = {}
        res_station_code = {}

        for item in rows:
            res_ip[item.id] = item.data_server
            res_data_folder[item.id] = item.data_folder
            res_username[item.id] = item.username
            res_pwd[item.id] = item.pwd
            res_port[item.id] = item.data_server_port

            try:
                if item.scan_failed:
                    res_scan_failed[item.id] = item.scan_failed
                else:
                    res_scan_failed[item.id] = 0
            except:
                res_scan_failed[item.id] = 0

            res_retry[item.id] = item.retry

            res_file_mapping2[item.id] = item.retry

            try:
                if item.file_mapping:
                    res_file_mapping[item.id] = item.file_mapping  # TriNT: Add 13/04/2019
                else:
                    res_file_mapping[item.id] = None
            except:
                res_file_mapping[item.id] = None

            res_station_name[item.id] = item.station_name  # TriNT: Add 13/04/2019
            res_station_code[item.id] = item.station_code  # TriNT: Add 13/04/2019

            # if item.file_mapping:
            #     logger.info("file_mapping = %s", item.file_mapping)  # TriNT: Add 13/04/2019
            #     # # res_file_mapping[item.file_mapping] = str(item.id) # Trint: delete
            #     # res_file_mapping[item.station_code] = str(item.file_mapping)  # Trint: add

            res_format[item.id] = item.path_format
            res_frequency_receiving_data[item.id] = item.frequency_receiving_data

        return res_ip, res_data_folder, res_username, res_pwd, res_port, res_file_mapping, res_scan_failed, \
               res_retry, res_file_mapping2, res_format, res_frequency_receiving_data, res_station_name, res_station_code
    except Exception as ex:
        traceback.print_exc()
        # logger.error('station_id --> Exception = %s', station_id)
        # logger.error('get_stations_ftp_load_update_by_station_id --> Exception = %s', ex.message)
        return dict()


################################################################################
def get_indicator_dict():
    rows = db(db.indicators.id > 0).select()
    res = {}
    for item in rows:
        res[str(item.id)] = item.indicator

    return res


################################################################################
def get_qcvn_kind_dict():
    rows = db(db.qcvn_kind.id > 0).select()
    res = {}
    for item in rows:
        res[str(item.id)] = item.qcvn_kind

    return res


################################################################################
# def get_station_dict_base_station_id_():
def get_station_dict_base_station_id():
    field = [
        db.stations.id,
        db.stations.station_code,
        db.stations.station_name,
        db.stations.station_type,
        db.stations.status,
        db.stations.scan_failed,
    ]

    # conditions = (db.station_indicator.station_id > 0)
    #         # conditions &= (db.station_indicator.indicator_id > 0)
    #         conditions = (db.station_indicator.indicator_id > 0)
    # data_mins = db(conditions).select(orderby=db.data_min.get_time)
    conditions = (db.stations.id > 0)
    # conditions &= (db.stations.scan_failed >= 0)
    # conditions &= (db.stations.scan_failed <= number_scan_failed_max)

    stations = db(conditions).select(*field)

    res_name = {}
    res_type = {}
    res_status = {}
    res_id = {}

    for item in stations:
        res_name[str(item.id)] = item.station_name
        res_type[str(item.id)] = item.station_type
        res_status[str(item.id)] = item.status
        res_id[str(item.id)] = str(item.id)

    return res_name, res_type, res_status, res_id


################################################################################
def get_station_dict_new_by_station_id(station_id):
    res_name = {}
    res_type = {}
    res_status = {}
    res_id = {}
    res_code = {}

    try:
        field = [
            db.stations.id,
            db.stations.station_code,
            db.stations.station_name,
            db.stations.station_type,
            db.stations.status,
        ]

        stations = db(db.stations.id == station_id).select(*field)

        for item in stations:
            res_name[str(item.id)] = item.station_name
            res_type[str(item.id)] = item.station_type
            res_status[str(item.id)] = item.status
            res_id[str(item.id)] = str(item.id)
            res_code[str(item.id)] = str(item.station_code)

        return res_name, res_type, res_status, res_id, res_code
    except:
        return res_name, res_type, res_status, res_id, res_code


################################################################################
def get_station_dict():
    field = [
        db.stations.id,
        db.stations.station_code,
        db.stations.station_name,
        db.stations.station_type,
        db.stations.status,
    ]

    stations = db(db.stations.id > 0).select(*field)
    res_name = {}
    res_type = {}
    res_status = {}
    res_code = {}

    for item in stations:
        res_name[str(item.id)] = item.station_name
        res_type[str(item.id)] = item.station_type
        res_status[str(item.id)] = item.status
        res_code[item.station_code] = str(item.id)

    return res_name, res_type, res_status, res_code


################################################################################
def get_station_dict_by_id(station_id):
    field = [
        db.stations.id,
        db.stations.station_code,
        db.stations.station_name,
        db.stations.station_type,
        db.stations.status,
    ]

    stations = db(db.stations.id == station_id).select(*field)
    res_name = {}
    res_type = {}
    res_status = {}
    res_code = {}

    for item in stations:
        res_name[str(item.id)] = item.station_name
        res_type[str(item.id)] = item.station_type
        res_status[str(item.id)] = item.status
        res_code[item.station_code] = str(item.id)

    return res_name, res_type, res_status, res_code


################################################################################
'''
    Description : Lay dict() cac tram voi nguong qua han cua tung chi so
    Return      : dict(station_id : dict(indicator : exceed value))
'''


# def get_station_indicator_thresdhold_dict():
#
# logger = current.logger

# fields = [  db.station_indicator.station_id,
# db.station_indicator.indicator_id,
# db.station_indicator.exceed_value]

# rows = db(db.station_indicator.id > 0).select(*fields)


# indicator_dict = get_indicator_dict()
# res = {}
# for item in rows:
# indicator = indicator_dict.get(item.indicator_id).upper()   # ten chi so

# if item.station_id in res:
# res[item.station_id][indicator] = item.exceed_value
# else:
# res[item.station_id] = {indicator : item.exceed_value}

# return res

################################################################################
def get_area_by_station_dict():
    '''
    Return : dict(key  : station_id,
                  value: all areas which station belonged (separated by comma))
    '''

    field = [
        db.areas.id,
        db.areas.area_name,
    ]

    records = db(db.areas.id > 0).select(*field)
    res_name = {}

    for item in records:
        if item.id not in res_name:
            res_name[str(item.id)] = item.area_name
        else:
            res_name[str(item.id)] = '%s, %s' % (res_name[str(item.id)], item.area_name)

    return res_name


################################################################################
def format_passed_time(seconds=0):
    if not seconds: return ''

    T = current.T
    if seconds >= 86400:  # Ngay
        return '%d %s %d %s' % (seconds / 86400, T('day'), (seconds % 86400) / 3600, T('hour'))
    elif seconds >= 3600:  # Gio
        return '%d %s %d %s' % (seconds / 3600, T('hour'), (seconds % 3600) / 60, T('minute'))
    elif seconds >= 60:  # Phut
        return '%d %s %d %s' % (seconds / 60, T('minute'), seconds % 60, T('second'))
    else:
        return '%d %s' % (seconds, T('second'))


################################################################################
def send_mail(mail_to='', mail_cc='', subject='Subject', message='Content'):
    try:
        myconf = current.myconf
        import smtplib
        from email.mime.text import MIMEText

        msg = MIMEText(message, 'html', 'UTF-8')
        msg['Subject'] = subject
        msg["From"] = myconf.get('smtp.sender')
        msg["To"] = mail_to
        msg["Cc"] = mail_cc

        server = smtplib.SMTP()
        mail_server = myconf.get('smtp.server')
        mail_port = myconf.get('smtp.port')
        server.connect(mail_server, mail_port)
        mail_user = myconf.get('smtp.login')
        mail_pwd = myconf.get('smtp.pwd')
        server.starttls()
        server.login(mail_user, mail_pwd)
        server.sendmail(msg["From"], msg["To"].split(','), msg.as_string())
        return True
    except Exception as ex:
        traceback.print_exc()
        # logger.error('send_mail --> Exception = %s', ex.message)
        return False


################################################################################
def send_mail2(mail_to='', mail_cc='', subject='Subject', message='Content'):
    try:
        import smtplib  # Su dung module smtp cua Python
        from email.mime.text import MIMEText

        # Khai bao username va pass
        username = 'c0909i1240'
        password = 'chinguyen12345'
        # Tao doi tuong smtp cua gmail
        server = smtplib.SMTP('smtp.gmail.com:587')  # Tao mot ket noi den SMTP cua Gmail
        server.starttls()  # Khoi tao ket noi TLS SMTP
        server.login(username, password)  # Dang nhap user, pass

        msg = MIMEText(message, 'html', 'UTF-8')
        msg['Subject'] = subject
        msg["To"] = mail_to
        msg["Cc"] = mail_cc
        server.sendmail(msg["From"], msg["To"].split(','),
                        msg.as_string())  # Gui email tu hocbaomat@gmail.com den maivanthang@gmail.com

        server.close()  # ket thuc
    except Exception as ex:
        traceback.print_exc()
        # logger.error('Exception = %s', ex.message)
        return False


################################################################################
def display_list_integer(resource, numbers):
    try:
        ret = ''
        for number in numbers:
            name = resource.get(str(number))
            if name:
                if ret: ret += ', '
                ret += name
        return ret
    except Exception as ex:
        traceback.print_exc()
        # logger.error('display_list_integer --> Exception = %s', ex.message)
        return numbers


################################################################################
def get_info_from_const(data, value):
    try:
        ret = []
        for key, item in data.iteritems():
            if item['value'] == value:
                return item
        return ret
    except Exception as ex:
        traceback.print_exc()
        # logger.error('get_info_from_const --> Exception = %s', ex.message)
        return []


################################################################################
# Format of item in dict: 'KEY1': {'value': 0, 'name': 'name1', 'seq': 1}
def sort_dict_const_by_value(dict_const):
    key_field = 'value'
    ret = dict_const.items()
    total = len(ret)
    if total > 0:
        item = ret[0][1]
        if item.has_key('seq'):
            key_field = 'seq'
    for i in range(0, total - 1):
        for j in range(i + 1, total):
            if ret[j][1][key_field] < ret[i][1][key_field]:
                temp = ret[j]
                ret[j] = ret[i]
                ret[i] = temp
    return ret


################################################################################
def get_const_by_value(dict_const, value):
    ret = []
    for k in dict_const:
        if str(dict_const[k]['value']) == str(value):
            return dict_const[k]
    return ret


################################################################################
'''
    Function get du lieu tu ftp
    Chia ra function de truong hop ko connect duoc ftp se connect lai
'''

################################################################################
'''
    Function get du lieu tu ftp
    Chia ra function de truong hop ko connect duoc ftp se connect lai
'''


################################################################################
def hour_data_calc(station_id, data_mins, lastest_hour):
    data = dict()  # {indicator : sum value}
    count = dict()  # {indicator : count}

    for i, row in enumerate(data_mins):
        # hungdx comment start calcu hour new issue 30
        # row.get_time = row.get_time.replace(minute = 0, second = 0, microsecond = 0)    # chuan hoa, cho phut, giay ve 0
        # Skip all previous min data to lastest hour
        # if row.get_time < lastest_hour:
        #     continue

        # Boc du lieu tu row vao data dict()
        # get_data = row.data         # kieu dict()
        # for indicator in get_data.keys():
        #     if data.has_key(indicator):
        #         data[indicator] += float(get_data[indicator])
        #         count[indicator] += 1
        #     else:
        #         data[indicator] = float(get_data[indicator])
        #         count[indicator] = 1
        #
        # # Check if new hour, thi insert record vao bang data_hour va reset lai cac bien
        # if row.get_time > lastest_hour:
        #     # Neu du lieu dict la empty thi skip, ko luu DB
        #     if bool(data):
        #         # Calc average
        #         for indicator in data.keys():
        #             data[indicator] = float("{0:.4f}".format(data[indicator] / count[indicator]))
        #
        #         db.data_hour.update_or_insert(
        #             (db.data_hour.station_id == station_id) & (db.data_hour.get_time == lastest_hour),
        #             station_id=station_id,
        #             get_time=lastest_hour,
        #             data=data
        #         )
        #     # Reset variables
        #     # lastest_hour = row.get_time.replace(minute = 0, second = 0, microsecond = 0) #hungdx comment calcu hour new issue 30
        #     data = dict()
        #     count = dict()
        # hungdx comment end calcu hour new issue 30
        # Boc du lieu tu row hien tai vao data dict()
        get_data = row.data
        for indicator in get_data.keys():
            if data.has_key(indicator):
                data[indicator] += float(get_data[indicator])
                count[indicator] += 1
            else:
                data[indicator] = float(get_data[indicator])
                count[indicator] = 1

        # Neu la row cuoi thi chot, insert vao db
        if i == len(data_mins) - 1:
            # Neu du lieu dict la empty thi skip, ko luu DB
            if bool(data):
                # Calc average
                for indicator in data.keys():
                    data[indicator] = float("{0:.4f}".format(data[indicator] / count[indicator]))

                try:
                    db.data_hour.update_or_insert(
                        (db.data_hour.station_id == station_id) & (db.data_hour.get_time == lastest_hour),
                        station_id=station_id,
                        get_time=lastest_hour,
                        data=data
                    )
                    db.commit()  # Luu data vao db ngay sau khi xu ly moi tram
                except:
                    traceback.print_exc()
                    db.rollback()

                try:
                    # hungdx add new table data_hour_lastest issue 30
                    db.data_hour_lastest.update_or_insert(
                        (db.data_hour_lastest.station_id == station_id),
                        station_id=station_id,
                        last_time=lastest_hour
                    )
                    db.commit()  # Luu data vao db ngay sau khi xu ly moi tram
                except:
                    traceback.print_exc()
                    db.rollback()
    return


################################################################################
def day_data_calc(station_id, data_hours, lastest_day):
    data = dict()  # {indicator : sum value}
    count = dict()  # {indicator : count}
    max_data = dict()
    min_data = dict()
    max_data_time = dict()
    min_data_time = dict()

    for i, row in enumerate(data_hours):
        # Neu ko co du lieu cua ngay hom truoc, tang ngay cho den ngay cua row hien tai thi thoi
        # hungdx comment start issue 30
        # if i == 0 and row.get_time.date() > lastest_day:
        #     while row.get_time.date() > lastest_day:
        #         lastest_day = lastest_day + timedelta(days=1)
        #
        # if row.get_time.date() == lastest_day:
        #     # Boc du lieu tu row vao data dict()
        #     get_data = row.data         # kieu dict()
        #     for indicator in get_data.keys():
        #         val = float(get_data[indicator])
        #
        #         if data.has_key(indicator):
        #             data[indicator] += val
        #             count[indicator] += 1
        #             if val > max_data[indicator]:
        #                 max_data[indicator] = val
        #                 max_data_time[indicator] = row.get_time
        #             if val < min_data[indicator]:
        #                 min_data[indicator] = val
        #                 min_data_time[indicator] = row.get_time
        #         else:
        #             data[indicator] = val
        #             count[indicator] = 1
        #             max_data[indicator] = val
        #             min_data[indicator] = val
        #             max_data_time[indicator] = row.get_time
        #             min_data_time[indicator] = row.get_time

        # # Check if new day thi insert record vao bang data_day va reset lai cac bien
        # if row.get_time.date() > lastest_day:
        # if row.get_time >= lastest_day:
        #     # Neu du lieu dict la empty thi skip, ko luu DB
        #     if bool(data):
        #         # Calc average
        #         for indicator in data.keys():
        #             data[indicator] = float("{0:.4f}".format(data[indicator] / count[indicator]))
        #
        #         db.data_day.update_or_insert(
        #             (db.data_day.station_id == station_id) & (db.data_day.get_time == lastest_day),
        #             station_id=station_id,
        #             get_time=lastest_day,
        #             data=data,
        #             data_min=min_data,
        #             data_max=max_data,
        #             data_min_time=min_data_time,
        #             data_max_time=max_data_time,
        #         )
        #     # Reset variables for new day
        #     lastest_day = row.get_time.date()
        #     data = dict()
        #     count = dict()
        #     max_data = dict()
        #     min_data = dict()
        #     max_data_time = dict()
        # #     min_data_time = dict()
        #     # Boc du lieu tu row hien tai vao data dict()
        #     get_data = row.data
        #     for indicator in get_data.keys():
        #         val = float(get_data[indicator])
        #
        #         if data.has_key(indicator):
        #             data[indicator] += val
        #             count[indicator] += 1
        #             if val > max_data[indicator]:
        #                 max_data[indicator] = val
        #                 max_data_time[indicator] = row.get_time
        #             if val < min_data[indicator]:
        #                 min_data[indicator] = val
        #                 min_data_time[indicator] = row.get_time
        #         else:
        #             data[indicator] = val
        #             count[indicator] = 1
        #             max_data[indicator] = val
        #             min_data[indicator] = val
        #             max_data_time[indicator] = row.get_time
        #             min_data_time[indicator] = row.get_time
        # hungdx comment end issue 30
        get_data = row.data
        for indicator in get_data.keys():
            val = float(get_data[indicator])
            if data.has_key(indicator):
                data[indicator] += val
                count[indicator] += 1
                if val > max_data[indicator]:
                    max_data[indicator] = val
                    max_data_time[indicator] = row.get_time
                if val < min_data[indicator]:
                    min_data[indicator] = val
                    min_data_time[indicator] = row.get_time
            else:
                data[indicator] = val
                count[indicator] = 1
                max_data[indicator] = val
                min_data[indicator] = val
                max_data_time[indicator] = row.get_time
                min_data_time[indicator] = row.get_time
        # Neu la row cuoi thi insert phan da doc vao DB
        if i == len(data_hours) - 1:
            if bool(data):
                # Calc average
                for indicator in data.keys():
                    data[indicator] = float("{0:.4f}".format(data[indicator] / count[indicator]))

                try:
                    db.data_day.update_or_insert(
                        (db.data_day.station_id == station_id) & (db.data_day.get_time == lastest_day),
                        station_id=station_id,
                        get_time=lastest_day,
                        data=data,
                        data_min=min_data,
                        data_max=max_data,
                        data_min_time=min_data_time,
                        data_max_time=max_data_time,
                    )
                    db.commit()  # Luu data vao db ngay sau khi xu ly moi tram
                except:
                    traceback.print_exc()
                    db.rollback()
                try:
                    # hungdx add new table data_day_lastest issue 30
                    db.data_day_lastest.update_or_insert(
                        (db.data_day_lastest.station_id == station_id),
                        station_id=station_id,
                        last_time=lastest_day
                    )
                    db.commit()  # Luu data vao db ngay sau khi xu ly moi tram
                except:
                    traceback.print_exc()
                    db.rollback()
    return


################################################################################
def mon_data_calc(station_id, data_days, lastest_mon):
    from calendar import mdays

    data = dict()  # {indicator : sum value}
    count = dict()  # {indicator : count}
    max_data = dict()
    min_data = dict()
    max_data_time = dict()
    min_data_time = dict()

    for i, row in enumerate(data_days):
        # hungdx comment start issue 30
        # # Neu ko co du lieu cua thang truoc, tang month cho den month cua row hien tai thi thoi
        # if i == 0 and row.get_time.replace(day=1) > lastest_mon:
        #     while row.get_time.replace(day=1) > lastest_mon:
        #         lastest_mon = lastest_mon + timedelta(mdays[datetime.now().month])
        #
        # # Boc du lieu tu row vao data dict()
        # get_data = row.data         # kieu dict()
        # for indicator in get_data.keys():
        #     val = float(get_data[indicator])
        #
        #     if data.has_key(indicator):
        #         data[indicator] += val
        #         count[indicator] += 1
        #         if val > max_data[indicator]:
        #             max_data[indicator] = val
        #             max_data_time[indicator] = datetime.fromordinal(row.get_time.toordinal())   # phai convert kieu date ve datetime thi mongo no moi save dc vao DB
        #         if val < min_data[indicator]:
        #             min_data[indicator] = val
        #             min_data_time[indicator] = datetime.fromordinal(row.get_time.toordinal())
        #     else:
        #         data[indicator] = val
        #         count[indicator] = 1
        #         max_data[indicator] = val
        #         min_data[indicator] = val
        #         max_data_time[indicator] = datetime.fromordinal(row.get_time.toordinal())
        #         min_data_time[indicator] = datetime.fromordinal(row.get_time.toordinal())
        #
        # # Check if new month thi insert record vao bang data_mon va reset lai cac bien
        # if row.get_time.replace(day=1) > lastest_mon:
        #     # Neu du lieu dict la empty thi skip, ko luu DB
        #     if bool(data):
        #         # Calc average
        #         for indicator in data.keys():
        #             data[indicator] = float("{0:.4f}".format(data[indicator] / count[indicator]))
        #
        #         db.data_mon.update_or_insert(
        #             (db.data_mon.station_id == station_id) & (db.data_mon.get_time == lastest_mon),
        #             station_id = station_id,
        #             get_time = lastest_mon,
        #             data = data,
        #             data_min = min_data,
        #             data_max = max_data,
        #             data_min_time = min_data_time,
        #             data_max_time = max_data_time,
        #         )
        #     # Reset variables for new day
        #     lastest_mon = row.get_time.replace(day=1)
        #     data = dict()
        #     count = dict()
        #     max_data = dict()
        #     min_data = dict()
        #     max_data_time = dict()
        #     min_data_time = dict()
        #
        # hungdx comment end issue 30
        # Boc du lieu tu row hien tai vao data dict()
        get_data = row.data
        for indicator in get_data.keys():
            val = float(get_data[indicator])
            if data.has_key(indicator):
                data[indicator] += val
                count[indicator] += 1
                if val > max_data[indicator]:
                    max_data[indicator] = val
                    max_data_time[indicator] = datetime.datetime.fromordinal(
                        row.get_time.toordinal())  # phai convert kieu date ve datetime thi mongo no moi save dc vao DB
                if val < min_data[indicator]:
                    min_data[indicator] = val
                    min_data_time[indicator] = datetime.datetime.fromordinal(row.get_time.toordinal())
            else:
                data[indicator] = val
                count[indicator] = 1
                max_data[indicator] = val
                min_data[indicator] = val
                max_data_time[indicator] = datetime.datetime.fromordinal(row.get_time.toordinal())
                min_data_time[indicator] = datetime.datetime.fromordinal(row.get_time.toordinal())

        # Check if la row cuoi cung, thi insert record vao bang data_mon
        if i == len(data_days) - 1:
            # Neu du lieu dict la empty thi skip, ko luu DB
            if bool(data):
                # Calc average
                for indicator in data.keys():
                    data[indicator] = float("{0:.4f}".format(data[indicator] / count[indicator]))
                try:
                    db.data_mon.update_or_insert(
                        (db.data_mon.station_id == station_id) & (db.data_mon.get_time == lastest_mon),
                        station_id=station_id,
                        get_time=lastest_mon,
                        data=data,
                        data_min=min_data,
                        data_max=max_data,
                        data_min_time=min_data_time,
                        data_max_time=max_data_time,
                    )
                    db.commit()  # Luu data vao db ngay sau khi xu ly moi tram
                except:
                    traceback.print_exc()
                    db.rollback()

                try:
                    # hungdx add new table data_month_lastest issue 30
                    db.data_month_lastest.update_or_insert(
                        (db.data_month_lastest.station_id == station_id),
                        station_id=station_id,
                        last_time=lastest_mon
                    )
                    db.commit()  # Luu data vao db ngay sau khi xu ly moi tram
                except:
                    traceback.print_exc()
                    db.rollback()
    return


################################################################################
# hungdx new functions start issue 30
def get_lastest_hour_calcu():
    rows = db(db.data_hour_lastest.id > 0).select(
        db.data_hour_lastest.station_id,
        db.data_hour_lastest.last_time,
    )
    last_time_calc = {}
    for item in rows:
        last_time_calc[str(item.station_id)] = item.last_time
    return last_time_calc


# hungdx new function
def calc_data_hour_new_all(number_hours):
    try:
        logger.info('Start calculate hour data new')
        # lay danh sach cac tram (theo code tram - truoc lam code tram)
        _, _, _, station_codes = get_station_dict()
        # lay danh sach time tinh cuoi cung cua data hour
        lastest_hours = get_lastest_hour_calcu()

        # vong lap
        for index, code in enumerate(station_codes):
            if not code:
                continue
            station_id = station_codes.get(code)

            if not station_id:
                continue

            last_hour = lastest_hours.get(station_id)

            current_time = datetime.datetime.now()

            if last_hour:
                last_hour = last_hour - datetime.timedelta(hours=1)  # neu co du lieu cuoi thi tinh lai 1h truoc do
            else:
                last_hour = current_time - datetime.timedelta(
                    hours=number_hours)  # neu khong co du lieu thi tinh tu 1 ngay tu hien tai

            while last_hour < current_time:
                try:
                    start = last_hour.replace(minute=0, second=0, microsecond=0)
                    end = start + datetime.timedelta(hours=1)
                    conditions = (db.data_min.station_id == station_id)
                    conditions &= (db.data_min.get_time >= start)
                    conditions &= (db.data_min.get_time < end)
                    data_mins = db(conditions).select(orderby=db.data_min.get_time)
                    if data_mins:
                        hour_data_calc(station_id, data_mins, start)
                        db.commit()
                except Exception as ex:
                    traceback.print_exc()
                    logger.error(str(ex))
                last_hour = last_hour + datetime.timedelta(hours=1)
                pass
    except Exception as ex:
        traceback.print_exc()
        logger.error(str(ex))
    finally:
        logger.info('End calculate hour data new')

    return


# hungdx new function
def calc_data_hour_new():
    try:
        logger.info('Start calculate hour data new')
        # lay danh sach cac tram (theo code tram - truoc lam code tram)
        _, _, _, station_codes = get_station_dict()
        # lay danh sach time tinh cuoi cung cua data hour
        lastest_hours = get_lastest_hour_calcu()

        # vong lap
        for index, code in enumerate(station_codes):
            if not code:
                continue
            station_id = station_codes.get(code)

            if not station_id:
                continue

            last_hour = lastest_hours.get(station_id)

            current_time = datetime.datetime.now()

            if last_hour:
                last_hour = last_hour - datetime.timedelta(hours=1)  # neu co du lieu cuoi thi tinh lai 1h truoc do
            else:
                last_hour = current_time - datetime.timedelta(
                    hours=24 * 365 * 3)  # neu khong co du lieu thi tinh tu 1 ngay tu hien tai

            while last_hour < current_time:
                try:
                    start = last_hour.replace(minute=0, second=0, microsecond=0)
                    end = start + datetime.timedelta(hours=1)
                    conditions = (db.data_min.station_id == station_id)
                    conditions &= (db.data_min.get_time >= start)
                    conditions &= (db.data_min.get_time < end)
                    data_mins = db(conditions).select(orderby=db.data_min.get_time)
                    if data_mins:
                        hour_data_calc(station_id, data_mins, start)
                        db.commit()
                except Exception as ex:
                    traceback.print_exc()
                    logger.error(str(ex))
                last_hour = last_hour + datetime.timedelta(hours=1)
                pass
    except Exception as ex:
        traceback.print_exc()
        logger.error(str(ex))
    finally:
        logger.info('End calculate hour data new')

    return


def process_data(ftp, station_ids, count, lastest_files_dict, last_times, data_folder, station_indicator_dict,
                 lastest_data, station_names, stations_off, thresholds, preparing_dict, tendency_dict, file_mapping,
                 station_id='', file_mapping2='', file_mapping_each_station='', last_day='', parm_station_code='',
                 param_station_name='', station_logger=logging.getLogger('logger'), input_scan_failed=0):
    '''
       Xu ly data trong data_folder ftp (folder chua txt file tuong ung voi ngay can xu ly)
    '''

    station_logger.info('*' * 80)
    station_logger.info('Start process_data')

    res = 0
    res_scan_failed = 0

    if input_scan_failed:
        res_scan_failed = input_scan_failed
    else:
        res_scan_failed = 0

    # lay db hien tai
    # station_logger.info('*'*80)
    # station_logger.info('Start process_data')
    # station_logger.info('process_data-->station_id = %s', station_id)
    # station_logger.info('process_data-->station_name = %s', param_station_name)
    lastest_file = lastest_files_dict.get(station_id)
    # station_logger.info('process_data-->lastest_file = %s', lastest_file)
    station_logger.debug('process_data-->station_ids = %s', station_ids)
    station_logger.debug('process_data-->station_names = %s', station_names)
    station_logger.debug('process_data-->file_mapping = %s', file_mapping)
    station_logger.debug('process_data-->file_mapping_each_station = %s', file_mapping_each_station)
    station_logger.debug('process_data-->file_mapping2 = %s', file_mapping2)

    # Xu ly tung file thu muc
    is_not_found_data = False
    # Danh sach cac file txt trong folder cua tram tuong ung
    files = []
    try:
        ftp.retrlines("NLST", files.append)
    except Exception as ex:
        station_logger.error('process_data-->Read file Error server_data {}'.format(ex.message))
        res_scan_failed += 1
        res = 1
        return res, res_scan_failed

    # Quet toan bo thu muc hien tai va tim ra file can lay du lieu
    # Truong hop format path = 1, tat ca txt trong 1 thu muc, thi se phai lam cach khac, vi luong file lon
    for fname in files:
        try:
            is_not_found_data = False
            station_logger.debug('=' * 80)
            # Lay ten file
            basename = os.path.basename(fname)
            station_logger.debug('Start search file =%s', fname)
            station_logger.debug('process_data-->station_id = %s', station_id)
            station_logger.debug('process_data-->station_name = %s', param_station_name)
            station_logger.debug('process_data-->file_mapping = %s', file_mapping_each_station)
            station_logger.debug('process_data-->basename = %s', basename)

            # Neu ko tim duoc station voi CODE tuong ung hoac ko co file mapping --> skip
            # filename co format : province_stationcode_type_datetime.txt
            # se lay ma tram la "stationcode_type"
            current_file_mapping = ''
            try:
                idx = basename.index(parm_station_code)
            except:
                idx = -1

            station_logger.debug('process_data-->basename.basename.index(%s_) = %s', parm_station_code, idx)

            # TriNT: Delete loi
            # if idx == -1:
            #     if file_mapping2:
            #         try:
            #             idx = basename.index(file_mapping2 + '_')
            #             current_fm = file_mapping2
            #         except:
            #             idx = -1

            # TriNT: Add - Begin: Sua loi file_mapping
            if idx == -1:
                if file_mapping_each_station:
                    try:
                        idx = basename.index(file_mapping_each_station)
                        current_file_mapping = file_mapping_each_station
                    except:
                        idx = -1

            station_logger.debug('process_data-->file_mapping: current_file_mapping = %s', current_file_mapping)
            # TriNT: Add - End: Sua loi file_mapping

            if idx == -1:
                # Todo : ghi ra log nhung tram ko co file du lieu
                station_logger.info('File is not found station id : %s' % station_id)
                station_logger.info('File is not found station code : %s' % parm_station_code)
                station_logger.info('File is not found station : %s' % basename)
                is_not_found_data = True
                continue

            # station_id = station_codes.get(station_code) if station_codes.has_key(station_code) else ''

            if not station_id:
                # Todo : ghi ra log nhung tram ko co file du lieu
                station_logger.info('process_data-->No data file with station_id = %s', station_id)
                is_not_found_data = True
                continue

            # station_id = str(station_id)
            # So sanh filename voi file lastest da doc tuong ung voi station_id
            lastest_files_dict, last_times = get_lastest_files_dict_new_by_station_id(station_id)
            lastest_file = lastest_files_dict.get(station_id)

            station_logger.debug('process_data-->station_id   = %s', station_id)
            station_logger.debug('process_data-->station_name = %s', param_station_name)
            station_logger.debug('process_data-->Start search file  = %s', fname)
            station_logger.debug('process_data-->lastest_file       = %s', lastest_file)
            station_logger.debug('process_data-->basename           = %s', basename)
            station_logger.debug('process_data-->current_file_mapping = %s', current_file_mapping)

            try:
                # Neu la file cu thi ko xu ly gi ca --> skip
                if lastest_file:
                    if current_file_mapping.strip() != '':  # Neu co file mapping
                        # if not lastest_file.startswith(current_file_mapping):   # TriNT: Delete # Neu file ko bat dau = file mapping thi skip
                        if not (current_file_mapping in lastest_file):  # TriNT: Add
                            station_logger.debug(
                                'process_data-->No found file = %s in station name = %s, continue search',
                                current_file_mapping, param_station_name)
                            is_not_found_data = True
                            continue
                        else:
                            if basename <= lastest_file:
                                station_logger.debug('process_data --> Old File --> Skip and continue search')
                                is_not_found_data = True
                                continue
                            else:
                                station_logger.debug('process_data-->station_id   = %s', station_id)
                                station_logger.debug('process_data-->station_name = %s', param_station_name)
                                station_logger.debug('process_data-->lastest_file = %s', lastest_file)
                                station_logger.info('process_data-->basename     = %s', basename)
                                station_logger.info('process_data-->Read file and save')
                    else:  # Neu ko co file mapping
                        station_logger.debug('process_data-->Have not file mapping = %s', current_file_mapping)
                        if basename <= lastest_file:  # va file cu thi skip
                            station_logger.debug('process_data-->Old File --> Skip and continue search')
                            is_not_found_data = True
                            continue
                        else:
                            station_logger.info('process_data-->station_id   = %s', station_id)
                            station_logger.info('process_data-->station_name = %s', param_station_name)
                            station_logger.info('process_data-->lastest_file = %s', lastest_file)
                            station_logger.info('process_data-->basename     = %s', basename)
                            station_logger.info('process_data-->Start read file and save')
            except Exception as ex:
                traceback.print_exc()
                station_logger.info('process_data-->Search file have Exception: %s, continue search file', ex.message)
                is_not_found_data = True
                continue

            station_logger.debug("-" * 20)
            station_logger.debug('process_data-->station_id   = %s', station_id)
            station_logger.debug('process_data-->station_name = %s', param_station_name)
            station_logger.debug('process_data-->lastest_file = %s', lastest_file)
            station_logger.debug('process_data-->Processing read file = %s', basename)
            station_logger.debug('process_data-->current_file_mapping = %s', current_file_mapping)

            # TriNT: Doc file vao he thong
            count += 1
            lines = ''
            try:
                # read_data_in_file = StringIO()
                try:
                    # Faster version of StringIO
                    read_data_in_file = cStringIO.StringIO()
                except:
                    read_data_in_file = StringIO()

                # data_folder2 = data_folder + os.sep + basename
                data_folder2 = data_folder + '/' + basename
                station_logger.info('process_data-->Read file = %s', data_folder2)
                # Doc File va do du lieu vao read_data_in_file
                # download the file
                ftp.retrbinary('RETR ' + data_folder2, read_data_in_file.write)

                if read_data_in_file:
                    lines = read_data_in_file.getvalue()

                read_data_in_file.close()
                # else:
                #     is_not_found_data = True
                #     # res = 1
                #     # continue
            except Exception as ex:
                # traceback.print_exc()
                # exc_buffer = io.StringIO()
                # traceback.print_exc(file=exc_buffer)
                # logging.error('Uncaught exception in read file in process:\n%s', exc_buffer.getvalue())
                traceback.print_exc()

                station_logger.info('process_data-->station_id         = %s', station_id)
                station_logger.info('process_data-->station_name       = %s', param_station_name)
                station_logger.info('process_data-->lastest_file       = %s', lastest_file)
                station_logger.info('process_data-->basename           = %s', basename)
                station_logger.error('process_data-->Can not read file = %s', data_folder2)
                station_logger.error('process_data-->Read file Error with exception = %s', ex.message)
                station_logger.error('process_data-->Read file Error server_data {}'.format(ex.message))
                res_scan_failed += 1
                res = 1
                return res, res_scan_failed

                # continue
                # Khong doc duoc du lieu txt can tim
                # Ben ngoai ham nay, res = 1 se cap nhat tran thai mat ket noi tai thoi dien do

            is_qcvn_exceed = False
            is_exceed = False
            is_preparing = False
            is_tendency = False
            is_equipment_error = False

            equipment_ids_err = []
            data_datetime = ''
            data = dict()

            # Quet tung dong trong file va day vao doi tuong items
            station_logger.debug("file name = %s", basename)
            station_logger.info("Data = %s", lines)

            for line in lines.splitlines():
                try:
                    # Remove whitespace characters like `\n` at the end of each line
                    if line:
                        line = line.strip()
                        items_temp = line.split()
                        if len(items_temp) < 3:  # Khong phai du lieu thong so do
                            continue
                    # else:
                    #     continue
                except:
                    station_logger.debug("lines.splitlines name = %s", basename)
                    # continue

                items = []
                # items[0] = indicator
                # items[1] = value
                # items[2] = unit
                # items[3] = '%Y%m%d%H%M%S'
                # items[4] = status
                try:
                    # Case 1: line co format :  "indicator   value   unit  datetime [status]"
                    check_time = datetime.datetime.strptime(items_temp[3], '%Y%m%d%H%M%S')
                    items = items_temp[:]
                except:
                    # traceback.print_exc()
                    try:
                        # Case 2: line co format :  "datetime indicator   value   unit"
                        check_time = datetime.datetime.strptime(items_temp[0], '%Y%m%d%H%M%S')
                        if len(items_temp) == 3:
                            # Case 3: line co format :  "datetime indicator  value"
                            items = [items_temp[1], items_temp[2], '---', items_temp[0]]
                        else:
                            # Convert ve case 1
                            items = [items_temp[1], items_temp[2], items_temp[3], items_temp[0]]
                    except:
                        try:
                            # Case 4: line co format :  "indicator   value   datetime [status]"
                            check_time = datetime.datetime.strptime(items_temp[2], '%Y%m%d%H%M%S')
                            items = [items_temp[0], items_temp[1], '---', items_temp[2]]
                        except:
                            items = []
                            pass
                    pass

                if not items:
                    continue

                # TriNT Kiem tra trang thai thiet bi do -------------------------------------------------------
                # Da co du lieu va da day va doi tuong luu tru la items
                sensor_status = 0  # status: 00 --> Dang do; 01: Hieu chinh; 02: Loi thiet bi

                # items[0] = indicator
                # items[1] = value
                # items[2] = unit
                # items[3] = '%Y%m%d%H%M%S'
                # items[4] = status
                station_logger.debug('-' * 10)
                station_logger.debug('Kiem tra trang thai thiet bi do')
                station_logger.debug('process_data-->station_id   = %s', station_id)
                station_logger.debug('process_data-->station_name = %s', param_station_name)
                station_logger.debug('process_data-->items : %s' % items)

                try:
                    sensor_status = int(items[4])
                except:
                    # Neu khong co cot status thi sensor khong hong, mac dinh hoat dong binh thuong
                    sensor_status = 0

                try:  # Try to parse value of indicator
                    items[1] = float(items[1])
                except:
                    items[1] = 0

                # If sensor is error, set value as 0
                if sensor_status == 2:
                    # TriNT: Neu sensor bi loi, gi set value = 0
                    items[1] = 0

                # TriNT: Kiem tra indicator da khai bao chua, neu co thi nhan ty le chuyen doi -------------------------------------------------------
                # items[0] = indicator
                # items[1] = value
                # items[2] = unit
                # items[3] = '%Y%m%d%H%M%S'
                # items[4] = status
                # station_logger.info('process_data-->items : %s' % items)
                try:
                    # Check indicator nay co ten Mapping ko, neu co, thi dung mapping name
                    station_logger.debug('-' * 10)
                    station_logger.debug("Start: Check define indicator, and convert unit")
                    station_logger.debug("station_id: %s", station_id)
                    station_logger.debug('process_data-->station_name = %s', param_station_name)

                    for key in station_indicator_dict[station_id]:
                        try:
                            if station_indicator_dict[station_id][key]['mapping_name'] == items[0]:
                                items[0] = key
                                break
                        except Exception as ex:
                            traceback.print_exc()
                            station_logger.error("station_indicator.station_id = %s", station_id)
                            station_logger.info('process_data-->station_name = %s', param_station_name)
                            station_logger.error("key = %s", key)
                            station_logger.error('%s not define', key)
                            station_logger.error('Exception = %s', ex.message)

                    # check ty le chuyen doi
                    station_logger.debug('process_data-->basename = %s', basename)
                    if station_indicator_dict[station_id].has_key(items[0]):
                        convert_rate = station_indicator_dict[station_id][items[0]]['convert_rate'] or 1
                        station_logger.debug("convert_rate: %s", convert_rate)
                        station_logger.debug("indicator value: %s", items[1])
                        items[1] = items[1] * convert_rate
                        station_logger.debug("indicator value after convert: %s", items[1])

                    # Neu indicator co trong file ma ko dang ky chi so cua tram thi skip
                    station_logger.debug('process_data-->station_id   = %s', station_id)
                    station_logger.debug('process_data-->station_name = %s', param_station_name)
                    station_logger.debug('thresholds = %s', thresholds)
                    station_logger.debug('items[0] = %s', items[0])
                    station_logger.debug('thresholds[station_id].has_key(items[0]) = %s',
                                         thresholds[station_id].has_key(items[0]))
                    station_logger.debug('-' * 20)
                    if not thresholds.has_key(station_id) or not thresholds[station_id].has_key(items[0].upper()):
                        continue
                except Exception as ex:
                    traceback.print_exc()
                    station_logger.debug("station_indicator.station_id = %s", station_id)
                    station_logger.debug('process_data-->station_name = %s', param_station_name)
                    station_logger.debug('Error when check define indicator, and convert unit. Exception = %s',
                                         ex.message)
                    # continue

                try:
                    data[items[0]] = items[1]
                    data_datetime = items[3]  # datetime trong 1 file se giong het nhau
                    # ==================================================
                    # TriNT: So sanh QCVN
                    # Chi can 1 chi so vuot nguong la danh dau 'exceed'
                    station_logger.debug('-' * 20)
                    station_logger.debug('So sanh QCVN: station_id = %s', station_id)
                    station_logger.debug('process_data-->station_name = %s', param_station_name)
                    station_logger.debug('process_data-->basename = %s', basename)
                    station_logger.debug('thresholds = %s', thresholds)
                    station_logger.debug('items[1] = value = %s', items[1])

                    try:
                        # Co mot so truong hop QCVN khong duoc khai bao
                        # station_logger.info('QCVN Max = %s ; threshold = %s', station_id, thresholds[station_id][items[0].upper()])
                        qcvn_detail_min_value = station_indicator_dict[station_id][items[0]]['qcvn_detail_min_value']
                        qcvn_detail_max_value = station_indicator_dict[station_id][items[0]]['qcvn_detail_max_value']
                    except Exception as ex:
                        qcvn_detail_min_value = None
                        qcvn_detail_max_value = None

                    station_logger.debug('Indicator = %s', items[0])
                    station_logger.debug('Indicator value = %s', items[1])
                    station_logger.debug('qcvn_detail_min_value = %s', qcvn_detail_min_value)
                    station_logger.debug('qcvn_detail_max_value = %s', qcvn_detail_max_value)

                    # station_logger.debug('preparing = %s', preparing_dict[station_id][items[0]])
                    # station_logger.debug('tendency = %s', tendency_dict[station_id][items[0]])

                    if float(items[1]) > thresholds[station_id][items[0].upper()]:
                        is_exceed = True
                    elif float(items[1]) >= preparing_dict[station_id][items[0].upper()]:
                        is_preparing = True
                    elif float(items[1]) >= tendency_dict[station_id][items[0].upper()]:
                        is_tendency = True

                    # items[0] = indicator
                    # items[1] = value
                    # items[2] = unit
                    # items[3] = '%Y%m%d%H%M%S'
                    # items[4] = status
                    compare_type = 0

                    if qcvn_detail_min_value and qcvn_detail_max_value:
                        # So sanh <= ... <=
                        if (float(items[1]) >= qcvn_detail_min_value) and (float(items[1]) <= qcvn_detail_max_value):
                            is_qcvn_exceed = False
                        else:
                            is_qcvn_exceed = True
                    else:
                        if qcvn_detail_max_value:
                            if float(items[1]) <= qcvn_detail_max_value:
                                is_qcvn_exceed = False
                            else:
                                is_qcvn_exceed = True
                        elif qcvn_detail_min_value:
                            if float(items[1]) >= qcvn_detail_min_value:
                                is_qcvn_exceed = False
                            else:
                                is_qcvn_exceed = True
                        else:
                            is_qcvn_exceed = False

                    station_logger.debug('is_qcvn_exceed = %s', is_qcvn_exceed)
                except Exception as ex:
                    traceback.print_exc()
                    station_logger.info("station_indicator.station_id = %s", station_id)
                    station_logger.info('process_data-->station_name = %s', param_station_name)
                    station_logger.error('Have error when check QCVN. Exception =   %s', ex.message)
                    is_qcvn_exceed = False
            # End for

            # Neu du lieu dict la empty thi skip, ko luu DB
            if not bool(data): continue

            # Luu du lien vao database
            station_logger.info('-' * 20)
            # data_datetime = items[3]  # datetime trong 1 file se giong het nhau
            get_time = datetime.datetime.strptime(items[3], '%Y%m%d%H%M%S')

            station_logger.info('process_data-->station_id     = %s', station_id)
            station_logger.info('process_data-->station_name   = %s', param_station_name)
            station_logger.debug('process_data-->lastest_file  = %s', lastest_file)
            station_logger.debug('process_data-->read file     = %s', basename)
            station_logger.info('process_data-->get_time       = %s', get_time)
            station_logger.info('process_data-->is_exceed      = %s', is_exceed)
            station_logger.info('process_data-->is_qcvn_exceed = %s', is_qcvn_exceed)
            station_logger.info('process_data-->data           = %s', data)

            try:
                station_logger.info("Call db.data_min.update_or_insert")
                try:
                    db.data_min.update_or_insert((db.data_min.station_id == station_id) &
                                                 (db.data_min.get_time == get_time),
                                                 station_id=station_id,
                                                 get_time=get_time,
                                                 # is_exceed=is_exceed, # TriNT: Custer change requirment,
                                                 is_exceed=is_qcvn_exceed,  # TriNT: Custer change requirment,
                                                 data=data
                                                 )
                    db.commit()
                    station_logger.info("Call db.data_min.update_or_insert: ok")
                except:
                    traceback.print_exc()
                    db.rollback()
            except Exception as ex:
                traceback.print_exc()
                station_logger.error('Save data into data_min have error. Exception = %s', ex.message)

            # TriNT: -------------------Xu ly HIEU CHINH du lieu cho bang data_adjust
            # sensor_status = 0  # status: 00 --> Dang do; 01: Hieu chinh; 02: Loi thiet bi
            station_logger.debug('-' * 20)
            station_logger.debug('Xu ly hieu chuan, va hieu chinh tu dong')
            station_logger.debug('station_id = %s', station_id)
            station_logger.debug('process_data-->station_name = %s', param_station_name)
            station_logger.debug("data = %s", data)

            data_adjust = dict()

            # sensor_status = 0  # status: 00 --> Dang do; 01: Hieu chinh; 02: Loi thiet bi
            for indicator in data:
                try:
                    station_logger.debug('-' * 10)
                    station_logger.debug('station_id = %s', station_id)
                    station_logger.debug('process_data-->station_name = %s', param_station_name)
                    station_logger.debug('process_data-->basename     = %s', basename)
                    station_logger.debug('process_data-->lastest_file = %s', lastest_file)
                    station_logger.debug('file_mapping_each_station = %s', file_mapping_each_station)
                    station_logger.debug('indicator = %s', indicator)
                    station_logger.debug('data[indicator] = %s', data[indicator])
                    # Check indicator value = Null --> Sensor error
                    if station_indicator_dict[station_id].has_key(indicator):
                        try:
                            data[indicator] = float(data[indicator])
                            station_logger.debug('data[indicator] = %s', data[indicator])
                        except Exception as ex:
                            traceback.print_exc()
                            station_logger.error('Exception = %s', ex.message)
                            data[indicator] = 0
                            is_equipment_error = True
                            station_logger.info('Exception = %s', ex.message)

                        station_logger.debug('data = %s', data)
                        station_logger.debug('indicator = %s', indicator)
                        station_logger.debug('data[indicator] = %s', data[indicator])
                        station_logger.debug('is_equipment_error = %s', is_equipment_error)
                        station_logger.debug('sensor_status = %s', sensor_status)

                        # sensor_status = 0  # status: 00 --> Dang do; 01: Hieu chinh; 02: Loi thiet bi
                        if sensor_status == 2:
                            is_equipment_error = True

                        if is_equipment_error:
                            # is_equipment_error = True
                            equipment_id = station_indicator_dict[station_id][indicator]['equipment_id']
                            station_logger.debug('equipment_id = %s', equipment_id)

                            # sensor_status = 0  # status: 00 --> Dang do; 01: Hieu chinh; 02: Loi thiet bi
                            if equipment_id:
                                equipment_ids_err.append(equipment_id)
                                # Cap nhat trang thai thiet bi tuong ung tram
                                try:
                                    db(db.equipments.id == equipment_id).update(
                                        status=2
                                    )
                                    db.commit()
                                except:
                                    traceback.print_exc()
                                    db.rollback()
                                # Cap nhat trang thai thiet bi vao bang lich su loi thiet bi
                                # db.define_table('equipments_status_history',
                                #                 Field('station_id', 'string', notnull=True),
                                #                 Field('status', 'integer', default=0),
                                #                 Field('equipment_id', 'string'),  # Mot thiet bi luu dc nhieu thong so
                                #                 Field('get_time', 'datetime', notnull=True),
                                #                 )
                                station_logger.info('equipments_status_history.update_or_insert')
                                station_logger.info('station_id = %s', station_id)
                                station_logger.info('process_data-->station_name = %s', param_station_name)
                                station_logger.info('equipment_id = %s', equipment_id)
                                station_logger.info('sensor_status = %s', sensor_status)
                                station_logger.info('get_time = %s', get_time)
                                # station_logger.info("Logger")
                                try:
                                    db.equipments_status_history.update_or_insert(
                                        (db.equipments_status_history.station_id == station_id) &
                                        (db.equipments_status_history.get_time == get_time),
                                        station_id=station_id,
                                        get_time=get_time,
                                        status=sensor_status,
                                        equipment_id=equipment_id,
                                        )
                                    db.commit()
                                except:
                                    traceback.print_exc()
                                    db.rollback()
                        ### TriNT: Check cac dieu kien hieu chinh tu dong --------------------------------------------
                        # Neu continous_equal = True, thi tim kiem xem truoc do co bi lap lai continous_times lan
                        station_logger.debug('continous_equal = %s',
                                             station_indicator_dict[station_id][indicator]['continous_equal'])
                        continous_equal = station_indicator_dict[station_id][indicator]['continous_equal']

                        # Neu thong so bat co continous_equal = True, thi tien hanh kiem tra du lieu lastest va du lieu hien tai co trung khong
                        # Neu trung nhau, thi tien hanh kiem tra da trung bao lan, neu vuot qua so lan qui dinh, thi loai bo du lieu

                        if continous_equal:
                            # Get current continous equal times
                            continous_time = station_indicator_dict[station_id][indicator]['continous_times'] or 0

                            station_logger.debug('station_indicator-->continous_times  = %s',
                                                 station_indicator_dict[station_id][indicator]['continous_times'])
                            station_logger.debug('continous_time = %s', continous_time)

                            # Check indicator's value with lastest value
                            if lastest_data.has_key(station_id) and lastest_data[station_id].has_key(indicator):
                                station_logger.debug('station_id = %s', station_id)
                                station_logger.debug('process_data-->station_name = %s', param_station_name)
                                station_logger.debug('indicator = %s', indicator)
                                station_logger.debug('lastest_data[station_id][indicator] = %s',
                                                     lastest_data[station_id][indicator])
                                station_logger.debug('data[indicator] = %s', data[indicator])
                                # Neu du lieu trong db la lastest_data, co gia tri =  data[indicator], thi tang continous_time len 1
                                if lastest_data[station_id][indicator] == data[indicator]:
                                    continous_time += 1
                                else:
                                    # Neu khong bang, thi reset continous_time ve gia tri ban dau
                                    continous_time = 1
                            else:
                                continous_time = 1

                            station_logger.debug('continous_time = %s', continous_time)

                            # Update continues times vao database
                            try:
                                conditions = (db.station_indicator.id == station_indicator_dict[station_id][indicator][
                                    'id'])
                                # TriNT: Update continous_times vao database sau moi lan lay du lieu tu txt
                                db(conditions).update(continous_times=continous_time)
                                db.commit()
                            except:
                                traceback.print_exc()
                                db.rollback()

                            # Neu gia tri trong station_indicator.continous_equal_value = continous_time, thi bo qua, ko luu vao data_adjustment
                            if station_indicator_dict[station_id][indicator]['continous_equal_value'] == continous_time:
                                continue

                        # Check gia tri co = 0 hay khong ?
                        if station_indicator_dict[station_id][indicator]['equal0'] and data[indicator] == 0: continue

                        # Check gia tri co <= hay khong ?
                        if station_indicator_dict[station_id][indicator]['negative_value'] and data[
                            indicator] < 0: continue

                        # Kiem tra ngoai khoang do cua thiet bi
                        if station_indicator_dict[station_id][indicator]['out_of_range'] and \
                                (data[indicator] > station_indicator_dict[station_id][indicator]['out_of_range_max'] or
                                 data[indicator] < station_indicator_dict[station_id][indicator]['out_of_range_min']):
                            continue

                        data_adjust[indicator] = data[indicator]
                except Exception as ex:
                    station_logger.error("Have error: %s", ex.message)
            # End for

            # Neu co du lieu hieu chuan, thi tien hanh luu vao database
            if bool(data_adjust):
                # Update du lieu vao 'data_adjust'
                # db.data_adjust.insert(
                #     station_id = station_id,
                #     get_time = get_time,
                #     is_exceed = is_exceed,
                #     data = data_adjust
                # )
                station_logger.info("Call db.data_adjust.update_or_insert")
                try:
                    db.data_adjust.update_or_insert((db.data_adjust.station_id == station_id) &
                                                    (db.data_adjust.get_time == get_time),
                                                    station_id=station_id,
                                                    get_time=get_time,
                                                    # is_exceed=is_exceed, # TriNT: Customer change request, using qcvn
                                                    is_exceed=is_qcvn_exceed,
                                                    # TriNT: Customer change request, using qcvn
                                                    data=data_adjust
                                                    )
                    db.commit()
                except:
                    traceback.print_exc()
                    db.rollback()

                station_logger.info("Call db.data_adjust.update_or_insert: ok")
            # Update du lieu vao 'data_lastest'
            station_logger.debug("db.data_lastest.update_or_insert")
            try:
                db.data_lastest.update_or_insert(
                    db.data_lastest.station_id == station_id,  # dieu kien
                    station_id=station_id,
                    get_time=get_time,
                    # is_exceed=is_exceed, # TriNT: Customer change request, using qcvn
                    is_exceed=is_qcvn_exceed,  # TriNT: Customer change request, using qcvn
                    data=data
                )
                db.commit()
            except:
                traceback.print_exc()
                db.rollback()

            station_logger.info("db.data_lastest.update_or_insert: ok time " + str(get_time))

            # logger.info("db.last_data_files.update_or_insert")
            # Update bang 'last_data_files'
            try:
                db.last_data_files.update_or_insert(
                    db.last_data_files.station_id == station_id,  # dieu kien
                    station_id=station_id,
                    filename=basename,
                    lasttime=get_time,
                    station_name=station_names.get(station_id)
                )
                db.commit()  # Luu data vao db ngay sau khi xu ly moi tram
            except:
                traceback.print_exc()
                db.rollback()

            station_logger.info("db.last_data_files.update_or_insert: ok")

            res = 0
            res_scan_failed = 0

            # TriNT: Canh bao ----------------------------------------------------

            # STATION_STATUS = {
            #     'GOOD': {'value': 0, 'name': 'Good', 'color': '#1dce6c', 'icon': 'fa fa-circle'},
            #     # 'TENDENCY': {'value': 1, 'name': 'Tendency', 'color': '#F1D748', 'icon': 'fa fa-circle'},
            #     'TENDENCY': {'value': 1, 'name': 'Good', 'color': '#1dce6c', 'icon': 'fa fa-circle'},
            #     # 'PREPARING': {'value': 2, 'name': 'Preparing', 'color': '#F08432', 'icon': 'fa fa-circle'},
            #     'PREPARING': {'value': 2, 'name': 'Good', 'color': '#1dce6c', 'icon': 'fa fa-circle'},
            #     'EXCEED': {'value': 3, 'name': 'Exceed', 'color': '#EA3223', 'icon': 'fa fa-circle'},
            #     'OFFLINE': {'value': 4, 'name': 'Offline', 'color': '#999999', 'icon': 'fa fa-stop'},
            #     'ADJUSTING': {'value': 5, 'name': 'Adjusting', 'color': 'purple', 'icon': 'fa fa-pause'},
            #     'ERROR': {'value': 6, 'name': 'Sensor error', 'color': 'red', 'icon': 'fa fa-times-circle-o'},
            # }

            station_status = 0  # GOOD
            # Update bang canh bao cho chi so 'data_alarm'
            alarm_level = ''  # Khong co canh bao

            # Xu huong vuot
            if is_tendency:
                station_status = 1
                alarm_level = 0

            # Xu chuan bi vuot
            if is_preparing:
                station_status = 2
                alarm_level = 1

            # Xu vuot QCVN
            # if is_exceed:  # TriNT: Customer change request, using qcvn
            if is_qcvn_exceed:  # TriNT: Customer change request, using qcvn
                station_status = 3
                alarm_level = 2
            res_scan_failed = 0
            try:
                db(db.stations.id == station_id).update(
                    status=station_status,
                    scan_failed=0
                )
                db.commit()  # Luu data vao db ngay sau khi xu ly moi tram
                station_logger.debug("db.stations.update_or_insert: ok")
            except:
                traceback.print_exc()
                db.rollback()

            if alarm_level:
                try:
                    db.data_alarm.update_or_insert(
                        (db.data_alarm.station_id == station_id) &
                        (db.data_alarm.get_time == get_time),
                        station_id=station_id,
                        get_time=get_time,
                        alarm_level=alarm_level,
                        data=data
                    )
                    db.commit()  # Luu data vao db ngay sau khi xu ly moi tram
                    station_logger.debug("db.data_alarm.update_or_insert: ok")
                except:
                    traceback.print_exc()
                    db.rollback()

            # Update bang 'station_off_log'

            station_logger.debug("-" * 10)
            station_logger.debug("Update station_off_log")
            station_logger.debug("Tim kiem cac tram stations_off = %s", stations_off)
            try:
                found_stations_off = False
                for row in stations_off:
                    # logger.info('row.station_id = %s', row.station_id)
                    # logger.info('station_id = %s', station_id)
                    if row.station_id == station_id:
                        # Tinh khoang tgian Inactive
                        # diff = get_time - row.start_off
                        # hungdx: fix error diff < 0
                        diff = datetime.datetime.now() - row.start_off
                        diff = diff.days * 24 * 3600 + diff.seconds
                        try:
                            row.update_record(
                                end_off=datetime.datetime.now(),
                                duration=diff
                            )
                            db.commit()
                        except:
                            traceback.print_exc()
                            db.rollback()

                        found_stations_off = True

                        station_logger.debug('row.station_id = %s', row.station_id)
                        station_logger.debug('station_id = %s', station_id)
                        station_logger.debug('process_data-->station_name = %s', param_station_name)
                        station_logger.info("Update station_off_log: OK")

                        break  # Ly thuyet thi chi co toi da duy nhat 1 row tuong ung voi station off
                if not found_stations_off:
                    station_logger.info("found_stations_off: Khong co")
            except Exception as ex:
                traceback.print_exc()
                station_logger.error('Exception = Update station_off_log have error: %s', ex.message)

            try:
                # Update equipment status
                station_logger.info('-' * 10)
                station_logger.debug("Update equipment status")
                equip_ids = []
                for indicator in data:
                    try:
                        equip_id = station_indicator_dict[station_id][indicator]['equipment_id']
                        station_logger.debug("equip_id = %s", equip_id)
                        if equip_id and equip_id not in equipment_ids_err:
                            equip_ids.append(equip_id)
                    except:
                        station_logger.debug("station_id = %s", station_id)
                        station_logger.debug("indicator = %s", indicator)
                        station_logger.debug("Tram khong ton tai thiet bi")
                        # continue

                station_logger.debug("equip_ids = %s", equip_ids)
                if equip_ids:
                    try:
                        db(db.equipments.id.belongs(equip_ids)).update(status=1)
                        db.commit()
                        station_logger.info("Update equipment status: ok")
                    except:
                        traceback.print_exc()
                        db.rollback()

                # Update station status
                station_logger.debug("is_equipment_error = %s", is_equipment_error)

                if is_equipment_error:
                    station_status = 6

                station_logger.debug("update station_status = %s", station_status)
                res_scan_failed = 0
                try:
                    db(db.stations.id == station_id).update(
                        status=station_status,
                        scan_failed=0
                    )

                    db.commit()  # Luu data vao db ngay sau khi xu ly moi tram

                    station_logger.info("update station_status = %s : ok", station_status)
                    station_logger.debug("update station_status = ok")
                    station_logger.debug("station_id = %s", station_id)
                    station_logger.debug('process_data-->station_name = %s', param_station_name)
                    station_logger.debug("station_status = %s", station_status)
                except:
                    traceback.print_exc()
                    db.rollback()

            except Exception as ex:
                traceback.print_exc()
                station_logger.error('Exception = Update equipment status have error: %s', ex.message)

            try:
                station_logger.debug('-' * 10)
                station_logger.debug("Start send mail, sms when have error")
                # Xu ly gui mail, sms
                # Get info of station_alarm
                station_alarm = db(db.station_alarm.station_id == station_id).select()
                if station_alarm:
                    station_alarm = station_alarm.first()
                else:
                    continue
                flag_email = False
                flag_sms = False
                # Kiem tra tram co phep gui email khong
                if station_alarm.tendency_method_email and is_tendency:
                    lst_email = station_alarm.tendency_email_list
                    subject = '%s %s (%s)' % (station_alarm.station_name, 'Tendency', data_datetime)
                    content = station_alarm.tendency_msg
                    flag_email = True
                elif station_alarm.preparing_method_email and is_preparing:
                    lst_email = station_alarm.preparing_email_list
                    content = station_alarm.preparing_msg
                    subject = '%s %s (%s)' % (station_alarm.station_name, 'Preparing', data_datetime)
                    flag_email = True

                elif station_alarm.exceed_method_email and is_qcvn_exceed:
                    lst_email = station_alarm.exceed_email_list
                    content = station_alarm.exceed_msg
                    subject = '%s %s (%s)' % (station_alarm.station_name, 'Exceed', data_datetime)
                    flag_email = True

                elif station_alarm.exceed_method_email and is_exceed:
                    lst_email = station_alarm.exceed_email_list
                    content = station_alarm.exceed_msg
                    subject = '%s %s (%s)' % (station_alarm.station_name, 'Exceed', data_datetime)
                    flag_email = True

                # Kiem tra tram co phep gui sms khong
                if station_alarm.tendency_method_sms and is_tendency:
                    lst_phones = station_alarm.tendency_phone_list
                    content = station_alarm.tendency_msg
                    flag_sms = True
                elif station_alarm.preparing_method_sms and is_preparing:
                    lst_phones = station_alarm.preparing_phone_list
                    content = station_alarm.preparing_msg
                    flag_sms = True
                elif station_alarm.exceed_method_sms and is_exceed:
                    lst_phones = station_alarm.exceed_phone_list
                    content = station_alarm.exceed_msg
                    flag_sms = True

                # Send mail
                if flag_email and False:
                    subject = subject
                    message = content
                    try:
                        send_mail(mail_to=lst_email, subject=subject, message=message)
                    except Exception as ex:
                        traceback.print_exc()
                        station_logger.error('Exception = %s', ex.message)
                        station_logger.error('Exception = Send mail failed')
                        station_logger.error(str(ex))

                # Send SMS
                # if flag_sms:
                #     phones = lst_phones.split(',')
                #     from suds.client import Client
                #     try:
                #         conn = Client('http://124.158.6.45/CMC_BRAND/Service.asmx?WSDL')
                #         for p in phones:
                #             p = p.strip()
                #             ret = conn.service.SendSMSBrandName(phone=p, sms=content, sender='CMC Telecom',
                #                                                 username='hn_telecom', password='telecom@123!')
                #     except Exception as ex:
                #         logger.error('Send SMS failed')
                #         logger.error(str(ex))
            except Exception as ex:
                traceback.print_exc()
                station_logger.error('Exception = Send mail, sms when have error: %s', ex.message)

        except Exception as ex:
            traceback.print_exc()
            station_logger.info('Exception all = %s', ex.message)

    # Ket thuc for quet cac file trong thu muc
    lastest_files_dict, last_times = get_lastest_files_dict_new_by_station_id(station_id)
    lastest_file = lastest_files_dict.get(station_id)
    station_logger.info('process_data-->station_id   = %s', station_id)
    station_logger.info('process_data-->station_name = %s', param_station_name)
    # logger.info('process_data-->get_time      = %s', get_time)
    station_logger.info('process_data-->lastest_file = %s', lastest_file)
    station_logger.info("process_data-->Ket thuc for quet cac file trong thu muc voi res = %s", res)
    station_logger.info("*" * 80)
    return res, res_scan_failed


################################################################################
def get_lastest_day_calcu():
    rows = db(db.data_day_lastest.id > 0).select(
        db.data_day_lastest.station_id,
        db.data_day_lastest.last_time,
    )
    last_time_calc = {}
    for item in rows:
        last_time_calc[str(item.station_id)] = item.last_time
    return last_time_calc


########################################################################################
def calc_data_day_new():
    try:
        logger.info('Start calculate day data new')
        _, _, _, station_codes = get_station_dict()
        # lay danh sach time tinh cuoi cung cua data day
        lastest_days = get_lastest_day_calcu()

        # vong lap
        for index, code in enumerate(station_codes):
            if not code:
                continue

            station_id = station_codes.get(code)
            if not station_id:
                continue
            last_days = lastest_days.get(station_id)
            current_time = datetime.datetime.now()
            if last_days:
                last_days = last_days - datetime.timedelta(days=1)  # neu co du lieu cuoi thi tinh lai 1h truoc do
            else:
                last_days = current_time - datetime.timedelta(
                    days=3 * 365)  # neu khong co du lieu thi tinh tu 1000 ngay tu hien tai

            while last_days < current_time:
                try:
                    start = last_days.replace(hour=0, minute=0, second=0, microsecond=0)
                    end = start + datetime.timedelta(days=1)
                    conditions = (db.data_hour.station_id == station_id)
                    conditions &= (db.data_hour.get_time >= start)
                    conditions &= (db.data_hour.get_time < end)
                    data_hours = db(conditions).select(orderby=db.data_hour.get_time)
                    if data_hours:
                        day_data_calc(station_id, data_hours, start)
                        db.commit()
                except Exception as ex:
                    traceback.print_exc()
                    logger.error(str(ex))
                last_days = last_days + datetime.timedelta(days=1)
            pass
        db.commit()
    except Exception as ex:
        traceback.print_exc()
        logger.error(str(ex))
    finally:
        logger.info('End calculate day data new')

    return


########################################################################################
def calc_data_day_new_all(days):
    try:
        logger.info('Start calculate day data new')
        _, _, _, station_codes = get_station_dict()
        # lay danh sach time tinh cuoi cung cua data day
        lastest_days = get_lastest_day_calcu()

        # vong lap
        for index, code in enumerate(station_codes):
            if not code:
                continue

            station_id = station_codes.get(code)
            if not station_id:
                continue
            last_days = lastest_days.get(station_id)
            current_time = datetime.datetime.now()

            if last_days:
                last_days = last_days - datetime.timedelta(days=1)  # neu co du lieu cuoi thi tinh lai 1h truoc do
            else:
                last_days = current_time - datetime.timedelta(
                    days=days)  # neu khong co du lieu thi tinh tu 1000 ngay tu hien tai

            while last_days < current_time:
                try:
                    start = last_days.replace(hour=0, minute=0, second=0, microsecond=0)
                    end = start + datetime.timedelta(days=1)
                    conditions = (db.data_hour.station_id == station_id)
                    conditions &= (db.data_hour.get_time >= start)
                    conditions &= (db.data_hour.get_time < end)
                    data_hours = db(conditions).select(orderby=db.data_hour.get_time)
                    if data_hours:
                        day_data_calc(station_id, data_hours, start)
                        db.commit()
                except Exception as ex:
                    traceback.print_exc()
                    logger.error(str(ex))
                last_days = last_days + datetime.timedelta(days=1)
            pass
        db.commit()
    except Exception as ex:
        traceback.print_exc()
        logger.error(str(ex))
    finally:
        logger.info('End calculate day data new')

    return


################################################################################
def get_lastest_month_calcu():
    rows = db(db.data_month_lastest.id > 0).select(
        db.data_month_lastest.station_id,
        db.data_month_lastest.last_time,
    )
    last_time_calc = {}
    for item in rows:
        last_time_calc[str(item.station_id)] = item.last_time
    return last_time_calc


# hungdx end issue 30
################################################################################
def calc_data_month_new_all(number_days):
    try:
        logger.info('Start calculate month data new')
        _, _, _, station_codes = get_station_dict()
        # lay danh sach time tinh cuoi cung cua data hour
        lastest_month = get_lastest_month_calcu()

        # vong lap
        for index, code in enumerate(station_codes):
            if not code:
                continue
            station_id = station_codes.get(code)
            if not station_id:
                continue
            last_month = lastest_month.get(station_id)
            current_time = datetime.datetime.now()
            if last_month:
                last_month = last_month  # month khac chut nen phai tinh lai cho dung
            else:
                last_month = current_time - datetime.timedelta(
                    days=365 * 3)  # neu khong co du lieu thi tinh tu 1000 ngay tu hien tai

            last_month = current_time - datetime.timedelta(
                number_days)  # neu khong co du lieu thi tinh tu 1000 ngay tu hien tai
            # tinh lui lai 1 month
            start_month = last_month.replace(day=1, hour=0, minute=0, second=0, microsecond=0)  # chuyen ve mung 1
            result_month_start = start_month - datetime.timedelta(days=2)
            start = result_month_start.replace(day=1, hour=0, minute=0, second=0, microsecond=0)
            current_time = current_time.replace(day=1, hour=0, minute=0, second=0, microsecond=0)

            while start < current_time:
                end_month = start.replace(day=28, hour=0, minute=0, second=0, microsecond=0)
                result_month_end = end_month + datetime.timedelta(days=5)
                end = result_month_end.replace(day=1, hour=0, minute=0, second=0, microsecond=0)
                try:
                    conditions = (db.data_day.station_id == station_id)
                    conditions &= (db.data_day.get_time >= start)
                    conditions &= (db.data_day.get_time < end)
                    data_days = db(conditions).select(orderby=db.data_day.get_time)
                    if data_days:
                        mon_data_calc(station_id, data_days, start)
                        db.commit()
                except Exception as ex:
                    traceback.print_exc()
                    logger.error(str(ex))
                start = end
            pass
        db.commit()
    except Exception as ex:
        traceback.print_exc()
        logger.error(str(ex))
    finally:
        logger.info('End calculate month data new')

    return


################################################################################
def calc_data_month_new():
    try:
        logger.info('Start calculate month data new')
        _, _, _, station_codes = get_station_dict()
        # lay danh sach time tinh cuoi cung cua data hour
        lastest_month = get_lastest_month_calcu()

        # vong lap
        for index, code in enumerate(station_codes):
            if not code:
                continue
            station_id = station_codes.get(code)
            if not station_id:
                continue
            last_month = lastest_month.get(station_id)
            current_time = datetime.datetime.now()
            if last_month:
                last_month = last_month  # month khac chut nen phai tinh lai cho dung
            else:
                last_month = current_time - datetime.timedelta(
                    days=365 * 3)  # neu khong co du lieu thi tinh tu 1000 ngay tu hien tai
            # tinh lui lai 1 month
            start_month = last_month.replace(day=1, hour=0, minute=0, second=0, microsecond=0)  # chuyen ve mung 1
            result_month_start = start_month - datetime.timedelta(days=2)
            start = result_month_start.replace(day=1, hour=0, minute=0, second=0, microsecond=0)
            current_time = current_time.replace(day=1, hour=0, minute=0, second=0, microsecond=0)

            while start < current_time:
                end_month = start.replace(day=28, hour=0, minute=0, second=0, microsecond=0)
                result_month_end = end_month + datetime.timedelta(days=5)
                end = result_month_end.replace(day=1, hour=0, minute=0, second=0, microsecond=0)
                try:
                    conditions = (db.data_day.station_id == station_id)
                    conditions &= (db.data_day.get_time >= start)
                    conditions &= (db.data_day.get_time < end)
                    data_days = db(conditions).select(orderby=db.data_day.get_time)
                    if data_days:
                        mon_data_calc(station_id, data_days, start)
                        db.commit()
                except Exception as ex:
                    traceback.print_exc()
                    logger.error(str(ex))
                start = end
            pass
        db.commit()
    except Exception as ex:
        traceback.print_exc()
        logger.error(str(ex))
    finally:
        logger.info('End calculate month data new')

    return


# hungdx end add issue 30

################################################################################
def station_process(station_id, number_days, station_logger, ftp):
    try:
        from_date = datetime.datetime.now() - datetime.timedelta(days=number_days)

        station_logger.info("-" * 80)
        station_logger.info("Start while true with station id = %s", station_id)

        while True:
            try:
                db._adapter.reconnect()

                # import ftplib
                count = 0  # dem nhung file duoc xu ly
                queue_station_list = []
                second_limit = 100  # Bien luu so giay gioi han de connect qua ftp voi moi station

                station_logger.info('-' * 80)
                station_names, _, _, station_ids, station_codes = get_station_dict_new_by_station_id(station_id)

                station_logger.info('#' * 100)
                station_logger.info('station_id : %s', station_id)
                station_logger.info('station_names : %s', station_names)
                station_logger.debug('station_ids : %s', station_ids)
                station_logger.debug('station_codes : %s', station_codes)

                # station_logger.info('ftp_station_info total: %s', ftp_station_info)
                # file cuoi + time cuoi cung get thanh cong

                lastest_files_dict, last_times = get_lastest_files_dict_new_by_station_id(station_id)
                # last_day = last_times.get(station_id)

                station_logger.debug('lastest_files_dict total: %s', lastest_files_dict)

                station_logger.info('last_times total: %s', last_times)

                # danh sach cac tram dang mat ket noi
                stations_off = get_station_off_log_by_station_id(station_id)

                # stations_off =[]
                # try:
                #     stations_off = db(db.station_off_log.end_off is None).select()
                # except Exception as ex:
                #     station_logger.info('stations_off error: ' + ex.message)

                # station_logger.info('stations_off total: ' + stations_off)

                # danh sach tat ca indicator va station_indicator dang duoc su dung
                station_indicator_dict, indicators, thresholds, preparing_dict, tendency_dict = get_indicator_station_info_by_station_id(
                    station_id)

                if not station_indicator_dict:
                    number_waiting = 5 * 60
                    station_logger.info("station_indicator_dict: null. Waiting %s min with station id = %s", number_waiting, station_id)
                    time.sleep(number_waiting)
                    continue

                if len(station_indicator_dict) <= 0:
                    number_waiting = 15 * 60
                    station_logger.info("station_indicator_dict: len <=0. Waiting %s min with station id = %s", number_waiting, station_id)
                    time.sleep(number_waiting)
                    continue

                station_logger.debug('station_indicator_dict total: %s', station_indicator_dict)

                # Lastest data dict with format : {station_id : {indicator : value, ...}, ...}
                lastest_data = get_all_data_lastest_by_station_id(station_id)

                station_logger.debug('lastest_data total: %s', lastest_data)

                # Get all station fpt info
                ftp_station_info = get_stations_ftp_load_update_by_station_id(station_id)

                if not ftp_station_info:
                    number_waiting = 15 * 60
                    station_logger.info("ftp_station_info: null. Waiting %s min with station id = %s", number_waiting, station_id)
                    time.sleep(number_waiting)
                    continue

                if len(ftp_station_info) <= 0:
                    number_waiting = 15 * 60
                    station_logger.info("ftp_station_info: len <= 0.Waiting %s min with station id = %s", number_waiting, station_id)
                    time.sleep(number_waiting)
                    continue

                station_logger.debug('ftp_station_info total: %s', ftp_station_info)

                file_mapping = ftp_station_info[5]

                station_logger.debug('file_mapping: %s', file_mapping)
                station_logger.debug('------> ip: %s', ftp_station_info[0].get(int(station_id)))
                station_logger.debug('------> ip: %s', ftp_station_info[0])

                # Get login info
                ip = ftp_station_info[0].get(int(station_id))
                data_folder = ftp_station_info[1].get(int(station_id))
                username = ftp_station_info[2].get(int(station_id))
                pwd = ftp_station_info[3].get(int(station_id))
                port = ftp_station_info[4].get(int(station_id))
                file_mapping_each_station = ftp_station_info[5].get(int(station_id))  # TriNT: Add

                scan_failed = int(ftp_station_info[6].get(int(station_id)))
                res_scan_failed = scan_failed

                retry_no = ftp_station_info[7].get(int(station_id))
                file_mapping2 = ftp_station_info[8].get(int(station_id))
                path_format = ftp_station_info[9].get(int(station_id))
                frequency_receiving_data = ftp_station_info[10].get(int(station_id))

                station_name = ftp_station_info[11].get(int(station_id))
                station_code = ftp_station_info[12].get(int(station_id))

                station_logger.debug('stations ip: %s', ip)
                station_logger.debug('stations id: : %s', station_id)
                station_logger.debug('stations name: : %s', station_name)
                station_logger.debug('stations code: : %s', station_code)
                station_logger.debug('stations data_folder: %s', data_folder)

                station_logger.debug('stations username:  %s', username)
                station_logger.debug('stations pwd:  %s', pwd)
                station_logger.debug('stations port:  %s', port)
                station_logger.info('path_format: %s', path_format)
                station_logger.debug('file_mapping_each_station: %s', file_mapping_each_station)  # TriNT: Add
                # station_logger.info('file_mapping: %s', file_mapping)  # TriNT: Add
                station_logger.debug('file_mapping2: %s', file_mapping2)
                station_logger.debug('scan_failed: %s', scan_failed)
                station_logger.debug('frequency_receiving_data: %s', frequency_receiving_data)

                # station_logger.info('stations file_mapping: ' + file_mapping)
                if not ip or not data_folder or not username:
                    number_waiting = 15 * 60
                    station_logger.info("Waiting %s min with station id = %s", number_waiting, station_id)
                    time.sleep(number_waiting)
                    continue

                try:
                    last_day = last_times.get(station_id)
                    if last_day:
                        last_day = last_day
                    else:
                        # Quet du lieu 3 nam
                        # last_day = datetime.datetime.now() - datetime.timedelta(days=3 * 365)
                        last_day = from_date
                        # last_day = datetime.datetime.now() - datetime.timedelta(days=1)
                except Exception as ex:
                    traceback.print_exc()
                    station_logger.error("Exception = %s", str(ex))
                    # last_day = datetime.datetime.now() - datetime.timedelta(days=3 * 365)
                    # last_day = datetime.datetime.now() - datetime.timedelta(days=1)
                    last_day = from_date

                station_logger.info('last_day : %s', last_day)
                station_logger.debug('path_format : %s', path_format)

                # path_format == 1 --> Du lieu 1 tram de het 1 thu muc
                if path_format == 1:
                    day_calculator_folder = ''
                    data_folder_current = data_folder + day_calculator_folder
                    data_folder_current = data_folder_current.replace('//', '/')
                    station_logger.info('data_folder_current = %s', data_folder_current)

                    retry = True

                    if not retry_no:
                        retry_no = 10
                    elif retry_no < 10:
                        retry_no = 10

                    count = 0

                    while retry:
                        count += 1
                        if count > retry_no:
                            # queue_station_list.append(station_id)

                            station_logger.info('station_id    : %s', station_id)
                            station_logger.debug('stations name: %s', station_name)
                            station_logger.error('FTP sung dot, da retry = %s', count)
                            station_logger.error('last_day = %s', last_day)
                            station_logger.error('data_folder_current = %s', data_folder_current)

                            retry = False
                            break

                        try:
                            station_logger.info("-" * 80)
                            station_logger.info("2. Go to data_folder_current to scan read file: %s",
                                                data_folder_current)
                            station_logger.info("Format type:  tat ca 1 thu muc = %s", path_format)

                            # station_logger.info("is_fpt_connected = %", is_fpt_connected)
                            # if not is_fpt_connected:

                            # station_logger.info("Create new FTP")

                            # ftp = ftplib.FTP(ip) # TriNT: Khi chay thay, thi phai bo rem
                            # ftp.connect(ip, port, second_limit) # TriNT: Khi chay thay, thi phai bo rem

                            # # Trint Can phai xoa------------------------------------------------
                            # ftp = ftplib.FTP('ftp.cem.gov.vn')  # TriNT: Khi chay thay, thi phai  rem
                            # ftp.connect('ftp.cem.gov.vn', 21, second_limit)  # TriNT: Khi chay thay, thi phai rem
                            # # Trint Can phai xoa------------------------------------------------

                            # # # # Trint Can phai xoa------------------------------------------------
                            # ftp = ftplib.FTP('113.160.218.8')  # TriNT: Khi chay thay, thi phai  rem
                            # ftp.connect('113.160.218.8', 21, second_limit)  # TriNT: Khi chay thay, thi phai rem
                            # # # Trint Can phai xoa------------------------------------------------

                            # ftp.login(username, pwd)

                            # is_fpt_connected = True
                            # else:
                            #     is_fpt_connected = True
                            #     station_logger.info("FTP Connected")

                            try:
                                # Keep FTP alive
                                station_logger.debug("Call ftp.voidcmd(NOOP): start ==> station name = %s", station_name)
                                ftp.voidcmd('NOOP')  # Send a 'NOOP' command every 30 seconds
                                station_logger.debug("Call ftp.voidcmd(NOOP): end ==> station name   = %s", station_name)
                            except Exception as ex:
                                station_logger.debug("Reconnect ftplib.FTP(ip): %s", ip)
                                station_logger.debug("Reconnect ftplib.FTP(ip): %s", port)
                                station_logger.debug("Reconnect ftplib.FTP(ip): %s", second_limit)

                                ftp = ftplib.FTP(ip)  # TriNT: Khi chay thay, thi phai bo rem
                                ftp.connect(ip, port, second_limit)  # TriNT: Khi chay thay, thi phai bo rem
                                ftp.login(username, pwd)

                            station_logger.debug("data_folder_current: %s", data_folder_current)
                            station_logger.debug("Call ftp.cwd(data_folder_current): start")

                            ftp.cwd(data_folder_current)

                            station_logger.info("2. Go to data_folder_current to read file: ok")

                            ftp.encoding = 'utf-8'
                            ftp.sendcmd('OPTS UTF8 ON')

                            station_logger.debug('data_folder_current = %s', data_folder_current)

                            station_logger.info("-" * 100)
                            # station_logger.info("2. start call process_data")
                            # station_logger.debug('thresholds = %s', thresholds)
                            try:
                                station_logger.info("2. Call process_data: start time = %s", datetime.datetime.now())

                                res, res_scan_failed = process_data(ftp, station_ids, count, lastest_files_dict,
                                                                    last_times,
                                                                    data_folder_current,
                                                                    station_indicator_dict, lastest_data, station_names,
                                                                    stations_off, thresholds, preparing_dict,
                                                                    tendency_dict,
                                                                    file_mapping,
                                                                    station_id, file_mapping2,
                                                                    file_mapping_each_station, last_day, station_code,
                                                                    station_name, station_logger, scan_failed)

                                station_logger.info("2. Call process_data: End time = %s", datetime.datetime.now())

                                station_logger.debug("Result call process_data: res = %s ; res_scan_failed = %s", res,
                                                     res_scan_failed)
                            except Exception as e:
                                traceback.print_exc()
                                station_logger.error('FTP Exception when call process_data = %s', e.message)

                            if res == 0:  # Doc thanh cong hoac da quet het
                                retry = False
                            else:  # if res > 0: Co su co xay ra
                                # Doi trong vong 2 giay, thi tien hanh thu lai
                                station_logger.debug("Waiting 1 min to retry scan file: current number retry = %s",
                                                     count)
                                # time.sleep(1*60)
                                time.sleep(1 * 10)
                        except Exception as ex:
                            traceback.print_exc()
                            station_logger.error('FTP Exception = %s', e.message)
                            # queue_station_list.append(station_id)
                        # finally:
                        #     try:
                        #         ftp.quit()
                        #     except Exception as ex:
                        #         station_logger.error('FTP.quit() have error: %', ex.message)
                else:
                    # last_day = today - timedelta(days=1000)
                    # path_format = 0 --> /tudong/hanam/hanam3/2019/04/16
                    # path_format = 1 --> Tat ca 1 thu muc

                    station_logger.info('path_format ' + str(path_format))
                    station_logger.debug('data_folder: %s', data_folder)
                    station_logger.debug('last_day: %s', last_day)

                    # timedelta(seconds = 33)
                    # timedelta(minute = 33)
                    # timedelta(days = 33)
                    # t = timedelta(days = 5, hours = 1, seconds = 33, microseconds = 233423)
                    # print("total seconds =", t.total_seconds())

                    today = datetime.datetime.now()

                    while last_day < today + datetime.timedelta(days=1):
                        # Build lai "data_folder" them nam/thang/ngay
                        day_calculator = last_day
                        if path_format == 0:
                            day_calculator_folder = '/%0.4d/%0.2d/%0.2d' % (day_calculator.year, day_calculator.month,
                                                                            day_calculator.day)
                        elif path_format == 2:
                            day_calculator_folder = '/%0.4d%0.2d%0.2d' % (day_calculator.year, day_calculator.month,
                                                                          day_calculator.day)
                        elif path_format == 3:
                            day_calculator_folder = '/%0.4d/Thang%0.2d/%0.4d%0.2d%0.2d' % (
                            day_calculator.year, day_calculator.month,
                            day_calculator.year, day_calculator.month,
                            day_calculator.day)
                        else:
                            day_calculator_folder = '/%0.4d/Thang%0.2d/Ngay%0.2d' % (
                            day_calculator.year, day_calculator.month,
                            day_calculator.day)

                        data_folder_current = data_folder + day_calculator_folder
                        data_folder_current = data_folder_current.replace('//',
                                                                          '/')  # loai bot dau /  (neu co 2 dau lien nhau)

                        # station_logger.info('data_folder_current: %s', data_folder_current)

                        retry = True

                        if not retry_no:
                            retry_no = 10
                        elif retry_no < 10:
                            retry_no = 10

                        count = 0

                        while retry:
                            count += 1
                            if count > retry_no:
                                # queue_station_list.append(station_id)

                                station_logger.info('station_id    : %s', station_id)
                                station_logger.debug('stations name: %s', station_name)
                                station_logger.error('FTP sung dot, da retry = %s', count)
                                station_logger.error('last_day = %s', last_day)
                                station_logger.error('data_folder_current = %s', data_folder_current)

                                retry = False
                                break

                            try:
                                station_logger.info("-" * 20)
                                station_logger.info("1. Go to data_folder_current to read file: %s",
                                                    data_folder_current)
                                #
                                # if not is_fpt_connected:
                                # station_logger.info("Create new FTP")

                                # ftp = ftplib.FTP(ip) # TriNT: Khi chay thay, thi phai bo rem
                                # ftp.connect(ip, port, second_limit) # TriNT: Khi chay thay, thi phai bo rem

                                # # Trint Can phai xoa------------------------------------------------
                                # ftp = ftplib.FTP('ftp.cem.gov.vn')  # TriNT: Khi chay thay, thi phai  rem
                                # ftp.connect('ftp.cem.gov.vn', 21, second_limit)  # TriNT: Khi chay thay, thi phai rem
                                # # Trint Can phai xoa------------------------------------------------
                                #
                                # # # # # Trint Can phai xoa------------------------------------------------
                                # # ftp = ftplib.FTP('113.160.218.8')  # TriNT: Khi chay thay, thi phai  rem
                                # # ftp.connect('113.160.218.8', 21, second_limit)  # TriNT: Khi chay thay, thi phai rem
                                # # # # # Trint Can phai xoa------------------------------------------------
                                #
                                # ftp.login(username, pwd)

                                # is_fpt_connected = True

                                # else:
                                #     # station_logger.info("Connected FTP")
                                #     is_fpt_connected = True

                                try:
                                    # Keep FTP alive
                                    station_logger.debug("Call ftp.voidcmd(NOOP): start ==> station name = %s", station_name)
                                    ftp.voidcmd('NOOP')  # Send a 'NOOP' command every 30 seconds
                                    station_logger.debug("Call ftp.voidcmd(NOOP): end ==> station name   = %s", station_name)
                                except Exception as ex:
                                    station_logger.debug("Reconnect ftplib.FTP(ip): %s", ip)
                                    station_logger.debug("Reconnect ftplib.FTP(ip): %s", port)
                                    station_logger.debug("Reconnect ftplib.FTP(ip): %s", second_limit)

                                    ftp = ftplib.FTP(ip)  # TriNT: Khi chay thay, thi phai bo rem
                                    ftp.connect(ip, port, second_limit)  # TriNT: Khi chay thay, thi phai bo rem
                                    ftp.login(username, pwd)

                                station_logger.debug("data_folder_current: %s", data_folder_current)
                                station_logger.debug("Call ftp.cwd(data_folder_current): start")

                                ftp.cwd(data_folder_current)

                                # station_logger.info("1. Go to data_folder_current to read file: ok")

                                ftp.encoding = 'utf-8'
                                ftp.sendcmd('OPTS UTF8 ON')

                                station_logger.info("-" * 80)
                                # station_logger.info('data_folder_current = %s', data_folder_current)
                                # station_logger.info("1. start call process_data")
                                # station_logger.debug('thresholds = %s', thresholds)
                                try:
                                    station_logger.info("1. Call process_data: start time = %s", datetime.datetime.now())

                                    res, res_scan_failed = process_data(ftp, station_ids, count, lastest_files_dict,
                                                                        last_times, data_folder_current,
                                                                        station_indicator_dict, lastest_data,
                                                                        station_names,
                                                                        stations_off, thresholds, preparing_dict,
                                                                        tendency_dict, file_mapping,
                                                                        station_id, file_mapping2,
                                                                        file_mapping_each_station, last_day,
                                                                        station_code, station_name, station_logger,
                                                                        scan_failed)

                                    station_logger.info("1. Call process_data: End time = %s", datetime.datetime.now())

                                    station_logger.debug("result call process_data: res = %s ; res_scan_failed = %s",
                                                         res, res_scan_failed)
                                except Exception as e:
                                    traceback.print_exc()
                                    station_logger.error('FTP Exception when call process_data = %s', e.message)

                                if res == 0:  # Doc thanh cong hoac da quet het
                                    retry = False
                                else:  # if res > 0: Co su co xay ra
                                    # Doi trong vong 5 giay, thi tien hanh thu lai
                                    station_logger.debug("Waiting 1 min to retry scan file: current number retry = %s",
                                                         count)
                                    lastest_files_dict, last_times = get_lastest_files_dict_new_by_station_id(
                                        station_id)
                                    last_day = last_times.get(station_id)
                                    time.sleep(1 * 60)
                            except Exception as e:
                                traceback.print_exc()
                                station_logger.error('FTP Exception = %s', e.message)
                                # queue_station_list.append(station_id)
                            # finally:
                            #     try:
                            #         ftp.quit()
                            #     except Exception as ex:
                            #         station_logger.error('FTP.quit() have error: %', ex.message)
                        # End While retry

                        last_day = last_day + datetime.timedelta(days=1)
                        # Start of a day
                        # last_day = last_day.replace(hour=0, minute=0, second=0, microsecond=0)

                # Update status cua station la "Mat ket noi"
                conditions = (db.stations.id == station_id)
                # conditions &= (db.stations.data_server == ip)
                # conditions &= (db.stations.data_folder == data_folder)
                station = db(conditions).select().first()

                lastest_files_dict, last_times = get_lastest_files_dict_new_by_station_id(station_id)

                lastest_file = lastest_files_dict.get(station_id)

                tmp_last_time_by_station = last_times.get(station_id)

                # lastest_files_dict, last_times = get_lastest_files_dict_new_by_station_id(station_id)
                #
                # tmp_last_time_by_station = get_last_time_by_station(station.id)

                # neu time cuoi + tan suat  + (khoang du di 5p) < hien tai --> thi mat ket noi

                is_disconnected = False
                check_time = None
                if frequency_receiving_data and tmp_last_time_by_station:
                    # check_time = last_day + datetime.timedelta(0, frequency_receiving_data) + datetime.timedelta(minutes = 5)
                    check_time = tmp_last_time_by_station + datetime.timedelta(
                        minutes=frequency_receiving_data) + datetime.timedelta(minutes=15)
                    if check_time < datetime.datetime.now():
                        is_disconnected = True
                else:  # 1 trong 2 la null
                    if tmp_last_time_by_station:  # tmp_last_time_by_station not Null, -->  frequency_receiving_data = null
                        check_time = tmp_last_time_by_station + datetime.timedelta(minutes=15)
                        if check_time < datetime.datetime.now():
                            is_disconnected = True
                        else:  # tmp_last_time_by_station = Null
                            is_disconnected = True

                station_logger.info('-' * 40)
                station_logger.info("1. Kiem tra co cap nhat trang thai mat ket noi hay khong")
                station_logger.info('station.id =%s', station.id)
                station_logger.info('station_name =%s', station_name)

                # lastest_files_dict, last_times = get_lastest_files_dict_new_by_station_id(station_id)
                lastest_file = lastest_files_dict.get(station_id)

                station_logger.info('lastest_file       : %s', lastest_file)

                station_logger.info("last_day           : %s", last_day)
                station_logger.info("check_time         : %s", check_time)
                station_logger.info("now()              : %s", datetime.datetime.now())
                station_logger.info("is_disconnected: %s", is_disconnected)

                if is_disconnected:
                    station_logger.info("Station code: %s is disconnected", station_name)

                    # station.status = 4 --> Mat ket noi
                    station_logger.info('station.id =%s', station.id)
                    station_logger.info('station.status (Mat ket noi = 4) =%s', station.status)
                    if station.status != 4:
                        station_logger.info("Set tram mat ket noi: station name = %s", station.id)
                        conditions = (db.stations.id == station_id)
                        try:
                            db(conditions).update(
                                status=4,
                                scan_failed=res_scan_failed + 1,
                                off_time=datetime.datetime.now()
                            )
                            db.commit()
                        except:
                            traceback.print_exc()
                            db.rollback()
                            try:
                                db(conditions).update(
                                    status=4,
                                    scan_failed=1,
                                    off_time=datetime.datetime.now()
                                )
                                db.commit()
                            except:
                                traceback.print_exc()
                                db.rollback()
                    else:
                        conditions = (db.stations.id == station_id)
                        try:
                            # db(conditions).update(
                            #     scan_failed=db.stations.scan_failed + 1,
                            # )
                            db(conditions).update(
                                scan_failed=res_scan_failed + 1,
                            )
                            db.commit()
                        except:
                            traceback.print_exc()
                            db.rollback()
                            try:
                                db(conditions).update(
                                    scan_failed=1,
                                )
                                db.commit()
                            except:
                                traceback.print_exc()
                                db.rollback()
                        # 2. Update station_off_log
                    if scan_failed + 1 == retry_no:
                        try:
                            db.station_off_log.insert(
                                station_id=str(station.id),
                                station_name=station.station_name,
                                province_id=station.province_id,
                                station_type=station.station_type,
                                start_off=datetime.datetime.now(),
                            )
                            db.commit()
                            station_logger.info("Cap nhat thanh cong station_off_log voi station name = %s",
                                                station_name)
                            station_logger.info("Cap nhat thanh cong station_off_log voi station id = %s", station.id)
                        except:
                            traceback.print_exc()
                            db.rollback()
                else:
                    station_logger.info("No update station status")
                # Reconnect for station on queue_station_list
                # station_logger.info('retry queue_station_list')
                # for s_code in queue_station_list:
                #     ip = ftp_station_info[0].get(s_code)
                #     data_folder = ftp_station_info[1].get(s_code)
                #     username = ftp_station_info[2].get(s_code)
                #     pwd = ftp_station_info[3].get(s_code)
                #     port = ftp_station_info[4].get(s_code)
                #     path_format = ftp_station_info[9].get(s_code)
                #
                #     station_id = station_codes.get(s_code)
                #     today = datetime.datetime.now()
                #     last_day = today - timedelta(days=1000)
                #     # try:
                #     #     last_day = last_times.get(station_id)
                #     # except Exception as ex:
                #     #     station_logger.error(str(ex))
                #     #     last_day = today - timedelta(days=1000)
                #
                #     while last_day < today + timedelta(days=1):
                #         # Build lai "data_folder" them nam/thang/ngay
                #         day_calculator = last_day
                #         if path_format == 0:
                #             day_calculator_folder = '/%0.4d/%0.2d/%0.2d' % (day_calculator.year, day_calculator.month,
                #                                                             day_calculator.day)
                #         elif path_format == 1:
                #             day_calculator_folder = '/%0.4d%0.2d%0.2d' % (day_calculator.year, day_calculator.month,
                #                                                           day_calculator.day)
                #         elif path_format == 2:
                #             day_calculator_folder = '/%0.4d' % day_calculator.year
                #
                #         elif path_format == 3:
                #             day_calculator_folder = '/%0.4d/%0.2d/%0.2d' % (day_calculator.year, day_calculator.month,
                #                                                             day_calculator.day)
                #         else:
                #             day_calculator_folder = '/%0.4d/%0.2d/%0.2d' % (day_calculator.year, day_calculator.month,
                #                                                             day_calculator.day)
                #
                #         data_folder_current = data_folder + day_calculator_folder
                #         data_folder_current = data_folder_current.replace('//', '/')  # loai bot dau /  (neu co 2 dau lien nhau)
                #
                #         station_logger.info(data_folder_current)
                #         if ip and username and pwd:
                #             retry = True
                #             while retry:
                #                 try:
                #                     ftp = ftplib.FTP()
                #                     ftp.connect(ip, port, second_limit)
                #                     ftp.login(username, pwd)
                #                     ftp.cwd(data_folder_current)
                #                     ftp.encoding = 'utf-8'
                #                     ftp.sendcmd('OPTS UTF8 ON')
                #                     service_load_update.process_data(ftp, station_codes, count, lastest_files_dict, data_folder_current,
                #                                          station_indicator_dict, lastest_data, station_names,
                #                                          stations_off, thresholds, preparing_dict, tendency_dict, file_mapping, s_code)
                #                     retry = False
                #                     continue
                #                 except Exception as e:
                #                     station_logger.error('Error {}'.format(e.message))
                #                     retry = False
                #                     continue
                #         last_day = last_day + timedelta(days=1)
                #         pass
                # db._adapter.close()
            except Exception as e:
                traceback.print_exc()
                station_logger.error('Exception = %s', e.message)

            number_waiting = 1 * 60
            if frequency_receiving_data:
                number_waiting = frequency_receiving_data * 60

            try:
                db._adapter.close()
            except Exception as ex:
                station_logger.error("db._adapter.close() have error = %s", ex.message)

            station_logger.info("Waiting %s min with station id = %s", number_waiting, station_id)
            time.sleep(number_waiting)

        # End True
    except Exception as ex:
        traceback.print_exc()
        station_logger.error("station_process have exception: %s", ex.message)
    finally:
        try:
            db._adapter.close()
        except Exception as ex:
            station_logger.error("db._adapter.close() have error = %s", ex.message)


################################################################################
################################################################################
def station_process_all(station_id, from_day, to_date, station_logger, ftp):
    try:
        station_logger.info("-" * 80)
        station_logger.info("Start while true with station id = %s", station_id)

        db._adapter.reconnect()
        is_fpt_connected = False

        try:
            # import ftplib
            count = 0  # dem nhung file duoc xu ly
            queue_station_list = []
            second_limit = 10  # Bien luu so giay gioi han de connect qua ftp voi moi station

            station_logger.info('-' * 80)
            station_names, _, _, station_ids, station_codes = get_station_dict_new_by_station_id(station_id)

            station_logger.info('#' * 100)
            station_logger.info('station_id : %s', station_id)
            station_logger.info('station_names : %s', station_names)
            station_logger.debug('station_ids : %s', station_ids)
            station_logger.debug('station_codes : %s', station_codes)

            # station_logger.info('ftp_station_info total: %s', ftp_station_info)
            # file cuoi + time cuoi cung get thanh cong

            lastest_files_dict, last_times = get_lastest_files_dict_new_by_station_id(station_id)
            station_logger.debug('lastest_files_dict total: %s', lastest_files_dict)

            station_logger.info('last_times total: %s', last_times)

            # danh sach cac tram dang mat ket noi
            stations_off = get_station_off_log_by_station_id(station_id)

            # stations_off =[]
            # try:
            #     stations_off = db(db.station_off_log.end_off is None).select()
            # except Exception as ex:
            #     station_logger.info('stations_off error: ' + ex.message)

            # station_logger.info('stations_off total: ' + stations_off)

            # danh sach tat ca indicator va station_indicator dang duoc su dung
            station_indicator_dict, indicators, thresholds, preparing_dict, tendency_dict = get_indicator_station_info_by_station_id(
                station_id)

            station_logger.debug('station_indicator_dict total: %s', station_indicator_dict)

            # Lastest data dict with format : {station_id : {indicator : value, ...}, ...}
            lastest_data = get_all_data_lastest_by_station_id(station_id)

            station_logger.debug('lastest_data total: %s', lastest_data)

            # Get all station fpt info
            ftp_station_info = get_stations_ftp_load_update_by_station_id(station_id)

            station_logger.debug('ftp_station_info total: %s', ftp_station_info)

            file_mapping = ftp_station_info[5]
            station_logger.debug('file_mapping: %s', file_mapping)
            station_logger.debug('------> ip: %s', ftp_station_info[0].get(int(station_id)))
            station_logger.debug('------> ip: %s', ftp_station_info[0])

            # Get login info
            ip = ftp_station_info[0].get(int(station_id))
            data_folder = ftp_station_info[1].get(int(station_id))
            username = ftp_station_info[2].get(int(station_id))
            pwd = ftp_station_info[3].get(int(station_id))
            port = ftp_station_info[4].get(int(station_id))
            file_mapping_each_station = ftp_station_info[5].get(int(station_id))  # TriNT: Add

            scan_failed = int(ftp_station_info[6].get(int(station_id)))
            res_scan_failed = scan_failed
            retry_no = ftp_station_info[7].get(int(station_id))
            file_mapping2 = ftp_station_info[8].get(int(station_id))
            path_format = ftp_station_info[9].get(int(station_id))
            frequency_receiving_data = ftp_station_info[10].get(int(station_id))

            station_name = ftp_station_info[11].get(int(station_id))
            station_code = ftp_station_info[12].get(int(station_id))

            station_logger.debug('stations ip: %s', ip)
            station_logger.debug('stations id: : %s', station_id)
            station_logger.debug('stations name: : %s', station_name)
            station_logger.debug('stations code: : %s', station_code)
            station_logger.debug('stations data_folder: %s', data_folder)

            station_logger.debug('stations username:  %s', username)
            station_logger.debug('stations pwd:  %s', pwd)
            station_logger.debug('stations port:  %s', port)
            station_logger.info('path_format: %s', path_format)
            station_logger.debug('file_mapping_each_station: %s', file_mapping_each_station)  # TriNT: Add
            # station_logger.info('file_mapping: %s', file_mapping)  # TriNT: Add
            station_logger.debug('file_mapping2: %s', file_mapping2)
            station_logger.debug('scan_failed: %s', scan_failed)
            station_logger.debug('frequency_receiving_data: %s', frequency_receiving_data)

            # station_logger.info('stations file_mapping: ' + file_mapping)
            if not ip or not data_folder or not username:
                return ''

            last_day = from_day
            station_logger.info('last_day : %s', last_day)
            station_logger.debug('path_format : %s', path_format)

            # path_format == 1 --> Du lieu 1 tram de het 1 thu muc
            if path_format == 1:
                day_calculator_folder = ''
                data_folder_current = data_folder + day_calculator_folder
                data_folder_current = data_folder_current.replace('//', '/')
                station_logger.info('data_folder_current = %s', data_folder_current)

                retry = True

                if not retry_no:
                    retry_no = 10
                elif retry_no < 10:
                    retry_no = 10

                count = 0

                while retry:
                    count += 1
                    if count > retry_no:
                        # queue_station_list.append(station_id)

                        station_logger.info('station_id    : %s', station_id)
                        station_logger.debug('stations name: %s', station_name)
                        station_logger.error('FTP sung dot, da retry = %s', count)
                        station_logger.error('last_day = %s', last_day)
                        station_logger.error('data_folder_current = %s', data_folder_current)

                        retry = False
                        break

                    try:
                        station_logger.info("-" * 80)
                        station_logger.info("2. Go to data_folder_current to read file: %s", data_folder_current)
                        station_logger.info("Format type:  tat ca 1 thu muc = %s", path_format)
                        station_logger.info("is_fpt_connected = %", is_fpt_connected)
                        # if not is_fpt_connected:
                        #     station_logger.info("Create new FTP")

                        # ftp = ftplib.FTP(ip) # TriNT: Khi chay thay, thi phai bo rem
                        # ftp.connect(ip, port, second_limit) # TriNT: Khi chay thay, thi phai bo rem

                        # # # Trint Can phai xoa------------------------------------------------
                        # ftp = ftplib.FTP('ftp.cem.gov.vn')  # TriNT: Khi chay thay, thi phai  rem
                        # ftp.connect('ftp.cem.gov.vn', 21, second_limit)  # TriNT: Khi chay thay, thi phai rem
                        # # Trint Can phai xoa------------------------------------------------
                        #
                        # # # # Trint Can phai xoa------------------------------------------------
                        # # ftp = ftplib.FTP('113.160.218.8')  # TriNT: Khi chay thay, thi phai  rem
                        # # ftp.connect('113.160.218.8', 21, second_limit)  # TriNT: Khi chay thay, thi phai rem
                        # # # Trint Can phai xoa------------------------------------------------
                        #
                        # ftp.login(username, pwd)

                        #     is_fpt_connected = True
                        # else:
                        #     is_fpt_connected = True
                        #     station_logger.info("FTP Connected")

                        try:
                            # Keep FTP alive
                            station_logger.debug("Call ftp.voidcmd(NOOP): start ==> station name = %s", station_name)
                            ftp.voidcmd('NOOP')  # Send a 'NOOP' command every 30 seconds
                            station_logger.debug("Call ftp.voidcmd(NOOP): end ==> station name   = %s", station_name)
                        except Exception as ex:
                            station_logger.debug("Reconnect ftplib.FTP(ip): %s", ip)
                            station_logger.debug("Reconnect ftplib.FTP(ip): %s", port)
                            station_logger.debug("Reconnect ftplib.FTP(ip): %s", second_limit)

                            ftp = ftplib.FTP(ip)  # TriNT: Khi chay thay, thi phai bo rem
                            ftp.connect(ip, port, second_limit)  # TriNT: Khi chay thay, thi phai bo rem
                            ftp.login(username, pwd)

                        station_logger.debug("data_folder_current: %s", data_folder_current)
                        station_logger.debug("Call ftp.cwd(data_folder_current): start")

                        ftp.cwd(data_folder_current)

                        station_logger.info("2. Go to data_folder_current to read file: ok")

                        ftp.encoding = 'utf-8'
                        ftp.sendcmd('OPTS UTF8 ON')

                        station_logger.debug('data_folder_current = %s', data_folder_current)

                        station_logger.info("-" * 100)
                        # station_logger.info("2. start call process_data")
                        # station_logger.debug('thresholds = %s', thresholds)
                        try:
                            station_logger.info("2. Call process_data: start time = %s", datetime.datetime.now())

                            res, res_scan_failed = process_data(ftp, station_ids, count, lastest_files_dict, last_times,
                                                                data_folder_current,
                                                                station_indicator_dict, lastest_data, station_names,
                                                                stations_off, thresholds, preparing_dict, tendency_dict,
                                                                file_mapping,
                                                                station_id, file_mapping2, file_mapping_each_station,
                                                                last_day, station_code, station_name, station_logger,
                                                                scan_failed)

                            station_logger.info("2. Call process_data: End time = %s", datetime.datetime.now())

                            station_logger.debug("result call process_data: res = %s ; res_scan_failed = %s", res,
                                                 res_scan_failed)
                        except Exception as e:
                            traceback.print_exc()
                            station_logger.error('FTP Exception when call process_data = %s', e.message)

                        if res == 0:  # Doc thanh cong hoac da quet het
                            retry = False
                        else:  # if res > 0: Co su co xay ra
                            # Doi trong vong 5 giay, thi tien hanh thu lai
                            station_logger.debug("Waiting 1 min to retry scan file: current number retry = %s", count)
                            time.sleep(1 * 60)
                    except Exception as e:
                        traceback.print_exc()
                        station_logger.error('FTP Exception = %s', e.message)
                        # queue_station_list.append(station_id)
                    # finally:
                    #     try:
                    #         ftp.quit()
                    #     except Exception as ex:
                    #         station_logger.error('FTP.quit() have error: %', ex.message)
            else:
                # last_day = today - timedelta(days=1000)
                # path_format = 0 --> /tudong/hanam/hanam3/2019/04/16
                # path_format = 1 --> Tat ca 1 thu muc

                station_logger.info('path_format ' + str(path_format))
                station_logger.debug('data_folder: %s', data_folder)
                station_logger.debug('last_day: %s', last_day)

                # timedelta(seconds = 33)
                # timedelta(minute = 33)
                # timedelta(days = 33)
                # t = timedelta(days = 5, hours = 1, seconds = 33, microseconds = 233423)
                # print("total seconds =", t.total_seconds())

                while last_day < to_date + datetime.timedelta(days=1):
                    # Build lai "data_folder" them nam/thang/ngay
                    day_calculator = last_day
                    if path_format == 0:
                        day_calculator_folder = '/%0.4d/%0.2d/%0.2d' % (day_calculator.year, day_calculator.month,
                                                                        day_calculator.day)
                    elif path_format == 2:
                        day_calculator_folder = '/%0.4d%0.2d%0.2d' % (day_calculator.year, day_calculator.month,
                                                                      day_calculator.day)
                    elif path_format == 3:
                        day_calculator_folder = '/%0.4d/Thang%0.2d/%0.4d%0.2d%0.2d' % (
                        day_calculator.year, day_calculator.month,
                        day_calculator.year, day_calculator.month,
                        day_calculator.day)
                    else:
                        day_calculator_folder = '/%0.4d/Thang%0.2d/Ngay%0.2d' % (
                        day_calculator.year, day_calculator.month,
                        day_calculator.day)

                    data_folder_current = data_folder + day_calculator_folder
                    data_folder_current = data_folder_current.replace('//',
                                                                      '/')  # loai bot dau /  (neu co 2 dau lien nhau)

                    # station_logger.info('data_folder_current: %s', data_folder_current)

                    retry = True

                    if not retry_no:
                        retry_no = 5
                    elif retry_no < 5:
                        retry_no = 5

                    count = 0

                    while retry:
                        try:
                            station_logger.info("-" * 20)
                            station_logger.info("1. Go to data_folder_current to read file: %s", data_folder_current)

                            # if not is_fpt_connected:
                            # station_logger.info("Create new FTP")

                            # ftp = ftplib.FTP(ip) # TriNT: Khi chay thay, thi phai bo rem
                            # ftp.connect(ip, port, second_limit) # TriNT: Khi chay thay, thi phai bo rem

                            # # # Trint Can phai xoa------------------------------------------------
                            # ftp = ftplib.FTP('ftp.cem.gov.vn')  # TriNT: Khi chay thay, thi phai  rem
                            # ftp.connect('ftp.cem.gov.vn', 21, second_limit)  # TriNT: Khi chay thay, thi phai rem
                            # # Trint Can phai xoa------------------------------------------------
                            #
                            # # # # Trint Can phai xoa------------------------------------------------
                            # # ftp = ftplib.FTP('113.160.218.8')  # TriNT: Khi chay thay, thi phai  rem
                            # # ftp.connect('113.160.218.8', 21, second_limit)  # TriNT: Khi chay thay, thi phai rem
                            # # # # Trint Can phai xoa------------------------------------------------
                            #
                            # ftp.login(username, pwd)

                            # is_fpt_connected = True
                            # else:
                            #     # station_logger.info("Connected FTP")
                            #     is_fpt_connected = True

                            try:
                                # Keep FTP alive
                                station_logger.debug("Call ftp.voidcmd(NOOP): start ==> station name = %s", station_name)
                                ftp.voidcmd('NOOP')  # Send a 'NOOP' command every 30 seconds
                                station_logger.debug("Call ftp.voidcmd(NOOP): end ==> station name   = %s", station_name)
                            except Exception as ex:
                                station_logger.debug("Reconnect ftplib.FTP(ip): %s", ip)
                                station_logger.debug("Reconnect ftplib.FTP(ip): %s", port)
                                station_logger.debug("Reconnect ftplib.FTP(ip): %s", second_limit)

                                ftp = ftplib.FTP(ip)  # TriNT: Khi chay thay, thi phai bo rem
                                ftp.connect(ip, port, second_limit)  # TriNT: Khi chay thay, thi phai bo rem
                                ftp.login(username, pwd)

                            station_logger.debug("data_folder_current: %s", data_folder_current)
                            station_logger.debug("Call ftp.cwd(data_folder_current): start")

                            ftp.cwd(data_folder_current)

                            # station_logger.info("1. Go to data_folder_current to read file: ok")

                            ftp.encoding = 'utf-8'
                            ftp.sendcmd('OPTS UTF8 ON')

                            station_logger.info("-" * 80)
                            # station_logger.info('data_folder_current = %s', data_folder_current)
                            # station_logger.info("1. start call process_data")
                            # station_logger.debug('thresholds = %s', thresholds)
                            try:
                                station_logger.info("1. Call process_data: start time = %s", datetime.datetime.now())

                                res, res_scan_failed = process_data(ftp, station_ids, count, lastest_files_dict,
                                                                    last_times, data_folder_current,
                                                                    station_indicator_dict, lastest_data, station_names,
                                                                    stations_off, thresholds, preparing_dict,
                                                                    tendency_dict, file_mapping,
                                                                    station_id, file_mapping2,
                                                                    file_mapping_each_station, last_day, station_code,
                                                                    station_name, station_logger, scan_failed)
                                station_logger.info("1. Call process_data: End time = %s", datetime.datetime.now())

                                station_logger.debug("result call process_data: res = %s ; res_scan_failed = %s", res,
                                                     res_scan_failed)
                            except Exception as e:
                                traceback.print_exc()
                                station_logger.error('FTP Exception when call process_data = %s', e.message)

                            if res == 0:  # Doc thanh cong hoac da quet het
                                retry = False
                            else:  # if res > 0: Co su co xay ra
                                # Doi trong vong 5 giay, thi tien hanh thu lai
                                station_logger.debug("Waiting 1 min to retry scan file: current number retry = %s",
                                                     count)
                                time.sleep(1 * 60)  # number of seconds

                        except Exception as e:
                            traceback.print_exc()
                            station_logger.error('FTP Exception = %s', e.message)
                            # queue_station_list.append(station_id)
                        # finally:
                        #     try:
                        #         ftp.quit()
                        #     except Exception as ex:
                        #         station_logger.error('FTP.quit() have error: %', ex.message)

                    last_day = last_day + datetime.timedelta(days=1)
                    # Start of a day
                    # last_day = last_day.replace(hour=0, minute=0, second=0, microsecond=0)
        except Exception as e:
            traceback.print_exc()
            station_logger.error('Exception = %s', e.message)
    finally:
        db._adapter.close()


# Lay list cac chi so PM 10, PM2.5 sau 12h tinh tu thoi diem lay
def get_list_log_after_12h(station_id, indicator, time):
    try:
        aaData = []  # Du lieu json se tra ve

        conditions = (db.data_hour.id > 0)
        conditions &= (db.data_hour.station_id == station_id)
        if time:
            time_delta = time - datetime.timedelta(hours=11)
            conditions &= (db.data_hour.get_time >= time_delta)
            conditions &= (db.data_hour.get_time <= time)

        list_data = db(conditions).select(orderby=~db.data_hour.get_time)

        # Thu tu ban ghi
        iRow = 1
        # Duyet tung phan tu trong mang du lieu vua truy van duoc
        for i, item in enumerate(list_data):
            row = []
            added_item = dict()
            i_name = indicator
            i_name_decode = i_name.decode('utf-8')
            v = item.data[indicator] if item.data.has_key(indicator) else ''
            if v == '':
                added_item[i_name] = 0
            else:
                v = float(v)
                added_item[i_name] = float(v)
            if added_item.has_key(i_name):
                aaData.append(added_item[i_name])
        return aaData
    except Exception as ex:
        traceback.print_exc()
        return 0


def getTruncatedPollutantConcentrationBaseOnPollutant(pollutant, concentration):
    if (pollutant == 'PM-10'):
        return float(concentration * 100 / 150);

    if (pollutant == 'PM-2-5'):
        return float(concentration * 100 / 50);


def getWeightFactor(indicator, data):
    maxConcentration = float('-inf')
    minConcentration = float('inf')

    for i in data:
        if (i < 0):
            continue
        else:
            if (i > maxConcentration):
                maxConcentration = i;
            if (i < minConcentration):
                minConcentration = i

    range = maxConcentration - minConcentration
    weightFactor = float(minConcentration) / float(maxConcentration)
    if weightFactor <= float(1) / 2:
        weightFactor = float(1) / 2
    return weightFactor


def isValidNowcastData(data):
    missingData = 0;
    x = range(0, 2)
    for i in x:
        if (data[i] < 0):
            missingData = missingData + 1
    return missingData


def truncateConcentration(pollutant, data):
    if (isValidNowcastData(data) > 1):
        return 0
    weight = getWeightFactor(pollutant, data);
    totalConcentrationWithWeight = 0;
    totalWeight = 0;

    indexDataSlot = 3
    numberItem = 0
    totalConcentration = 0
    if weight > 0.5:
        for item in data:
            if item < 0:
                continue;
            else:
                totalConcentrationWithWeight += item * math.pow(weight, numberItem)
                totalWeight += math.pow(weight, numberItem)
            numberItem = numberItem + 1
        totalConcentration = totalConcentrationWithWeight / totalWeight
    else:
        for item in (data):

            if item < 0:
                continue;
            totalConcentrationWithWeight += item * math.pow(0.5, numberItem + 1)
            numberItem = numberItem + 1

        totalConcentration = totalConcentrationWithWeight
    return getTruncatedPollutantConcentrationBaseOnPollutant(pollutant, totalConcentration)


def getNowcastConcentration(pollutant, data):
    # if isValidNowcastData(data) :
    #     return -1;
    return truncateConcentration(pollutant, data)


################################################################################
def calc_aqi_data_hour(start=datetime.datetime.now()):
    try:
        logger.info('Start calculate AQI data hour')

        # Start of day
        start = start.replace(hour=0, minute=0, second=0, microsecond=0)

        # Chi loai station_type = 3, 4 and is_qi = True
        conditions = (db.stations.station_type.belongs(
            [STATION_TYPE['AMBIENT_AIR']['value'], STATION_TYPE['STACK_EMISSION']['value']]))
        conditions &= (db.stations.is_qi == True)
        ambients = db(conditions).select(db.stations.id)
        ambients = [str(station.id) for station in ambients]

        # Get data from 'data_hour' tu cac station o tren de tinh toan
        conditions = (db.data_hour.station_id.belongs(ambients))
        conditions &= (db.data_hour.get_time >= start)
        data_hours = db(conditions).select(orderby=db.data_hour.station_id | db.data_hour.get_time)

        # Lay cac chi so qui chuan cua cac indicator
        qc = db(db.aqi_indicators.id > 0).select(db.aqi_indicators.indicator, db.aqi_indicators.qc_1h)
        qc_dict = dict()
        for item in qc:
            qc_dict[item.indicator] = item.qc_1h

        for item in data_hours:
            data = {'aqi': None}  # du lieu AQI se insert/update vao bang 'aqi_data_hour'
            hour_data = item.data

            # Tinh toan gtri AQI cho tung indicator (dc dinh nghia truoc trong qc_dict)
            for indicator in hour_data.keys():
                # print(indicator)
                # Chi lay nhung chi so AQI
                if qc_dict.has_key(indicator):
                    # Ko tinh toan AQI 1h cho cac chi so ko co gtri qui chuan (PM10, Pb)
                    if qc_dict[indicator]:
                        # print(indicator)
                        if (indicator == 'PM-10'):
                            get_time = item.get_time.replace(minute=0, second=0,
                                                             microsecond=0)  # Chuan hoa : cat minute, second ve 0
                            # if ((item.station_id) == '28560877461938780203765592307') :
                            #     print(get_time)
                            dataAfter12h = get_list_log_after_12h(str(item.station_id), indicator, get_time);
                            # if ((item.station_id) == '28560877461938780203765592307') :
                            #     print(dataAfter12h)
                            # print(get_time)
                            aqi = getNowcastConcentration(indicator, dataAfter12h)
                            data[indicator] = aqi
                        elif (indicator == 'PM-2-5'):
                            get_time = item.get_time.replace(minute=0, second=0, microsecond=0)
                            dataAfter12h = get_list_log_after_12h(str(item.station_id), indicator, get_time);
                            aqi = getNowcastConcentration(indicator, dataAfter12h)
                            data[indicator] = aqi
                        else:
                            aqi = hour_data[indicator] / qc_dict[
                                indicator] * 100  # Theo cong thuc tinh AQI cho tung chi so
                            data[indicator] = aqi
                        # So sanh voi chi so AQI chung tong the
                        if data['aqi'] < aqi: data['aqi'] = aqi
            # Neu co du lieu thi insert/update bang 'aqi_data_hour'
            if data['aqi']:
                get_time = item.get_time.replace(minute=0, second=0,
                                                 microsecond=0)  # Chuan hoa : cat minute, second ve 0
                try:
                    db.aqi_data_hour.update_or_insert(
                        (db.aqi_data_hour.station_id == item.station_id) & (db.aqi_data_hour.get_time == get_time),
                        station_id=item.station_id,
                        get_time=get_time,
                        data=data
                    )
                    db.commit()  # Luu data vao db ngay sau khi xu ly moi tram
                except:
                    traceback.print_exc()
                    db.rollback()
                try:
                    # Update AQI cho station
                    db(db.stations.id == item.station_id).update(qi=data['aqi'], qi_time=get_time)
                    db.commit()  # Luu data vao db ngay sau khi xu ly moi tram
                except:
                    traceback.print_exc()
                    db.rollback()
        db.commit()
    except Exception as ex:
        traceback.print_exc()
        logger.error(str(ex))
    finally:
        logger.info('End calculate AQI data hour')
    return


# Lay max api day cac chi so PM
def get_max_day_aqi_pm(station_id, indicator, time):
    try:
        aaData = []  # Du lieu json se tra ve

        conditions = (db.aqi_data_hour.id > 0)
        conditions &= (db.aqi_data_hour.station_id == station_id)
        if time:
            time_delta = time + datetime.timedelta(hours=23)
            conditions &= (db.aqi_data_hour.get_time >= time)
            conditions &= (db.aqi_data_hour.get_time <= time_delta)

        list_data = db(conditions).select(orderby=~db.aqi_data_hour.get_time)

        # Thu tu ban ghi
        iRow = 1
        # Duyet tung phan tu trong mang du lieu vua truy van duoc
        if list_data:
            for i, item in enumerate(list_data):
                row = []
                added_item = dict()
                i_name = indicator
                i_name_decode = i_name.decode('utf-8')
                v = item.data[indicator] if item.data.has_key(indicator) else ''
                if v == '':
                    added_item[i_name] = 0
                else:
                    v = float(v)
                    added_item[i_name] = float(v)
                if added_item.has_key(i_name):
                    aaData.append(added_item[i_name])
        max_day_api = max(aaData)

        return max_day_api
    except Exception as ex:
        traceback.print_exc()
        return 0


################################################################################
def calc_aqi_data_24h(start=datetime.datetime.now()):
    try:
        logger.info('Start calculate AQI data day')

        # Start of day
        start = start.replace(hour=0, minute=0, second=0, microsecond=0)
        currentStart = datetime.datetime.now();
        currentStart = currentStart.replace(hour=0, minute=0, second=0, microsecond=0)

        # Xu ly fix khong cho tinh ngay hien tai
        if (start == currentStart):
            start = start.replace(hour=0, minute=0, second=0, microsecond=0) - datetime.timedelta(days=1)

        # Chi loai station_type = 4 and is_qi = True
        conditions = (db.stations.station_type.belongs(
            [STATION_TYPE['AMBIENT_AIR']['value'], STATION_TYPE['STACK_EMISSION']['value']]))
        conditions &= (db.stations.is_qi == True)
        ambients = db(conditions).select(db.stations.id)
        ambients = [str(station.id) for station in ambients]

        # Get data from 'data_day' tu cac station o tren de tinh toan
        conditions = (db.data_day.station_id.belongs(ambients))
        conditions &= (db.data_day.get_time >= start)
        conditions &= (db.data_day.get_time < currentStart)
        data_days = db(conditions).select(orderby=db.data_day.station_id | db.data_day.get_time)

        # Lay cac chi so qui chuan cua cac indicator
        qc = db(db.aqi_indicators.id > 0).select(db.aqi_indicators.indicator, db.aqi_indicators.qc_1h,
                                                 db.aqi_indicators.qc_24h)
        qc_dict_1h = dict()
        qc_dict_24h = dict()
        for item in qc:
            qc_dict_1h[item.indicator] = item.qc_1h
            qc_dict_24h[item.indicator] = item.qc_24h

        for item in data_days:
            data_24h = {'aqi': None}  # du lieu AQI se insert/update vao bang 'aqi_data_24h'
            data_1d = {'aqi': None}  # du lieu AQI se insert/update vao bang 'aqi_data_24h'
            day_data = item.data  # Du lieu quan trac trung binh 1 ngay cua thong so = SUM/count
            max_data = item.data_max

            # Tinh toan gtri AQI cho tung indicator (dc dinh nghia truoc trong qc_dict)
            for indicator in day_data.keys():
                # Chi lay nhung chi so AQI
                if qc_dict_24h.has_key(indicator):
                    # Ko tinh toan AQI 24h cho chi so ko co gtri qui chuan hoac O3
                    if qc_dict_24h[indicator] and indicator not in ['O3', 'CO']:
                        aqi = day_data[indicator] / qc_dict_24h[
                            indicator] * 100  # Theo cong thuc tinh AQI cho tung chi so
                        data_24h[indicator] = aqi

                        # So sanh voi chi so AQI chung tong the
                        if data_24h['aqi'] < aqi: data_24h['aqi'] = aqi

            # Neu co du lieu thi insert/update bang 'aqi_data_24h'
            if data_24h['aqi']:
                # So sanh du lieu AQI_24h vua tinh duoc voi gtri max cua AQI_1h de lay gtri AQI_1d
                keys = data_24h.keys()
                keys.remove('aqi')
                for indicator in keys:
                    get_time = datetime.datetime.fromordinal(item.get_time.toordinal())
                    if (indicator == 'PM-10'):
                        aqi_max_indicator = get_max_day_aqi_pm(str(item.station_id), indicator, get_time);
                        data_1d[indicator] = aqi_max_indicator if aqi_max_indicator > data_24h[indicator] else data_24h[
                            indicator]
                    elif (indicator == 'PM-2-5'):
                        aqi_max_indicator = get_max_day_aqi_pm(str(item.station_id), indicator, get_time);
                        data_1d[indicator] = aqi_max_indicator if aqi_max_indicator > data_24h[indicator] else data_24h[
                            indicator]
                    else:
                        aqi_max_indicator = max_data[indicator] / qc_dict_1h[indicator] * 100 if qc_dict_1h[
                            indicator] else 0
                        data_1d[indicator] = aqi_max_indicator if aqi_max_indicator > data_24h[indicator] else data_24h[
                            indicator]

                    # Gtri AQI_1d chung cua tram
                    if data_1d['aqi'] < data_1d[indicator]:
                        data_1d['aqi'] = data_1d[indicator]

                # Do qui dinh : AQI_1d cua O3 = max (AQI_1h cua O3)
                if max_data.has_key('O3'):
                    data_1d['O3'] = max_data['O3'] / qc_dict_1h['O3'] * 100  # Gtri AQI_1d cua O3
                    # Gtri AQI_1d chung cua tram
                    if data_1d['aqi'] < data_1d['O3']:
                        data_1d['aqi'] = data_1d['O3']

                # Do qui dinh : AQI_1d cua CO = max (AQI_1h cua CO)
                if max_data.has_key('CO'):
                    data_1d['CO'] = max_data['CO'] / qc_dict_1h['CO'] * 100  # Gtri AQI_1d cua O3
                    # Gtri AQI_1d chung cua tram
                    if data_1d['aqi'] < data_1d['CO']:
                        data_1d['aqi'] = data_1d['CO']

                get_time = datetime.datetime.fromordinal(item.get_time.toordinal())

                try:
                    db.aqi_data_24h.update_or_insert(
                        (db.aqi_data_24h.station_id == item.station_id) & (db.aqi_data_24h.get_time == get_time),
                        station_id=item.station_id,
                        get_time=get_time,
                        data_24h=data_24h,
                        data_1d=data_1d
                    )
                    db.commit()  # Luu data vao db ngay sau khi xu ly moi tram
                except:
                    traceback.print_exc()
                    db.rollback()

        db.commit()
    except Exception as ex:
        traceback.print_exc()
        logger.error(str(ex))
    finally:
        logger.info('End calculate AQI data day')
    return


################################################################################
# HungDX load + update database
def load_update_data(number_days):
    count = 0
    logger.info('-' * 80)
    logger.info('Time start load/update data: ' + str(datetime.datetime.now()))

    # Quet tung tram va doc va xu ly du lieu
    count = 0
    using_station_list = {}
    threads = []
    second_limit = 100  # Bien luu so giay gioi han de connect qua ftp voi moi station

    while True:
        try:
            logger.debug('-' * 80)
            # danh sach cac tram + code tram
            number_scan_failed_min = 0
            number_scan_failed_max = 5
            # station_names, _, _, station_ids = get_station_dict_base_station_id(number_scan_failed_min, number_scan_failed_max)
            # station_names, _, _, station_ids = get_station_dict_base_station_id(number_scan_failed_min, number_scan_failed_max)

            station_names, _, _, station_ids = get_station_dict_base_station_id()

            # logger.debug('station names list: %s', station_names)
            # logger.debug('station ids list  : %s', station_ids)



            for index, station_id in enumerate(station_ids):
                if not station_id:
                    continue
                logger.debug("-"*100)
                logger.debug("station_id = %s", station_id)

                #
                # if station_id != '28560877461938780203765592307' or station_id != '28560877461938780203765592307':
                #     continue

                # if station_id != '28560877461938780203765592307':  # Khi nguyen van cu
                #     continue

                # if station_id != '28494690359734869565924903870': # Ha Nam 3
                #     continue

                # if station_id != '28500868561706780035137882520': # Ha Nam 1
                #     continue

                # if station_id != '28695443980435702745237899322': # Xi mang thac lam
                #     continue

                # if station_id != '28695443980435702745237899322': # Nam Dinh
                #     continue

                # if station_id != '28565902650172363841171747059': # Formosa ND Khi Lo 1
                #     continue

                try:
                    # logger.info("Create and run station_process thread with station_id = %s", station_id)
                    # # station_process(station_id, number_days)

                    # ----------------------------------------------------
                    # Cach 2: Chay thread
                    #
                    # Thread(target=station_process, args=(station_id, 1)).start()

                    # from_day = datetime.datetime.now() - datetime.timedelta(days=365 * 3) + datetime.timedelta(days=31 * 1)
                    #
                    # to_date = datetime.datetime.now() - datetime.timedelta(days=31 * 1)

                    # Thread(target=station_process_all, args=(station_id, from_day, to_date)).start()

                    ftp_station_info = get_stations_ftp_load_update_by_station_id(station_id)
                    ip = ftp_station_info[0].get(int(station_id))
                    username = ftp_station_info[2].get(int(station_id))
                    pwd = ftp_station_info[3].get(int(station_id))
                    port = ftp_station_info[4].get(int(station_id))

                    # station_logger.info('stations file_mapping: ' + file_mapping)
                    if not ip or not port or not username or not pwd:
                        logger.error("ftp_station_info: have error")
                        continue

                    try:
                        logger.debug("ftp_station_info all :    = %s", ftp_station_info)
                        logger.debug("ftp_session: ip           = %s", ip)
                        logger.debug("ftp_session: port         = %s", port)
                        logger.debug("ftp_session: second_limit = %s", second_limit)
                        logger.debug("ftp_session: username     = %s", username)
                        logger.debug("ftp_session: pwd          = %s", pwd)

                        ftp_session = ftplib.FTP(ip) # TriNT: Khi chay thay, thi phai bo rem
                        ftp_session.connect(ip, port, second_limit) # TriNT: Khi chay thay, thi phai bo rem

                        # # Trint Can phai xoa------------------------------------------------
                        # ftp_session = ftplib.FTP('ftp.cem.gov.vn')  # TriNT: Khi chay thay, thi phai  rem
                        # ftp_session.connect('ftp.cem.gov.vn', 21, second_limit)  # TriNT: Khi chay thay, thi phai rem
                        # # Trint Can phai xoa------------------------------------------------

                        # # # # Trint Can phai xoa------------------------------------------------
                        # ftp_session = ftplib.FTP('113.160.218.8')  # TriNT: Khi chay thay, thi phai  rem
                        # ftp_session.connect('113.160.218.8', 21, second_limit)  # TriNT: Khi chay thay, thi phai rem
                        # # # Trint Can phai xoa------------------------------------------------

                        ftp_session.login(username, pwd)

                        ftp_session_pool[str(station_id)] = ftp_session

                    except Exception as ex:
                        logger.error("Cannot Connect FTP Server with = %s", station_id)
                        continue


                    if not using_station_list: # TriNT: Code tam, truong hop tram update FTP thi ko duoc, phai dung queue thi moi ok

                        # station_logger = getLogger(station_id)
                        station_logger = getLogger(station_id, LOGGER_STATION_FOLDER, LOGGER_NAME, LOGGER_MAX_SIZE,
                                                   LOGGER_BACKUP_COUNT, LOGGER_LEVEL_FOR_STATION)

                        logger.info("Create and run station_process thread with station_id = %s", station_id)
                        # Start threads, Multithreading is your best bet because of its low overhead
                        # Thread(name=str(station_id), target=station_process, args=(station_id, number_days, station_logger)).start()

                        wordker = Thread(name=str(station_id), target=station_process,
                                         args=(station_id, number_days, station_logger, ftp_session))
                        wordker.start()
                        threads.append(wordker)

                        # You should use multiprocessing (if your machine has multiple cores)
                        # wordker = multiprocessing.Process(name=str(station_id), target=station_process,args=(station_id, number_days, station_logger))
                        # wordker.start()
                        # threads.append(wordker)

                        using_station_list[str(station_id)] = station_id
                        # Add threads to thread list

                        # logger.debug('Added: %s', station_id)
                    else:
                        if not station_id == using_station_list.get(station_id):
                            # station_logger = getLogger(station_id)
                            station_logger = getLogger(station_id, LOGGER_STATION_FOLDER, LOGGER_NAME, LOGGER_MAX_SIZE,
                                                       LOGGER_BACKUP_COUNT, LOGGER_LEVEL_FOR_STATION)

                            logger.info("Create and run station_process thread with station_id = %s", station_id)

                            # Start threads, Multithreading is your best bet because of its low overhead
                            # Thread(name=str(station_id), target=station_process, args=(station_id, number_days, station_logger)).start()
                            wordker = Thread(name=str(station_id), target=station_process,
                                             args=(station_id, number_days, station_logger, ftp_session))
                            wordker.start()
                            threads.append(wordker)

                            using_station_list[str(station_id)] = station_id
                            # logger.debug('Added: %s', station_id)
                        # else:
                        # logger.debug('No have new station to add: %s', station_id)
                    count += 1
                except Exception as ex:
                    traceback.print_exc()
                    # logger.error('Exception = %s', ex.message)

            # End for

            # try:
            #     logger.debug('Scan ftp_session_pool to call quit()')
            #     for station_id in ftp_session_pool:
            #         logger.debug("ftp_session_pool %s call quit()", station_id)
            #         if ftp_session_pool[str(station_id)]:
            #             ftp_session_pool[str(station_id)].quit()
            #             logger.debug("ftp_session_pool %s call quit(): ok")
            # except Exception as ex:
            #     traceback.print_exc()
            #     # logger.error('Scan ftp_session_pool to call quit. Exception = %s', ex.message)

            logger.debug('-' * 100)
            logger.debug('calc_data_hour_new_all: number_day = %s', number_days * 24)
            calc_data_hour_new_all(number_days * 24)

            logger.debug('calc_data_day_new_all: number_day = %s', number_days)
            calc_data_day_new_all(number_days)

            logger.debug('calc_data_month_new_all: number_day = %s', number_days)
            calc_data_month_new_all(number_days)

            logger.debug('calc_data_min_collect: number_day = %s', number_days)
            calc_data_min_collect()

            # logger.debug('calc_aqi_data_hour: number_day = %s', number_days)
            # calc_aqi_data_hour()

            # logger.debug('calc_aqi_data_24h: number_day = %s', number_days)
            # calc_aqi_data_24h()

        except Exception as ex:
            traceback.print_exc()
            logger.error("load_update_data have exception: %s", ex.message)

        logger.debug('End white --> waiting 10 m to restart')
        time.sleep(10 * 60)
    # End while true
    # finally:
    #     logger.info('Total number created thread = %s', count)
    # return count


################################################################################
def data_collection_prcess(number_days):

    time.sleep(60 * 60)

    logger.debug('-' * 100)
    logger.debug('calc_data_hour_new_all: number_day = %s', number_days * 24)
    calc_data_hour_new_all(number_days * 24)

    logger.debug('calc_data_day_new_all: number_day = %s', number_days)
    calc_data_day_new_all(number_days)

    logger.debug('calc_data_month_new_all: number_day = %s', number_days)
    calc_data_month_new_all(number_days)

    logger.debug('calc_data_min_collect: number_day = %s', number_days)
    calc_data_min_collect()

    logger.debug('calc_aqi_data_hour: number_day = %s', number_days)
    calc_aqi_data_hour()

    logger.debug('calc_aqi_data_24h: number_day = %s', number_days)
    calc_aqi_data_24h()

def main():
    number_days = 1
    load_update_data(number_days)

if __name__ == "__main__":
    main()