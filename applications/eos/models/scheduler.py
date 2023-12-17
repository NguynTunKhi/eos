# -*- coding: utf-8 -*-
import logging
import os
from datetime import datetime, timedelta
import math

from applications.eos.modules import const, common, indicator_calc, wqi, server_data
from gluon.scheduler import Scheduler

################################################################################
# '''
#     Scan data of stations stored in remote server by interval (via FTP)
#     Each station has its own server
#     Data after retrived will be process as follow:
#         - Save in "data_min" table, if data of indicator exceed threshold value, "is_exceed" flag is set True
#         - Update "last_data_files" table.
#         - Check "station_off_log" to update lastest station's status (if any)
#         - If no file data and after number of retry, update status of station to "In-active"
# '''
# def get_data():
#     count = 0       # dem nhung file duoc xu ly
#     try:
#         logger.info('-'*80)
#         logger.info('Start scan minute data')
#
#         # Get station_codes : dict(station_code : station_id)
#         # Get station_names : dict(station_id : station_name)
#         station_names, _ , _ , station_codes = common.get_station_dict()
#         lastest_files_dict = common.get_lastest_files_dict()
#         # Get all 'station_off_log' with records have 'end_off' field = None : co nghia nhung station dang o trang thai In-active
#         stations_off = db(db.station_off_log.end_off == None).select()
#
#
#         # Todo : path - hardcode
#         dir_path = os.path.join(request.folder, 'uploads', 'data')
#
#         # Get all file names *.txt in directory
#         import glob
#         files = glob.glob(os.path.join(dir_path, '*.txt'))
#
#         ### Xu ly tung file du lieu
#         for fname in files:
#             # Get filename only
#             basename = os.path.basename(fname)
#
#             # Neu ko tim duoc station voi CODE tuong ung --> skip
#             station_code = basename.split('_')[1]    # filename co format : province_stationcode_type_datetime.txt
#             station_id = station_codes.get(station_code)
#             if not station_id: continue
#
#             # station_id = str(station_id)
#             # So sanh filename voi file lastest da doc tuong ung voi station_id
#             lastest_file = lastest_files_dict.get(station_id)
#
#             # Neu la file cu thi ko xu ly gi ca --> skip
#             if lastest_file and basename <= lastest_file: continue
#
#             logger.info('Processing file : %s' % basename)
#             count += 1
#             # Read file data and save each line in "lines" array
#             with open(fname) as f:
#                 lines = f.readlines()
#
#             # Remove whitespace characters like `\n` at the end of each line
#             lines = [x.strip() for x in lines]
#
#             # Get threshold cua cac chi so tram
#             thresholds = common.get_station_indicator_thresdhold_dict()
#             is_exceed = False
#
#             data_datetime = ''
#             data = dict()
#             for i, line in enumerate(lines):
#                 items = line.split()        # line co format :  "indicator   value   unit  datetime"
#
#                 # Neu indicator co trong file ma ko dang ky trong chi so cua tram thi skip
#                 if not thresholds.has_key(station_id) or not thresholds[station_id].has_key(items[0].upper()):
#                     continue
#
#                 data[items[0]] = items[1]
#                 data_datetime = items[3]         # datetime trong 1 file se giong het nhau
#
#                 # Chi can 1 chi so vuot nguong la danh dau 'exceed'
#                 if float(items[1]) > thresholds[station_id][items[0].upper()]:
#                     is_exceed = True
#
#
#
#
#             # Neu du lieu dict la empty thi skip, ko luu DB
#             if not bool(data): continue
#
#             get_time = datetime.strptime(data_datetime, '%Y%m%d%H%M%S')
#             # Insert du lieu vao DB
#             db.data_min.insert(
#                 station_id = station_id,
#                 get_time = get_time,
#                 is_exceed = is_exceed,
#                 data = data
#             )
#
#             # Update du lieu vao 'data_lastest'
#             db.data_lastest.update_or_insert(
#                 db.data_lastest.station_id == station_id,           # dieu kien
#                 station_id = station_id,
#                 get_time = get_time,
#                 is_exceed = is_exceed,
#                 data = data
#             )
#
#             # Update bang 'last_data_files'
#             db.last_data_files.update_or_insert(
#                 db.last_data_files.station_id == station_id,        # dieu kien
#                 station_id = station_id,
#                 filename = basename,
#                 lasttime = get_time,
#                 station_name = station_names.get(station_id)
#             )
#
#             # Update bang canh bao cho chi so 'data_alarm'
#             if is_exceed:
#                 db.data_alarm.insert(
#                     station_id = station_id,
#                     get_time = get_time,
#                     alarm_level = 2,
#                     data = data
#                 )
#
#             # Update bang 'station_off_log'
#             for row in stations_off:
#                 if row.station_id == station_id:
#                     # Tinh khoang tgian Inactive
#                     diff = get_time - row.start_off
#                     diff = diff.days * 24 * 3600 + diff.seconds
#
#                     row.update_record(
#                         end_off = get_time,
#                         duration = diff
#                     )
#                     break       # Ly thuyet thi chi co toi da duy nhat 1 row tuong ung voi station off
#
#         db.commit()
#     except Exception as ex:
#         logger.error(str(ex))
#     finally:
#         logger.info('Finished scan minute data')
#
#     return count
################################################################################

def get_data():
    logger.info('-'*100)
    logger.info('get_data() running')
    logger.info(request.now)


    return 0

