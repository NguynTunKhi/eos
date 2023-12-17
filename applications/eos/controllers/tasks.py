# -*- coding: utf-8 -*-
###############################################################################
# Author : 
# Date   : 
# 
# Description : 
# 
###############################################################################
from datetime import datetime, timedelta
from applications.eos.modules import const
from gluon.tools import prettydate
import json
from gluon.tools import AuthJWT
import datetime
from datetime import datetime, timedelta
import math

from applications.eos.modules import const, common, indicator_calc, wqi, server_data
from gluon.scheduler import Scheduler

def call():
    return service()

################################################################################
# @decor.requires_login()
def index():
    return locals()

################################################################################
@service.json
# @decor.requires_login()
def start_task_get_data():
    try:
        from datetime import timedelta
        
        # Delete all old 'task_get_data' and Queue new one
        # db2(db2.scheduler_task.task_name == 'task_get_data').delete()
       # db2(db2.scheduler_task.id > 0).delete()

        # hungdx off issue 56
        # scheduler.queue_task('task_get_data',
        #                      start_time = datetime.strptime('2019-04-10 00:00:01.243860', '%Y-%m-%d %H:%M:%S.%f')+ timedelta(seconds = 5),
        #                      timeout = 450,         # should take less than 600 seconds
        #                      prevent_drift = True,
        #                      period = 300,          # Chay cach 5p/lan
        #                      retry_failed=-1,       # unlimited
        #                      repeats=0)
        # scheduler.queue_task('task_calc_data_hour',
        #                      start_time=datetime.strptime('2019-04-10 00:00:01.243860', '%Y-%m-%d %H:%M:%S.%f') + timedelta(seconds=5),
        #                      timeout=6000,               # should take less than 600 seconds
        #                      prevent_drift=True,
        #                      period=3600,               # Chay cach 1h/lan
        #                      retry_failed=-1,
        #                      repeats=0)
        # scheduler.queue_task('task_calc_data_day',
        #                      start_time=datetime.strptime('2019-04-10 00:00:01.243860', '%Y-%m-%d %H:%M:%S.%f') + timedelta(seconds=5),
        #                      timeout=6000,
        #                      prevent_drift=True,
        #                      period=86400,              # Chay cach 1d/lan
        #                      retry_failed=-1,
        #                      repeats=0)
        # scheduler.queue_task('task_calc_data_month',
        #                      start_time=datetime.strptime('2019-04-01 00:00:01.243860', '%Y-%m-%d %H:%M:%S.%f') + timedelta(seconds=5),
        #                      timeout=6000,
        #                      prevent_drift=True,
        #                      period=2592000,            # Chay cach 1 mon/lan
        #                      retry_failed=-1,
        #                      repeats=0)
        # scheduler.queue_task('task_calc_aqi_data_hour',
        #                      start_time=datetime.strptime('2019-04-10 00:00:01.243860', '%Y-%m-%d %H:%M:%S.%f') + timedelta(seconds=5),
        #                      timeout=600,
        #                      prevent_drift=True,
        #                      period=3600,               # Chay cach 1h/lan
        #                      retry_failed=-1,
        #                      repeats=0)
        # scheduler.queue_task('task_calc_aqi_data_24h',
        #                      start_time=datetime.strptime('2019-04-10 00:00:01.243860', '%Y-%m-%d %H:%M:%S.%f') + timedelta(seconds=5),
        #                      timeout=600,
        #                      prevent_drift=True,
        #                      period=86400,              # Chay cach 1d/lan
        #                      retry_failed=-1,
        #                      repeats=0)
        # scheduler.queue_task('task_calc_wqi_data_hour',
        #                      start_time=datetime.strptime('2019-04-10 00:00:01.243860', '%Y-%m-%d %H:%M:%S.%f') + timedelta(seconds=5),
        #                      timeout=600,
        #                      prevent_drift=True,
        #                      period=3600,               # Chay cach 1h/lan
        #                      retry_failed=-1,
        #                      repeats=0)
        # scheduler.queue_task('task_calc_data_min_collect',
        #                      start_time=datetime.strptime('2019-04-10 00:00:01.243860', '%Y-%m-%d %H:%M:%S.%f') + timedelta(seconds=5),
        #                      timeout=600,
        #                      prevent_drift=True,
        #                      period=600,               # Chay cach 10p/lan
        #                      retry_failed=-1,
        #                      repeats=0)

        session.pop('request_active_task_get_data')
        return dict(success = True)
    except Exception, ex:
        return dict(message = str(ex), success = False)

