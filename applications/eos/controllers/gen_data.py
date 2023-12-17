# -*- coding: utf-8 -*-
###############################################################################
# Author : 
# Date   : 
# 
# Description : 
# 
###############################################################################
from datetime import datetime, timedelta
import random, timeit

def call():
    return service()
    
################################################################################
# @decor.requires_login()
def index():
    return dict()
    
@service.json
def gen_data(*args, **kwargs):
    try:    
        get_time_str = request.vars.start
        get_time_str += ' 00:00:00'
        
        # get_time_str = '2018/09/15  00:00:00'
        # get_time = datetime.strptime(get_time_str, '%Y/%m/%d %H:%M:%S')
        get_time = datetime.strptime(get_time_str, '%Y-%m-%d %H:%M:%S')
        
        # now = datetime.now().replace(hour = 23, minute = 55, second = 0, microsecond = 0)
        now = '2018-12-11'
        now = datetime.strptime(now, '%Y-%m-%d')
        # now = now.replace(hour = 23, minute = 55, second = 0, microsecond = 0)
        
        total = 0
        start = timeit.default_timer()
        
        while get_time <= now:
            data_lastest = []
            
            nox_3_rand = random.uniform( -100, 40 )
            no_3_rand = random.uniform( -3, 3 )
            no2_3_rand = random.uniform( -10, 5 )
            so2_3_rand = random.uniform( -100, 60 )
            ph_rand = random.uniform( -5, 3 )
            orp_rand = random.uniform( -70, 50 )
            temp_rand = random.uniform( -8, 8 )
            tss_rand = random.uniform( -8, 6 )
            do_rand = random.uniform( -6, 3 )
            ec_rand = random.uniform( -100, 30 )
            o2_rand = random.uniform( -0.5, 0.3)
            cod_rand = random.uniform( -20, 5)
            toc_rand = random.uniform( -40, 20)
            co_rand = random.uniform( -150, 20 )
            o3_rand = random.uniform( -15, 5 )
            thc_rand = random.uniform( -1.5, 0.5 )
            tn_rand = random.uniform( -35, 10 )
            tp_rand = random.uniform( -30, 5 )
            pm10_rand = random.uniform( -20, 3 )
            
            time1 = datetime.strptime('2018/10/30', '%Y/%m/%d')
            time2 = datetime.strptime('2018/11/02 16:00', '%Y/%m/%d %H:%S')
            
            data = {
                'NOx': 390 + nox_3_rand + no_3_rand*random.uniform( -1, 1 ), 
                'NO': 4 + no_3_rand*random.uniform( -1, 1 ) + nox_3_rand, 
                'NO2': 17 + no2_3_rand*random.uniform( -1, 1 ) + no_3_rand, 
                'SO2': 350 + so2_3_rand + nox_3_rand*random.uniform( -1, 1 ),
                'CO': 1800 + co_rand,
                'O3': 50 + o3_rand*random.uniform( -0.2, 0.2 ),
                'THC': 4 + thc_rand*random.uniform( -0.2, 0.2 ),
            }
            # if get_time >= time1 and get_time <= time2:
                # # st_k_kc
                # db.data_min.insert(station_id = st_k_kc.id, get_time = get_time, data = data) 
                # data_lastest.append(dict(station_id = st_k_kc.id, get_time = get_time, data = data))
                
                # # st_k_pn
                # db.data_min.insert(station_id = st_k_pn.id, get_time = get_time, data = data) 
                # data_lastest.append(dict(station_id = st_k_pn.id, get_time = get_time, data = data))
                
                # # st_k_nct
                # db.data_min.insert(station_id = st_k_nct.id, get_time = get_time, data = data) 
                # data_lastest.append(dict(station_id = st_k_nct.id, get_time = get_time, data = data))
                
                # # st_k_qh
                # db.data_min.insert(station_id = st_k_qh.id, get_time = get_time, data = data) 
                # data_lastest.append(dict(station_id = st_k_qh.id, get_time = get_time, data = data))
            
            # st_ld
            data = {
                'NOx': 390 + nox_3_rand, 
                'NO': 4 + no_3_rand, 
                'NO2': 17 + no2_3_rand, 
                'SO2': 350 + so2_3_rand,
            }
            if st_ld:
                db.data_min.insert(station_id = st_ld.id, get_time = get_time, data = data)
                data_lastest.append(dict(station_id = st_ld.id, get_time = get_time, data = data))
            
            # st_cn
            data = {
                'NOx': 390 + nox_3_rand*1.2, 
                'NO': 4 + no_3_rand*1.4, 
                'NO2': 17 + no2_3_rand*1.3, 
                'SO2': 350 + so2_3_rand*0.9,
            }
            if st_cn:
                db.data_min.insert(station_id = st_cn.id, get_time = get_time, data = data)
                data_lastest.append(dict(station_id = st_cn.id, get_time = get_time, data = data))
            
            # st_lt
            data = {
                'pH': 9 + ph_rand, 
                'ORP': 270 + orp_rand, 
                'Temp': 29 + temp_rand, 
            }
            if st_lt:
                db.data_min.insert(station_id = st_lt.id, get_time = get_time, data = data) 
                data_lastest.append(dict(station_id = st_lt.id, get_time = get_time, data = data))
            
            # st_fomosa
            data = {
                'pH': 9 + ph_rand, 
                'ORP': 270 + orp_rand, 
                'Temp': 29 + temp_rand, 
                'TSS': 33 + tss_rand, 
            }
            if st_fomosa:
                db.data_min.insert(station_id = st_fomosa.id, get_time = get_time, data = data) 
                data_lastest.append(dict(station_id = st_fomosa.id, get_time = get_time, data = data))
            
            # st_hmac
            data = {
                'pH': 9 + ph_rand*0.8, 
                'ORP': 270 + orp_rand*1.2, 
                'Temp': 29 + temp_rand*1.1, 
                'TSS': 33 + tss_rand*0.9, 
            }
            if st_hmac:
                db.data_min.insert(station_id = st_hmac.id, get_time = get_time, data = data) 
                data_lastest.append(dict(station_id = st_hmac.id, get_time = get_time, data = data))
            
            # st_yb
            data = {
                'pH': 9 + ph_rand*random.uniform( -1, 1 ), 
                'ORP': 270 + orp_rand*random.uniform( -1, 0.3 ), 
                'Temp': 29 + temp_rand*random.uniform( -1, 1 ), 
                'TSS': 33 + tss_rand*random.uniform( -1, 1 ), 
            }
            if st_yb:
                db.data_min.insert(station_id = st_yb.id, get_time = get_time, data = data) 
                data_lastest.append(dict(station_id = st_yb.id, get_time = get_time, data = data))
            
            # st_cg
            data = {
                'NOx': 390 + nox_3_rand + no_3_rand*10, 
                'NO': 4 + no_3_rand + nox_3_rand, 
                'NO2': 17 + no2_3_rand + no_3_rand*10, 
                'SO2': 350 + so2_3_rand + nox_3_rand,
            }
            if st_cg:
                db.data_min.insert(station_id = st_cg.id, get_time = get_time, data = data) 
                data_lastest.append(dict(station_id = st_cg.id, get_time = get_time, data = data))
            
            # st_ntbd
            data = {
                'NOx': 390 + nox_3_rand*random.uniform( -1, 1 ), 
                'NO': 4 + no_3_rand + nox_3_rand, 
                'NO2': 17 + no2_3_rand + no_3_rand*random.uniform( -1, 1 ), 
                'SO2': 350 + so2_3_rand*random.uniform( -1, 1 ) + nox_3_rand,
                'DO': 10 + do_rand,
                'EC': 480 + ec_rand,
            }
            if st_ntbd:
                db.data_min.insert(station_id = st_ntbd.id, get_time = get_time, data = data) 
                data_lastest.append(dict(station_id = st_ntbd.id, get_time = get_time, data = data))
            
            # st_ntub
            data = {
                'NOx': 390 + nox_3_rand + no_3_rand*random.uniform( -1, 1 ), 
                'NO': 4 + no_3_rand*random.uniform( -1, 1 ) + nox_3_rand, 
                'NO2': 17 + no2_3_rand*random.uniform( -1, 1 ) + no_3_rand, 
                'SO2': 350 + so2_3_rand + nox_3_rand*random.uniform( -1, 1 ),
                'DO': 10 + do_rand*random.uniform( -1, 0 ),
                'EC': 480 + ec_rand*random.uniform( -1, 0 ),
            }
            if st_ntub:
                db.data_min.insert(station_id = st_ntub.id, get_time = get_time, data = data) 
                data_lastest.append(dict(station_id = st_ntub.id, get_time = get_time, data = data))
            
            
            # st_hn
            data = {
                'NOx': 390 + nox_3_rand + no_3_rand*random.uniform( -1, 1 ), 
                'NO': 4 + no_3_rand*random.uniform( -1, 1 ) + nox_3_rand, 
                'NO2': 17 + no2_3_rand*random.uniform( -1, 1 ) + no_3_rand, 
                'SO2': 350 + so2_3_rand + nox_3_rand*random.uniform( -1, 1 ),
                'CO': 1800 + co_rand,
                'O3': 50 + o3_rand,
                'THC': 4 + thc_rand,
            }
            if st_hn:
                db.data_min.insert(station_id = st_hn.id, get_time = get_time, data = data) 
                data_lastest.append(dict(station_id = st_hn.id, get_time = get_time, data = data))
            
            # st_pt
            data = {
                'NOx': 390 + nox_3_rand + no_3_rand*random.uniform( -1, 1 ), 
                'NO': 4 + no_3_rand*random.uniform( -1, 1 ) + nox_3_rand, 
                'NO2': 17 + no2_3_rand*random.uniform( -1, 1 ) + no_3_rand, 
                'SO2': 350 + so2_3_rand + nox_3_rand*random.uniform( -1, 1 ),
                'CO': 1800 + co_rand*random.uniform( -1, 0.5 ),
                'O3': 50 + o3_rand*random.uniform( -1, 0.5 ),
            }
            if st_pt:
                db.data_min.insert(station_id = st_pt.id, get_time = get_time, data = data) 
                data_lastest.append(dict(station_id = st_pt.id, get_time = get_time, data = data))
            
            # st_hm
            data = {
                'NOx': 390 + no_3_rand*random.uniform( -1, 1 ), 
                'NO': 4 + no_3_rand*random.uniform( -1, 1 ), 
                'NO2': 17 + no2_3_rand*random.uniform( -1, 1 ), 
                'SO2': 350 + random.uniform( -50, 10 ),
                'CO': 1800 + co_rand - 30,
                'O3': 50 + o3_rand - 3,
                'THC': 4 + thc_rand - 0.5,
            }
            if st_hm:
                db.data_min.insert(station_id = st_hm.id, get_time = get_time, data = data) 
                data_lastest.append(dict(station_id = st_hm.id, get_time = get_time, data = data))
            
            # st_ub
            data = {
                'NOx': 390 + nox_3_rand*random.uniform( -1, 1 ), 
                'NO': 4 + no_3_rand + nox_3_rand*random.uniform( -1, 1 ), 
                'NO2': 17 + no2_3_rand*random.uniform( -1, .5 ), 
                'SO2': 350 + so2_3_rand*random.uniform( -1, 1 ),
                'CO': 1800 + co_rand*random.uniform( -0.5, 0.2 ),
                'O3': 50 + o3_rand*random.uniform( -0.1, 0.2 ),
            }
            if st_ub:
                db.data_min.insert(station_id = st_ub.id, get_time = get_time, data = data) 
                data_lastest.append(dict(station_id = st_ub.id, get_time = get_time, data = data))
            
            # st_nmnb
            data = {
                'pH': 9 + ph_rand, 
                'ORP': 270 + orp_rand, 
                'Temp': 29 + temp_rand, 
                'TSS': 33 + tss_rand, 
                'DO': 10 + do_rand - 1,
                'EC': 480 + ec_rand*random.uniform( -0.9, 0.5 ),
            }
            if st_nmnb:
                db.data_min.insert(station_id = st_nmnb.id, get_time = get_time, data = data) 
                data_lastest.append(dict(station_id = st_nmnb.id, get_time = get_time, data = data))
            
            # st_sstn
            if st_sstn:
                db.data_min.insert(station_id = st_sstn.id, get_time = get_time, data = data) 
                data_lastest.append(dict(station_id = st_sstn.id, get_time = get_time, data = data))
            
            # st_nmbn
            data = {
                'pH': 9 + ph_rand*random.uniform( -0.1, 0.1 ), 
                'ORP': 270 + orp_rand*random.uniform( -0.1, 0.1 ), 
                'Temp': 29 + temp_rand*random.uniform( -0.1, 0.1 ), 
                'TSS': 33 + tss_rand*random.uniform( -0.1, 0.2 ), 
                'DO': 10 + do_rand*random.uniform( -0.1, 0.2 ),
                'EC': 480 + ec_rand*random.uniform( -0.8, 0.1 ),
            }
            if st_nmbn:
                db.data_min.insert(station_id = st_nmbn.id, get_time = get_time, data = data) 
                data_lastest.append(dict(station_id = st_nmbn.id, get_time = get_time, data = data))
            
            # st_nmbh
            if st_nmbh:
                db.data_min.insert(station_id = st_nmbh.id, get_time = get_time, data = data) 
                data_lastest.append(dict(station_id = st_nmbh.id, get_time = get_time, data = data))
            
            # st_nmhna
            data = {
                'pH': 9 + ph_rand*random.uniform( -0.1, 0.1 ), 
                'ORP': 270 + orp_rand*random.uniform( -0.1, 0.1 ), 
                'Temp': 29 + temp_rand*random.uniform( -0.1, 0.1 ), 
                'TSS': 33 + tss_rand*random.uniform( -0.1, 0.2 ), 
                'DO': 10 + do_rand*random.uniform( -0.1, 0.2 ),
                'EC': 480 + ec_rand*random.uniform( -0.8, 0.1 ),
                'TOC': 110 + toc_rand*random.uniform( -0.5, 0.1 ),
                'TN': 100 + tn_rand,
                'TP': 90 + tp_rand*random.uniform( -0.8, 0.1 ),
            }
            if st_nmhna:
                db.data_min.insert(station_id = st_nmhna.id, get_time = get_time, data = data) 
                data_lastest.append(dict(station_id = st_nmhna.id, get_time = get_time, data = data))
            
            # st_nmbd
            data = {
                'pH': 9 + ph_rand*random.uniform( -0.1, 0.1 ), 
                'ORP': 270 + orp_rand*random.uniform( -0.5, 0.1 ), 
                'Temp': 29 + temp_rand*random.uniform( -0.2, 0.1 ), 
                'TSS': 33 + tss_rand*random.uniform( -0.2, 0.2 ), 
                'DO': 10 + do_rand*random.uniform( -0.1, 0.2 ),
                'EC': 480 + ec_rand*random.uniform( -0.8, 0.1 ),
            }
            if st_nmbd:
                db.data_min.insert(station_id = st_nmbd.id, get_time = get_time, data = data) 
                data_lastest.append(dict(station_id = st_nmbd.id, get_time = get_time, data = data))
            
            # st_hue
            data = {
                'NOx': 390 + nox_3_rand + no_3_rand*random.uniform( -1, 1 ), 
                'NO': 4 + no_3_rand*random.uniform( -1, 1 ) + nox_3_rand, 
                'NO2': 17 + no2_3_rand*random.uniform( -1, 1 ) + no_3_rand, 
                'SO2': 350 + so2_3_rand + nox_3_rand*random.uniform( -1, 1 ),
                'CO': 1800 + co_rand,
                'O3': 50 + o3_rand*random.uniform( -0.2, 0.2 ),
                'THC': 4 + thc_rand*random.uniform( -0.2, 0.2 ),
            }
            if st_hue:
                db.data_min.insert(station_id = st_hue.id, get_time = get_time, data = data) 
                data_lastest.append(dict(station_id = st_hue.id, get_time = get_time, data = data))
            
            # st_nb
            data = {
                'O3': 50 + o3_rand*random.uniform( -0.2, 0.2 ),
                'CO': 1800 + co_rand,
                'SO2': 350 + so2_3_rand + nox_3_rand*random.uniform( -1, 1 ),
                'NOx': 390 + nox_3_rand + no_3_rand*random.uniform( -1, 1 ), 
                'NO': 4 + no_3_rand*random.uniform( -1, 1 ) + nox_3_rand, 
                'NO2': 17 + no2_3_rand*random.uniform( -1, 1 ) + no_3_rand, 
                'Temp': 30 + temp_rand*random.uniform( -0.2, 0.2 ),
                'PM10': 50 + pm10_rand,
            }
            if st_nb:
                db.data_min.insert(station_id = st_nb.id, get_time = get_time, data = data) 
                data_lastest.append(dict(station_id = st_nb.id, get_time = get_time, data = data))
            
            # st_v
            data = {
                'NOx': 390 + nox_3_rand*random.uniform( -1, 0 ), 
                'SO2': 350 + so2_3_rand*random.uniform( -1, 0 ),
                'CO': 1800 + co_rand*random.uniform( -0.5, 00 ),
                'O3': 50 + o3_rand*random.uniform( -0.1, 0 ),
            }
            if st_v:
                db.data_min.insert(station_id = st_v.id, get_time = get_time, data = data) 
                data_lastest.append(dict(station_id = st_v.id, get_time = get_time, data = data))
            
            # st_nmcp
            data = {
                'pH': 9 + ph_rand, 
                'O2': 1.2 + o2_rand, 
                'Temp': 29 + temp_rand, 
                'TSS': 33 + tss_rand - 1.5, 
                'COD': 100 + cod_rand,
                'TOC': 110 + toc_rand,
            }
            if st_nmcp:
                db.data_min.insert(station_id = st_nmcp.id, get_time = get_time, data = data) 
                data_lastest.append(dict(station_id = st_nmcp.id, get_time = get_time, data = data))
            
            # st_nmhl
            data = {
                'pH': 9 + ph_rand*random.uniform( -1, 1), 
                'O2': 1.2 + o2_rand*random.uniform( -1, 1), 
                'Temp': 29 + temp_rand*random.uniform( -1, 1), 
                'TSS': 33 + tss_rand*random.uniform( -1, 1), 
            }
            if st_nmhl:
                db.data_min.insert(station_id = st_nmhl.id, get_time = get_time, data = data) 
                data_lastest.append(dict(station_id = st_nmhl.id, get_time = get_time, data = data))
            
            # st_k_qn
            data = {
                'NOx': 390 + nox_3_rand*random.uniform( -1, 0 ) - 80, 
                'NO': 4 + no_3_rand*random.uniform( -1, 0 ) - 2, 
                'NO2': 17 + no2_3_rand*random.uniform( -1, 0 ) - 5, 
                'SO2': 350 + so2_3_rand*random.uniform( -1, 0 ) - 50,
                'CO': 1800 + co_rand - 50,
                'O3': 50 + o3_rand*random.uniform( -0.2, 0.2 ) - 20,
                'THC': 4 + thc_rand*random.uniform( -0.2, 0.2 ) - 2,
            }
            if st_k_qn:
                db.data_min.insert(station_id = st_k_qn.id, get_time = get_time, data = data) 
                data_lastest.append(dict(station_id = st_k_qn.id, get_time = get_time, data = data))
            
            # st_k_mk
            if st_k_mk:
                db.data_min.insert(station_id = st_k_mk.id, get_time = get_time, data = data) 
                data_lastest.append(dict(station_id = st_k_mk.id, get_time = get_time, data = data))
            
            
            ### Cong them 5 phut cho vong lap moi
            get_time = get_time + timedelta(minutes = 5)
            total += 18         # Con so nay la tuong doi, ko chinh xac hoan toan
            
        # Insert vao bang data_lastest
        for item in data_lastest:
            db.data_lastest.update_or_insert(db.data_lastest.station_id == item['station_id'], **item)
            
            # Random insert vao data_alarm (ti le 1/50)
            rand = random.randint(0,50)
            if rand in [0, 1]:
                level = random.randint(0,2)
                item['alarm_level'] = level
                # Insert vao bang data_alarm
                db.data_alarm.insert(**item)
            
        stop = timeit.default_timer()

        print 'Total : %s records' % total
        print
        
        return dict(success = True, end = str(stop-start), total = str(total))
    except Exception, ex:
        logger.error(str(ex))
        return dict(message = str(ex), success = False)