################################################################################
'''
   Using ftp get from Station info
'''
def get_data2():
    try:
        import ftplib

        count = 0               # dem nhung file duoc xu ly
        queue_station_list = []
        second_limit = 10      # Bien luu so giay gioi han de connect qua ftp voi moi station

        logger.info('-' * 80)
        logger.info('Start scan minute data')

        # Get station_codes : dict(station_code : station_id)
        # Get station_names : dict(station_id : station_name)
        station_names, _ , _ , station_codes = common.get_station_dict()
        # hungdx add last_times fix lost data (khong phai viet them ham trong common
        lastest_files_dict, last_times = common.get_lastest_files_dict()
        # Get all 'station_off_log' with records have 'end_off' field = None : co nghia nhung station dang o trang thai In-active
        stations_off = db(db.station_off_log.end_off == None).select()
        # Get all indicator and station_indicator being using
        station_indicator_dict, indicators, thresholds, preparing_dict, tendency_dict = common.get_indicator_station_info()

        # Lastest data dict with format : {station_id : {indicator : value, ...}, ...}
        lastest_data = common.get_all_data_lastest()
        # Get all station fpt info
        ftp_station_info = common.get_all_station_ftp_info()
        file_mapping = ftp_station_info[5]

        today = datetime.now()
        today_folder = '/%0.4d/%0.2d/%0.2d' % (today.year, today.month, today.day)

        for index, code in enumerate(station_codes):
            if not code:
                continue
            # Get login info
            ip = ftp_station_info[0].get(code)
            data_folder = ftp_station_info[1].get(code)
            username = ftp_station_info[2].get(code)
            pwd = ftp_station_info[3].get(code)
            port = ftp_station_info[4].get(code)
            scan_failed = ftp_station_info[6].get(code)
            retry_no = ftp_station_info[7].get(code)
            file_mapping2 = ftp_station_info[8].get(code)

            if not ip or not data_folder or not username:
                continue

            # Build lai "data_folder" them nam/thang/ngay
            data_folder_today = data_folder + today_folder
            data_folder_today = data_folder_today.replace('//', '/')    # loai bot dau /  (neu co 2 dau lien nhau)

            if ip and username and pwd :
                ftp = ftplib.FTP()
                retry = True
                while (retry):
                    try:
                        ftp = ftplib.FTP(ip)
                        ftp.connect(ip, port, second_limit)
                        ftp.login(username, pwd)
                        ftp.cwd(data_folder_today)
                        ftp.encoding = 'utf-8'
                        ftp.sendcmd('OPTS UTF8 ON')
                        logger.info(data_folder_today)
                        res = server_data.process_data(ftp, station_codes, count, lastest_files_dict, data_folder_today,
                                                 station_indicator_dict, lastest_data, station_names,
                                                 stations_off, thresholds, preparing_dict, tendency_dict, file_mapping,
                                                 code, file_mapping2)
                        retry = False

                        if res > 0:
                            queue_station_list.append(code)
                            retry = False

                            # Update status cua station la "Mat ket noi"
                            conditions = (db.stations.station_code == code)
                            conditions &= (db.stations.data_server == ip)
                            conditions &= (db.stations.data_folder == data_folder)
                            station = db(conditions).select().first()

                            if station.status != 4:
                                db(conditions).update(
                                    status=4,
                                    scan_failed = db.stations.scan_failed + 1,
                                    off_time = request.now
                                )
                            else:
                                db(conditions).update(
                                    scan_failed=db.stations.scan_failed + 1,
                                )
                            # Update station_off_log
                            if scan_failed + 1 == retry_no:
                                db.station_off_log.insert(
                                    station_id = str(station.id),
                                    station_name = station.station_name,
                                    province_id = station.province_id,
                                    station_type = station.station_type,
                                    start_off = request.now,
                                )
                            db.commit()
                            continue

                    except Exception as e:
                        queue_station_list.append(code)
                        retry = False

                        # Update status cua station la "Mat ket noi"
                        conditions = (db.stations.station_code == code)
                        conditions &= (db.stations.data_server == ip)
                        conditions &= (db.stations.data_folder == data_folder)
                        station = db(conditions).select().first()

                        if station.status != 4:
                            db(conditions).update(
                                status=4,
                                scan_failed = db.stations.scan_failed + 1,
                                off_time = request.now
                            )
                        else:
                            db(conditions).update(
                                scan_failed=db.stations.scan_failed + 1,
                            )
                        # Update station_off_log
                        if scan_failed + 1 == retry_no:
                            db.station_off_log.insert(
                                station_id = str(station.id),
                                station_name = station.station_name,
                                province_id = station.province_id,
                                station_type = station.station_type,
                                start_off = request.now,
                            )
                        db.commit()
                        continue

        # Reconnect for station on queue_station_list
        logger.info('retry queue_station_list')
        for s_code in queue_station_list:
            ip = ftp_station_info[0].get(s_code)
            data_folder = ftp_station_info[1].get(s_code)
            username = ftp_station_info[2].get(s_code)
            pwd = ftp_station_info[3].get(s_code)
            port = ftp_station_info[4].get(s_code)

            # Build lai "data_folder" them nam/thang/ngay
            data_folder_today = data_folder + today_folder
            data_folder_today = data_folder_today.replace('//', '/')  # loai bot dau /  (neu co 2 dau lien nhau)
            logger.info(data_folder_today)
            if ip and username and pwd :
                ftp = ftplib.FTP()
                retry = True
                while (retry):
                    try:
                        ftp = ftplib.FTP()
                        ftp.connect(ip, port, second_limit)
                        ftp.login(username, pwd)
                        ftp.cwd(data_folder_today)
                        ftp.encoding = 'utf-8'
                        ftp.sendcmd('OPTS UTF8 ON')
                        server_data.process_data(ftp, station_codes, count, lastest_files_dict, data_folder_today,
                                                 station_indicator_dict, lastest_data, station_names,
                                                 stations_off, thresholds, preparing_dict, tendency_dict, file_mapping, s_code)
                        retry = False
                    except Exception as e:
                        logger.error('Error {}'.format(e.message))
                        retry = False
                        continue

    except Exception as ex:
        logger.error(str(ex))
    finally:
        logger.info('Finished scan minute data')

    return count