################################################################################
@service.json
# @decor.requires_login()
def start_task_get_data_later():
    try:
        session.pop('request_active_task_get_data')
        return dict(success = True)
    except Exception, ex:
        return dict(message = str(ex), success = False)
    
################################################################################

################################################################################
@service.json
# @decor.requires_login()
def get_list_worker(*args, **kwargs):
    try:
        aaData = [] # Du lieu json se tra ve
    
        conditions = (db2.scheduler_worker.id > 0)
        list_data = db2(conditions).select( db2.scheduler_worker.worker_name,
                                            db2.scheduler_worker.group_names,
                                            db2.scheduler_worker.status,
                                            db2.scheduler_worker.first_heartbeat,
                                            db2.scheduler_worker.last_heartbeat,
                                            db2.scheduler_worker.is_ticker,
                                            orderby = ~db2.scheduler_worker.status)
        iTotalRecords = len(list_data)
        active_worker = 0

        # Duyet tung phan tu trong mang du lieu vua truy van duoc
        for i, item in enumerate(list_data):
            # Check alive worker:
            last = (request.now - item.last_heartbeat).seconds if request.now >= item.last_heartbeat else (item.last_heartbeat - request.now).seconds
            if last < schedule_heartbeat * 10:
                active_worker += 1
                
            aaData.append([
                i + 1,
                item.worker_name,
                item.group_names,
                item.first_heartbeat,
                item.last_heartbeat,
                item.is_ticker,
                item.status,
                #INPUT(_name = 'select_item', _class = 'select_item_0', _type = 'checkbox', _value = item.id),
            ])

        return dict(iTotalRecords = iTotalRecords, iTotalDisplayRecords = iTotalRecords, aaData = aaData, success = True, active_worker = active_worker)
    except Exception, ex:
        return dict(iTotalRecords = 0, iTotalDisplayRecords = 0, aaData = [], message = str(ex), success = False)                                    
                                            
################################################################################

################################################################################
@service.json
# @decor.requires_login()
def get_list_task(*args, **kwargs):
    try:
        iDisplayStart = int(request.vars.iDisplayStart)
        iDisplayLength = int(request.vars.iDisplayLength)
        s_search = request.vars.sSearch
        aaData = []
        limitby = (iDisplayStart, iDisplayLength + 1) # Tuple dung de phan trang (vtri bat dau - chieu dai)
    
        conditions = (db2.scheduler_task.id > 0)
        if s_search:
            conditions &= ((db2.scheduler_task.task_name.contains(s_search)) | (db2.scheduler_task.group_name.contains(s_search)))
            
        list_data = db2(conditions).select( db2.scheduler_task.task_name,
                                            db2.scheduler_task.group_name,
                                            db2.scheduler_task.status,
                                            db2.scheduler_task.start_time,
                                            db2.scheduler_task.stop_time,
                                            db2.scheduler_task.next_run_time,
                                            db2.scheduler_task.vars,
                                            orderby = ~db2.scheduler_task.start_time | db2.scheduler_task.status,
                                            limitby = limitby)
        
        iTotalRecords = db2(conditions).count()
            
        ### Build return array for datatable
        alive_task = 0
        is_daily_task = 0

        # Duyet tung phan tu trong mang du lieu vua truy van duoc
        for i, item in enumerate(list_data):
            # Count for task alive : QUEUE, ASSIGNED, RUNNING
            if item.status in ['QUEUED', 'ASSIGNED', 'RUNNING']:
                alive_task += 1
            
            # # Check daily task QUEUED or not?
            # if 'task_get_data' in item.task_name and item.status in ['QUEUED', 'RUNNING'] and item.next_run_time >= request.now:
            #     is_daily_task = 1
                
            aaData.append([
                iDisplayStart + 1 + i,
                item.task_name,
                item.group_name,
                item.status,
                item.start_time,
                item.stop_time,
                #INPUT(_name = 'select_item', _class = 'select_item_0', _type = 'checkbox', _value = item.id),
            ])

        return dict(iTotalRecords = iTotalRecords, iTotalDisplayRecords = iTotalRecords, aaData = aaData, success = True, alive_task = alive_task, is_daily_task = is_daily_task)
    except Exception, ex:
        return dict(iTotalRecords = 0, iTotalDisplayRecords = 0, aaData = [], message = str(ex), success = False)
        