@service.json
def copy_data_adjust(*args, **kwargs):
    try:    
        start_time_str = request.vars.start
        end_time_str = request.vars.end
        start_time_str += ' 00:00:00'
        start = datetime.strptime(start_time_str, '%Y-%m-%d %H:%M:%S')
        
        if end_time_str:
            end_time_str += ' 23:55:00'
            end = datetime.strptime(end_time_str, '%Y-%m-%d %H:%M:%S').replace(hour = 23, minute = 55, second = 0, microsecond = 0)
        else:
            end = datetime.now().replace(hour = 23, minute = 55, second = 0, microsecond = 0)
            
        start_run = timeit.default_timer()

        # Lay du lieu tu bang data_min
        conditions = (db.data_min.id > 0)
        conditions &= (db.data_min.get_time >= start)
        conditions &= (db.data_min.get_time <= end)
        rows = db(conditions).select(db.data_min.ALL)
        for row in rows:
            conditions2 = (db.data_adjust.station_id == row.station_id)
            conditions2 &= (db.data_adjust.get_time == row.get_time)
            db.data_adjust.update_or_insert(conditions2, station_id=row.station_id, get_time=row.get_time, data=row.data, is_approved=False)

        stop_run = timeit.default_timer()

        return dict(success = True, end = str(stop_run - start_run), total=len(rows))
    except Exception, ex:
        logger.error(str(ex))
        return dict(message = str(ex), success = False)