################################################################################
#Hungdx fix lost data
def get_data2_new():
    try:
        import ftplib

        count = 0               # dem nhung file duoc xu ly
        queue_station_list = []
        second_limit = 10      # Bien luu so giay gioi han de connect qua ftp voi moi station

        logger.info('-' * 80)
        logger.info('Start scan minute data')

        # Get station_codes : dict(station_code : station_id)
        # Get station_names : dict(station_id : station_name)
        station_names, _ , _ , station_codes = common.get_station_dict()
        #lastest_files_dict = common.get_lastest_files_dict()
        #hungdx fix lost data
        lastest_files_dict, last_times = common.get_lastest_files_dict_new()
        # Get all 'station_off_log' with records have 'end_off' field = None : co nghia nhung station dang o trang thai In-active
        stations_off = db(db.station_off_log.end_off == None).select()
        # Get all indicator and station_indicator being using
        station_indicator_dict, indicators, thresholds, preparing_dict, tendency_dict = common.get_indicator_station_info()

        # Lastest data dict with format : {station_id : {indicator : value, ...}, ...}
        lastest_data = common.get_all_data_lastest()
        # Get all station fpt info
        ftp_station_info = common.get_all_station_ftp_info()
        file_mapping = ftp_station_info[5]

        today = datetime.now()
        today_folder = '/%0.4d/%0.2d/%0.2d' % (today.year, today.month, today.day)

        for index, code in enumerate(station_codes):
            if not code:
                continue
            # Get login info
            ip = ftp_station_info[0].get(code)
            data_folder = ftp_station_info[1].get(code)
            username = ftp_station_info[2].get(code)
            pwd = ftp_station_info[3].get(code)
            port = ftp_station_info[4].get(code)
            scan_failed = ftp_station_info[6].get(code)
            retry_no = ftp_station_info[7].get(code)
            file_mapping2 = ftp_station_info[8].get(code)

            if not ip or not data_folder or not username:
                continue

            station_id = station_codes.get(code)
            last_day = last_times.get(station_id)
            if last_day:
                last_day = last_day
            else:
                last_day = today - timedelta(days=100)

            while last_day < today + timedelta(days=1):
            # Build lai "data_folder" them nam/thang/ngay
                day_caculater = last_day
                day_caculater_folder = '/%0.4d/%0.2d/%0.2d' % (day_caculater.year, day_caculater.month,
                                                               day_caculater.day)
                data_folder_today = data_folder + day_caculater_folder
                data_folder_today = data_folder_today.replace('//', '/')    # loai bot dau /  (neu co 2 dau lien nhau)
                if ip and username and pwd :
                    ftp = ftplib.FTP()
                    retry = True
                    while (retry):
                        try:
                            ftp = ftplib.FTP(ip)
                            ftp.connect(ip, port, second_limit)
                            ftp.login(username, pwd)
                            ftp.cwd(data_folder_today)
                            ftp.encoding = 'utf-8'
                            ftp.sendcmd('OPTS UTF8 ON')
                            logger.info(data_folder_today)
                            res = server_data.process_data(ftp, station_codes, count, lastest_files_dict, data_folder_today,
                                                 station_indicator_dict, lastest_data, station_names,
                                                 stations_off, thresholds, preparing_dict, tendency_dict, file_mapping,
                                                 code, file_mapping2)
                            retry = False

                            if res > 0:
                                queue_station_list.append(code)
                                retry = False

                                # Update status cua station la "Mat ket noi"
                                conditions = (db.stations.station_code == code)
                                conditions &= (db.stations.data_server == ip)
                                conditions &= (db.stations.data_folder == data_folder)
                                station = db(conditions).select().first()

                                if station.status != 4:
                                    db(conditions).update(
                                        status=4,
                                        scan_failed = db.stations.scan_failed + 1,
                                        off_time = request.now
                                    )
                                else:
                                    db(conditions).update(
                                        scan_failed=db.stations.scan_failed + 1,
                                    )
                                # Update station_off_log
                                if scan_failed + 1 == retry_no:
                                    db.station_off_log.insert(
                                        station_id = str(station.id),
                                        station_name = station.station_name,
                                        province_id = station.province_id,
                                        station_type = station.station_type,
                                        start_off = request.now,
                                    )
                                db.commit()
                                continue

                        except Exception as e:
                            queue_station_list.append(code)
                            retry = False

                            # Update status cua station la "Mat ket noi"
                            conditions = (db.stations.station_code == code)
                            conditions &= (db.stations.data_server == ip)
                            conditions &= (db.stations.data_folder == data_folder)
                            station = db(conditions).select().first()

                            if station.status != 4:
                                db(conditions).update(
                                    status=4,
                                    scan_failed = db.stations.scan_failed + 1,
                                    off_time = request.now
                                )
                            else:
                                db(conditions).update(
                                    scan_failed=db.stations.scan_failed + 1,
                                )
                            # Update station_off_log
                            if scan_failed + 1 == retry_no:
                                db.station_off_log.insert(
                                    station_id = str(station.id),
                                    station_name = station.station_name,
                                    province_id = station.province_id,
                                    station_type = station.station_type,
                                    start_off = request.now,
                                )
                            db.commit()
                            continue
                last_day = last_day + timedelta(days=1)
                pass
            # Reconnect for station on queue_station_list
        logger.info('retry queue_station_list')
        for s_code in queue_station_list:
            ip = ftp_station_info[0].get(s_code)
            data_folder = ftp_station_info[1].get(s_code)
            username = ftp_station_info[2].get(s_code)
            pwd = ftp_station_info[3].get(s_code)
            port = ftp_station_info[4].get(s_code)

            station_id = station_codes.get(s_code)
            last_day = last_times.get(station_id)
            if last_day:
                last_day = last_day
            else:
                last_day = today - timedelta(days=100)

            while last_day < today + timedelta(days=1):
                # Build lai "data_folder" them nam/thang/ngay
                day_caculater = last_day
                day_caculater_folder = '/%0.4d/%0.2d/%0.2d' % (day_caculater.year, day_caculater.month,
                                                               day_caculater.day)
                data_folder_today = data_folder + day_caculater_folder
                data_folder_today = data_folder + data_folder_today
                data_folder_today = data_folder_today.replace('//', '/')  # loai bot dau /  (neu co 2 dau lien nhau)
                logger.info(data_folder_today)
                if ip and username and pwd :
                    ftp = ftplib.FTP()
                    retry = True
                    while (retry):
                        try:
                            ftp = ftplib.FTP()
                            ftp.connect(ip, port, second_limit)
                            ftp.login(username, pwd)
                            ftp.cwd(data_folder_today)
                            ftp.encoding = 'utf-8'
                            ftp.sendcmd('OPTS UTF8 ON')
                            server_data.process_data(ftp, station_codes, count, lastest_files_dict, data_folder_today,
                                                 station_indicator_dict, lastest_data, station_names,
                                                 stations_off, thresholds, preparing_dict, tendency_dict, file_mapping, s_code)
                            retry = False
                        except Exception as e:
                            logger.error('Error {}'.format(e.message))
                            retry = False
                            continue
                last_day = last_day + timedelta(days=1)
                pass
    except Exception as ex:
        logger.error(str(ex))
    finally:
        logger.info('Finished scan minute data')

    return count