################################################################################
@service.json
def start_task_get_data_aqi():
    try:
        start = datetime.now()
        logger.info('Start calculate AQI data hour')

        # Start of day
        # Lay lui ve it nhat 12h so voi ngay hien tai
        # day = start.day - 1
        # start = start.replace(day = 11, hour=0, minute=0, second=0, microsecond=0)
        # chú ý: hour sẽ lữu vào station update
        start = start.replace(day = 19, hour=0, minute=0, second=0, microsecond=0)
        # print(start)
        # Chi loai station_type = 3, 4 and is_qi = True
        conditions = (db.stations.station_type.belongs([const.STATION_TYPE['AMBIENT_AIR']['value'], const.STATION_TYPE['STACK_EMISSION']['value']]))
        conditions &= (db.stations.is_qi == True)
        ambients = db(conditions).select(db.stations.id)
        ambients = [str(station.id) for station in ambients]

        # Get data from 'data_hour' tu cac station o tren de tinh toan
        conditions = (db.data_hour.station_id.belongs(ambients))
        conditions &= (db.data_hour.get_time >= start)

        data_hours = db(conditions).select(orderby=db.data_hour.station_id | db.data_hour.get_time)
        # print(data_hours)

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
                        if (indicator == 'PM-10') :
                            get_time = item.get_time.replace(minute=0, second=0, microsecond=0)  # Chuan hoa : cat minute, second ve 0
                            # if ((item.station_id) == '28560877461938780203765592307') :
                            #     print(get_time)
                            dataAfter12h = get_list_log_after_12h(str(item.station_id), indicator, get_time);
                            # if ((item.station_id) == '28560877461938780203765592307') :
                            #     print(dataAfter12h)
                            # print(get_time)
                            aqi = getNowcastConcentration(indicator, dataAfter12h)
                            data[indicator] = aqi
                        elif (indicator == 'PM-2-5') :
                            get_time = item.get_time.replace(minute=0, second=0, microsecond=0)
                            dataAfter12h = get_list_log_after_12h(str(item.station_id), indicator, get_time);
                            aqi = getNowcastConcentration(indicator, dataAfter12h)
                            data[indicator] = aqi
                        else :
                            aqi = hour_data[indicator] / qc_dict[indicator] * 100  # Theo cong thuc tinh AQI cho tung chi so
                            data[indicator] = aqi
                        # So sanh voi chi so AQI chung tong the
                        if data['aqi'] < aqi: data['aqi'] = aqi
            # Neu co du lieu thi insert/update bang 'aqi_data_hour'
            if data['aqi']:
                get_time = item.get_time.replace(minute=0, second=0, microsecond=0)  # Chuan hoa : cat minute, second ve 0

                db.aqi_data_hour.update_or_insert(
                    (db.aqi_data_hour.station_id == item.station_id) & (db.aqi_data_hour.get_time == get_time),
                    station_id=item.station_id,
                    get_time=get_time,
                    data=data
                )
                # Update AQI cho station
                db(db.stations.id == item.station_id).update(qi=data['aqi'], qi_time=get_time)
        db.commit()
    except Exception as ex:
        logger.error(str(ex))
    finally:
        logger.info('End calculate AQI data hour')
    return 'done'

