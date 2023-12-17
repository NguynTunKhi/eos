# -*- coding: utf-8 -*-

import os
from datetime import datetime

from gluon import current
from applications.eos.modules import common
from StringIO import StringIO

################################################################################
'''
    Function get du lieu tu ftp
    Chia ra function de truong hop ko connect duoc ftp se connect lai
'''

def process_data(ftp, station_codes, count, lastest_files_dict, data_folder, station_indicator_dict,
                 lastest_data, station_names, stations_off, thresholds, preparing_dict, tendency_dict, file_mapping):
    '''
       Child class for read content file from ftp
    '''
    class ftpReader:
        def __init__(self):
            self.data = ""

        def __call__(self, s):
            self.data += s

    db = current.db
    logger = current.logger
    T = current.T

    # List all file in folder
    files = []
    ftp.retrlines("NLST", files.append)
    ### Xu ly tung file du lieu
    for fname in files:
        # Get filename only
        basename = os.path.basename(fname)

        # Neu ko tim duoc station voi CODE tuong ung hoac ko co file mapping --> skip
        # filename co format : province_stationcode_type_datetime.txt
        # se lay ma tram la "stationcode_type"
        station_code = '%s_%s' % (basename.split('_')[1], basename.split('_')[2])
        station_id = station_codes.get(station_code)
        current_fm = ''
        if not station_id:
            # Check file_mapping co hay ko
            station_id = ''
            for fm in file_mapping:
                if basename.startswith(fm):
                    station_id = file_mapping.get(fm)
                    current_fm = fm
            if not station_id:
                # Todo : ghi ra log nhung tram ko co file du lieu

                continue

        # station_id = str(station_id)
        # So sanh filename voi file lastest da doc tuong ung voi station_id
        lastest_file = lastest_files_dict.get(station_id)

        # Neu la file cu thi ko xu ly gi ca --> skip
        if lastest_file:
            if current_fm.strip() != '':                        # Neu co file mapping
                if not lastest_file.startswith(current_fm):     # Neu file ko bat dau = file mapping thi skip
                    continue
                else:
                    if basename <= lastest_file:
                        continue
            else:                               # Neu ko co file mapping
                if basename <= lastest_file:    # va file cu thi skip
                    continue

        logger.info('Processing file : %s' % basename)
        count += 1
        # r = ftpReader()
        r = StringIO()

        # Get file in binary mode

        # ftp.retrbinary('RETR ' + os.path.join(data_folder, basename), r)
        # ftp.retrbinary('RETR ' + os.path.join(data_folder, basename), r.write)
        data_folder2 = data_folder + '/' + basename
        ftp.retrbinary('RETR ' + data_folder2, r.write)
        # lines = r.data
        lines = r.getvalue()
        
        is_exceed = False
        is_preparing = False
        is_tendency = False
        is_equipment_error = False
        equipment_ids_err = []
        data_datetime = ''
        data = dict()
        for line in lines.splitlines():
            # Remove whitespace characters like `\n` at the end of each line
            line = line.strip()
            items = line.split()  # line co format :  "indicator   value   unit  datetime"
            
            try: # Try to parse value of indicator
                items[1] = float(items[1])
            except:
                items[1] = 0

            # Check indicator nay co ten Mapping ko
            for key in station_indicator_dict[station_id]:
                if station_indicator_dict[station_id][key]['mapping_name'] == items[0]:
                    items[0] = key
                    break

            # check ty le chuyen doi
            if station_indicator_dict[station_id].has_key(items[0]):
                convert_rate = station_indicator_dict[station_id][items[0]]['convert_rate'] or 1
                items[1] = items[1] * convert_rate

            # Neu indicator co trong file ma ko dang ky trong chi so cua tram thi skip
            if not thresholds.has_key(station_id) or not thresholds[station_id].has_key(items[0].upper()):
                continue

            data[items[0]] = items[1]
            data_datetime = items[3]  # datetime trong 1 file se giong het nhau

            # Chi can 1 chi so vuot nguong la danh dau 'exceed'
            if float(items[1]) > thresholds[station_id][items[0].upper()]:
                is_exceed = True
            elif float(items[1]) >= preparing_dict[station_id][items[0].upper()]:
                is_preparing = True
            elif float(items[1]) >= tendency_dict[station_id][items[0].upper()]:
                is_tendency = True

        # Neu du lieu dict la empty thi skip, ko luu DB
        if not bool(data): continue

        get_time = datetime.strptime(data_datetime, '%Y%m%d%H%M%S')
        # Insert du lieu vao DB
        # db.data_min.insert(
        #     station_id=station_id,
        #     get_time=get_time,
        #     is_exceed=is_exceed,
        #     data=data
        # )
        db.data_min.update_or_insert( (db.data_min.station_id == station_id) &
                                      (db.data_min.get_time == get_time),
            station_id=station_id,
            get_time=get_time,
            is_exceed=is_exceed,
            data=data
        )

        # Xu ly HIEU CHINH du lieu cho bang data_adjust
        data_adjust = dict()
        for indicator in data:
            if station_indicator_dict[station_id].has_key(indicator):
                try:
                    data[indicator] = float(data[indicator])
                except:
                    data[indicator] = 0
                # Check indicator value = 0 --> Sensor error
                if data[indicator] == 0:
                    is_equipment_error = True
                    if station_indicator_dict[station_id][indicator]['equipment_id']:
                        equipment_ids_err.append(station_indicator_dict[station_id][indicator]['equipment_id'])
                        db(db.equipments.id == station_indicator_dict[station_id][indicator]['equipment_id']).update(
                            status = 2
                        )

                ### Check cac dieu kien hieu chinh tu dong
                if station_indicator_dict[station_id][indicator]['continous_equal']:
                    # Get current continous equal times
                    continous_time = station_indicator_dict[station_id][indicator]['continous_times'] or 0
                    # Check indicator's value with lastest value
                    if lastest_data.has_key(station_id) and lastest_data[station_id].has_key(indicator):
                        if lastest_data[station_id][indicator] == data[indicator]:
                            continous_time += 1
                    else:
                        continous_time = 1

                    # Update continues times
                    conditions = (db.station_indicator.id == station_indicator_dict[station_id][indicator]['id'])

                    db(conditions).update(continous_times = continous_time)

                    if station_indicator_dict[station_id][indicator]['continous_equal_value'] == continous_time:
                        continue

                if station_indicator_dict[station_id][indicator]['equal0'] and data[indicator] == 0: continue


                if station_indicator_dict[station_id][indicator]['negative_value'] and data[indicator] < 0: continue

                if station_indicator_dict[station_id][indicator]['out_of_range'] and \
                        (data[indicator] > station_indicator_dict[station_id][indicator]['out_of_range_max'] or
                            data[indicator] < station_indicator_dict[station_id][indicator]['out_of_range_min']):
                    continue

                data_adjust[indicator] = data[indicator]

        if bool(data_adjust):
            # Update du lieu vao 'data_adjust'
            # db.data_adjust.insert(
            #     station_id = station_id,
            #     get_time = get_time,
            #     is_exceed = is_exceed,
            #     data = data_adjust
            # )
            db.data_adjust.update_or_insert( (db.data_adjust.station_id == station_id) &
                                             (db.data_adjust.get_time == get_time),
                station_id=station_id,
                get_time=get_time,
                is_exceed=is_exceed,
                data=data_adjust
            )

        # Update du lieu vao 'data_lastest'
        db.data_lastest.update_or_insert(
            db.data_lastest.station_id == station_id,  # dieu kien
            station_id=station_id,
            get_time=get_time,
            is_exceed=is_exceed,
            data=data
        )

        # Update bang 'last_data_files'
        db.last_data_files.update_or_insert(
            db.last_data_files.station_id == station_id,  # dieu kien
            station_id=station_id,
            filename=basename,
            lasttime=get_time,
            station_name=station_names.get(station_id)
        )

        station_status = 0      # GOOD
        # Update bang canh bao cho chi so 'data_alarm'
        alarm_level = ''
        if is_exceed:
            station_status = 3
            alarm_level = 2

        if is_preparing:
            station_status = 2

        if is_tendency:
            station_status = 1
            alarm_level = 0

        if alarm_level:
            db.data_alarm.update_or_insert(
                (db.data_alarm.station_id == station_id) &
                (db.data_alarm.get_time == get_time),
                station_id = station_id,
                get_time = get_time,
                alarm_level = alarm_level,
                data = data
            )

        # Update bang 'station_off_log'
        for row in stations_off:
            if row.station_id == station_id:
                # Tinh khoang tgian Inactive
                diff = get_time - row.start_off
                diff = diff.days * 24 * 3600 + diff.seconds

                row.update_record(
                    end_off=get_time,
                    duration=diff
                )
                break  # Ly thuyet thi chi co toi da duy nhat 1 row tuong ung voi station off

        # Update equipment status
        equip_ids = []
        for indicator in data:
            equip_id = station_indicator_dict[station_id][indicator]['equipment_id']
            if equip_id and equip_id not in equipment_ids_err:
                equip_ids.append(equip_id)
        if equip_ids:
            db(db.equipments.id.belongs(equip_ids)).update(status = 1)

        # Update station status
        if is_equipment_error:
            station_status = 6
        db(db.stations.id == station_id).update(
            status = station_status,
            scan_failed = 0
        )

        db.commit()  # Luu data vao db ngay sau khi xu ly moi tram
        
        
        
        # Xử lý gửi mail, sms
        # Get info of station_alarm
        station_alarm = db(db.station_alarm.station_id == station_id).select()
        if station_alarm:
            station_alarm = station_alarm.first()
        else:
            continue
        flag_email = False
        flag_sms = False
        # kiểm tra trạm có có phép gửi email ko?
        if station_alarm.tendency_method_email and is_tendency:
            lst_email = station_alarm.tendency_email_list
            subject = '%s %s (%s)' %(station_alarm.station_name, T('Tendency'), data_datetime)
            content = station_alarm.tendency_msg
            flag_email = True
        elif station_alarm.preparing_method_email and is_preparing:
            lst_email = station_alarm.preparing_email_list
            content = station_alarm.preparing_msg
            subject = '%s %s (%s)' % (station_alarm.station_name, T('Preparing'), data_datetime)
            flag_email = True
        elif station_alarm.exceed_method_email and is_exceed:
            lst_email = station_alarm.exceed_email_list
            content = station_alarm.exceed_msg
            subject = '%s %s (%s)' % (station_alarm.station_name, T('Exceed'), data_datetime)
            flag_email = True
        # kiểm tra trạm có có phép gửi sms ko?
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
        # if flag_email:
        #     # Send mail
        #     subject = subject
        #     message = content
        #     try:
        #         common.send_mail2(mail_to=lst_email, subject=subject, message=message)
        #     except Exception as ex:
        #         logger.error('Send mail failed')
        #         logger.error(str(ex))

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
        
    ftp.quit()

################################################################################