################################################################################
'''
    Batch chạy 10p/lần
    Tinh toan du lieu cho bảng 'data_min_collect'
'''
def calc_data_min_collect(year = 0, month = 0):
    try:
        logger.info('Start calculate data min collect')
        today = datetime.now()
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

        first_date_in_this_month = '%s%s01000000' %('%0.4d' %year, '%0.2d' %month)
        first_date_in_this_month = datetime.strptime(first_date_in_this_month, '%Y%m%d%H%M%S')
        next_month = month + 1
        next_year = year
        if next_month > 12:
            next_month = 1
            next_year += 1
        first_date_in_next_month = '%s%s01000000' %('%0.4d' %next_year, '%0.2d' %next_month)
        first_date_in_next_month = datetime.strptime(first_date_in_next_month, '%Y%m%d%H%M%S')

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
'''
   Using ftp get from Station info
'''
def get_data22():
    try:
        from datetime import datetime
        from datetime import timedelta
        import ftplib

        count = 0               # dem nhung file duoc xu ly
        queue_station_list = []
        second_limit = 10      # Bien luu so giay gioi han de connect qua ftp voi moi station

        logger.info('-' * 80)
        logger.info('Start scan minute data')

        # Get station_codes : dict(station_code : station_id)
        # Get station_names : dict(station_id : station_name)
        station_names, _ , _ , station_codes = common.get_station_dict()
        lastest_files_dict = common.get_lastest_files_dict()
        # Get all 'station_off_log' with records have 'end_off' field = None : co nghia nhung station dang o trang thai In-active
        stations_off = db(db.station_off_log.end_off == None).select()
        # Get all indicator and station_indicator being using
        station_indicator_dict, indicators, thresholds, preparing_dict, tendency_dict = common.get_indicator_station_info()

        # Lastest data dict with format : {station_id : {indicator : value, ...}, ...}
        lastest_data = common.get_all_data_lastest()
        # Get all station fpt info
        ftp_station_info = common.get_all_station_ftp_info()
        file_mapping = ftp_station_info[5]
        from_date = datetime.strptime('2019-01-01', '%Y-%m-%d')
        to_date = datetime.strptime('2019-01-06', '%Y-%m-%d')
        while from_date <= to_date:
            today = from_date
            today_folder = '/%0.4d/%0.2d/%0.2d' % (today.year, today.month, today.day)

            for index, code in enumerate(station_codes):
                if not code:
                    continue
                # Get login info
                ip = ftp_station_info[0].get(code)
                data_folder = ftp_station_info[1].get(code)
                username = ftp_station_info[2].get(code)
                pwd = ftp_station_info[3].get(code)
                port = ftp_station_info[4].get(code)
                scan_failed = ftp_station_info[6].get(code)
                retry_no = ftp_station_info[7].get(code)
                file_mapping2 = ftp_station_info[8].get(code)

                if not ip or not data_folder or not username:
                    continue

                # Build lai "data_folder" them nam/thang/ngay
                data_folder_today = data_folder + today_folder
                data_folder_today = data_folder_today.replace('//', '/')    # loai bot dau /  (neu co 2 dau lien nhau)

                if ip and username and pwd :
                    ftp = ftplib.FTP()
                    retry = True
                    while (retry):
                        try:
                            ftp = ftplib.FTP(ip)
                            ftp.connect(ip, port, second_limit)
                            ftp.login(username, pwd)
                            ftp.cwd(data_folder_today)
                            ftp.encoding = 'utf-8'
                            ftp.sendcmd('OPTS UTF8 ON')
                            server_data.process_data(ftp, station_codes, count, lastest_files_dict, data_folder_today,
                                                     station_indicator_dict, lastest_data, station_names,
                                                     stations_off, thresholds, preparing_dict, tendency_dict, file_mapping,
                                                     code, file_mapping2)
                            retry = False
                        except Exception as e:
                            queue_station_list.append(code)
                            retry = False

                            # Update status cua station la "Mat ket noi"
                            conditions = (db.stations.station_code == code)
                            conditions &= (db.stations.data_server == ip)
                            conditions &= (db.stations.data_folder == data_folder)
                            station = db(conditions).select().first()

                            if station.status != 4:
                                db(conditions).update(
                                    status=4,
                                    scan_failed = db.stations.scan_failed + 1,
                                    off_time = request.now
                                )
                            else:
                                db(conditions).update(
                                    scan_failed=db.stations.scan_failed + 1,
                                )
                            # Update station_off_log
                            if scan_failed + 1 == retry_no:
                                db.station_off_log.insert(
                                    station_id = str(station.id),
                                    station_name = station.station_name,
                                    province_id = station.province_id,
                                    station_type = station.station_type,
                                    start_off = request.now,
                                )
                            db.commit()
                            continue

            # Reconnect for station on queue_station_list
            for s_code in queue_station_list:
                ip = ftp_station_info[0].get(s_code)
                data_folder = ftp_station_info[1].get(s_code)
                username = ftp_station_info[2].get(s_code)
                pwd = ftp_station_info[3].get(s_code)
                port = ftp_station_info[4].get(s_code)

                # Build lai "data_folder" them nam/thang/ngay
                data_folder_today = data_folder + today_folder
                data_folder_today = data_folder_today.replace('//', '/')  # loai bot dau /  (neu co 2 dau lien nhau)

                if ip and username and pwd :
                    ftp = ftplib.FTP()
                    retry = True
                    while (retry):
                        try:
                            ftp = ftplib.FTP()
                            ftp.connect(ip, port, second_limit)
                            ftp.login(username, pwd)
                            ftp.cwd(data_folder_today)
                            ftp.encoding = 'utf-8'
                            ftp.sendcmd('OPTS UTF8 ON')
                            server_data.process_data(ftp, station_codes, count, lastest_files_dict, data_folder_today,
                                                     station_indicator_dict, lastest_data, station_names,
                                                     stations_off, thresholds, preparing_dict, tendency_dict, file_mapping)
                            retry = False
                        except Exception as e:
                            logger.error('Error {}'.format(e.message))
                            retry = False
                            continue

            from_date += timedelta(days=1)
            pass

    except Exception as ex:
        logger.error(str(ex))
    finally:
        logger.info('Finished scan minute data')

    return count

################################################################################
'''
    Batch chạy 1h/lần
    Đọc dữ liệu ở bảng 'data_min' (trong ngày) tính trung bình giá trị các chỉ só theo giờ
'''
def calc_data_hour(start = datetime.now(), end = datetime.now()):
    try:
        logger.info('Start calculate hour data')
        
        # Start of day
        start = start.replace(hour = 0, minute = 0, second = 0, microsecond = 0)
        end   = end.replace(hour = 23, minute = 55, second = 0, microsecond = 0)
        
        # Get data from 'data_min' for calculate
        conditions =  (db.data_min.get_time >= start)
        conditions &= (db.data_min.get_time <= end)
        data_mins = db(conditions).select(orderby = db.data_min.station_id | db.data_min.get_time)
        
        # Get data from 'data_hour' to compare, 
        conditions =  (db.data_hour.get_time >= start)
        conditions &= (db.data_hour.get_time <= end)
        data_hours = db(conditions).select(orderby = db.data_hour.station_id | db.data_hour.get_time)
        
        # Bien cac du lieu gio, phut sang kieu dict
        data_mins_dict = dict()         # co dang {station_id : [mang cac row]}
        data_hours_lastest = dict()     # co dang {station_id : datetime}
        
        for item in data_mins:
            if data_mins_dict.has_key(item.station_id):
                data_mins_dict[item.station_id].append(item)
            else:
                data_mins_dict[item.station_id] = [item]
        
        for item in data_hours:
            data_hours_lastest[item.station_id] = item.get_time
        
        # Tinh trung binh theo gio
        # Tinh lai ca gio ngay truoc do (tranh truong hop gio truoc bi tinh chua du data_min)
        for station_id in data_mins_dict.keys():
            # Neu ko co du lieu gio (tu thoi diem "start" cua station_id, thi lay thoi diem la ngay gio cua record dau tien
            if not data_hours_lastest.has_key(station_id):
                if data_mins_dict[station_id]:
                    start = data_mins_dict[station_id][0].get_time.replace(minute = 0, second = 0, microsecond = 0)
                    indicator_calc.hour_data_calc(station_id, data_mins_dict[station_id], start)
            else:
                indicator_calc.hour_data_calc(station_id, data_mins_dict[station_id], data_hours_lastest[station_id])
                
        db.commit()
    except Exception as ex:
        logger.error(str(ex))
    finally:
        logger.info('End calculate hour data')
        
    return 
    