@service.json
def start_task_get_data_aqi_24():
    return 'exit'
    try:
        logger.info('Start calculate AQI data day')
        start = datetime.now()
        # Start of day
        start = start.replace(day = 11, hour=0, minute=0, second=0, microsecond=0)
        print(start)
        # Chi loai station_type = 4 and is_qi = True
        conditions = (db.stations.station_type.belongs([const.STATION_TYPE['AMBIENT_AIR']['value'], const.STATION_TYPE['STACK_EMISSION']['value']]))
        conditions &= (db.stations.is_qi == True)
        ambients = db(conditions).select(db.stations.id)
        ambients = [str(station.id) for station in ambients]

        # Get data from 'data_day' tu cac station o tren de tinh toan
        conditions = (db.data_day.station_id.belongs(ambients))
        conditions &= (db.data_day.get_time >= start)
        data_days = db(conditions).select(orderby=db.data_day.station_id | db.data_day.get_time)

        # Lay cac chi so qui chuan cua cac indicator
        qc = db(db.aqi_indicators.id > 0).select(db.aqi_indicators.indicator, db.aqi_indicators.qc_1h, db.aqi_indicators.qc_24h)
        qc_dict_1h = dict()
        qc_dict_24h = dict()
        for item in qc:
            qc_dict_1h[item.indicator] = item.qc_1h
            qc_dict_24h[item.indicator] = item.qc_24h

        for item in data_days:
            data_24h = {'aqi': None}  # du lieu AQI se insert/update vao bang 'aqi_data_24h'
            data_1d = {'aqi': None}  # du lieu AQI se insert/update vao bang 'aqi_data_24h'
            day_data = item.data
            max_data = item.data_max

            # Tinh toan gtri AQI cho tung indicator (dc dinh nghia truoc trong qc_dict)
            for indicator in day_data.keys():
                # Chi lay nhung chi so AQI
                if qc_dict_24h.has_key(indicator):
                    # Ko tinh toan AQI 24h cho chi so ko co gtri qui chuan hoac O3
                    if qc_dict_24h[indicator] and indicator != 'O3':
                        aqi = day_data[indicator] / qc_dict_24h[indicator] * 100  # Theo cong thuc tinh AQI cho tung chi so
                        data_24h[indicator] = aqi

                        # So sanh voi chi so AQI chung tong the
                        if data_24h['aqi'] < aqi: data_24h['aqi'] = aqi

            # Neu co du lieu thi insert/update bang 'aqi_data_24h'
            if data_24h['aqi']:
                # So sanh du lieu AQI_24h vua tinh duoc voi gtri max cua AQI_1h de lay gtri AQI_1d
                keys = data_24h.keys()
                keys.remove('aqi')
                for indicator in keys:
                    aqi_max_indicator = max_data[indicator] / qc_dict_1h[indicator] * 100 if qc_dict_1h[indicator] else 0
                    data_1d[indicator] = aqi_max_indicator if aqi_max_indicator > data_24h[indicator] else data_24h[indicator]

                    # Gtri AQI_1d chung cua tram
                    if data_1d['aqi'] < data_1d[indicator]:
                        data_1d['aqi'] = data_1d[indicator]

                # Do qui dinh : AQI_1d cua O3 = max (AQI_1h cua O3)
                if max_data.has_key('O3'):
                    data_1d['O3'] = max_data['O3'] / qc_dict_1h['O3'] * 100  # Gtri AQI_1d cua O3
                    # Gtri AQI_1d chung cua tram
                    if data_1d['aqi'] < data_1d['O3']:
                        data_1d['aqi'] = data_1d['O3']

                get_time = datetime.fromordinal(item.get_time.toordinal())

                db.aqi_data_24h.update_or_insert(
                    (db.aqi_data_24h.station_id == item.station_id) & (db.aqi_data_24h.get_time == get_time),
                    station_id=item.station_id,
                    get_time=get_time,
                    data_24h=data_24h,
                    data_1d=data_1d
                )

        db.commit()
    except Exception as ex:
        logger.error(str(ex))
    finally:
        logger.info('End calculate AQI data day')
    return 'done'

def testgetran() :
    # return getNowcastConcentration('PM-10', [60.39,64.85,61.61,66.17,81.99,90.97,83.80,103.91,100.77,35.37,87.01,61.59]);
    # return getNowcastConcentration('PM-10', [80.02,51.98,76.23,60.27,68.77,65.26,52.24,61.10,73.38,52.49,78.13,61.09]);
    start = datetime.now()
    start = start.replace(day=7, hour=15, minute=0, second=0, microsecond=0)

    return get_list_log_after_12h('28560877461938780203765592307', 'PM-10', start);
def getNowcastConcentration(pollutant, data) :
    # if isValidNowcastData(data) :
    #     return -1;
    return truncateConcentration(pollutant, data)


def truncateConcentration(pollutant, data) :
    if (isValidNowcastData(data) > 1) :
        return 0
    weight = getWeightFactor(pollutant, data);
    totalConcentrationWithWeight = 0;
    totalWeight = 0;

    indexDataSlot = 3
    numberItem = 0
    totalConcentration = 0
    if weight > 0.5 :
        for item in data :
            if item < 0 :
                continue;
            else :
                totalConcentrationWithWeight += item * math.pow(weight, numberItem)
                totalWeight += math.pow(weight, numberItem)
            numberItem = numberItem + 1
        totalConcentration = totalConcentrationWithWeight / totalWeight
    else :
        for item in (data):

            if item < 0 :
                continue;
            totalConcentrationWithWeight += item * math.pow(0.5, numberItem + 1)
            numberItem = numberItem + 1

        totalConcentration = totalConcentrationWithWeight
    return getTruncatedPollutantConcentrationBaseOnPollutant(pollutant, totalConcentration)

