# -*- coding: utf-8 -*-

from gluon import current
from datetime import datetime, timedelta


################################################################################
def hour_data_calc(station_id, data_mins, lastest_hour):
    db = current.db
    data = dict()       # {indicator : sum value}
    count = dict()      # {indicator : count}
    
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
                try:
                    data[indicator] += float(get_data[indicator])
                    count[indicator] += 1
                except:
                    continue
            else:
                try:
                    data[indicator] = float(get_data[indicator])
                    count[indicator] = 1
                except:
                    continue

        # Neu la row cuoi thi chot, insert vao db
        if i == len(data_mins) - 1:    
            # Neu du lieu dict la empty thi skip, ko luu DB
            if bool(data):
                # Calc average
                for indicator in data.keys():
                    try:
                        data[indicator] = float("{0:.4f}".format(data[indicator] / count[indicator]))
                    except:
                        data[indicator] = None

                db.data_hour.update_or_insert(
                    (db.data_hour.station_id == station_id) & (db.data_hour.get_time == lastest_hour),
                    station_id=station_id,
                    get_time=lastest_hour,
                    data=data
                )
                # hungdx add new table data_hour_lastest issue 30
                db.data_hour_lastest.update_or_insert(
                    (db.data_hour_lastest.station_id == station_id),
                    station_id=station_id,
                    last_time=lastest_hour
                )
    return   
    
################################################################################
def day_data_calc(station_id, data_hours, lastest_day):
    db = current.db
    data = dict()       # {indicator : sum value}
    count = dict()      # {indicator : count}
    max_data = dict()      
    min_data = dict()      
    max_data_time = dict()      
    min_data_time = dict()      
    
    for i, row in enumerate(data_hours):
        # Neu ko co du lieu cua ngay hom truoc, tang ngay cho den ngay cua row hien tai thi thoi
        #hungdx comment start issue 30
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
            try:
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
            except:
                continue
        # Neu la row cuoi thi insert phan da doc vao DB
        if i == len(data_hours) - 1:    
            if bool(data):
                # Calc average
                for indicator in data.keys():
                    try:
                        data[indicator] = float("{0:.4f}".format(data[indicator] / count[indicator]))
                    except:
                        continue

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
                # hungdx add new table data_day_lastest issue 30
                db.data_day_lastest.update_or_insert(
                    (db.data_day_lastest.station_id == station_id),
                    station_id=station_id,
                    last_time=lastest_day
                )
    return   
    
################################################################################    
def mon_data_calc(station_id, data_days, lastest_mon):
    from calendar import mdays
    db = current.db
    data = dict()       # {indicator : sum value}
    count = dict()      # {indicator : count}
    max_data = dict()      
    min_data = dict()      
    max_data_time = dict()      
    min_data_time = dict()      
    
    for i, row in enumerate(data_days):
        #hungdx comment start issue 30
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
        #hungdx comment end issue 30
            # Boc du lieu tu row hien tai vao data dict()    
        get_data = row.data
        for indicator in get_data.keys():
            try:
                val = float(get_data[indicator])
                if data.has_key(indicator):
                    data[indicator] += val
                    count[indicator] += 1
                    if val > max_data[indicator]:
                        max_data[indicator] = val
                        max_data_time[indicator] = datetime.fromordinal(row.get_time.toordinal())   # phai convert kieu date ve datetime thi mongo no moi save dc vao DB
                    if val < min_data[indicator]:
                        min_data[indicator] = val
                        min_data_time[indicator] = datetime.fromordinal(row.get_time.toordinal())
                else:
                    data[indicator] = val
                    count[indicator] = 1
                    max_data[indicator] = val
                    min_data[indicator] = val
                    max_data_time[indicator] = datetime.fromordinal(row.get_time.toordinal())
                    min_data_time[indicator] = datetime.fromordinal(row.get_time.toordinal())
            except:
                continue

        # Check if la row cuoi cung, thi insert record vao bang data_mon
        if i == len(data_days) - 1:    
            # Neu du lieu dict la empty thi skip, ko luu DB
            if bool(data):
                # Calc average
                for indicator in data.keys():
                    try:
                        data[indicator] = float("{0:.4f}".format(data[indicator] / count[indicator]))
                    except:
                        continue

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
                # hungdx add new table data_month_lastest issue 30
                db.data_month_lastest.update_or_insert(
                    (db.data_month_lastest.station_id == station_id),
                    station_id=station_id,
                    last_time=lastest_mon
                )
    return      