################################################################################
'''
    Batch chạy 1 ngày/lần
    Đọc dữ liệu ở bảng 'data_hour' (trong ngày) tính trung bình giá trị các chỉ só theo ngày
'''
def calc_data_day(start = datetime.now()):
    try:
        logger.info('Start calculate day data')
        
        # Start day to get data
        # Get data from previous day de tinh toan lai, de phong hom truoc chua tinh du du lieu gio
        start = start - timedelta(days = 1)
        start = start.replace(hour = 0, minute = 0, second = 0, microsecond = 0)
        
        # Get data from 'data_hour' for calculate
        data_hours = db(db.data_hour.get_time >= start).select(orderby = db.data_hour.station_id | db.data_hour.get_time)
        
        # Get data from 'data_day' to compare, 
        data_days = db(db.data_day.get_time >= start.date()).select(orderby = db.data_day.station_id | db.data_day.get_time)
        
        # Bien cac du lieu gio, phut sang kieu dict
        data_hours_dict = dict()        # co dang {station_id : [mang cac row]}
        data_days_lastest = dict()      # co dang {station_id : date}
        
        for item in data_hours:
            if data_hours_dict.has_key(item.station_id):
                data_hours_dict[item.station_id].append(item)
            else:
                data_hours_dict[item.station_id] = [item]
        
        for item in data_days:
            data_days_lastest[item.station_id] = item.get_time

        # Tinh trung binh theo ngay
        # Tinh lai ca ngay truoc do (tranh truong hop ngay truoc tinh khi chua du data_hour)
        for station_id in data_hours_dict.keys():
            if not data_days_lastest.has_key(station_id):
                if data_hours_dict[station_id]:
                    start = data_hours_dict[station_id][0].get_time.date()
                    indicator_calc.day_data_calc(station_id, data_hours_dict[station_id], start)
            else:
                indicator_calc.day_data_calc(station_id, data_hours_dict[station_id], data_days_lastest[station_id])
        
        db.commit()
    except Exception as ex:
        logger.error(str(ex))
    finally:
        logger.info('End calculate day data')
        
    return
################################################################################
#hungdx new function
def calc_data_hour_new():
    try:
        logger.info('Start calculate hour data new')
        # lay danh sach cac tram (theo code tram - truoc lam code tram)
        _, _, _, station_codes = common.get_station_dict()
        # lay danh sach time tinh cuoi cung cua data hour
        lastest_hours = common.get_lastest_hour_calcu()

        #vong lap
        for index, code in enumerate(station_codes):
            if not code:
                continue
            station_id = station_codes.get(code)
            if not station_id:
                continue
            last_hour = lastest_hours.get(station_id)
            current_time = datetime.now()
            if last_hour:
                last_hour = last_hour - timedelta(hours=1) #neu co du lieu cuoi thi tinh lai 1h truoc do
            else:
                last_hour = current_time - timedelta(hours=24000) #neu khong co du lieu thi tinh tu 1000 ngay tu hien tai
            while last_hour < current_time:
                try:
                    start = last_hour.replace(minute=0, second=0, microsecond=0)
                    end = start + timedelta(hours=1)
                    conditions = (db.data_min.station_id == station_id)
                    conditions &= (db.data_min.get_time >= start)
                    conditions &= (db.data_min.get_time < end)
                    data_mins = db(conditions).select(orderby=db.data_min.get_time)
                    if data_mins:
                        indicator_calc.hour_data_calc(station_id, data_mins, start)
                        db.commit()
                except Exception as ex:
                    logger.error(str(ex))
                last_hour = last_hour + timedelta(hours=1)
                pass
    except Exception as ex:
        logger.error(str(ex))
    finally:
        logger.info('End calculate hour data new')

    return

########################################################################################
def calc_data_day_new():
    try:
        logger.info('Start calculate day data new')
        _, _, _, station_codes = common.get_station_dict()
        # lay danh sach time tinh cuoi cung cua data day
        lastest_days = common.get_lastest_day_calcu()

        # vong lap
        for index, code in enumerate(station_codes):
            if not code:
                continue

            station_id = station_codes.get(code)
            if not station_id:
                continue
            last_days = lastest_days.get(station_id)
            current_time = datetime.now()
            if last_days:
                last_days = last_days - timedelta(days=1)  # neu co du lieu cuoi thi tinh lai 1h truoc do
            else:
                last_days = current_time - timedelta(days=1000)  # neu khong co du lieu thi tinh tu 1000 ngay tu hien tai
            while last_days < current_time:
                try:
                    start = last_days.replace(hour=0, minute=0, second=0, microsecond=0)
                    end = start + timedelta(days=1)
                    conditions = (db.data_hour.station_id == station_id)
                    conditions &= (db.data_hour.get_time >= start)
                    conditions &= (db.data_hour.get_time < end)
                    data_hours = db(conditions).select(orderby=db.data_hour.get_time)
                    if data_hours:
                        indicator_calc.day_data_calc(station_id, data_hours, start)
                        db.commit()
                except Exception as ex:
                    logger.error(str(ex))
                last_days = last_days + timedelta(days=1)
            pass
        db.commit()
    except Exception as ex:
        logger.error(str(ex))
    finally:
        logger.info('End calculate day data new')

    return


################################################################################
def calc_data_month_new():
    try:
        logger.info('Start calculate month data new')
        _, _, _, station_codes = common.get_station_dict()
        # lay danh sach time tinh cuoi cung cua data hour
        lastest_month = common.get_lastest_month_calcu()

        # vong lap
        for index, code in enumerate(station_codes):
            if not code:
                continue
            station_id = station_codes.get(code)
            if not station_id:
                continue
            last_month = lastest_month.get(station_id)
            current_time = datetime.now()
            if last_month:
                last_month = last_month # month khac chut nen phai tinh lai cho dung
            else:
                last_month = current_time - timedelta(days=1000)  # neu khong co du lieu thi tinh tu 1000 ngay tu hien tai
            # tinh lui lai 1 month
            start_month = last_month.replace(day=1, hour=0, minute=0, second=0, microsecond=0) # chuyen ve mung 1
            result_month_start = start_month - timedelta(days=2)
            start = result_month_start.replace(day=1, hour=0, minute=0, second=0, microsecond=0)
            current_time = current_time.replace(day=1, hour=0, minute=0, second=0, microsecond=0)

            while start < current_time:
                end_month = start.replace(day=28, hour=0, minute=0, second=0, microsecond=0)
                result_month_end = end_month + timedelta(days=5)
                end = result_month_end.replace(day=1, hour=0, minute=0, second=0, microsecond=0)
                try:
                    conditions = (db.data_day.station_id == station_id)
                    conditions &= (db.data_day.get_time >= start)
                    conditions &= (db.data_day.get_time < end)
                    data_days = db(conditions).select(orderby=db.data_day.get_time)
                    if data_days:
                        indicator_calc.mon_data_calc(station_id, data_days, start)
                        db.commit()
                except Exception as ex:
                    logger.error(str(ex))
                start = end
            pass
        db.commit()
    except Exception as ex:
        logger.error(str(ex))
    finally:
        logger.info('End calculate month data new')

    return