def getWeightFactor(indicator, data):
    maxConcentration = float('-inf')
    minConcentration = float('inf')

    for i in data :
        if (i < 0) :
            continue
        else :
            if (i > maxConcentration) :
                maxConcentration = i;
            if (i < minConcentration) :
                minConcentration = i

    range = maxConcentration - minConcentration

    try:
        weightFactor = float(minConcentration) / float(maxConcentration)
    except:
        weightFactor = 0

    if weightFactor <= float(1) / 2:
        weightFactor = float(1) / 2
    return weightFactor


def getTruncatedPollutantConcentrationBaseOnPollutant(pollutant, concentration) :
    if (pollutant == 'PM-10') :
        return float(concentration * 100 / 150)

    if (pollutant == 'PM-2-5') :
        return float(concentration * 100 / 50)

def isValidNowcastData(data) :
    try :
        missingData = 0;
        x = range(0, 2)
        if len(data) >= 3 :
            for i in x:
                if (data[i] < 0) :
                    missingData = missingData + 1
        return missingData

    except Exception as ex:
        return 0

# Lay list cac chi so PM 10, PM2.5 sau 12h tinh tu thoi diem lay
def get_list_log_after_12h(station_id, indicator, time):
    try:
        aaData = []  # Du lieu json se tra ve

        conditions = (db.data_hour.id > 0)
        conditions &= (db.data_hour.station_id == station_id)
        if time:
            time_delta = time - timedelta(hours=11)
            conditions &= (db.data_hour.get_time >= time_delta)
            conditions &= (db.data_hour.get_time <= time)

        list_data = db(conditions).select(orderby=~db.data_hour.get_time)

        # Thu tu ban ghi
        iRow = 1
        # Duyet tung phan tu trong mang du lieu vua truy van duoc
        for i, item in enumerate(list_data):
            row=[]
            added_item = dict()
            i_name = indicator
            i_name_decode = i_name.decode('utf-8')
            v = item.data[indicator] if item.data.has_key(indicator) else ''
            if v == '':
                added_item[i_name] = 0
            else:
                try:
                    v = float(v)
                    added_item[i_name] = float(v)
                except:
                    added_item[i_name] = 0
            if added_item.has_key(i_name):
                aaData.append(added_item[i_name])
        return aaData
    except Exception as ex:
        return 0