@service.json
def calc_data(*args, **kwargs):
    try:
        start_time_str = request.vars.start
        end_time_str = request.vars.end
        start_time_str += ' 00:00:00'
        start = datetime.strptime(start_time_str, '%Y-%m-%d %H:%M:%S')

        if end_time_str:
            end_time_str += ' 23:55:00'
            end = datetime.strptime(end_time_str, '%Y-%m-%d %H:%M:%S').replace(hour = 23, minute = 55, second = 0, microsecond = 0)
        else:
            end = datetime.now().replace(hour = 23, minute = 55, second = 0, microsecond = 0)

        start_run = timeit.default_timer()

        # Chay batch tinh hour, day, month
        calc_data_hour(start, end)
        calc_data_day(start)
        calc_data_month(start)
        calc_aqi_data_hour(start)
        calc_aqi_data_24h(start)

        stop_run = timeit.default_timer()

        return dict(success = True, end = str(stop_run - start_run))
    except Exception, ex:
        logger.error(str(ex))
        return dict(message = str(ex), success = False)
        
@service.json
def update_threshold(*args, **kwargs):
    try: 
        conditions = (db.station_indicator.id > 0)
        conditions &= (db.station_indicator.status == const.SI_STATUS['IN_USE']['value'])
        thresholds = db(conditions).select()
        
        for item in thresholds:
            if item.tendency_value == 0:
                item.update_record(
                    tendency_value = item.exceed_value * 0.8,
                    preparing_value = item.exceed_value * 0.9
                )
    
        return dict(success = True)
    except Exception, ex:
        logger.error(str(ex))
        return dict(message = str(ex), success = False)
        
@service.json
def test_get_data2():        
    try:
        # get_data2()
        # hungdx fix lost data
        get_data2_new()
        return dict(success = True)
    except Exception, ex:
        logger.error(str(ex))
        return dict(message = str(ex), success = False)
        
@service.json
def test_get_data3():   
    try:
        # calc_data_min_collect(2018, 10)
        # calc_data_min_collect(2018, 11)
        # calc_data_min_collect(2018, 12)
        calc_data_min_collect(2019, 1)
        return dict(success = True)
    except Exception as ex:
        logger.error(str(ex))
        return dict(message = str(ex), success = False)