#hungdx end add issue 30
################################################################################
def calc_data_month(start = datetime.now()):
    try:
        logger.info('Start calculate month data')
        
        # Start day to get data
        # Get data tu ngay dau tien cua thang truoc de tinh toan lai, de phong thang truoc chua tinh du du lieu ngay
        start = start.replace(day = 1) - timedelta(days = 1)
        start = start.replace(day = 1, hour = 0, minute = 0, second = 0, microsecond = 0)
        start = start.date()
        
        # Get data from 'data_hour' for calculate
        data_days = db(db.data_day.get_time >= start).select(
            db.data_day.station_id,
            db.data_day.get_time,
            db.data_day.data,
            orderby = db.data_day.station_id | db.data_day.get_time)
        
        # Get data from 'data_day' to compare, 
        data_mons = db(db.data_mon.get_time >= start).select(
            db.data_mon.station_id,
            db.data_mon.get_time,
            db.data_mon.data,
            orderby = db.data_mon.station_id | db.data_mon.get_time)
        
        # Bien cac du lieu gio, phut sang kieu dict
        data_days_dict = dict()        # co dang {station_id : [mang cac row]}
        data_mons_lastest = dict()      # co dang {station_id : date}
        
        for item in data_days:
            if data_days_dict.has_key(item.station_id):
                data_days_dict[item.station_id].append(item)
            else:
                data_days_dict[item.station_id] = [item]
        
        for item in data_mons:
            data_mons_lastest[item.station_id] = item.get_time

        # Tinh trung binh theo ngay
        # Tinh lai ca ngay truoc do (tranh truong hop ngay truoc tinh khi chua du data_hour)
        for station_id in data_days_dict.keys():
            if not data_mons_lastest.has_key(station_id):
                if data_days_dict[station_id]:
                    start = data_days_dict[station_id][0].get_time.replace(day=1)
                    indicator_calc.mon_data_calc(station_id, data_days_dict[station_id], start)
            else:
                indicator_calc.mon_data_calc(station_id, data_days_dict[station_id], data_mons_lastest[station_id])
        
        db.commit()
    except Exception as ex:
        logger.error(str(ex))
    finally:
        logger.info('End calculate month data')
        
    return    

################################################################################    
def calc_aqi_data_hour(start = datetime.now()):
    try:
        logger.info('Start calculate AQI data hour')
        
        # Start of day
        start = start.replace(hour = 0, minute = 0, second = 0, microsecond = 0)
        
        # Chi loai station_type = 3, 4 and is_qi = True
        conditions = (db.stations.station_type.belongs([const.STATION_TYPE['AMBIENT_AIR']['value'], const.STATION_TYPE['STACK_EMISSION']['value']]))  
        conditions &= (db.stations.is_qi == True)
        ambients = db(conditions).select(db.stations.id)
        ambients = [str(station.id) for station in ambients]
        
        # Get data from 'data_hour' tu cac station o tren de tinh toan 
        conditions = (db.data_hour.station_id.belongs(ambients))
        conditions &= (db.data_hour.get_time >= start)
        data_hours = db(conditions).select(orderby = db.data_hour.station_id | db.data_hour.get_time)
        
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
                            get_time = item.get_time.replace(minute=0, second=0, microsecond=0)  # Chuan hoa : cat minute, second ve 0
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
    return 
    
################################################################################    
def calc_aqi_data_24h(start = datetime.now()):
    try:
        logger.info('Start calculate AQI data day')

        # Start of day
        start = start.replace(hour = 0, minute = 0, second = 0, microsecond = 0)
        currentStart = datetime.now();
        currentStart = currentStart.replace(hour=0, minute=0, second=0, microsecond=0)
        # Xử lý fix ko cho tính ngày hiện tại
        if (start == currentStart):
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
            day_data = item.data  # Du lieu quan trac trung binh 1 ngay cua thong so = SUM/count
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