#Script test aqi ngay
def calc_aqi_data_24h():
    start = datetime.now()
    currentStart = datetime.now();
    try:
        logger.info('Start calculate AQI data day')

        # Start of day
        # start = start.replace(hour=0, minute=0, second=0, microsecond=0)
        start = start.replace(day = 20, hour=0, minute=0, second=0, microsecond=0)
        currentStart = currentStart.replace(hour=0, minute=0, second=0, microsecond=0)
        # Xử lý fix ko cho tính ngày hiện tại
        if (start == currentStart) :
            start = start.replace(hour=0, minute=0, second=0, microsecond=0) - timedelta(days=1)

        # Chi loai station_type = 4 and is_qi = True
        conditions = (db.stations.station_type.belongs([const.STATION_TYPE['AMBIENT_AIR']['value'], const.STATION_TYPE['STACK_EMISSION']['value']]))
        conditions &= (db.stations.is_qi == True)
        ambients = db(conditions).select(db.stations.id)
        ambients = [str(station.id) for station in ambients]

        # Get data from 'data_day' tu cac station o tren de tinh toan
        conditions = (db.data_day.station_id.belongs(ambients))
        conditions &= (db.data_day.get_time >= start)
        conditions &= (db.data_day.get_time < currentStart)
        data_days = db(conditions).select(orderby=db.data_day.station_id | db.data_day.get_time)

        # Lay cac chi so qui chuan cua cac indicator
        qc = db(db.aqi_indicators.id > 0).select(db.aqi_indicators.indicator, db.aqi_indicators.qc_1h, db.aqi_indicators.qc_24h)
        qc_dict_1h = dict()
        qc_dict_24h = dict()
        for item in qc:
            qc_dict_1h[item.indicator] = item.qc_1h
            qc_dict_24h[item.indicator] = item.qc_24h

        for item in data_days:
            data_24h = {'aqi': None}  # du lieu AQI se insert/update vao bang 'aqi_data_24h'
            data_1d = {'aqi': None}  # du lieu AQI se insert/update vao bang 'aqi_data_24h'
            day_data = item.data # Du lieu quan trac trung binh 1 ngay cua thong so = SUM/count
            max_data = item.data_max

            # Tinh toan gtri AQI cho tung indicator (dc dinh nghia truoc trong qc_dict)
            for indicator in day_data.keys():
                # Chi lay nhung chi so AQI
                if qc_dict_24h.has_key(indicator):
                    # Ko tinh toan AQI 24h cho chi so ko co gtri qui chuan hoac O3
                    if qc_dict_24h[indicator] and indicator not in ['O3', 'CO']:
                        aqi = day_data[indicator] / qc_dict_24h[indicator] * 100  # Theo cong thuc tinh AQI cho tung chi so
                        data_24h[indicator] = aqi

                        # So sanh voi chi so AQI chung tong the
                        if data_24h['aqi'] < aqi: data_24h['aqi'] = aqi

            # Neu co du lieu thi insert/update bang 'aqi_data_24h'
            if data_24h['aqi']:
                # So sanh du lieu AQI_24h vua tinh duoc voi gtri max cua AQI_1h de lay gtri AQI_1d
                keys = data_24h.keys()
                keys.remove('aqi')
                for indicator in keys:
                    get_time = datetime.fromordinal(item.get_time.toordinal())
                    if (indicator == 'PM-10'):
                        aqi_max_indicator = get_max_day_aqi_pm(str(item.station_id), indicator, get_time);
                        data_1d[indicator] = aqi_max_indicator if aqi_max_indicator > data_24h[indicator] else data_24h[indicator]
                    elif (indicator == 'PM-2-5'):
                        aqi_max_indicator = get_max_day_aqi_pm(str(item.station_id), indicator, get_time);
                        data_1d[indicator] = aqi_max_indicator if aqi_max_indicator > data_24h[indicator] else data_24h[indicator]
                    else:
                        aqi_max_indicator = max_data[indicator] / qc_dict_1h[indicator] * 100 if qc_dict_1h[indicator] else 0
                        data_1d[indicator] = aqi_max_indicator if aqi_max_indicator > data_24h[indicator] else data_24h[indicator]

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

                get_time = datetime.fromordinal(item.get_time.toordinal())

                db.aqi_data_24h.update_or_insert(
                    (db.aqi_data_24h.station_id == item.station_id) & (db.aqi_data_24h.get_time == get_time),
                    station_id=item.station_id,
                    get_time=get_time,
                    data_24h=data_24h,
                    data_1d=data_1d
                )

        db.commit()
    except Exception as ex:
        logger.error(str(ex))
    finally:
        logger.info('End calculate AQI data day')
    return

# Lay max api day cac chi so PM
def get_max_day_aqi_pm(station_id, indicator, time):
    try:
        aaData = []  # Du lieu json se tra ve
        max_day_api = 0
        conditions = (db.aqi_data_hour.id > 0)
        conditions &= (db.aqi_data_hour.station_id == station_id)
        if time:
            time_delta = time + timedelta(hours=23)
            conditions &= (db.aqi_data_hour.get_time >= time)
            conditions &= (db.aqi_data_hour.get_time <= time_delta)

        list_data = db(conditions).select(orderby=~db.aqi_data_hour.get_time)

        # Thu tu ban ghi
        iRow = 1
        # Duyet tung phan tu trong mang du lieu vua truy van duoc
        if list_data :
            for i, item in enumerate(list_data):
                row=[]
                added_item = dict()
                i_name = indicator
                i_name_decode = i_name.decode('utf-8')
                v = item.data[indicator] if item.data.has_key(indicator) else ''
                if v == '':
                    added_item[i_name] = 0
                else:
                    try:
                        v = float(v)
                        added_item[i_name] = float(v)
                    except:
                        added_item[i_name] = 0
                if added_item.has_key(i_name):
                    aaData.append(added_item[i_name])
        if aaData :
            max_day_api = max(aaData)

        return max_day_api
    except Exception as ex:
        return 0