################################################################################    
def calc_wqi_data_hour(start = datetime.now()):
    try:
        logger.info('Start calculate WQI data hour')
        
        # Start of day
        start = start.replace(hour = 0, minute = 0, second = 0, microsecond = 0)
        type = [
            const.STATION_TYPE['WASTE_WATER']['value'], 
            const.STATION_TYPE['SURFACE_WATER']['value'], 
            const.STATION_TYPE['UNDERGROUND_WATER']['value']
        ]
        # Chi loai station_type = 0,1,2 and is_qi = True
        conditions = (db.stations.station_type.belongs(type))
        conditions &= (db.stations.is_qi == True)
        waters = db(conditions).select(db.stations.id)
        waters = [str(station.id) for station in waters]
        
        # Get data from 'data_hour' tu cac station o tren de tinh toan 
        conditions = (db.data_hour.station_id.belongs(waters))
        conditions &= (db.data_hour.get_time >= start)
        data_hours = db(conditions).select(orderby = db.data_hour.station_id | db.data_hour.get_time)
        
        # Cac chi so qui chuan cua cac indicator
        # duoc dinh nghia trong const : WQI_BP, QI, DO_BP, DO_QI, PH_BP, PH_QI
        
        for item in data_hours:
            data = {'wqi' : 0}           # du lieu WQI se insert/update vao bang 'wqi_data_hour'
            hour_data = item.data
            
            # Dieu kien can : trong hour_data du cac indicator (WQI_INDICATOR, DO, PH, Temp)
            # convert key sang upper() de so sanh
            keys = [x.upper() for x in hour_data.keys()]
            
            condition = set(const.WQI_INDICATOR_ALL).issubset(set(keys))
            
            if not condition:
                continue
                
            # Tinh toan gtri WQI cho tung cac indicator
            for indicator in hour_data.keys():
                # Chi lay nhung chi so WQI : BOD5, COD, N-NH4, P-PO4, Turbidity, TSS, Coliform
                if indicator.upper() in const.WQI_INDICATOR:
                    # Tim nguong "i" cua indicator
                    i = 0
                    # Thuc hien phep so sanh : operator(a, b)
                    while not const.OP_1[indicator.upper()][i]( hour_data[indicator], const.WQI_BP[indicator.upper()][i] ):
                        i +=1
                    # Neu gia tri chi so bang dung gtri BP nguong "i-1" thi WQI = q cua nguong "i"
                    if const.WQI_BP[indicator.upper()][i - 1] == hour_data[indicator]:
                        data[indicator] = const.QI[i]
                    else:
                        # Ap cong thuc tinh WQI cho chi so "indicator" voi nguong "i":
                        if i + 1 == len(const.QI):
                            data[indicator] = const.QI[i]
                        else:
                            data[indicator] = wqi.formular_1(const.QI[i-1], const.QI[i], const.WQI_BP[indicator.upper()][i-1], const.WQI_BP[indicator.upper()][i], hour_data[indicator])
                    
                elif indicator.upper() == 'DO':
                    # Tinh DO bao hoa
                    do_baohoa = wqi.do_baohoa(hour_data['Temp'])
                    do_baohoa_percent = hour_data['DO'] / do_baohoa * 100
                    
                    if const.OP_2[0]( do_baohoa_percent, const.DO_BP[0] ):     # Neu gtri <= 20 : WQI cua DO = 1
                        data['DO'] = const.DO_QI[0]
                    elif const.OP_2[9]( do_baohoa_percent, const.DO_BP[9] ):   # Neu gtri >= 200: WQI cua DO = 1
                        data['DO'] = const.DO_QI[9]
                    else:
                        i = 1
                        # Thuc hien phep so sanh : operator(a, b)
                        while not const.OP_2[i]( do_baohoa_percent, const.DO_BP[i] ):
                            i += 1
                        # Neu gtri < 88
                        if i <= 4:
                            data['DO'] = wqi.formular_2( const.DO_QI[i - 1], const.DO_QI[i], const.DO_BP[i - 1], const.DO_BP[i], do_baohoa_percent)
                        elif i == 5:    # neu 88 <= gtri <= 112
                            data['DO'] = const.DO_QI[5]
                        else:           # neu 112 < gtri < 200
                            data['DO'] = wqi.formular_1( const.DO_QI[i - 1], const.DO_QI[i], const.DO_BP[i - 1], const.DO_BP[i], do_baohoa_percent)
                            
                elif indicator.upper() == 'PH':
                    if const.OP_3[0]( hour_data['pH'], const.PH_BP[0] ):     # Neu gtri <= 5.5 : WQI cua pH = 1
                        data['pH'] = const.PH_QI[0]
                    elif const.OP_3[5]( hour_data['pH'], const.PH_BP[5] ):   # Neu gtri >= 9:    WQI cua pH = 1
                        data['pH'] = const.PH_QI[5]
                    else:
                        i = 1
                        # Thuc hien phep so sanh : operator(a, b)
                        while not const.OP_3[i]( hour_data['pH'], const.PH_BP[i] ):
                            i += 1
                        # Neu gtri < 6
                        if i <= 2:      # neu 5.5 < gtri < 6
                            data['pH'] = wqi.formular_2( const.PH_QI[i - 1], const.PH_QI[i], const.PH_BP[i - 1], const.PH_BP[i], hour_data['pH'])
                        elif i == 5:    # gtri >= 9
                            data['pH'] = const.PH_QI[5]
                        else:           # neu 8.5 < gtri < 9
                            data['pH'] = wqi.formular_1( const.PH_QI[i - 1], const.PH_QI[i], const.PH_BP[i - 1], const.PH_BP[i], hour_data['pH'])
                    
            # Tinh WQI tong hop
            temp_a, temp_b = 0, 0
            for k in const.WQI_INDICATOR_A:
                for m in data:
                    if m.upper() == k:
                        temp_a +=  data[m]
                        break
            for k in const.WQI_INDICATOR_B:
                for m in data:
                    if m.upper() == k:
                        temp_b +=  data[m]
                        break
                
            data['wqi'] = data['pH']/100*(0.2 * temp_a * 0.5 * temp_b * data['Coliform'])**(1./3)
            data['wqi'] = round(data['wqi'])
            
            # insert/update bang 'wqi_data_hour'
            get_time = item.get_time.replace(minute = 0, second = 0, microsecond = 0)   # Chuan hoa : cat minute, second ve 0
            
            db.wqi_data_hour.update_or_insert(
                (db.wqi_data_hour.station_id == item.station_id) & (db.wqi_data_hour.get_time == get_time),
                station_id = item.station_id,
                get_time = get_time,
                data = data
            )
            # Update WQI cho station
            db(db.stations.id == item.station_id).update(qi = data['wqi'], qi_time = get_time)
        db.commit()
    except Exception as ex:
        logger.error(str(ex))
    finally:
        logger.info('End calculate WQI data hour')
    return

def get_list_report_data_info_5_all(station_type, from_date, to_date, view_type, added_stations, added_columns):
    try:
        from w2pex import date_util
        if from_date:
            from_date = date_util.string_to_datetime(from_date)
        if to_date:
            to_date = date_util.string_to_datetime(to_date)
        if not station_type:
            return dict(iTotalRecords=0, iTotalDisplayRecords=0, aaData=[],
                        message=T('Select a station type for viewing data'), success=True)
        aaData = []  # Du lieu json se tra ve
        list_data = None  # Du lieu truy van duoc
        iTotalRecords = 0  # Tong so ban ghi
        table = 'data_min'
        conditions = db.stations.station_type == station_type
        if added_stations:
            conditions &= db.stations.id.belongs(added_stations)
        stations = db(conditions).select(
            db.stations.id,
            db.stations.station_name,
            db.stations.frequency_receiving_data,
        )
        table_adjust = 'data_adjust'
        iTotalRecords = len(added_stations)
        iRow = 1
        for c, station in enumerate(stations):
            station_id = station.id
            delta = to_date - from_date
            if not station.frequency_receiving_data or station.frequency_receiving_data == 5:
                total_data = int((delta.days + 1) * 288)
            else:
                freq = station.frequency_receiving_data
                total_data = int((delta.days + 1) * 24 * 60 / freq)
            # station_ids = [str(item.id) for item in stations
            conditions = (db[table]['id'] > 0)
            conditions &= (db[table]['station_id'] == station_id)
            conditions_adjust = (db[table_adjust]['id'] > 0)
            conditions_adjust &= (db[table_adjust]['station_id'] == station_id)
            if from_date:
                conditions &= (db[table]['get_time'] >= from_date)
                conditions_adjust &= (db[table_adjust]['get_time'] >= from_date)
            if to_date:
                conditions &= (db[table]['get_time'] < to_date + timedelta(days=1))
                conditions_adjust &= (db[table_adjust]['get_time'] < to_date + timedelta(days=1))
            if not from_date and not to_date:
                to_date = datetime.now()
                from_date = to_date - timedelta(days=365)
                conditions &= (db[table]['get_time'] >= from_date)
                conditions &= (db[table]['get_time'] < to_date)
                conditions_adjust &= (db[table_adjust]['get_time'] >= from_date)
                conditions_adjust &= (db[table_adjust]['get_time'] < to_date)
            list_data = []
            list_data_adjust = []
            if view_type == "1":
                list_data = db(conditions).select(db[table].id,
                                                  db[table].get_time,
                                                  db[table].station_id,
                                                  db[table].data,
                                                  )
            elif view_type == "0" or view_type == "2":
                list_data_adjust = db(conditions_adjust).select(db[table_adjust].id,
                                                                db[table_adjust].get_time,
                                                                db[table_adjust].station_id,
                                                                db[table_adjust].data,
                                                                )
            # Du lieu nhan duoc
            if view_type == '1' or view_type == '0':
                count = dict()
                for i, item in enumerate(list_data):
                    if item.data:
                        for indicator_name in item.data:
                            try:
                                z = str(item.data[indicator_name])
                                if z == 'NULL' or z == 'None' or z == '-':
                                    continue
                                name_decode = indicator_name.encode('utf-8')
                                if not count.has_key(name_decode):
                                    count[name_decode] = 1
                                else:
                                    count[name_decode] = int(count[name_decode]) + 1
                            except:
                                pass
                row = [
                    str(iRow + c),
                    station.station_name,
                ]
                content = '%s %s' % (common.convert_data(total_data), T('data'))
                row.append(content)
                content = '%s (%s)' % (T('Percent Data Recieved'), '%')
                row.append(content)
                for column in added_columns:
                    if column and count.has_key(column):
                        try:
                            v = float(count[column]) / float(total_data) * 100
                            v = common.convert_data(v)
                            row.append(v)
                        except:
                            row.append(0)
                    else:
                        row.append(0)
                aaData.append(row)
            # Du lieu hop le
            if view_type == '0':
                count = dict()
                for i, item in enumerate(list_data_adjust):
                    if item.data:
                        for indicator_name in item.data:
                            try:
                                z = str(item.data[indicator_name])
                                if z == 'NULL' or z == 'None' or z == '-':
                                    continue
                                else:
                                    x = z.replace(",", "")
                                name_decode = indicator_name
                                if not count.has_key(name_decode):
                                    count[name_decode] = 1
                                else:
                                    count[name_decode] = int(count[name_decode]) + 1
                            except:
                                pass
                row = [
                    '',
                    '',
                ]
                content = '%s %s' % (common.convert_data(total_data), T('data'))
                row.append(content)
                content = '%s (%s)' % (T('Percent Data Adjusted'), '%')
                row.append(content)
                for column in added_columns:
                    if column and count.has_key(column):
                        try:
                            v = float(count[column]) / float(total_data) * 100
                            v = common.convert_data(v)
                            row.append(v)
                        except:
                            row.append(0)
                    else:
                        row.append(0)
                aaData.append(row)
            if view_type == '2':
                count = dict()
                for i, item in enumerate(list_data_adjust):
                    if item.data:
                        for indicator_name in item.data:
                            try:
                                z = str(item.data[indicator_name])
                                if z == 'NULL' or z == 'None' or z == '-':
                                    continue
                                else:
                                    x = z.replace(",", "")
                                name_decode = indicator_name
                                if not count.has_key(name_decode):
                                    count[name_decode] = 1
                                else:
                                    count[name_decode] = int(count[name_decode]) + 1
                            except:
                                pass
                row = [
                    str(iRow + c),
                    station.station_name,
                ]
                content = '%s %s' % (common.convert_data(total_data), T('data'))
                row.append(content)
                content = '%s (%s)' % (T('Percent Data Adjusted'), '%')
                row.append(content)
                for column in added_columns:
                    if column and count.has_key(column):
                        try:
                            v = float(count[column]) / float(total_data) * 100
                            v = common.convert_data(v)
                            row.append(v)
                        except:
                            row.append(0)
                    else:
                        row.append(0)
                aaData.append(row)
        return aaData
    except Exception as ex:
        return []


def task_get_list_report_data_info_5_all(ticket_id, station_type, from_date, to_date, view_type, added_stations, added_columns , page):
    aaData = get_list_report_data_info_5_all(station_type, from_date, to_date, view_type, added_stations, added_columns)
    if page == 1:
        db(db.ticket_report.ticket_id == ticket_id).update(aaData_page_1=aaData)
    elif page == 2:
        db(db.ticket_report.ticket_id == ticket_id).update(aaData_page_2=aaData)
    elif page == 3:
        db(db.ticket_report.ticket_id == ticket_id).update(aaData_page_3=aaData)
    elif page == 4:
        db(db.ticket_report.ticket_id == ticket_id).update(aaData_page_4=aaData)
    elif page == 5:
        db(db.ticket_report.ticket_id == ticket_id).update(aaData_page_5=aaData)
    elif page == 6:
        db(db.ticket_report.ticket_id == ticket_id).update(aaData_page_6=aaData)
    elif page == 7:
        db(db.ticket_report.ticket_id == ticket_id).update(aaData_page_7=aaData)
    elif page == 8:
        db(db.ticket_report.ticket_id == ticket_id).update(aaData_page_8=aaData)
    elif page == 9:
        db(db.ticket_report.ticket_id == ticket_id).update(aaData_page_9=aaData)
    elif page == 10:
        db(db.ticket_report.ticket_id == ticket_id).update(aaData_page_10=aaData)
        
################################################################################
# Schedule object
schedule_heartbeat = 1
scheduler = Scheduler(db2,
                       tasks=dict(
                           # task_get_data = get_data,
                           # task_get_data = get_data2,
                           # hungdx fix lost data
                           # task_get_data=get_data2_new, #hungdx off issue 56
                           # task_calc_data_hour = calc_data_hour, #hungdx comment issue 30
                           # task_calc_data_day = calc_data_day,
                           # task_calc_data_month = calc_data_month,
                           # task_calc_data_hour = calc_data_hour_new, #hungdx add issue 30
                           # task_calc_data_day = calc_data_day_new, #hungdx add issue 30
                           # task_calc_data_month = calc_data_month_new,#hungdx add issue 30
                           # task_calc_aqi_data_hour = calc_aqi_data_hour,
                           # task_calc_aqi_data_24h = calc_aqi_data_24h,
                           # task_calc_wqi_data_hour = calc_wqi_data_hour,
                           # task_calc_data_min_collect = calc_data_min_collect,
                       ),
                       migrate=False,
                       worker_name=None,
                       group_names=None,
                       heartbeat=schedule_heartbeat,
                       max_empty_runs=0,
                       discard_results=False,
                       utc_time=False)
                      
def get_schedule_worker_running():
    workers = scheduler.get_workers()
    
    for key, worker in workers.items():
        last = (request.now - worker.last_heartbeat).seconds
        if last < schedule_heartbeat * 5:
            return True
    return False


# Start the worker
# If you want start multiple workers for the same app, you can do so just passing myapp,myapp
# python web2py.py -K myapp

# To add tasks via the API, use
# from datetime import timedelta
# scheduler.queue_task('mytask', start_time=request.now + timedelta(seconds=30))

# scheduler.queue_task(function,
                     # pargs=[],
                     # pvars={},
                     # start_time=now,  # datetime
                     # stop_time=None,  # datetime
                     # timeout = 60,  # seconds
                     # prevent_drift=False,
                     # period=60,  # seconds between next run
                     # immediate=False,
                     # repeats=1)

#Func for calc AQI PM
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

    if weightFactor <= float(1) / 2 :
        weightFactor = float(1) / 2
    return weightFactor


def getTruncatedPollutantConcentrationBaseOnPollutant(pollutant, concentration) :
    if (pollutant == 'PM-10') :
        return float(concentration * 100 / 150)

    if (pollutant == 'PM-2-5') :
        return float(concentration * 100 / 50)

def isValidNowcastData(data) :
    missingData = 0
    x = range(0, 2)
    for i in x:
        if (data[i] < 0) :
            missingData = missingData + 1
    return missingData

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

# Lay max api day cac chi so PM
def get_max_day_aqi_pm(station_id, indicator, time):
    try:
        aaData = []  # Du lieu json se tra ve

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
        max_day_api = max(aaData)

        return max_day_api
    except Exception as ex:
        return 0