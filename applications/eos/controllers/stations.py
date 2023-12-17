# -*- coding: utf-8 -*-
###############################################################################
# Author : 
# Date   : 
# 
# Description : 
# 
###############################################################################
import os

from applications.eos.modules import common as common
from applications.eos.modules import const
from datetime import datetime
from applications.eos.repo.ftp_repo import FtpRepo
from applications.eos.services.ftp_services import *
from applications.eos.services.request_sync_station_service import *
from applications.eos.enums import request_station as request_station_enums
from applications.eos.common import my_const



import requests
import sys
import traceback
import time

if False:
    from gluon import *

    request = current.request
    response = current.response
    session = current.session
    cache = current.cache
    T = current.T
    db = current.db
    pydb = pydb

reload(sys)
sys.setdefaultencoding('utf8')


def get_ftp_file_from_data(ftp_last_file_name, path_format):
    file_name = ftp_last_file_name.split("/")
    last_time = ""
    ftp_folder_path = ""
    if len(file_name)  <= 1:
        return "/", ftp_last_file_name, ""
    if path_format == "0": # VL_CANG_NUOC01_20230506000500.txt => folder = Mã trạm/YYYY/MM/DD/ (Ví dụ: hanam3/2019/05/30)
        ftp_last_file_name_string = ""
        if ftp_last_file_name != None and ftp_last_file_name != "":
            file_name = ftp_last_file_name.split("/")
            ftp_last_file_name_string = file_name[-1].split("_")[-1]
            ftp_last_file_name = file_name[-1]

            file_name.remove(file_name[-1])
            file_name.remove(file_name[-1])
            file_name.remove(file_name[-1])
            file_name.remove(file_name[-1])
            ftp_folder_path = '/'.join(file_name)
            
        if ftp_last_file_name_string != "" and ftp_last_file_name_string != None:
            last_time = datetime.strptime(ftp_last_file_name_string[:8], "%Y%m%d").strftime('%Y-%m-%d')
            
        print("ftp_last_file_name", ftp_last_file_name, "ftp_folder_path", ftp_folder_path) 
        return ftp_folder_path, ftp_last_file_name, last_time
    if path_format == "1": # 01_06_2023 00_06.lsi  folder = Mã trạm/ (Tất cả txt vào 1 thư mục của trạm)
        ftp_last_file_name_string = ""
        if ftp_last_file_name != None and ftp_last_file_name != "":
            file_name = ftp_last_file_name.split("/")
            ftp_last_file_name_string = file_name[-1].split()[-1] # => 01_06_2023
            ftp_last_file_name = file_name[-1]

            file_name.remove(file_name[-1])
            ftp_folder_path = '/'.join(file_name)
            
        if ftp_last_file_name_string != "" and ftp_last_file_name_string != None:
            last_time = datetime.strptime(ftp_last_file_name_string[:8], "%d_%m_%Y").strftime('%Y-%m-%d')
        return ftp_folder_path, ftp_last_file_name, last_time
    if path_format == "2":  # VL_CANG_NUOC01_20230506000500.txt => folder = Mã trạm/YYYYMMDD/ (Ví dụ: hanam3/20190530)
        ftp_last_file_name_string = ""
        if ftp_last_file_name != None and ftp_last_file_name != "":
            file_name = ftp_last_file_name.split("/")
            ftp_last_file_name_string = file_name[-1].split("_")[-1]
            ftp_last_file_name = file_name[-1]
            
            file_name.remove(file_name[-1])
            file_name.remove(file_name[-1])
            ftp_folder_path = '/'.join(file_name)
            
        if ftp_last_file_name_string != "" and ftp_last_file_name_string != None:
            last_time = datetime.strptime(ftp_last_file_name_string[:8], "%Y%m%d").strftime('%Y-%m-%d')
        return ftp_folder_path, ftp_last_file_name, last_time
    if path_format == "3": # VL_CANG_NUOC01_20230506000500.txt => Mã trạm/YYYY/ThangMM/YYYYMMDD/ (Ví dụ: hanam3/2019/Thang05/20190530)
        ftp_last_file_name_string = ""
        if ftp_last_file_name != None and ftp_last_file_name != "":
            file_name = ftp_last_file_name.split("/")
            ftp_last_file_name_string = file_name[-1].split("_")[-1]
            ftp_last_file_name = file_name[-1]

            file_name.remove(file_name[-1])
            file_name.remove(file_name[-1])
            file_name.remove(file_name[-1])
            file_name.remove(file_name[-1])
            ftp_folder_path = '/'.join(file_name)
            
        if ftp_last_file_name_string != "" and ftp_last_file_name_string != None:
            last_time = datetime.strptime(ftp_last_file_name_string[:8], "%Y%m%d").strftime('%Y-%m-%d')
        return ftp_folder_path, ftp_last_file_name, last_time
    if path_format == "4": # VL_CANG_NUOC01_20230506000500.txt  => folder =Mã trạm/YYYY/ThangMM/NgayDD/ (Ví dụ: hanam3/2019/Thang05/Ngay30/)
        ftp_last_file_name_string = ""
        if ftp_last_file_name != None and ftp_last_file_name != "":
            file_name = ftp_last_file_name.split("/")
            ftp_last_file_name_string = file_name[-1].split("_")[-1]
            ftp_last_file_name = file_name[-1]

            file_name.remove(file_name[-1])
            file_name.remove(file_name[-1])
            file_name.remove(file_name[-1])
            file_name.remove(file_name[-1])
            ftp_folder_path = '/'.join(file_name)
            
        if ftp_last_file_name_string != "" and ftp_last_file_name_string != None:
            last_time = datetime.strptime(ftp_last_file_name_string[:8], "%Y%m%d").strftime('%Y-%m-%d')
        return ftp_folder_path, ftp_last_file_name, last_time
    if path_format == "5": #VL_CANG_NUOC01_20230506000500.txt  => folder = Mã trạm/YYYY-MM-DD/ (Ví dụ: hanam3/2019-05-30)
        ftp_last_file_name_string = ""
        if ftp_last_file_name != None and ftp_last_file_name != "":
            file_name = ftp_last_file_name.split("/")
            ftp_last_file_name_string = file_name[-1].split("_")[-1]
            ftp_last_file_name = file_name[-1]

            file_name.remove(file_name[-1])
            file_name.remove(file_name[-1])
            ftp_folder_path = '/'.join(file_name)
            
        if ftp_last_file_name_string != "" and ftp_last_file_name_string != None:
            last_time = datetime.strptime(ftp_last_file_name_string[:8], "%Y%m%d").strftime('%Y-%m-%d')
        return ftp_folder_path, ftp_last_file_name, last_time
    if path_format == "6": #VL_CANG_NUOC01_20230506000500.txt  => folder = Mã trạm/YYYY/ThangMM/DDMMYYYY/ (Ví dụ: hanam3/2019/Thang05/30052019)
        ftp_last_file_name_string = ""
        if ftp_last_file_name != None and ftp_last_file_name != "":
            file_name = ftp_last_file_name.split("/")
            ftp_last_file_name_string = file_name[-1].split("_")[-1]
            ftp_last_file_name = file_name[-1]

            file_name.remove(file_name[-1])
            file_name.remove(file_name[-1])
            file_name.remove(file_name[-1])
            file_name.remove(file_name[-1])
            ftp_folder_path = '/'.join(file_name)
            
        if ftp_last_file_name_string != "" and ftp_last_file_name_string != None:
            last_time = datetime.strptime(ftp_last_file_name_string[:8], "%Y%m%d").strftime('%Y-%m-%d')
        return ftp_folder_path, ftp_last_file_name, last_time
    if path_format == "7": #VL_CANG_NUOC01_20230506000500.txt  => folder = Mã trạm/YYYY_MM_DD/ (Ví dụ: hanam3/2019_05_30)
        ftp_last_file_name_string = ""
        if ftp_last_file_name != None and ftp_last_file_name != "":
            file_name = ftp_last_file_name.split("/")
            ftp_last_file_name_string = file_name[-1].split("_")[-1]
            ftp_last_file_name = file_name[-1]

            file_name.remove(file_name[-1])
            file_name.remove(file_name[-1])
            ftp_folder_path = '/'.join(file_name)
            
        if ftp_last_file_name_string != "" and ftp_last_file_name_string != None:
            last_time = datetime.strptime(ftp_last_file_name_string[:8], "%Y%m%d").strftime('%Y-%m-%d')
        return ftp_folder_path, ftp_last_file_name, last_time
    if path_format == "8": #VL_CANG_NUOC01_20230506000500.txt  => folder = Mã trạm/YYYY/MM/DDMMYYY (Ví dụ: hanam/2019/05/30052019)
        ftp_last_file_name_string = ""
        if ftp_last_file_name != None and ftp_last_file_name != "":
            file_name = ftp_last_file_name.split("/")
            ftp_last_file_name_string = file_name[-1].split("_")[-1]
            ftp_last_file_name = file_name[-1]

            file_name.remove(file_name[-1])
            file_name.remove(file_name[-1])
            file_name.remove(file_name[-1])
            file_name.remove(file_name[-1])
            ftp_folder_path = '/'.join(file_name)
            
        if ftp_last_file_name_string != "" and ftp_last_file_name_string != None:
            last_time = datetime.strptime(ftp_last_file_name_string[:8], "%Y%m%d").strftime('%Y-%m-%d')
        return ftp_folder_path, ftp_last_file_name, last_time
    if path_format == "9": #VL_CANG_NUOC01_20230506000500.txt  => folder = Mã trạm/Nam YYYY/thang MM/ngay DD/ (Ví dụ: hanam3/Nam 2019/thang 05/ngay 30/)
        ftp_last_file_name_string = ""
        if ftp_last_file_name != None and ftp_last_file_name != "":
            file_name = ftp_last_file_name.split("/")
            ftp_last_file_name_string = file_name[-1].split("_")[-1]
            ftp_last_file_name = file_name[-1]

            file_name.remove(file_name[-1])
            file_name.remove(file_name[-1])
            file_name.remove(file_name[-1])
            file_name.remove(file_name[-1])
            ftp_folder_path = '/'.join(file_name)
            
        if ftp_last_file_name_string != "" and ftp_last_file_name_string != None:
            last_time = datetime.strptime(ftp_last_file_name_string[:8], "%Y%m%d").strftime('%Y-%m-%d')
        return ftp_folder_path, ftp_last_file_name, last_time
    return "", "", ""

@auth.requires(
    lambda: (auth.has_permission('create', 'stations') or auth.has_permission('edit', 'stations')))
def form():
    db = current.db
    ftp_repo = FtpRepo(db)
    # If in Update mode, get equivallent record
    last_time = request.vars.last_time
    province = ""
    ftp_last_file_name = request.vars.ftp_file_name
    ftp_folder_path = request.vars.ftp_folder_path
    ftp_path_format = request.vars.path_format
    ftp_id = request.vars.ftp_id
    
    if ftp_last_file_name != None and ftp_path_format != None:
        ftp_folder_path, ftp_last_file_name, last_time = get_ftp_file_from_data(ftp_last_file_name, ftp_path_format)
        
    data_station_id = request.args(0)
    record = db.stations(data_station_id) or None
    station_id = request.args(0) or None
    type = record.station_type if record else ''
    name = record.station_name if record else ''
    implement_agency_ra = record.implement_agency_ra if record else ''
    period_ra = record.period_ra if record else ''
    
    pwd = record.pwd if record else ''
    mqtt_pwd = record.mqtt_pwd if record else ''
    ftp_last_file_name_res = record.last_file_name if record else ''
    ftp_folder_path_res = record.data_folder if record else ''
    ftp_id_res = record.ftp_id if record else ''
    
    if ftp_folder_path_res != "" and ftp_folder_path_res != None:
        ftp_folder_path = ftp_folder_path_res
    
    code = request.vars.station_code
    msg = ''
    station_name = db(db.stations.station_code == code).select().first()
    qi_adjsut_time = None
    qi_adjust = None
    itemStationsQi = db(db.stations.id == station_id).select(db.stations.qi_adjust)
    itemStationsQiTime = db(db.stations.id == station_id).select(db.stations.qi_adjsut_time)

    ftp_list = ftp_repo.get_all(auth)
    agents = db(db.agents.id >0).select()

    if itemStationsQi:
        for i in itemStationsQi:
            qi_adjust = i.qi_adjust
    if itemStationsQiTime:
        for i in itemStationsQiTime:
            qi_adjsut_time = i.qi_adjsut_time
    frm = SQLFORM(db.stations, record, _method='POST', hideerror=True, showid=False, _id='frmMain')

    # if request.vars.last_time != None:
    # frm.vars.last_time =  datetime.now()
    # frm.vars.last_time = datetime.strptime(request.vars.last_time, '%Y/%m/%d %H:%M')
    if frm.process(onvalidation=validate,  detect_record_change=False, hideerror=True).accepted:
        # update history
        # newName = db.stations(request.args(0)).station_name or None
        new_station_id = frm.vars.id
        

        # add station id if new stations is created
        if record is None:
            db(db.stations.id == new_station_id).update(station_id=new_station_id, area_ids=frm.vars.area_ids)

        # Update FTP information
        if ftp_id != "":
            ftp_info = ftp_repo.get_ftp_by_id(ftp_id)
            db(db.stations.id == new_station_id).update(
                ftp_id=ftp_info.id,
                username=ftp_info.ftp_user,
                pwd=ftp_info.ftp_password,
                data_folder=ftp_folder_path,
                last_file_name=ftp_last_file_name,
                data_server=ftp_info.ftp_ip,
                data_server_port=ftp_info.ftp_port
            )

        # <-- update last_time in db data_lastest
        last_time_update = None
        if last_time:
            # last_time_update = datetime.strftime(datetime.strptime(last_time,'%Y-%m-%d'),'%Y-%m-%dT%H:%M')
            update_lastlog_reafile_ftp(last_time, data_station_id, type)
            remove_key_redis_by(data_station_id)

        if qi_adjust:
            db(db.stations.id == station_id).update(qi_adjust=qi_adjust)
        if qi_adjsut_time:
            db(db.stations.id == station_id).update(qi_adjsut_time=qi_adjsut_time)

        if request.vars.transfer_type == 'mqtt':
            res = check_mqtt_status(request.vars, record)
        else:
            res = check_ftp_status(request.vars)
        if record:
            description = 'Thay_doi_noi_dung_thong_tin_tram.'
            # update o day nhe
            db.manager_stations_history.insert(station_id=data_station_id,
                                               action='Update',
                                               username=current_user.fullname or None,
                                               description=description,
                                               update_time=datetime.now())
            if record.order_no is None:
                record.update_record(order_no=0)
            if qi_adjust:
                db(db.stations.id == station_id).update(qi_adjust=qi_adjust)
            if qi_adjsut_time:
                db(db.stations.id == station_id).update(qi_adjsut_time=qi_adjsut_time)
            db(db.stations.id == station_id).update(ftp_connection_status=res)
        else:
            newrecord = db(db.stations.id > 0).select().last() or None
            
            db.manager_stations_history.insert(station_id=newrecord.id,
                                               station_name=newrecord.station_name,
                                               action='Create',
                                               username=current_user.fullname or None,
                                               description='',
                                               update_time=datetime.now())
            db(db.stations.id == newrecord.id).update(ftp_connection_status=res)
            if current_user:
                if not (auth.has_membership('admin') or auth.has_membership(const.GROUP_MANAGER)):
                    data_user = db(db.manager_areas.areas_id == str(newrecord.area_id)).select(db.manager_areas.user_id)
                    user_ids = [str(it.user_id) for it in data_user]
                    if user_ids:
                        for i in user_ids:
                            db.manager_stations.insert(user_id=i,
                                                       station_id=str(newrecord.id))
            session.flash = T('MSG_INFO_SAVE_SUCCESS')
            redirect(URL('form', args=[newrecord.id])) # redirect to edit form
        # update_ftp_status(data_station_id)
        ###
        agent = db.agents(db.agents.id == request.vars.agents_id)
        if agent is not None:
            conditions = (db.agent_station.agent_id == str(agent.id))
            conditions &= (db.agent_station.station_id == str(station_id))
            fields = {
                'agent_id': str(agent.id),
                'agent_name': agent.agent_name,
                'order_no': 1,
                'station_id': str(station_id),
                'station_name': name,
                'station_type': type ,
            }
            db.agent_station.update_or_insert(conditions, **fields)
        session.flash = T('MSG_INFO_SAVE_SUCCESS')
        redirect(URL('index'))
    elif frm.record_changed:
        redirect(URL('home', 'error'))
    elif frm.errors:
        # frm.errors.station_code = T('Station code used')+' '+station_name.station_name
        for item in frm.errors:
            if item == 'station_code':
                msg += T('Station code used') + ' ' + station_name.station_name
            else:
                msg += '%s: %s<br />' % (item, frm.errors[item])

    else:
        pass
        # response.flash = message.REQUEST_INPUT

    if True:  # Custom validate
        frm.custom.widget.station_code['_required'] = ''
        frm.custom.widget.station_code['_maxlength'] = '64'
        frm.custom.widget.station_name['_required'] = ''
        frm.custom.widget.station_name['_maxlength'] = '128'
        frm.custom.widget.longitude['_data-type'] = 'number'
        frm.custom.widget.last_time['_data-type'] = 'datetime'
        frm.custom.widget.verification_deadline['_data-type'] = 'datetime'
        frm.custom.widget.longitude['_data-range'] = '7,24'
        frm.custom.widget.description['_maxlength'] = '512'
        frm.custom.widget.description['_rows'] = '4'
        frm.custom.widget.address['_maxlength'] = '128'
        frm.custom.widget.data_source['_maxlength'] = '128'

    indicators, qcvns, equipments, alarm, qcvn_station_kind, qcvn_station_kind_list_by_qcvn, \
        qcvn_const_value_by_qcvn, datalogger, datalogger_command_list, data_send = [], [], [], [], [], [], [], [], [], []
    # Get Station alarm info
    list_status_data_send = []
    current_send_status = 0
    curent_send_name = ''
    send_file_name = ''
    alarm = get_alarm_by_station_id(station_id)
    if station_id:
        # Get all indicators to fill in dropdown
        # indicators = db((db.indicators.id > 0) & (db.indicators.indicator_type == type)).select()
        # Get all QCVN to fill in dropdown
        qcvns = db((db.qcvn.id > 0) & (db.qcvn.qcvn_type == record.station_type)).select(db.qcvn.id, db.qcvn.qcvn_code,
                                                                                         db.qcvn.qcvn_const_value)
        province = db.provinces(db.provinces.id == record.province_id)
        agent = db.agents(db.agents.id == record.agents_id)
        data_send_list = db((db.stations_send_data.id > 0) & (db.stations_send_data.station_id == station_id)).select()
        send_file_name = get_send_file_name(record, province, agent, data_send_list)


        if data_send_list:
            data_send = data_send_list[0]
            current_send_status = data_send.status
            if current_send_status == 0:
                curent_send_name = 'In-active'
                list_status_data_send.append({'value': current_send_status, 'name': 'In-active'})
                list_status_data_send.append({'value': 1, 'name': 'Active'})
            elif current_send_status == 1:
                curent_send_name = 'Active'
                list_status_data_send.append({'value': current_send_status, 'name': 'Active'})
                list_status_data_send.append({'value': 0, 'name': 'In-active'})
        else:
            list_status_data_send.append({'value': 0, 'name': 'In-active'})
            list_status_data_send.append({'value': 1, 'name': 'Active'})
        datalogger = None
        datalogger_list = db((db.datalogger.id > 0) & (db.datalogger.station_id == station_id)).select()
        if datalogger_list:
            datalogger = datalogger_list[len(datalogger_list) - 1]
            # Get all command list
            datalogger_command_list = db((db.datalogger_command.id > 0)
                                         & (db.datalogger_command.station_id == station_id)).select()

        # Get all QCVN with qcvn_station_kind
        qcvn_station_kind = db((db.qcvn_station_kind.id > 0) & (db.qcvn_station_kind.station_id == station_id)).select()
        if qcvn_station_kind:
            qcvn_details = db.qcvn(qcvn_station_kind[0].qcvn_id) or None
            if qcvn_details:
                qcvn_station_kind[0].qcvn_code = qcvn_details.qcvn_code
            else:
                qcvn_station_kind[0].qcvn_code = '-'

            qcvn_kind_details = db.qcvn_kind(qcvn_station_kind[0].qcvn_kind_id) or None
            if qcvn_kind_details:
                qcvn_station_kind[0].qcvn_kind_name = qcvn_kind_details.qcvn_kind
            else:
                qcvn_station_kind[0].qcvn_kind_name = '---'

            qcvn_station_kind = qcvn_station_kind.first()

            # Get all QCVN kink by qcvn ID
            qcvn_station_kind_list_by_qcvn = db((db.qcvn_kind.id > 0) & (db.qcvn_kind.qcvn_kind_delete_flag == 0) & (
                    db.qcvn_kind.qcvn_id == qcvn_station_kind.qcvn_id)).select(orderby=db.qcvn_kind.qcvn_kind_order)
            if qcvn_station_kind.qcvn_id != "-999":
                qcvn_const_value_by_qcvn = db((db.qcvn.id > 0) & (db.qcvn.id == qcvn_station_kind.qcvn_id)).select()
                for i in range(len(qcvn_station_kind_list_by_qcvn)):
                    qcvn_station_kind_list_by_qcvn[i].id = str(qcvn_station_kind_list_by_qcvn[i].id)
                for i in range(len(qcvn_const_value_by_qcvn)):
                    qcvn_const_value_by_qcvn[i].id = str(qcvn_const_value_by_qcvn[i].id)

        # Get all Equipments to fill in dropdown
        equipments = db(db.equipments.station_id == station_id).select(
            db.equipments.id,
            db.equipments.equipment,
            db.equipments.series,
            db.equipments.lrv,
            db.equipments.urv,
        )
    
    res_ftp_folder_path = ""
    if station_id:
        folder_path = ["NuocThai","NuocMat","NuocNgam","KhiThai","KhongKhi"]
        if record.station_type in folder_path:
            if record.station_code != "" or record.station_code != None:
                res_ftp_folder_path = "/".join(["",folder_path[record.station_type], record.station_code])
            else:
                res_ftp_folder_path = "/".join(["",folder_path[record.station_type]])

    provinces = dict()
    if os.getenv(my_const.APP_SIDE) == my_const.APP_SIDE_LOCAL_DP:
        provinces = db(db.provinces.default == 1).select()
    else:
        provinces = db(db.provinces.id > 0).select()
    res = dict(frm=frm, msg=XML(msg),
               station_id=station_id,
               pwd=pwd,
               mqtt_pwd='' if mqtt_pwd is None else mqtt_pwd,
               type=type,
               name=name,
               code=code,
               implement_agency_ra=implement_agency_ra,
               period_ra=period_ra,
               indicators=indicators,
               equipments=equipments,
               qcvns=qcvns,
               qcvn_station_kind=qcvn_station_kind,
               qcvn_station_kind_list_by_qcvn=qcvn_station_kind_list_by_qcvn,
               qcvn_const_value_by_qcvn=qcvn_const_value_by_qcvn,
               datalogger=datalogger,
               type_datalogger=const.TYPE_SAMPLING,
               datalogger_command_list=datalogger_command_list,
               data_send=data_send,
               list_status_data_send=list_status_data_send,
               current_send_status=current_send_status,
               curent_send_name=curent_send_name,
               send_file_name=send_file_name,
               alarm=alarm,
               ftp_list=ftp_list,
               ftp_id_res=ftp_id_res,
               ftp_last_file_name_res=ftp_last_file_name_res,
               ftp_folder_path_res=ftp_folder_path_res,
               res_ftp_folder_path=res_ftp_folder_path,
               agents=agents,
               provinces=provinces,
               province=province,
               )
    return res


def get_alarm_by_station_id(station_id):
    if not station_id:
        return None
    alarm = db(db.station_alarm.station_id == station_id).select()
    if alarm:
        return alarm.first()
    return None


def update_lastlog_reafile_ftp(last_time, station_id, type):
    last_time_update = datetime.strptime(datetime.strftime(datetime.strptime(last_time, '%Y-%m-%d'), '%Y-%m-%dT%H:%M'),
                                         '%Y-%m-%dT%H:%M')
    item_data_hour_lastest = db(db.data_hour_lastest.station_id == station_id).select(db.data_hour_lastest.station_id)
    if item_data_hour_lastest:
        db(db.data_hour_lastest.station_id == station_id).update(last_time=last_time_update)
    item_data_month_lastest = db(db.data_month_lastest.station_id == station_id).select(
        db.data_month_lastest.station_id)
    if item_data_month_lastest:
        db(db.data_month_lastest.station_id == station_id).update(last_time=last_time_update)
    item_data_day_lastest = db(db.data_day_lastest.station_id == station_id).select(db.data_day_lastest.last_time)
    if item_data_day_lastest:
        db(db.data_day_lastest.station_id == station_id).update(last_time=last_time_update)
    item_data_lastest = db(db.data_lastest.station_id == station_id).select(db.data_lastest.station_id)
    if item_data_lastest:
        db(db.data_lastest.station_id == station_id).update(get_time=last_time_update)
    item_last_data_files = db(db.last_data_files.station_id == station_id).select(db.last_data_files.station_id)
    if item_last_data_files:
        db(db.last_data_files.station_id == station_id).update(lasttime=last_time_update, filename='', file_name='')
    if type == 4:
        item_data_aqi_hour_lastest = db(db.data_aqi_hour_lastest.station_id == station_id).select(
            db.data_aqi_hour_lastest.station_id)
        if item_data_aqi_hour_lastest:
            db(db.data_aqi_hour_lastest.station_id == station_id).update(last_time=last_time_update)

        item_data_aqi_24h_lastest = db(db.data_aqi_24h_lastest.station_id == station_id).select(
            db.data_aqi_24h_lastest.station_id)
        if item_data_aqi_24h_lastest:
            db(db.data_aqi_24h_lastest.station_id == station_id).update(last_time=last_time_update)


def remove_key_redis_by(station_id):
    try:
        REDIS_KEY = '0RJITA9ewVBPYVdggzWi5YNvm+H4nPfy%'
        # REDIS_HOST = '192.168.101.46'  # 'localhost'
        REDIS_HOST = 'localhost'
        REDIS_PORT = 6379
        from redis import Redis
        r = Redis(host=REDIS_HOST, port=REDIS_PORT, password=REDIS_KEY)
        for k in r.keys():
            if '{}'.format(station_id).endswith(station_id):
                r.delete(k)
    except Exception as ex:
        pass


def check_ftp_status(data):
    from ftplib import FTP
    import ftplib
    res = True
    ftp_ip = data.data_server
    data_folder = data.data_folder
    username = data.username
    password = data.pwd
    ftp_port = data.data_server_port
    ftp = FTP()
    try:
        ftp.connect(ftp_ip, ftp_port)
        ftp.login(username, password)
        ftp.cwd(data_folder)
    except ftplib.all_errors:
        res = False
    finally:
        try:
            ftp.quit()
        except Exception as ex:
            pass
    return res


def check_mqtt_status(vars, record):
    try:
        if record:
            if not vars.mqtt_usr == record.mqtt_usr or not vars.mqtt_pwd == record.mqtt_pwd:
                rs = post_mqtt_api('api/v4/auth_username', {'username': vars.mqtt_usr, 'password': vars.mqtt_pwd})
                print rs
        data = get_mqtt_api('api/v4/clients/' + vars['mqtt_client_id'])
        print data
        if data.has_key('data') and len(data['data']) > 0:
            print data['data'][0]['connected']
            return data['data'][0]['connected']
    except:
        pass
    return False


################################################################################
def validate(frm):
    # Check condion
    # Get control value by : frm.vars.ControlName
    # If validate fail : frm.errors.ControlName = some message
    pass


def call():
    return service()


################################################################################
@auth.requires(lambda: (auth.has_permission('view', 'stations')))
def index():
    conditions = (db.stations.id > 0)
    if current_user:
        if not (auth.has_membership('admin') or auth.has_membership(const.GROUP_MANAGER)):
            list_station_manager = db(db.manager_stations.user_id == current_user.id). \
                select(db.manager_stations.station_id)
            station_ids = [str(item.station_id) for item in list_station_manager]
            conditions &= (db.stations.id.belongs(station_ids))
    row = db(conditions).select(db.stations.province_id)
    provinces_ids = []
    for it in row:
        if it.province_id:
            provinces_ids.append(str(it.province_id))
    query = db.provinces.id > 0
    query &= db.provinces.id.belongs(provinces_ids)
    provinces = db(query).select()
    return dict(provinces=provinces, message='')


@auth.requires(lambda: (auth.has_permission('view', 'stations')))
def profile():
    station_id = request.args(0) or None
    if not station_id:
        return dict()

    station = db.stations(station_id) or None
    name = station.station_name if station else ''
    province = db.provinces(db.provinces.id == station.province_id)
    agent = db.agents(db.agents.id == station.agents_id)
    area = db.areas(db.areas.id == station.area_id)
    type = db.station_types(db.station_types.code == station.station_type)

    frm = SQLFORM(db.stations, station, _id='frmMain')

    data_send_list = db((db.stations_send_data.id > 0) & (db.stations_send_data.station_id == station_id)).select()
    data_send = data_send_list[0] if data_send_list else None

    send_file_name = get_send_file_name(station, province, agent, data_send_list)
    send_data_status = get_send_data_status(data_send_list)

    alarm = get_alarm_by_station_id(station_id)

    status = {}
    for item in const.STATION_STATUS.values():
        if station.status == item['value']:
            status = {'value': item['value'], 'name': T(item['name'])}
    using_status = {}
    for item in const.STATION_USING_STATUS.values():
        if station.using_status == item['value']:
            using_status = {'value': item['value'], 'name': T(item['name'])}

    # res = dict(frm=frm, msg=XML(msg),
    #            station_id=station_id,
    #            type=type,
    #            name=name,
    #            code=code,
    #            indicators=indicators,
    #            equipments=equipments,
    #            qcvns=qcvns,
    #            qcvn_station_kind=qcvn_station_kind,
    #            qcvn_station_kind_list_by_qcvn=qcvn_station_kind_list_by_qcvn,
    #            qcvn_const_value_by_qcvn=qcvn_const_value_by_qcvn,
    #            datalogger=datalogger,
    #            type_datalogger=const.TYPE_SAMPLING,
    #            datalogger_command_list=datalogger_command_list,
    #            data_send=data_send,
    #            list_status_data_send=list_status_data_send,
    #            current_send_status=current_send_status,
    #            curent_send_name=curent_send_name,
    #            send_file_name=send_file_name,
    #            alarm=alarm)
    return dict(frm=frm, station_id=station_id, name=name, station=station, data_send=data_send,
                type=type, province=province, area=area, agent=agent, status=status,
                using_status=using_status, send_data_status=send_data_status, send_file_name=send_file_name,
                alarm=alarm)


def get_send_file_name(station, province, agents, data_send_list):
    send_file_name = ""
    if data_send_list:
        send_file_name = data_send_list[0].file_name
    else:
        send_file_name += province.province_code + '_' if province else '_'
        send_file_name += agents.agent_code + '_' if agents else ''
        send_file_name += station.station_code

    return send_file_name


def get_send_data_status(data_send_list):
    if data_send_list:
        data_send = data_send_list[0]
        if data_send.status == 0:
            curent_send_name = 'In-active'
        elif data_send.status == 1:
            curent_send_name = 'Active'
        return {'value': data_send.status, 'name': curent_send_name}
    return dict()


################################################################################
@service.json
@auth.requires(
    lambda: (auth.has_permission('view', 'stations')) or (auth.has_permission('view', 'manager_station_type')))
def get_list_stations_sort(*args, **kwargs):
    try:
        iDisplayStart = int(data.iDisplayStart)
        iDisplayLength = int(request.vars.iDisplayLength)
        s_search = request.vars.sSearch
        type = request.vars.type
        status = request.vars.status
        using_status = request.vars.using_status
        sometext = request.vars.sometext
        province_id = request.vars.province_id
        ftp_connection_status = request.vars.ftp_connection_status
        sort_type = request.vars.sort_type
        if sort_type:
            sort_type = int(sort_type)

        aaData = []
        limitby = (iDisplayStart, iDisplayLength + 1)  # Tuple dung de phan trang (vtri bat dau - chieu dai)

        conditions = (db.stations.id > 0)
        if current_user:
            if not (auth.has_membership('admin') or auth.has_membership(const.GROUP_MANAGER)):
                list_station_manager = db(db.manager_stations.user_id == current_user.id).select(
                    db.manager_stations.station_id)
                station_ids = [str(item.station_id) for item in list_station_manager]
                conditions &= (db.stations.id.belongs(station_ids))
        # Neu chuoi tim kiem khac rong thi them dieu kien truy van voi chuoi tim kiem
        if sometext:
            conditions &= ((db.stations.station_code.contains(sometext)) |
                           (db.stations.station_name.contains(sometext)) |
                           (db.stations.description.contains(sometext)) |
                           (db.stations.contact_point.contains(sometext)) |
                           (db.stations.phone.contains(sometext)) |
                           (db.stations.email.contains(sometext)) |
                           (db.stations.address.contains(sometext)))
        if type:
            conditions &= (db.stations.station_type == type)
        if province_id:
            conditions &= (db.stations.province_id == province_id)
        if status:
            if status == '0':
                conditions &= (db.stations.status >= '0')
                conditions &= (db.stations.status <= '2')
            else:
                conditions &= (db.stations.status == status)
        if using_status:
            if using_status == '0':
                conditions &= ((db.stations.using_status == 0) | (db.stations.using_status == None))
            else:
                conditions &= (db.stations.using_status == using_status)
        if ftp_connection_status:
            conditions &= (db.stations.ftp_connection_status == ftp_connection_status)
        if sort_type == 0:
            list_data = db(conditions).select(db.stations.id,
                                              db.stations.station_name,
                                              db.stations.status,
                                              db.stations.station_type,
                                              db.stations.province_id,
                                              db.stations.area_id,
                                              db.stations.address,
                                              db.stations.phone,
                                              db.stations.email,
                                              db.stations.ftp_connection_status,
                                              db.stations.order_no,
                                              orderby=db.stations.station_name,
                                              limitby=limitby)
        else:
            list_data = db(conditions).select(db.stations.id,
                                              db.stations.station_name,
                                              db.stations.status,
                                              db.stations.station_type,
                                              db.stations.province_id,
                                              db.stations.area_id,
                                              db.stations.address,
                                              db.stations.phone,
                                              db.stations.email,
                                              db.stations.ftp_connection_status,
                                              db.stations.order_no,
                                              orderby=~db.stations.station_name,
                                              limitby=limitby)
        # Tong so ban ghi khong thuc hien phan trang
        iTotalRecords = db(conditions).count()
        # Thu tu ban ghi
        iRow = iDisplayStart + 1
        provice_dict = common.get_province_dict()

        ## Get station's area info
        areas = common.get_area_by_station_dict()
        station_type = dict()
        status = dict()
        for item in common.get_station_types():
            station_type[str(item['value'])] = item['name']

        for key, item in const.STATION_STATUS.iteritems():
            status[str(item['value'])] = T(item['name'])

        # Duyet tung phan tu trong mang du lieu vua truy van duoc
        for item in list_data:
            if item.ftp_connection_status:
                text = 'Kết nối'
            else:
                text = 'Không kết nối'
            aaData.append([
                A(str(iRow), _href=URL('form', args=[item.id])),
                A(item.station_name, _href=URL('form', args=[item.id])),
                status[str(item.status)],
                TR(text, _class="ftp_connection_status", _value=str(item.ftp_connection_status)),
                station_type[str(item.station_type)],
                provice_dict.get(item.province_id),
                item.address,
                areas.get(item.area_id),
                item.email,
                item.phone,
                item.order_no,
                A(I(_class='fa fa-folder', _style='color: #FBDB79; font-size: 19px;'),
                  _href=URL('ftp_viewer', args=[str(item.id)])),
                INPUT(_group='0', _class='select_item', _type='checkbox', _value=item.id),
                item.id
            ])

            iRow += 1
        return dict(iTotalRecords=iTotalRecords, iTotalDisplayRecords=iTotalRecords, aaData=aaData, success=True)
    except Exception as ex:
        return dict(iTotalRecords=0, iTotalDisplayRecords=0, aaData=[], message=str(ex), success=False)


################################################################################


@service.json
@auth.requires(
    lambda: (auth.has_permission('view', 'stations')) or (auth.has_permission('view', 'manager_station_type')))
def get_list_stations(*args, **kwargs):
    iDisplayStart = int(request.vars.iDisplayStart)
    iDisplayLength = int(request.vars.iDisplayLength)
    s_search = request.vars.sSearch
    type = request.vars.type
    status = request.vars.status
    using_status = request.vars.using_status
    sometext = request.vars.sometext
    province_id = request.vars.province_id
    ftp_connection_status = request.vars.ftp_connection_status

    aaData = []
    limitby = (iDisplayStart, iDisplayLength + 1)  # Tuple dung de phan trang (vtri bat dau - chieu dai)

    conditions = (db.stations.id > 0)
    if current_user:
        if not (auth.has_membership('admin') or auth.has_membership(const.GROUP_MANAGER)):
            list_station_manager = db(db.manager_stations.user_id == current_user.id).select(
                db.manager_stations.station_id)
            station_ids = [str(item.station_id) for item in list_station_manager]
            conditions &= (db.stations.id.belongs(station_ids))
    # Neu chuoi tim kiem khac rong thi them dieu kien truy van voi chuoi tim kiem
    if sometext:
        conditions &= ((db.stations.station_code.contains(sometext)) |
                       (db.stations.station_name.contains(sometext)) |
                       (db.stations.description.contains(sometext)) |
                       (db.stations.contact_point.contains(sometext)) |
                       (db.stations.phone.contains(sometext)) |
                       (db.stations.email.contains(sometext)) |
                       (db.stations.contact_info.contains(sometext)) |
                       (db.stations.address.contains(sometext)))
    if type:
        conditions &= (db.stations.station_type == type)
    if province_id:
        conditions &= (db.stations.province_id == province_id)
    if status:
        if status == '0':
            conditions &= (db.stations.status >= '0')
            conditions &= (db.stations.status <= '2')
        else:
            conditions &= (db.stations.status == status)

    if using_status:
        if using_status == '0':
            conditions &= ((db.stations.using_status == 0) | (db.stations.using_status == None))
        else:
            conditions &= (db.stations.using_status == using_status)

    if ftp_connection_status:
        conditions &= (db.stations.ftp_connection_status == ftp_connection_status)

    list_data = db(conditions).select(db.stations.id,
                                      db.stations.station_code,
                                      db.stations.station_name,
                                      db.stations.status,
                                      db.stations.using_status,
                                      db.stations.station_type,
                                      db.stations.province_id,
                                      db.stations.area_id,
                                      db.stations.area_ids,
                                      db.stations.address,
                                      db.stations.phone,
                                      db.stations.email,
                                      db.stations.contact_info,
                                      db.stations.ftp_connection_status,
                                      db.stations.order_no,
                                      db.stations.username,
                                      db.stations.pwd,
                                      db.stations.data_folder,
                                      db.stations.data_server_port,
                                      db.stations.data_server,
                                      db.stations.is_synced,
                                      db.stations.tw_request_sync_station_id,
                                      orderby=db.stations.order_no,
                                      limitby=limitby)
    # Tong so ban ghi khong thuc hien phan trang
    iTotalRecords = db(conditions).count()
    # Thu tu ban ghi
    iRow = iDisplayStart + 1
    provice_dict = common.get_province_dict()

    ## Get station's area info
    areas = common.get_area_by_station_dict()
    station_type = dict()
    status = dict()
    using_status = dict()
    for item in common.get_station_types():
        station_type[str(item['value'])] = item['name']

    for key, item in const.STATION_STATUS.iteritems():
        status[str(item['value'])] = T(item['name'])

    for key, item in const.STATION_USING_STATUS.iteritems():
        using_status[str(item['value'])] = T(item['name'])

    # Duyet tung phan tu trong mang du lieu vua truy van duoc
    # import itertools
    # list_data_1, list_data = itertools.tee(list_data_origin, 2)

    tw_request_station_ids = []
    list_approve_status = []
    if os.getenv(my_const.APP_SIDE) == my_const.APP_SIDE_LOCAL_DP:
        for item in list_data:
            if item.tw_request_sync_station_id:
                tw_request_station_ids.append(str(item.tw_request_sync_station_id))
        if tw_request_station_ids:
            list_approve_status, err = RequestSyncStationService(mongo_client=pydb, T=T).get_request_sync_stations_approve_status_from_local_dp(tw_request_station_ids)

    for item in list_data:
        if item.using_status is None:
            item.using_status = 0
        sync_tw_status = T('None-Synced request')
        url_ftp = 'ftp://%s:%s@%s:%s%s' % (
            item.username, item.pwd, item.data_server, item.data_server_port, item.data_folder);
        if item.ftp_connection_status:
            text = 'Kết nối'
        else:
            text = 'Không kết nối'
        profile_url = URL('form', args=[item.id] , vars={"preview":True})
        form_url = URL('form', args=[item.id])

        contact_info = item.contact_info if item.contact_info else item.email

        if item.is_synced:
            sync_tw_status = T('Synced request')
        str_tw_hex_id = item.tw_request_sync_station_id
        approve_status = ''
        approve_reason = ''
        if str_tw_hex_id in list_approve_status:
            approve_info = list_approve_status[str_tw_hex_id]
            if 'approve_status' in approve_info:
                if approve_info['approve_status'] == request_station_enums.RequestStationApproveStatus.WAITING:
                    approve_status = T('Wait Approve')
                if approve_info['approve_status'] == request_station_enums.RequestStationApproveStatus.APPROVED:
                    approve_status = T('Approved')
                if approve_info['approve_status'] == request_station_enums.RequestStationApproveStatus.REJECTED:
                    approve_status = T('Rejected')
            if 'reason' in approve_info:
                approve_reason = approve_info['reason']

        if item.is_synced:
            sync_status = UL(XML('<b>Đồng bộ:</b>'+ sync_tw_status), XML('<b>Trạng thái:</b>' + approve_status),  XML('<b>Lý do:</b>' + approve_reason), _class="ul-tw-sync-station")
        else:
            sync_status= UL(XML('<b>Đồng bộ:</b>'+ sync_tw_status), _class="ul-tw-sync-station")

        station_type_string = ""
        if station_type.has_key(str(item.station_type)):
            station_type_string= station_type[str(item.station_type)]
        aaData.append([
            A(str(iRow), _href=profile_url),
            A(item.station_name, _href=profile_url),
            status[str(item.status)],
            using_status[str(item.using_status)],
            TR(text, _class="ftp_connection_status", _value=str(item.ftp_connection_status)),
            station_type_string,
            provice_dict.get(item.province_id),
            item.address,
            areas.get(item.area_id),
            contact_info,
            item.phone,
            sync_status,
            item.order_no,
            A(I(_class='fa fa-folder', _style='color: #FBDB79; font-size: 19px;'),
              _href=URL('ftp_viewer', args=[str(item.id)])),
            A(I(_class='fa fa-edit'), _href=form_url),
            INPUT(_group='0', _class='select_item', _type='checkbox', _value=item.id),
            item.id
        ])

        iRow += 1
    return dict(iTotalRecords=iTotalRecords, iTotalDisplayRecords=iTotalRecords, aaData=aaData, success=True)


################################################################################
@service.json
@auth.requires(lambda: (auth.has_permission('view', 'indicators')))
def get_list_indicators(*args, **kwargs):
    try:
        iDisplayStart = int(request.vars.iDisplayStart)  # Vi tri bat dau lay du lieu
        iDisplayLength = int(request.vars.iDisplayLength)  # So luong ban ghi se lay toi da
        station_id = request.vars.station_id  # Chuoi tim kiem nhap tu form
        aaData = []  # Du lieu json se tra ve
        limitby = (iDisplayStart, iDisplayLength + 1)  # Tuple dung de phan trang (vtri bat dau - chieu dai)

        conditions = (db.station_indicator.id > 0)
        if station_id:
            conditions &= (db.station_indicator.station_id == station_id) & (db.station_indicator.is_public == True)
        list_data = db(conditions).select(db.station_indicator.id,
                                          db.station_indicator.indicator_id,
                                          db.station_indicator.tendency_value,
                                          db.station_indicator.preparing_value,
                                          db.station_indicator.exceed_value,
                                          db.station_indicator.qcvn_code,
                                          db.station_indicator.qcvn_detail_type_code,
                                          db.station_indicator.qcvn_detail_min_value,
                                          db.station_indicator.qcvn_detail_max_value,
                                          db.station_indicator.qcvn_detail_const_area_value,
                                          db.station_indicator.equipment_name,
                                          db.station_indicator.equipment_lrv,
                                          db.station_indicator.equipment_urv,
                                          db.station_indicator.mapping_name,
                                          db.station_indicator.convert_rate,
                                          db.station_indicator.status, )
        # limitby = limitby)
        # Tong so ban ghi khong thuc hien phan trang
        iTotalRecords = db(conditions).count()
        indicator_dict = common.get_indicator_dict()
        status = dict(db.station_indicator.status.requires.options())
        # Thu tu ban ghi
        iRow = iDisplayStart + 1

        # Duyet tung phan tu trong mang du lieu vua truy van duoc
        for item in list_data:
            indicator = db.indicators(item.indicator_id) or None
            listA = [
                str(iRow),  # A(str(iRow), _href = URL('form', args = [item.id])),
                indicator.indicator + '(' + indicator.unit + ')',
                item.mapping_name,
                "{:,}".format(item.convert_rate) if item.convert_rate else 1,
                # "{0:.4f}".format(item.tendency_value),
                # "{0:.4f}".format( item.preparing_value),
                # "{0:.4f}".format(item.exceed_value),
                item.equipment_name,
                item.equipment_lrv,
                item.equipment_urv,
                item.qcvn_code,
                item.qcvn_detail_type_code,
                item.qcvn_detail_min_value,
                item.qcvn_detail_max_value,
                # item.qcvn_detail_const_area_value,
                status[str(item.status)] if item.status else '',
                INPUT(_group='1', _class='select_item', _type='checkbox', _value=item.id),
                item.id
            ]

            aaData.append(listA)
            iRow += 1
        return dict(iTotalRecords=iTotalRecords, iTotalDisplayRecords=iTotalRecords, aaData=aaData, success=True)
    except Exception as ex:
        return dict(iTotalRecords=0, iTotalDisplayRecords=0, aaData=[], message=str(ex), success=False)


################################################################################
@service.json
@auth.requires(lambda: (auth.has_permission('view', 'indicators')))
def get_list_indicators_for_station(*args, **kwargs):
    try:
        iDisplayStart = int(request.vars.iDisplayStart)  # Vi tri bat dau lay du lieu
        iDisplayLength = int(request.vars.iDisplayLength)  # So luong ban ghi se lay toi da
        station_id = request.vars.station_id  # Chuoi tim kiem nhap tu form
        aaData = []  # Du lieu json se tra ve
        limitby = (iDisplayStart, iDisplayLength + 1)  # Tuple dung de phan trang (vtri bat dau - chieu dai)
        view_only = request.vars.view_only
        conditions = (db.station_indicator.id > 0)
        if station_id:
            conditions &= (db.station_indicator.station_id == station_id) & ((
                    db.station_indicator.status == const.SI_STATUS['IN_USE']['value']) | (db.station_indicator.status == const.SI_STATUS['NEED_UPDATE']['value']))
        list_data = db(conditions).select(db.station_indicator.id,
                                        db.station_indicator.indicator_id,
                                        db.station_indicator.tendency_value,
                                        db.station_indicator.preparing_value,
                                        db.station_indicator.exceed_value,
                                        db.station_indicator.qcvn_code,
                                        db.station_indicator.qcvn_detail_type_code,
                                        db.station_indicator.qcvn_detail_min_value,
                                        db.station_indicator.qcvn_detail_max_value,
                                        db.station_indicator.qcvn_detail_const_area_value,
                                        db.station_indicator.equipment_name,
                                        db.station_indicator.equipment_lrv,
                                        db.station_indicator.equipment_urv,
                                        db.station_indicator.mapping_name,
                                        db.station_indicator.convert_rate,
                                        db.station_indicator.status,
                                        db.station_indicator.qcvn_id,
                                        db.station_indicator.qcvn_detail_id,
                                        db.station_indicator.qcvn_kind_id,
                                        db.station_indicator.station_id,
                                        )
        # limitby = limitby)
        # Tong so ban ghi khong thuc hien phan trang
        iTotalRecords = db(conditions).count()
        indicator_dict = common.get_indicator_dict()
        status = dict(db.station_indicator.status.requires.options())
        # Thu tu ban ghi
        iRow = iDisplayStart + 1
        hide_class = "" if( request.vars.preview is None or request.vars.preview == 'None') else "hide"
        # Duyet tung phan tu trong mang du lieu vua truy van duoc
        for item in list_data:

            if (item.qcvn_detail_type_code is not None) & (item.qcvn_detail_type_code != '-- Chọn loại --') \
                    & (item.qcvn_detail_type_code != '---'):
                text = item.qcvn_detail_type_code
            else:
                text = '---'
            indicator = db.indicators(item.indicator_id) or None
            qcvn_id = ""
            qcvn_kind_id = ""
            conditions_kind = (db.qcvn_station_kind.station_id == station_id) 
            if item.qcvn_id != "" or item.qcvn_id != None:
                qcvn_id = str(item.qcvn_id)
                conditions_kind &= (db.qcvn_station_kind.qcvn_id == item.qcvn_id)
            if item.qcvn_kind_id != "" or  item.qcvn_kind_id != None:
                qcvn_kind_id = str(item.qcvn_kind_id)
                conditions_kind &= (db.qcvn_station_kind.qcvn_kind_id == item.qcvn_kind_id)
            
            qcvn_station_kind = db.qcvn_station_kind(conditions_kind) or None
            
            qcvn_detail_const_area_value_1 = 0
            qcvn_detail_const_area_value_2 = 0
            qcvn_detail_const_area_value_3 = 0
            if qcvn_station_kind:
                qcvn_detail_const_area_value_1 = qcvn_station_kind.qcvn_detail_const_area_value_1 if qcvn_station_kind.qcvn_detail_const_area_value_1 else 0
                qcvn_detail_const_area_value_2 = qcvn_station_kind.qcvn_detail_const_area_value_2 if qcvn_station_kind.qcvn_detail_const_area_value_2 else 0
                qcvn_detail_const_area_value_3 = qcvn_station_kind.qcvn_detail_const_area_value_3 if qcvn_station_kind.qcvn_detail_const_area_value_3 else 0

            idd = item.id if item.id > 0 else ''

            listA = [
                str(iRow),  # A(str(iRow), _href = URL('form', args = [item.id])),
                indicator.indicator + '(' + indicator.unit + ')',
                item.mapping_name,
                "{:,}".format(item.convert_rate) if item.convert_rate else 1,
                # "{0:.4f}".format(item.tendency_value),
                # "{0:.4f}".format( item.preparing_value),
                # "{0:.4f}".format(item.exceed_value),
                item.equipment_name,
                item.equipment_lrv,
                item.equipment_urv,
                item.qcvn_code,
                round(qcvn_detail_const_area_value_1,2) if qcvn_detail_const_area_value_1 > 0 else None,
                round(qcvn_detail_const_area_value_2,2) if qcvn_detail_const_area_value_2 > 0 else None,
                round(qcvn_detail_const_area_value_3,2) if qcvn_detail_const_area_value_3 > 0 else None,
                TD(text, _class="qcvn_detail_type_code", _value=str(item.qcvn_detail_type_code)),
                round(item.qcvn_detail_min_value, 6) if item.qcvn_detail_min_value else None,
                round(item.qcvn_detail_max_value, 6) if item.qcvn_detail_max_value else None,
                # item.qcvn_detail_const_area_value,
                status[str(item.status)] if item.status else '',
                A(I(_class='fa fa-edit ' + hide_class), data={'url': '/eos/stations/popup_edit_thong_so?station_id='+station_id+'&qcvn_id='+qcvn_id +'&qcvn_kind_id='+qcvn_kind_id +'&station_indicator_id='+ str(idd)}, _class="edit_thong_so_btn btnAddNew", _href="javascript: {};")
            ]
            
            if not view_only:
                listA.append(INPUT(_group='1', _class='select_item ' + hide_class, _type='checkbox', _value=item.id))
            listA.append(item.id)

            aaData.append(listA)
            iRow += 1
        return dict(iTotalRecords=iTotalRecords, iTotalDisplayRecords=iTotalRecords, aaData=aaData, success=True)
    except Exception as ex:
        exc_type, exc_obj, exc_tb = sys.exc_info()
        fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
        print("exc_type",exc_type, fname, exc_tb.tb_lineno)
        return dict(iTotalRecords=0, iTotalDisplayRecords=0, aaData=[], message=str(ex), success=False)


################################################################################
@service.json
def del_station_indicator(*args, **kwargs):
    try:
        table = 'station_indicator'
        id = request.vars.id  # for single record
        array_data = request.vars.ids  # for list record (dc truyen qua app.executeFunction())
        func_code = get_function_code_by_table(table)
        if not auth.has_permission('delete', func_code):
            return dict(success=False, message=T('Access denied!'))

        list_ids = []
        if array_data:  list_ids = array_data.split(',')
        list_ids.append(id) if id else list_ids

        if list_ids:
            db(db[table].id.belongs(list_ids ,null=True)).update(status=const.SI_STATUS['DELETED']['value'])

        return dict(success=True)
    except Exception as ex:
        return dict(success=False, message=str(ex))

@service.json
def edit_station_indicator(*args, **kwargs):
    try:
        table = 'station_indicator'
        id = request.vars.id  # for single record
        array_data = request.vars.ids  # for list record (dc truyen qua app.executeFunction())
        func_code = get_function_code_by_table(table)

        list_ids = []
        if array_data:  list_ids = array_data.split(',')
        list_ids.append(id) if id else list_ids

        if list_ids:
            db(db[table].id.belongs(list_ids)).update(status=const.SI_STATUS['IN_USE']['value'])

        return dict(success=True)
    except Exception as ex:
        return dict(success=False, message=str(ex))

################################################################################
@service.json
@auth.requires(lambda: (auth.has_permission('view', 'indicators')))
def get_list_indicators_auto_adjust(*args, **kwargs):
    try:
        station_id = request.vars.station_id  # Chuoi tim kiem nhap tu form
        view_only = request.vars.view_only
        aaData = []  # Du lieu json se tra ve

        conditions = (db.station_indicator.id > 0)
        conditions &= (db.station_indicator.status == const.SI_STATUS['IN_USE']['value'])
        if station_id:
            conditions &= (db.station_indicator.station_id == station_id)

        list_data = db(conditions).select()
        # Tong so ban ghi khong thuc hien phan trang
        iTotalRecords = db(conditions).count()
        indicator_dict = common.get_indicator_dict()

        # Get range min/max of equipments
        equipment_ids = [item.equipment_id for item in list_data]
        equipments = db(db.equipments.id.belongs(equipment_ids)).select(
            db.equipments.id,
            db.equipments.lrv,
            db.equipments.urv,
        )
        equipments_dict = {}
        for item in equipments:
            id = str(item.id)
            if not equipments_dict.has_key(id):
                equipments_dict[id] = {
                    'lrv': item.lrv,
                    'urv': item.urv,
                }
        
        indicator_ids = []
        for item in list_data:
            indicator_ids.append(indicator_dict[item.indicator_id])
        # Duyet tung phan tu trong mang du lieu vua truy van duoc
        for item in list_data:
            # Equipment range column
            if not equipments_dict.has_key(item.equipment_id):
                out_of_range = T('No equipment equivalent!')
            else:
                out_of_range = '%s %s %s' % (
                    INPUT(_class='', _name='out_of_range', _type='checkbox',
                          _checked=item.out_of_range,_disabled=view_only),
                    INPUT(_class='form_control', _name='out_of_range_min', _readonly='true', _type='text',
                          _value='%s' % equipments_dict[str(item.equipment_id)]['lrv'],
                          _style="width:80px",_disabled=view_only),
                    INPUT(_class='form_control', _name='out_of_range_max', _readonly='true', _type='text',
                          _value='%s' % equipments_dict[str(item.equipment_id)]['urv'],
                          _style="width:80px",_disabled=view_only),
                )

            # Contiuous value column
            textbox = INPUT(_class='form_control continous_equal', _id='continous_equal_%s' % (item.id),
                            _name='continous_equal_value', _style="width:80px",
                            _type='text',
                            _value="%s" % item.continous_equal_value if item.continous_equal_value else '',
                            _readonly=(not item.continous_equal),
                            _disabled=view_only)

            textbox1 = SELECT(
                indicator_ids,
                _class='form_control choosen',
                _id='parameter_value_%s' % (item.id),
                _name='remove_with_indicator',
                _style="width:80px",
                _type='checkbox', _checked=item.remove_with_indicator_check,
                _disabled=view_only,
                value="%s" % item.remove_with_indicator if item.remove_with_indicator else '')
            
            textbox2 = INPUT(_class='form_control extraordinary_value_check',
                             _id='extraordinary_value_check_%s' % (item.id),
                             _name='extraordinary_value',
                             _style="width:80px",
                             _type='text',
                             _value="%s" % item.extraordinary_value if item.extraordinary_value else '',
                             _disabled=view_only)
            
            typeCompareValue = [">" , "<", "=" , "<=" ,">="]
            textbox3 = SELECT(typeCompareValue, _class='form_control choosen',
                             _id='compare_value_check_%s' % (item.id),
                             _name='compare_value',
                             _style="width:80px",
                             _type='text',
                             value="%s" % item.compare_value if item.compare_value else '',
                             _disabled=view_only)
            
            textbox4 = INPUT(_class='form_control coefficient_data',
                             _id='coefficient_data_%s' % (item.id),
                             _name='coefficient_data',
                             _style="width:80px",
                             _type='text',
                             _value="%s" % item.coefficient_data if item.coefficient_data else '')
            
            textbox5 = SELECT(
                indicator_ids,
                _class='form_control choosen',
                             _id='parameter_value_%s' % (item.id),
                             _name='parameter_value',
                             _style="width:80px",
                             _type='text',
                             value="%s" % item.parameter_value if item.parameter_value else '')
            

            aaData.append([
                indicator_dict[item.indicator_id],
                INPUT(_class='', _name='equal0', _type='checkbox', _checked=item.equal0, _disabled=view_only),
                INPUT(_class='', _name='negative_value', _type='checkbox', _checked=item.negative_value, _disabled=view_only),
                out_of_range,
                INPUT(_class='', _name='equipment_adjust', _type='checkbox', _checked=item.equipment_adjust, _disabled=view_only),
                INPUT(_class='', _name='equipment_status', _type='checkbox', _checked=item.equipment_status, _disabled=view_only),
                '%s %s' % (INPUT(_class='', _name='continous_equal', _type='checkbox', _checked=item.continous_equal, _disabled=view_only),
                            textbox),
                '%s %s' % (INPUT(_class='', _name='remove_with_indicator_check', _type='checkbox', _checked=item.remove_with_indicator_check, _disabled=view_only),
                    textbox1,
                ),
                '%s %s' % (INPUT(_class='', _name='extraordinary_value_check', _type='checkbox', _checked=item.extraordinary_value_check, _disabled=view_only),
                    textbox2,
                ),
                '%s %s' % (INPUT(_class='', _name='compare_value_check', _type='checkbox', _checked=item.compare_value_check, _disabled=view_only),
                    textbox3,
                ),
                '%s' % (textbox4),
                '%s' % (textbox5),
                str(item.id)
            ])
        return dict(iTotalRecords=iTotalRecords, iTotalDisplayRecords=iTotalRecords, aaData=aaData, success=True)
    except Exception as ex:
        return dict(iTotalRecords=0, iTotalDisplayRecords=0, aaData=[], message=str(ex), success=False)


################################################################################
@service.json
@auth.requires(lambda: (auth.has_permission('edit', 'indicators')))
def ajax_save_auto_adjust(*args, **kwargs):
    try:
        import json
        data = request.vars.data
        data = json.loads(data)

        print("data", data)
        for station_indicator_id in data:
            db(db.station_indicator.id == station_indicator_id).update(**data[station_indicator_id])

        return dict(success=True)
    except Exception as ex:
        return dict(message=str(ex), success=False)


################################################################################
@service.json
@auth.requires(lambda: (auth.has_permission('delete', 'stations')))
def del_stations(*args, **kwargs):
    try:
        array_data = request.vars.ids
        list_ids = array_data.split(',')
        # update history
        for id in list_ids:
            db(db.manager_stations.station_id == id).delete()
            station_name = db.stations(id).station_name
            db.manager_stations_history.insert(station_id=id,
                                               station_name=station_name,
                                               action='Delete',
                                               username=current_user.fullname or None,
                                               description='',
                                               update_time=datetime.now())
        ######
        db(db.stations.id.belongs(list_ids)).delete()
        return dict(success=True)
    except Exception as ex:
        return dict(success=False, message=str(ex))


################################################################################
@service.json
@auth.requires(lambda: (auth.has_permission('edit', 'stations')))
def link_indicator_to_station(*args, **kwargs):
    try:
        station_id = request.vars.station_id
        station_name = request.vars.station_name
        indicator_id = request.vars.indicator
        tendency = request.vars.tendency
        preparing = request.vars.preparing
        exceed = request.vars.exceed
        equipment_id = request.vars.equipment_id
        equipment = request.vars.equipment if equipment_id else ''
        equipment_lrv = request.vars.equipment_lrv
        equipment_urv = request.vars.equipment_urv
        qcvn_id = request.vars.qcvn_id
        qcvn_code = request.vars.qcvn_code if qcvn_id else ''
        qcvn_kind_id = request.vars.qcvn_kind_id
        qcvn_detail_id = request.vars.qcvn_detail_id
        qcvn_detail_type_code = request.vars.qcvn_detail_type_code
        qcvn_detail_min_value = request.vars.qcvn_detail_min_value
        qcvn_detail_max_value = request.vars.qcvn_detail_max_value
        qcvn_detail_const_area_value = request.vars.qcvn_detail_const_area_value
        qcvn_detail_const_area_value_1 = request.vars.qcvn_detail_const_area_value_1
        qcvn_detail_const_area_value_2 = request.vars.qcvn_detail_const_area_value_2
        qcvn_detail_const_area_value_3 = request.vars.qcvn_detail_const_area_value_3
        
        indicator_name_mapping = request.vars.indicator_name_mapping
        convert_rate = request.vars.convert_rate
        if equipment_id:
            data_equiment = db(db.equipments.id == equipment_id).select(db.equipments.lrv,
                                                                        db.equipments.urv,
                                                                        db.equipments.equipment)
            for item in data_equiment:
                equipment_lrv = item.lrv
                equipment_urv = item.urv
                equipment_name = item.equipment

        indicator = db.indicators(indicator_id) or None
        station = db.stations(station_id) or None
        qcvn_detail = get_qcvn_detail_by_indicator_and_qcvn(indicator_id, qcvn_id, qcvn_kind_id)
        if not station:
            return dict(success=False, message=T('Station does not exist!'))
        station_type = station.station_type or const.STATION_TYPE['WASTE_WATER']['value']
        if not indicator:
            return dict(success=False, message=T('Indicator does not exist!'))
        unit = indicator.unit
        conditions = ((db.station_indicator.station_id == station_id) &
                      (db.station_indicator.indicator_id == indicator_id) &
                      (db.station_indicator.status == const.SI_STATUS['IN_USE']['value']) &
                      (db.station_indicator.station_type == station_type))
        existed = db(conditions).count(db.station_indicator.id)
        if existed:
            return dict(success=False, message=T('Indicator is existed!'))
        qcvn_min, qcvn_max = get_station_indicator_min_max_value(
            qcvn_detail, qcvn_detail_const_area_value_1, qcvn_detail_const_area_value_2, qcvn_detail_const_area_value_3)
        
        db.station_indicator.update_or_insert(
            (db.station_indicator.station_id == station_id) & (db.station_indicator.indicator_id == indicator_id),
            station_id=station_id, station_name=station_name, station_type=station_type,
            indicator_id=indicator_id, tendency_value=tendency, preparing_value=preparing,
            exceed_value=exceed, unit=unit, qcvn_id=qcvn_id, qcvn_code=qcvn_code,
            equipment_id=equipment_id, equipment_name=equipment, equipment_lrv=equipment_lrv,
            equipment_urv=equipment_urv,
            status=const.SI_STATUS['IN_USE']['value'],
            qcvn_detail_type_code=qcvn_detail_type_code,
            qcvn_detail_min_value=qcvn_min,
            qcvn_detail_max_value=qcvn_max,
            qcvn_kind_id=qcvn_kind_id,
            qcvn_detail_const_area_value=qcvn_detail_const_area_value,
            mapping_name=indicator_name_mapping, convert_rate=convert_rate)
        
        db.qcvn_station_kind.update_or_insert((db.qcvn_station_kind.station_id == station_id) & (db.qcvn_station_kind.qcvn_id == qcvn_id) & (db.qcvn_station_kind.qcvn_kind_id == qcvn_kind_id),
                                            station_id=station_id, station_name=station_name, qcvn_id=qcvn_id,
                                            station_type=station_type,
                                            qcvn_kind_id=qcvn_kind_id,
                                            qcvn_detail_const_area_value_1=qcvn_detail_const_area_value_1,
                                            qcvn_detail_const_area_value_2=qcvn_detail_const_area_value_2,
                                            qcvn_detail_const_area_value_3=qcvn_detail_const_area_value_3,
                                            status=const.SI_STATUS['IN_USE']['value'])
        # update history
        db.manager_stations_history.insert(station_id=station_id,
                                           action='Update',
                                           username=current_user.fullname or None,
                                           description='Them_Thong_So',
                                           update_time=datetime.now())
        ###
        return dict(success=True)
    except Exception as ex:
        return dict(success=False, message=str(ex))

@service.json
@auth.requires(lambda: (auth.has_permission('edit', 'stations')))
def elink_indicator_to_station(*args, **kwargs):
    try:
        indicator_id = request.vars.indicator_id
        station_id = request.vars.station_id
        station_name = request.vars.station_name
        qcvn_id = request.vars.qcvn_id
        qcvn_code = request.vars.qcvn_code if qcvn_id else ''
        qcvn_kind_id = request.vars.qcvn_kind_id
        qcvn_detail_type_code = request.vars.qcvn_detail_type_code
        qcvn_detail_const_area_value_1 = request.vars.qcvn_detail_const_area_value_1
        qcvn_detail_const_area_value_2 = request.vars.qcvn_detail_const_area_value_2
        qcvn_detail_const_area_value_3 = request.vars.qcvn_detail_const_area_value_3
        indicator_name_mapping = request.vars.indicator_name_mapping
        station_indicator_id = request.vars.station_indicator_id
        

        indicator = db.indicators(indicator_id) or None
        station = db.stations(station_id) or None
        qcvn_detail = get_qcvn_detail_by_indicator_and_qcvn(indicator_id, qcvn_id, qcvn_kind_id)
        if not station:
            return dict(success=False, message=T('Station does not exist!'))
        station_type = station.station_type or const.STATION_TYPE['WASTE_WATER']['value']
        if not indicator:
            return dict(success=False, message=T('Indicator does not exist!'))
        unit = indicator.unit
        status = const.SI_STATUS['IN_USE']['value']
        qcvn_min, qcvn_max = get_station_indicator_min_max_value(
            qcvn_detail, qcvn_detail_const_area_value_1, qcvn_detail_const_area_value_2, qcvn_detail_const_area_value_3)
        
        db.station_indicator.update_or_insert(
            (db.station_indicator.id == station_indicator_id),
            station_id=station_id, station_name=station_name,
            station_type=station_type,
            indicator_id=indicator_id, 
            unit=unit, qcvn_id=qcvn_id,
            qcvn_code=qcvn_code,
            status=status,
            qcvn_detail_type_code=qcvn_detail_type_code,
            qcvn_detail_min_value=qcvn_min,
            qcvn_detail_max_value=qcvn_max,
            qcvn_kind_id=qcvn_kind_id,
            mapping_name=indicator_name_mapping,
            )
        
        db.qcvn_station_kind.update_or_insert((db.qcvn_station_kind.station_id == station_id) & (db.qcvn_station_kind.qcvn_id == qcvn_id) & (db.qcvn_station_kind.qcvn_kind_id == qcvn_kind_id),
                                            station_id=station_id, station_name=station_name, qcvn_id=qcvn_id,
                                            station_type=station_type,
                                            qcvn_kind_id=qcvn_kind_id,
                                            qcvn_detail_const_area_value_1=qcvn_detail_const_area_value_1,
                                            qcvn_detail_const_area_value_2=qcvn_detail_const_area_value_2,
                                            qcvn_detail_const_area_value_3=qcvn_detail_const_area_value_3,
                                            status=const.SI_STATUS['IN_USE']['value'])
        
        # update history
        db.manager_stations_history.insert(station_id=station_id,
                                           action='Update',
                                           username=current_user.fullname or None,
                                           description='Sua_Thong_So',
                                           update_time=datetime.now())
        ###
        return dict(success=True)
    except Exception as ex:
        exc_type, exc_obj, exc_tb = sys.exc_info()
        fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
        print("exc_type", exc_type, fname, exc_tb.tb_lineno)
        return dict(success=False, message=str(ex))


def get_station_indicator_min_max_value(qcvn_detail,
                                        qcvn_detail_const_area_value_1,
                                        qcvn_detail_const_area_value_2,qcvn_detail_const_area_value_3):
    qcvn_min_value_indicator = qcvn_max_value_indicator = None
    if qcvn_detail is None:
        return qcvn_min_value_indicator, qcvn_max_value_indicator

    if qcvn_detail_const_area_value_1 == "":
        qcvn_detail_const_area_value_1 = 1

    if qcvn_detail_const_area_value_2 == "":
        qcvn_detail_const_area_value_2 = 1

    if qcvn_detail_const_area_value_3 == "":
        qcvn_detail_const_area_value_3 = 1


    if qcvn_detail.have_factor_qcvn == 1:
        if qcvn_detail.qcvn_min_value:
            qcvn_min_value_indicator = float(qcvn_detail.qcvn_min_value) * float(
                qcvn_detail_const_area_value_1) * float(qcvn_detail_const_area_value_2)*float(qcvn_detail_const_area_value_3)
        if qcvn_detail.qcvn_max_value:
            qcvn_max_value_indicator = float(qcvn_detail.qcvn_max_value) * float(
                qcvn_detail_const_area_value_1) * float(qcvn_detail_const_area_value_2)*float(qcvn_detail_const_area_value_3)
    else:
        if qcvn_detail.qcvn_min_value:
            qcvn_min_value_indicator = float(qcvn_detail.qcvn_min_value)
        if qcvn_detail.qcvn_max_value:
            qcvn_max_value_indicator = float(qcvn_detail.qcvn_max_value)

    return qcvn_min_value_indicator, qcvn_max_value_indicator


def get_qcvn_detail_by_indicator_and_qcvn(indicator_id, qcvn_id, qcvn_kind_id):
    row = db(
        (db.qcvn_detail.id > 0) &
        (db.qcvn_detail.qcvn_id == qcvn_id) &
        (db.qcvn_detail.indicator_id == indicator_id) &
        (db.qcvn_detail.qcvn_type_code == qcvn_kind_id) &
        (db.qcvn_detail.status == const.SI_STATUS['IN_USE']['value'])
    ).select()
    if row:
        return row.first()
    else:
        return None


################################################################################
@service.json
@auth.requires(lambda: (auth.has_permission('edit', 'stations')))
def link_qcvn_kind_to_station(*args, **kwargs):
    try:
        # get parameters
        station_id = request.vars.station_id
        station_name = request.vars.station_name
        qcvn_id = request.vars.qcvn_id
        qcvn_kind_id = request.vars.qcvn_kind_id
        qcvn_code = request.vars.qcvn_code
        qcvn_detail_type_code = request.vars.qcvn_detail_type_code
        qcvn_detail_const_area_value_1 = request.vars.qcvn_detail_const_area_value_1
        qcvn_detail_const_area_value_2 = request.vars.qcvn_detail_const_area_value_2
        qcvn_detail_const_area_value_3 = request.vars.qcvn_detail_const_area_value_3
        station_type = request.vars.station_type

        if qcvn_kind_id == '':
            qcvn_detail_const_area_value_1 = 1
            qcvn_detail_const_area_value_2 = 1
            qcvn_detail_const_area_value_3 = 1

        if qcvn_detail_type_code == '-- Chọn loại --':
            qcvn_detail_type_code = '---'
        station = db.stations(station_id) or None
        if not station:
            return dict(success=False, message=T('Station is not existed!'))
        station_type = station.station_type or const.STATION_TYPE['WASTE_WATER']['value']

        # conditions = ((db.qcvn_station_kind.station_id == station_id) &
        #               (db.qcvn_station_kind.qcvn_id == qcvn_id) &
        #               (db.qcvn_station_kind.qcvn_kind_id == qcvn_kind_id) &
        #               (db.qcvn_station_kind.status == const.SI_STATUS['IN_USE']['value']) &
        #               (db.qcvn_station_kind.station_type == station_type))
        # existed = db(conditions).count(db.qcvn_station_kind.id)
        # if existed:
        #     return dict(success=False, message=T('Loại trong QCVN is existed!'))

        db.qcvn_station_kind.update_or_insert((db.qcvn_station_kind.station_id == station_id),
                                              station_id=station_id, station_name=station_name, qcvn_id=qcvn_id,
                                              station_type=station_type,
                                              qcvn_kind_id=qcvn_kind_id,
                                              qcvn_detail_const_area_value_1=qcvn_detail_const_area_value_1,
                                              qcvn_detail_const_area_value_2=qcvn_detail_const_area_value_2,
                                              qcvn_detail_const_area_value_3=qcvn_detail_const_area_value_3,
                                              status=const.SI_STATUS['IN_USE']['value'])

        # Update for all indicator in station
        #  Get all indicator in station
        conditionsAllIndicator = ((db.station_indicator.station_id == station_id) &
                                  (db.station_indicator.status == const.SI_STATUS['IN_USE']['value']) &
                                  (db.station_indicator.station_type == station_type))
        allIndicators = db(conditionsAllIndicator).select()

        if allIndicators:
            for indicator in allIndicators:
                if indicator:
                    indicator_id = indicator.indicator_id
                    qcvn_detail = get_qcvn_detail_by_indicator_and_qcvn(indicator_id, qcvn_id, qcvn_kind_id)

                    qcvn_min_value_indicator = ''
                    qcvn_max_value_indicator = ''
                    if qcvn_detail:
                        if qcvn_detail.have_factor_qcvn == 1:
                            if qcvn_detail.qcvn_min_value:
                                qcvn_min_value_indicator = float(qcvn_detail.qcvn_min_value) * float(
                                    qcvn_detail_const_area_value_1) * float(qcvn_detail_const_area_value_2) * float(qcvn_detail_const_area_value_3)
                            if qcvn_detail.qcvn_max_value:
                                qcvn_max_value_indicator = float(qcvn_detail.qcvn_max_value) * float(
                                    qcvn_detail_const_area_value_1) * float(qcvn_detail_const_area_value_2) * float(qcvn_detail_const_area_value_3)
                        else:
                            if qcvn_detail.qcvn_min_value:
                                qcvn_min_value_indicator = float(qcvn_detail.qcvn_min_value)
                            if qcvn_detail.qcvn_max_value:
                                qcvn_max_value_indicator = float(qcvn_detail.qcvn_max_value)

                        # Update
                        db.station_indicator.update_or_insert(
                            (db.station_indicator.station_id == station_id) & (
                                    db.station_indicator.indicator_id == indicator_id) & (
                                    db.station_indicator.status == const.SI_STATUS['IN_USE']['value']),
                            qcvn_id=qcvn_id,
                            qcvn_code=qcvn_code,
                            qcvn_detail_type_code=qcvn_detail_type_code,
                            qcvn_detail_min_value=qcvn_min_value_indicator,
                            qcvn_detail_max_value=qcvn_max_value_indicator)
            # update history
            db.manager_stations_history.insert(station_id=station_id,
                                               action='Update',
                                               username=current_user.fullname or None,
                                               description='Thay_doi_noi_dung_QCVN',
                                               update_time=datetime.now())
        ###
        return dict(success=True, content=T('MSG_INFO_SAVE_SUCCESS'))
    except Exception as ex:
        return dict(success=False, message=str(ex))


################################################################################
@service.json
@auth.requires(lambda: (auth.has_permission('edit', 'alarm_log')))
def ajax_save_station_alarm(*args, **kwargs):
    try:
        station_id = request.vars.station_id
        station_name = request.vars.station_name
        type = request.vars.station_type
        tendency_method_email = request.vars.tendency_method_email
        tendency_method_sms = request.vars.tendency_method_sms
        tendency_emails = request.vars.tendency_emails
        tendency_phones = request.vars.tendency_phones
        tendency_msg = request.vars.tendency_msg
        preparing_method_email = request.vars.preparing_method_email
        preparing_method_sms = request.vars.preparing_method_sms
        preparing_emails = request.vars.preparing_emails
        preparing_phones = request.vars.preparing_phones
        preparing_msg = request.vars.preparing_msg
        exceed_method_email = request.vars.exceed_method_email
        exceed_method_sms = request.vars.exceed_method_sms
        exceed_method_notification = request.vars.exceed_method_notification
        exceed_emails = request.vars.exceed_emails
        exceed_phones = request.vars.exceed_phones
        exceed_msg = request.vars.exceed_msg
        exceed_mail_header = request.vars.exceed_mail_header
        frequency_notify = request.vars.frequency_notify

        # Check if record existed
        count = db(db.station_alarm.station_id == station_id).count()
        if count:
            db(db.station_alarm.station_id == station_id).update(
                tendency_method_email=tendency_method_email,
                tendency_method_sms=tendency_method_sms,
                tendency_email_list=tendency_emails,
                tendency_phone_list=tendency_phones,
                tendency_msg=tendency_msg,
                preparing_method_email=preparing_method_email,
                preparing_method_sms=preparing_method_sms,
                preparing_email_list=preparing_emails,
                preparing_phone_list=preparing_phones,
                preparing_msg=preparing_msg,
                exceed_method_email=exceed_method_email,
                exceed_method_sms=exceed_method_sms,
                exceed_method_notification=exceed_method_notification,
                exceed_email_list=exceed_emails,
                exceed_phone_list=exceed_phones,
                exceed_msg=exceed_msg,
                exceed_emails_header=exceed_mail_header,

            )

        else:
            db.station_alarm.insert(
                station_id=station_id,
                station_name=station_name,
                station_type=type,
                tendency_method_email=tendency_method_email,
                tendency_method_sms=tendency_method_sms,
                tendency_email_list=tendency_emails,
                tendency_phone_list=tendency_phones,
                tendency_msg=tendency_msg,
                preparing_method_email=preparing_method_email,
                preparing_method_sms=preparing_method_sms,
                preparing_email_list=preparing_emails,
                preparing_phone_list=preparing_phones,
                preparing_msg=preparing_msg,
                exceed_method_email=exceed_method_email,
                exceed_method_sms=exceed_method_sms,
                exceed_method_notification=exceed_method_notification,
                exceed_email_list=exceed_emails,
                exceed_phone_list=exceed_phones,
                exceed_msg=exceed_msg,
                exceed_emails_header=exceed_mail_header,
            )
        if frequency_notify:
            db(db.station_alarm.station_id == station_id).update(frequency_notify=frequency_notify)

        # update history
        db.manager_stations_history.insert(station_id=station_id,
                                           action='Update',
                                           username=current_user.fullname or None,
                                           description='Thay_doi_canh_bao',
                                           update_time=datetime.now())
        ###
        return dict(success=True)
    except Exception as ex:
        return dict(success=False, message=str(ex))


################################################################################
@service.json
@auth.requires(lambda: (auth.has_permission('edit', 'stations')))
def ajax_save_send_data(*args, **kwargs):
    try:
        station_id = request.vars.station_id
        file_mapping = request.vars.file_mapping
        file_mapping_desc = request.vars.file_mapping_desc

        db(db.stations.id == station_id).update(
            file_mapping=file_mapping,
            file_mapping_desc=file_mapping_desc,
        )

        return dict(success=True)
    except Exception as ex:
        return dict(success=False, message=str(ex))


################################################################################

################################################################################
@service.json
@auth.requires(lambda: (auth.has_permission('edit', 'stations')))
def ajax_save_file_mapping(*args, **kwargs):
    try:
        station_id = request.vars.station_id
        file_mapping = request.vars.file_mapping
        file_mapping_desc = request.vars.file_mapping_desc

        db(db.stations.id == station_id).update(
            file_mapping=file_mapping,
            file_mapping_desc=file_mapping_desc,
        )
        # update history
        db.manager_stations_history.insert(station_id=station_id,
                                           action='Update',
                                           username=current_user.fullname or None,
                                           description='Thay_doi_file_mapping',
                                           update_time=datetime.now())
        ###
        return dict(success=True)
    except Exception as ex:
        return dict(success=False, message=str(ex))


################################################################################
def test():
    provinces = db(db.provinces.id > 0).select()
    return dict(provinces=provinces)


################################################################################
@service.json
@auth.requires(lambda: (auth.has_permission('view', 'indicators')) or (auth.has_permission('view', 'view_report')) or (
        auth.has_permission('view', 'view_log')))
def get_indicators(*args, **kwargs):
    try:
        aqi = request.vars.aqi
        html = ''
        station_id = request.vars.station_id
        from_public = request.vars.from_public
        conditions = (db.station_indicator.station_id == station_id)
        conditions &= (db.station_indicator.status == const.SI_STATUS['IN_USE']['value'])
        if request.vars.is_calc_qi == "true":
            conditions &= (db.station_indicator.is_calc_qi == True)
        if from_public:
            conditions &= (db.station_indicator.is_public == True)
        rows = db(conditions).select(db.station_indicator.indicator_id)
        indicators = []
        for row in rows:
            indicators.append(row.indicator_id)
        rows = db(db.indicators.id.belongs(indicators)).select(db.indicators.ALL)
        for row in rows:
            if aqi is None:
                html += '<option value="%(value)s" selected>%(name)s (%(unit)s)</option>' % dict(value=row.indicator,
                                                                                                 name=row.indicator,
                                                                                                 unit=row.unit)
            else:
                html += '<option value="%(value)s" selected>%(name)s</option>' % dict(value=row.indicator,
                                                                                                 name=row.indicator)

        return dict(success=True, html=html)
    except Exception as ex:
        return dict(success=False, message=str(ex))


################################################################################
@service.json
@auth.requires(lambda: (auth.has_permission('view', 'stations')))
def get_station_by_area(*args, **kwargs):
    try:
        longitude_min = False
        longitude_max = False
        latitude_min = False
        latitude_max = False
        find_log = False
        find_lat = False
        html = '<option value="">%s</option>' % (T('-- Select an option --'))
        # Get variables from request
        area_id = request.vars.area_id
        # Create conditions
        conditions = (db.stations.id > 0)
        if area_id:
            conditions &= (db.stations.area_ids == area_id)
        
        # Get data by conditions
        # hungdx phan quyen quan ly trạm theo user issue 44
        if current_user:
            if not (auth.has_membership('admin') or auth.has_membership(const.GROUP_MANAGER)):
                list_station_manager = db(db.manager_stations.user_id == current_user.id).select(
                    db.manager_stations.station_id)
                station_ids = [str(item.station_id) for item in list_station_manager]
                conditions &= (db.stations.id.belongs(station_ids))

        rows = db(conditions).select(db.stations.id, db.stations.station_name,
                                     db.stations.longitude, db.stations.latitude)
        # Create options from result and append to html
        for row in rows:
            html += '<option value="%s" data-id="%s" data-lat="%s" data-lon="%s">%s</option>' \
                    % (str(row.id), str(row.id), row.latitude, row.longitude, row.station_name)
            if row.longitude:
                if longitude_min == False:
                    longitude_min = row.longitude
                    longitude_max = row.longitude
                    find_log = True
                else:
                    if longitude_min > row.longitude:
                        longitude_min = row.longitude
                    if longitude_max < row.longitude:
                        longitude_max = row.longitude
            if row.latitude:
                if latitude_min == False:
                    latitude_min = row.latitude
                    latitude_max = row.latitude
                    find_lat = True
                else:
                    if latitude_min > row.latitude:
                        latitude_min = row.latitude
                    if latitude_max < row.latitude:
                        latitude_max = row.latitude
        longitude_average = (longitude_max + longitude_min) / 2 if find_log and find_lat else False
        latitude_average = (latitude_max + latitude_min) / 2 if find_log and find_lat else False
        return dict(success=True, html=html, longitude_average=longitude_average, latitude_average=latitude_average)
    except Exception as ex:
        return dict(success=False, message=str(ex))


################################################################################
@service.json
@auth.requires(lambda: (auth.has_permission('view', 'stations')))
def get_station_by_province(*args, **kwargs):
    try:
        longitude_min = False
        longitude_max = False
        latitude_min = False
        latitude_max = False
        find_log = False
        find_lat = False
        html = '<option value="">%s</option>' % (T('-- Select an option --'))
        # Get variables from request
        province_id = request.vars.province_id
        # Create conditions
        conditions = (db.stations.id > 0)
        if province_id:
            conditions &= (db.stations.province_id == province_id)
        # Get data by conditions
        # hungdx phan quyen quan ly trạm theo user issue 44
        if current_user:
            if not (auth.has_membership('admin') or auth.has_membership(const.GROUP_MANAGER)):
                list_station_manager = db(db.manager_stations.user_id == current_user.id).select(
                    db.manager_stations.station_id)
                station_ids = [str(item.station_id) for item in list_station_manager]
                conditions &= (db.stations.id.belongs(station_ids))

        rows = db(conditions).select(db.stations.id, db.stations.station_name,
                                     db.stations.longitude, db.stations.latitude)
        # Create options from result and append to html
        for row in rows:
            html += '<option value="%s" data-id="%s" data-lat="%s" data-lon="%s">%s</option>' \
                    % (str(row.id), str(row.id), row.latitude, row.longitude, row.station_name)
            if row.longitude:
                if longitude_min == False:
                    longitude_min = row.longitude
                    longitude_max = row.longitude
                    find_log = True
                else:
                    if longitude_min > row.longitude:
                        longitude_min = row.longitude
                    if longitude_max < row.longitude:
                        longitude_max = row.longitude
            if row.latitude:
                if latitude_min == False:
                    latitude_min = row.latitude
                    latitude_max = row.latitude
                    find_lat = True
                else:
                    if latitude_min > row.latitude:
                        latitude_min = row.latitude
                    if latitude_max < row.latitude:
                        latitude_max = row.latitude
        longitude_average = (longitude_max + longitude_min) / 2 if find_log and find_lat else False
        latitude_average = (latitude_max + latitude_min) / 2 if find_log and find_lat else False
        return dict(success=True, html=html, longitude_average=longitude_average, latitude_average=latitude_average)
    except Exception as ex:
        return dict(success=False, message=str(ex))


################################################################################
@service.json
@auth.requires(lambda: (auth.has_permission('view', 'stations')))
def get_station_by_station_type(*args, **kwargs):
    try:
        longitude_min = False
        longitude_max = False
        latitude_min = False
        latitude_max = False
        find_log = False
        find_lat = False
        html = '<option value="">%s</option>' % (T('-- Select an option --'))
        # Get variables from request
        station_type = request.vars.station_type
        # Create conditions
        conditions = (db.stations.id > 0)
        if station_type:
            conditions &= (db.stations.station_type == station_type)
        # Get data by conditions
        # hungdx phan quyen quan ly trạm theo user issue 44
        if current_user:
            if not (auth.has_membership('admin') or auth.has_membership(const.GROUP_MANAGER)):
                list_station_manager = db(db.manager_stations.user_id == current_user.id).select(
                    db.manager_stations.station_id)
                station_ids = [str(item.station_id) for item in list_station_manager]
                conditions &= (db.stations.id.belongs(station_ids))

        rows = db(conditions).select(db.stations.id, db.stations.station_name,
                                     db.stations.longitude, db.stations.latitude)
        # Create options from result and append to html
        for row in rows:
            html += '<option value="%s" data-id="%s" data-lat="%s" data-lon="%s">%s</option>' \
                    % (str(row.id), str(row.id), row.latitude, row.longitude, row.station_name)
            if row.longitude:
                if longitude_min == False:
                    longitude_min = row.longitude
                    longitude_max = row.longitude
                    find_log = True
                else:
                    if longitude_min > row.longitude:
                        longitude_min = row.longitude
                    if longitude_max < row.longitude:
                        longitude_max = row.longitude
            if row.latitude:
                if latitude_min == False:
                    latitude_min = row.latitude
                    latitude_max = row.latitude
                    find_lat = True
                else:
                    if latitude_min > row.latitude:
                        latitude_min = row.latitude
                    if latitude_max < row.latitude:
                        latitude_max = row.latitude
        longitude_average = (longitude_max + longitude_min) / 2 if find_log and find_lat else False
        latitude_average = (latitude_max + latitude_min) / 2 if find_log and find_lat else False
        return dict(success=True, html=html, longitude_average=longitude_average, latitude_average=latitude_average)
    except Exception as ex:
        return dict(success=False, message=str(ex))


################################################################################
@service.json
@auth.requires(lambda: (auth.has_permission('view', 'stations')))
def get_station_by_conditions(*args, **kwargs):
    try:
        longitude_min = False
        longitude_max = False
        latitude_min = False
        latitude_max = False
        find_log = False
        find_lat = False
        html = '<option value="">%s</option>' % (T('-- Select an option --'))
        # Get variables from request
        area_id = request.vars.area_id
        province_id = request.vars.province_id
        station_type = request.vars.station_type
        from_public = request.vars.from_public
        # Create conditions
        conditions = (db.stations.id > 0)
        if area_id:
            conditions &= (db.stations.area_id == area_id)
        if province_id:
            conditions &= (db.stations.province_id == province_id)
        if station_type:
            conditions &= (db.stations.station_type == station_type)
        if from_public:
            conditions &= (db.stations.is_public == True)
        # hungdx phan quyen quan ly trạm theo user issue 44
        if current_user:
            if not (auth.has_membership('admin') or auth.has_membership(const.GROUP_MANAGER)):
                list_station_manager = db(db.manager_stations.user_id == current_user.id). \
                    select(db.manager_stations.station_id)
                station_ids = [str(item.station_id) for item in list_station_manager]
                conditions &= (db.stations.id.belongs(station_ids))
        # Get data by conditions
        rows = db(conditions).select(db.stations.id, db.stations.station_name,
                                     db.stations.longitude, db.stations.latitude)
        # Create options from result and append to html
        for row in rows:
            html += '<option value="%s" data-id="%s" data-lat="%s" data-lon="%s">%s</option>' \
                    % (str(row.id), str(row.id), row.latitude, row.longitude, row.station_name)
            if row.longitude:
                if longitude_min == False:
                    longitude_min = row.longitude
                    longitude_max = row.longitude
                    find_log = True
                else:
                    if longitude_min > row.longitude:
                        longitude_min = row.longitude
                    if longitude_max < row.longitude:
                        longitude_max = row.longitude
            if row.latitude:
                if latitude_min == False:
                    latitude_min = row.latitude
                    latitude_max = row.latitude
                    find_lat = True
                else:
                    if latitude_min > row.latitude:
                        latitude_min = row.latitude
                    if latitude_max < row.latitude:
                        latitude_max = row.latitude
        longitude_average = (longitude_max + longitude_min) / 2 if find_log and find_lat else False
        latitude_average = (latitude_max + latitude_min) / 2 if find_log and find_lat else False
        return dict(success=True, html=html, longitude_average=longitude_average, latitude_average=latitude_average)
    except Exception as ex:
        return dict(success=False, message=str(ex))


################################################################################
@service.json
@auth.requires(
    lambda: (auth.has_permission('view', 'stations')) or (auth.has_permission('view', 'manager_station_type')))
def get_list_stations_for_test(*args, **kwargs):
    try:
        iDisplayStart = int(request.vars.iDisplayStart)
        iDisplayLength = int(request.vars.iDisplayLength)
        s_search = request.vars.sSearch
        added_columns = request.vars.added_columns or ''
        if added_columns:
            added_columns = added_columns.split(',')
        type = request.vars.type
        sometext = request.vars.sometext
        province_id = request.vars.province_id

        aaData = []
        limitby = (iDisplayStart, iDisplayLength + 1)  # Tuple dung de phan trang (vtri bat dau - chieu dai)

        conditions = (db.stations.id > 0)
        if current_user:
            if not (auth.has_membership('admin') or auth.has_membership(const.GROUP_MANAGER)):
                list_station_manager = db(db.manager_stations.user_id == current_user.id).select(
                    db.manager_stations.station_id)
                station_ids = [str(item.station_id) for item in list_station_manager]
                conditions &= (db.stations.id.belongs(station_ids))
        # Neu chuoi tim kiem khac rong thi them dieu kien truy van voi chuoi tim kiem
        if sometext:
            conditions &= ((db.stations.station_code.contains(sometext)) |
                           (db.stations.station_name.contains(sometext)) |
                           (db.stations.description.contains(sometext)) |
                           (db.stations.contact_point.contains(sometext)) |
                           (db.stations.phone.contains(sometext)) |
                           (db.stations.email.contains(sometext)) |
                           (db.stations.address.contains(sometext)))
        if type:
            conditions &= (db.stations.station_type == type)
        if province_id:
            conditions &= (db.stations.province_id == province_id)

        list_data = db(conditions).select(db.stations.id,
                                          db.stations.station_name,
                                          db.stations.status,
                                          db.stations.station_type,
                                          db.stations.province_id,
                                          db.stations.address,
                                          db.stations.phone,
                                          db.stations.email,
                                          limitby=limitby)
        # Tong so ban ghi khong thuc hien phan trang
        iTotalRecords = db(conditions).count()
        # Thu tu ban ghi
        iRow = iDisplayStart + 1
        provice_dict = common.get_province_dict()

        ## Get station's area info
        areas = common.get_area_by_station_dict()

        # Duyet tung phan tu trong mang du lieu vua truy van duoc
        added_item = dict()
        for item in list_data:
            if added_columns:
                added_item['status'] = provice_dict.get(item.status)
                added_item['province_id'] = provice_dict.get(item.province_id)
                added_item['address'] = item.address
                added_item['area_id'] = areas.get(item.id)
                added_item['phone'] = item.phone
                added_item['email'] = item.email
            row = [
                INPUT(_group='0', _class='select_item', _type='checkbox', _value=item.id),
                A(str(iRow), _href=URL('form', args=[item.id])),
                A(item.station_name, _href=URL('form', args=[item.id])),
                # station_type[item.station_type]
            ]
            for column in added_columns:
                if column and added_item.has_key(column):
                    row.append(added_item[column])
            aaData.append(row)
            iRow += 1
        return dict(iTotalRecords=iTotalRecords, iTotalDisplayRecords=iTotalRecords, aaData=aaData, success=True)
    except Exception as ex:
        return dict(iTotalRecords=0, iTotalDisplayRecords=0, aaData=[], message=str(ex), success=False)


################################################################################
@service.json
@auth.requires(lambda: (auth.has_permission('view', 'adjust_manager')))
def inline_adjust(*args, **kwargs):
    try:
        table = request.vars.table
        record_id = request.vars.record_id
        indicator = request.vars.indicator
        new_value = request.vars.new_value
        if not table:
            table = 'data_min'
        rec = db[table](record_id) or None
        if rec:
            conditions = (db.data_adjust.station_id == rec.station_id)
            conditions &= (db.data_adjust.get_time == rec.get_time)
            rec2 = db(conditions).select(db.data_adjust.ALL).first()
            data2 = dict()
            log_str = ''  # '{}'.format()
            old_value = new_value
            if rec2:
                data2 = rec2.data
                old_value = data2[indicator]
                log_str = '{} -> {}'.format(data2[indicator], new_value)
            data2[indicator] = new_value
            db.data_adjust.update_or_insert(conditions, station_id=rec.station_id, get_time=rec.get_time, data=data2,
                                            is_approved=False)
            if old_value != new_value:
                db.manager_stations_history.insert(station_id=rec.station_id,
                                                   action='Approve data',
                                                   username=current_user.fullname or None,
                                                   description='{}: {}'.format(indicator, log_str),
                                                   update_time=datetime.now())
        return dict(success=True)
    except Exception as ex:
        return dict(success=False, message=str(ex))


###################################################################################
@service.json
@auth.requires_login()
def view_camera_on_dashboard():
    station_id = request.vars.station_id
    rows = db(db.camera_links.station_id == station_id).select(db.camera_links.ALL, orderby=db.camera_links.order_no)
    return dict(rows=rows)


#################

################################################################################
@service.json
def export_excel():
    import os.path, openpyxl
    # get search parameters
    type = request.vars.type
    sometext = request.vars.sometext
    province_id = request.vars.province_id
    conditions = (db.stations.id > 0)
    # Neu chuoi tim kiem khac rong thi them dieu kien truy van voi chuoi tim kiem
    if sometext:
        conditions &= ((db.stations.station_code.contains(sometext)) |
                       (db.stations.station_name.contains(sometext)) |
                       (db.stations.description.contains(sometext)) |
                       (db.stations.contact_point.contains(sometext)) |
                       (db.stations.phone.contains(sometext)) |
                       (db.stations.email.contains(sometext)) |
                       (db.stations.address.contains(sometext)))
    if type:
        conditions &= (db.stations.station_type == type)
    if province_id:
        conditions &= (db.stations.province_id == province_id)

    aaData = []  # Du lieu json se tra ve
    list_data = None  # Du lieu truy van duoc
    iTotalRecords = 0  # Tong so ban ghi
    stations = db(conditions).select()
    provice_dict = common.get_province_dict()
    areas = common.get_area_by_station_dict()
    careers = common.get_career_by_station_dict()
    agents = common.get_agents_by_station_dict()
    status = dict()
    for key, item in const.STATION_STATUS.iteritems():
        status[str(item['value'])] = T(item['name'])
    list_station_type = dict()
    for item in common.get_station_types():
        list_station_type[str(item['value'])] = item['name']

    for c, station in enumerate(stations):
        if station.ftp_connection_status:
            text = 'Kết nối'
        else:
            text = 'Không kết nối'
        station_name = station.station_name
        station_status = station.status
        if station_status == 0:
            a = 'Hoạt động tốt'
        if station_status == 1:
            a = 'Xu hướng vượt'
        if station_status == 2:
            a = 'Chuẩn bị vượt'
        if station_status == 3:
            a = 'Vượt qui chuẩn'
        if station_status == 4:
            a = ' Mất kết nối'
        if station_status == 5:
            a = 'Hiệu chuẩn'
        if station_status == 6:
            a = 'Lỗi thiết bị'
        station_type = list_station_type[str(station.station_type)]
        station_province = provice_dict.get(station.province_id)
        station_areas_List = []
        if station.area_ids is not None:
            for item in station.area_ids:
                data =areas.get(item)
                if data is not None:
                  station_areas_List.append(data)
        station_areas = ", ".join(station_areas_List)
        career_name = careers.get(station.career)
        agent_name = agents.get(station.agents_id)
        address = station.address
        station_port = station.data_server_port
        station_description = station.description
        station_latitude = station.latitude
        station_longitude = station.longitude
        station_code = station.station_code
        contact_point = station.contact_point
        data_server = station.data_server
        data_folder = station.data_folder
        username = station.username
        list = [c + 1, station_code, station_name, station_longitude, station_latitude, a, text, station_type,
                station_province, address, station_areas, career_name, agent_name, station_description, contact_point, data_server,
                data_folder, station_port, username]
        aaData.append(list)

    wb2 = openpyxl.Workbook(write_only=True)
    ws2 = wb2.create_sheet()

    temp_headers = ['No', 'Mã trạm', 'Tên trạm', 'Kinh độ', 'Vĩ độ', 'Trạng thái', 'Trạng thái FTP',
                    'Thành phần môi trường', 'Tỉnh', 'Địa chỉ', 'Nhóm', 'Ngành nghề', 'Cơ quan quản lý', 'Mô tả',
                    'Đầu mối liên hệ', 'Đường dẫn máy chủ', 'Đường dẫn thư mục', 'Cổng', 'Tên người dùng']
    headers = []

    ws2.append(temp_headers)
    # Write data
    try:
        for row in aaData:
            ws2.append(row)

    except Exception as ex:
        return dict(success=False, message=str(ex))

    # Get station name

    file_name = request.now.strftime('Danh sách trạm_%Y%m%d_%H%M%S.xlsx')
    file_path = os.path.join(request.folder, 'static', 'export', file_name)
    # wb.save(file_path)
    wb2.save(file_path)

    data = open(file_path, "rb").read()
    os.unlink(file_path)
    response.headers['Content-Type'] = 'application/vnd.ms-excel'
    response.headers['Content-Disposition'] = 'attachment;filename=%s' % file_name

    return data


#########################
# def export_csv():
#     import os.path
#     # get search parameters
#     s_search = request.vars.sSearch
#     type = request.vars.type
#     sometext = request.vars.sometext
#     province_id = request.vars.province_id
#     conditions = (db.stations.id > 0)
#     # Neu chuoi tim kiem khac rong thi them dieu kien truy van voi chuoi tim kiem
#     if sometext:
#         conditions &= ((db.stations.station_code.contains(sometext)) |
#                        (db.stations.station_name.contains(sometext)) |
#                        (db.stations.description.contains(sometext)) |
#                        (db.stations.contact_point.contains(sometext)) |
#                        (db.stations.phone.contains(sometext)) |
#                        (db.stations.email.contains(sometext)) |
#                        (db.stations.address.contains(sometext)))
#     if type:
#         conditions &= (db.stations.station_type == type)
#     if province_id:
#         conditions &= (db.stations.province_id == province_id)
#
#     list_data = db(conditions).select()
#     import csv
#     station_name = T('Stations list')
#     file_name = request.now.strftime(station_name + '_%Y%m%d_%H%M%S.csv')
#     file_path = os.path.join(request.folder, 'static', 'export', file_name)
#
#     if list_data:
#         with open(file_path, mode='wb') as out_file:
#             out_file.write(u'\ufeff'.encode('utf8'))
#             writer = csv.writer(out_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
#
#             # Write header
#             row = [T('LBL_STT'), T('LBL_STATION_CODE'), T('LBL_STATION_NAME'), T('LBL_LONGITUDE'), T('LBL_LATITUDE'),
#                    T('Station type'), T('LBL_PROVINCE'), T('LBL_ADDRESS'), T('LBL_DESCRIPTION'),
#                    T('Area'), T('Email'), T('Phone'), T('Contact point'), T('LBL_STATUS'), T('Server link'), T('Port'),
#                    T('Folder link'), T('Username')]
#             writer.writerow(row)
#
#             provice_dict = common.get_province_dict()
#             ## Get station's area info
#             areas = common.get_area_by_station_dict()
#             station_type = dict()
#             # for key, item in const.STATION_TYPE.iteritems():
#             for item in common.get_station_types():
#                 station_type[str(item['value'])] = item['name']
#             status = dict(db.stations.status.requires.options())
#             # Write data
#             iRow = 1
#             for i, item in enumerate(list_data):
#                 writer.writerow([
#                     str(iRow),
#                     item.station_code,
#                     item.station_name,
#                     item.longitude,
#                     item.latitude,
#                     station_type[str(item.station_type)],
#                     provice_dict.get(item.province_id),
#                     item.address,
#                     item.description,
#                     areas.get(item.area_id),
#                     item.email,
#                     item.phone,
#                     item.contact_point,
#                     status[str(item.status)],
#                     item.data_server,
#                     item.data_server_port,
#                     item.data_folder,
#                     item.username,
#                 ])
#                 iRow += 1
#         data = open(file_path, "rb").read()
#         os.unlink(file_path)
#         response.headers['Content-Type'] = 'text/csv'
#         response.headers['Content-Disposition'] = 'attachment;filename=%s' % file_name
#
#         return data
#     else:
#         return T('export data empty')


###################################################################################
@service.json
@auth.requires(lambda: (auth.has_permission('create', 'datalogger') or auth.has_permission('edit', 'datalogger')))
def save_datalogger(*args, **kwargs):
    try:
        record = db.datalogger(request.args(0)) or None
        station_id = request.vars.station_id
        logger_id = request.vars.logger_id
        logger_name = request.vars.logger_name
        type_logger = request.vars.type_logger
        count = db(db.datalogger.station_id == station_id).count()
        station_name = request.vars.station_name
        if count:
            db(db.datalogger.station_id == station_id). \
                update(logger_id=logger_id, logger_name=logger_name, station_name=station_name, type_logger=type_logger)
        else:
            db.datalogger.insert(logger_id=logger_id, logger_name=logger_name,
                                 station_id=station_id, station_name=station_name, type_logger=type_logger)
        # update history
        db.manager_stations_history.insert(station_id=station_id,
                                           action='Update',
                                           username=current_user.fullname or None,
                                           description='Thay_doi_noi_dung_datalogger',
                                           update_time=datetime.now())
        ###
        return dict(success=True)
    except Exception as ex:
        return dict(success=False, message=str(ex))


###################################################################################

@service.json
@auth.requires(
    lambda: (auth.has_permission('create', 'stations_send_data') or auth.has_permission('edit', 'stations_send_data')))
def save_send_data(*args, **kwargs):
    from ftplib import FTP
    import ftplib
    ftp_path = request.vars.ftp_path
    ftp_ip = request.vars.ftp_ip
    ftp_port = request.vars.ftp_port
    ftp_user = request.vars.ftp_user
    ftp_password = request.vars.ftp_password
    res = True

    ftp = FTP()

    try:
        ftp.connect(ftp_ip, ftp_port)
        ftp.login(ftp_user, ftp_password)
    except ftplib.all_errors:
        res = False
    finally:
        try:
            ftp.quit()
        except Exception as ex:
            pass
    print res
    try:
        record = db.stations_send_data(request.args(0)) or None
        station_id = request.vars.station_id
        status = request.vars.status
        time_send_data = request.vars.time_send_data
        from_date = datetime.strptime(request.vars.from_date, "%Y-%m-%dT%H:%M:%S.%fZ")
        file_format = request.vars.file_format
        file_name = request.vars.file_name
        ftp_path = request.vars.ftp_path
        ftp_ip = request.vars.ftp_ip
        ftp_port = request.vars.ftp_port
        ftp_user = request.vars.ftp_user
        ftp_password = request.vars.ftp_password

        count = db(db.stations_send_data.station_id == station_id).count()
        if count:
            db(db.stations_send_data.station_id == station_id). \
                update(status=status, time_send_data=time_send_data, from_date=from_date, file_format=file_format,
                       file_name=file_name, ftp_path=ftp_path, ftp_ip=ftp_ip, ftp_port=ftp_port, ftp_user=ftp_user,
                       ftp_password=ftp_password)
            db(db.stations.id == station_id).update(ftp_connection_status=res)
        else:
            db.stations_send_data.insert(station_id=station_id, status=status, time_send_data=time_send_data,
                                         from_date=from_date, file_format=file_format, file_name=file_name,
                                         ftp_path=ftp_path, ftp_ip=ftp_ip, ftp_port=ftp_port, ftp_user=ftp_user,
                                         ftp_password=ftp_password)
            db(db.stations.id == station_id).update(ftp_connection_status=res)
        # update history
        db.manager_stations_history.insert(station_id=station_id,
                                           action='Update',
                                           username=current_user.fullname or None,
                                           description='Thay_doi_noi_dung_truyen_du_lieu',
                                           update_time=datetime.now())
        ###
        return dict(success=True, res=res)
    except Exception as ex:
        return dict(success=False, message=str(ex), res=res)


###################################################################################

@service.json
@auth.requires(
    lambda: (auth.has_permission('view', 'commands') or auth.has_permission('view', 'commands')))
def add_datalogger_command(*args, **kwargs):
    try:
        station_id = request.vars.station_id
        data = dict()
        for key in request.vars:
            f = key
            if key == 'r-ip':
                f = 'ip'
            elif key == 'r-usr':
                f = 'username'
            elif key == 'r-pwd':
                f = 'password'
            data[f] = request.vars[key]
        datalogger = db(db.datalogger.station_id == station_id).select().first()
        if datalogger:
            if data['type_logger'] != datalogger.type_logger or data['type_logger'] != datalogger.type_logger or data[
                'logger_name'] != datalogger.logger_name:
                datalogger.logger_id = data['logger_id']
                datalogger.type_logger = data['type_logger']
                datalogger.logger_name = data['logger_name']
                datalogger.update_record()
                try:
                    db.manager_stations_history.insert(station_id=station_id,
                                                       action='Update',
                                                       username=current_user.fullname or None,
                                                       description='Thay_doi_noi_dung_truyen_du_lieu',
                                                       update_time=datetime.now())
                except:
                    pass
        else:
            db.datalogger.insert(**data)
            try:
                db.manager_stations_history.insert(station_id=station_id,
                                                   action='Add',
                                                   username=current_user.fullname or None,
                                                   description='Thay_doi_noi_dung_truyen_du_lieu',
                                                   update_time=datetime.now())
            except:
                pass
        if not data.has_key('command_id'):
            data['command_id'] = data['command_name']
        conditions = (db.datalogger_command.station_id == station_id)
        conditions &= (db.datalogger_command.command_name == data['command_name'])
        c = db(conditions).count()
        if c > 0:
            db(conditions).update(**data)
        else:
            db.datalogger_command.insert(**data)

        return dict(success=True)
    except Exception as ex:
        return dict(success=False, message=str(ex))


################################################################################
@service.json
def get_datalogger_command_by_station(*args, **kwargs):
    try:
        iDisplayStart = int(request.vars.iDisplayStart)  # Vi tri bat dau lay du lieu
        iDisplayLength = int(request.vars.iDisplayLength)  # So luong ban ghi se lay toi da
        station_id = request.vars.station_id  # Chuoi tim kiem nhap tu form
        logger_type = request.vars.type
        aaData = []  # Du lieu json se tra ve
        limitby = (iDisplayStart, iDisplayLength + 1)  # Tuple dung de phan trang (vtri bat dau - chieu dai)
        conditions = (db.datalogger_command.id > 0)
        if station_id:
            conditions &= (db.datalogger_command.station_id == station_id)
        if logger_type:
            conditions &= (db.datalogger_command.type_logger == logger_type)

        list_data = db(conditions).select(db.datalogger_command.ALL,
                                          limitby=limitby,
                                          orderby=~db.datalogger_command.id)
        # Tong so ban ghi khong thuc hien phan trang
        iTotalRecords = db(conditions).count()
        # List kind
        rowsKind = db(db.datalogger_command.id > 0).select()
        resKind = {}
        for item in rowsKind:
            resKind[str(item.id)] = item.id
        # Thu tu ban ghi
        iRow = iDisplayStart + 1
        # Duyet tung phan tu trong mang du lieu vua truy van duoc

        for item in list_data:
            if logger_type is not None:
                if logger_type == 'D_LOGGER':
                    r_item = [str(iRow),
                              item.command_id,
                              item.command_name,
                              item.command_content,
                              INPUT(_group='1', _class='select_item', _type='checkbox', _value=item.id),
                              item.id]
                elif logger_type in ['ADAM', 'BL']:
                    r_item = [str(iRow),
                              item.command_name,
                              item.ip,
                              item.username,
                              item.ch,
                              item.slot,
                              INPUT(_group='1', _class='select_item', _type='checkbox', _value=item.id),
                              item.id]
                else:
                    r_item = [str(iRow),
                              item.command_name,
                              item.ip,
                              item.username,
                              item.command_content,
                              INPUT(_group='1', _class='select_item', _type='checkbox', _value=item.id),
                              item.id]
            else:
                r_item = [str(iRow),
                          item.command_name,
                          item.ip,
                          item.username,
                          item.ch,
                          item.slot,
                          INPUT(_group='1', _class='select_item', _type='checkbox', _value=item.id),
                          item.id]
            aaData.append(r_item)
            iRow += 1
        return dict(iTotalRecords=iTotalRecords, iTotalDisplayRecords=iTotalRecords, aaData=aaData, success=True)
    except Exception as ex:
        return dict(iTotalRecords=0, iTotalDisplayRecords=0, aaData=[], message=str(ex), success=False)


################################################################################
@service.json
def check_connection_ftp(*args, **kwargs):
    from ftplib import FTP
    import ftplib
    res = True
    ftp_ip = request.vars.ftp_ip
    ftp_path = request.vars.ftp_path
    user = request.vars.user
    password = request.vars.password
    ftp_port = request.vars.ftp_port
    ftp = FTP()
    # ftp.connect(ftp_ip, ftp_port)
    # ftp.login(user, password)
    try:
        ftp.connect(ftp_ip, ftp_port)
        ftp.login(user, password)
        # ftp.cwd(ftp_path)
    # except ftp.error_perm:
    except ftplib.all_errors:
        res = False
    finally:
        # ftp.quit()
        try:
            ftp.quit()
        except Exception as ex:
            pass
    # return dict(success=res)
    return res


################################################################################
@service.json
def check_connection_ftp2(*args, **kwargs):
    ftp_id = request.vars.ftp_id
    is_connect_success = check_ftp_connection_by_id(db, ftp_id)
    station_id = request.vars.station_id
    if station_id != '':
        db(db.stations.id == station_id).update(ftp_connection_status=is_connect_success)
    return is_connect_success


################################################################################
# hungdx issue 44 -fix add (co the ap dung cho cac chon tinh, vung ... fix sau
@service.json
def dropdown_content(table, filter_field, get_value_field, get_dsp_field, *args, **kwargs):
    try:
        filter_value = request.vars.filter_value
        filter_value = filter_value.split(';')
        filter_field = filter_field.split('-')
        conditions = (db[table]['id'] > 0)
        t1 = len(filter_field)
        t2 = len(filter_value)
        if t1 == t2:
            for i in range(0, t1):
                if filter_field[i] and filter_value[i] != '':
                    if filter_field[i] == 'area_ids' or filter_field[i] == 'careers':
                        conditions &= (db[table][filter_field[i]].belongs([filter_value[i]]))
                    else:
                        conditions &= (db[table][filter_field[i]] == filter_value[i])
        if current_user:
            if not (auth.has_membership('admin') or auth.has_membership(const.GROUP_MANAGER)):
                list_station_manager = db(db.manager_stations.user_id == current_user.id).select(
                    db.manager_stations.station_id)
                station_ids = [str(item.station_id) for item in list_station_manager]
                conditions &= (db[table]['id'].belongs(station_ids))
        records = db(conditions).select(db[table][get_value_field], db[table][get_dsp_field])

        if records:
            html1 = "<option value=''>%s</option>" % (T('-- Select an option --'))
            html = ["<option value='%s'>%s</option>" % (item[get_value_field], item[get_dsp_field]) for item in records]
            html = html1 + ''.join(html)
        else:
            html = "<option value=''>%s</option>" % (T('-- No data --'))

        return dict(success=True, html=html)
    except Exception as ex:
        return dict(success=False, message=str(ex))


def setting_qi():
    # Select all AQI stations
    conditions = (db.stations.is_qi == True)
    conditions &= (db.stations.station_type == const.STATION_TYPE['AMBIENT_AIR']['value'])

    if current_user:
        if not (auth.has_membership('admin') or auth.has_membership(const.GROUP_MANAGER)):
            list_station_manager = db(db.manager_stations.user_id == current_user.id).select(
                db.manager_stations.station_id)
            station_ids = [str(item.station_id) for item in list_station_manager]
            conditions &= (db.stations.id.belongs(station_ids))
    stations = db(conditions).select(db.stations.id, db.stations.station_name)

    return dict(stations=stations)


################################################################################

def setting_wqi():
    # Select all AQI stations
    # conditions = (db.stations.is_qi == True)
    conditions = (db.stations.station_type == const.STATION_TYPE['SURFACE_WATER']['value'])
    conditions &= (db.stations.is_qi == True)
    # Get all station_ids which belonged to current login user (group)
    # if not 'admin' in current_user.roles:
    #    station_ids = common.get_stations_belong_current_user()
    #    conditions &= (db.stations.id.belongs(station_ids))
    if current_user:
        if not (auth.has_membership('admin') or auth.has_membership(const.GROUP_MANAGER)):
            list_station_manager = db(db.manager_stations.user_id == current_user.id).select(
                db.manager_stations.station_id)
            station_ids = [str(item.station_id) for item in list_station_manager]
            conditions &= (db.stations.id.belongs(station_ids))
    stations = db(conditions).select(db.stations.id, db.stations.station_name)

    return dict(stations=stations)


################################################################################

@service.json
def get_list_stations_calc_qi(*args, **kwargs):
    try:
        sometext = request.vars.sometext
        station_id = request.vars.station_id
        station_type = const.STATION_TYPE['AMBIENT_AIR']['value']
        iDisplayStart = int(request.vars.iDisplayStart)
        iDisplayLength = int(request.vars.iDisplayLength)
        limitby = (iDisplayStart, iDisplayLength + 1)  # Tuple dung de phan trang (vtri bat dau - chieu dai)
        aaData = []

        conditions = (db.stations.is_qi == True)
        if station_type:
            conditions &= (db.stations.station_type == station_type)
        if station_id:
            conditions &= (db.stations.id == station_id)
        # Get all station_ids which belonged to current login user (group)
        # if not 'admin' in current_user.roles:
        #    station_ids = common.get_stations_belong_current_user()
        #    conditions &= (db.stations.id.belongs(station_ids))
        if current_user:
            if not (auth.has_membership('admin') or auth.has_membership(const.GROUP_MANAGER)):
                list_station_manager = db(db.manager_stations.user_id == current_user.id).select(
                    db.manager_stations.station_id)
                station_ids = [str(item.station_id) for item in list_station_manager]
                conditions &= (db.stations.id.belongs(station_ids))
        stations = db(conditions).select(db.stations.id, db.stations.station_name)
        ids = [str(item.id) for item in stations]

        # Get dict(indicator_id : indicator_name)
        indicators_dict = common.get_indicator_dict()

        # Get all indicators of AQI stations
        station_indicators = db(db.station_indicator.station_id.belongs(ids)).select(
            db.station_indicator.id,
            db.station_indicator.station_id,
            db.station_indicator.station_name,
            db.station_indicator.station_type,
            db.station_indicator.indicator_id,
            db.station_indicator.is_public,
            db.station_indicator.is_calc_qi,
        )

        # build dict(station_id : {indicator_id: indicator_name,...})
        res = {}
        for item in station_indicators:
            if (indicators_dict.get(item.indicator_id) in const.AQI_INDICATOR_SETTING):
                if (not res.has_key(item.station_id)):
                    res[item.station_id] = {}
                    res[item.station_id]['indicator'] = []
                indicator = item.as_dict()
                indicator['indicator_code'] = indicators_dict.get(item.indicator_id)
                res[item.station_id]['indicator'].append(indicator)
                # res[item.station_id]['station_name'] = item.station_name
                for item2 in stations:
                    if str(item2.id) == str(item.station_id):
                        res[item.station_id]['station_name'] = item2.station_name

        # Tong so ban ghi khong thuc hien phan trang
        iTotalRecords = len(res.keys())
        i = 0
        for station_id in sorted(res)[iDisplayStart: iDisplayStart + iDisplayLength + 1]:  # Thuc hien paging
            i += 1
            indicator_str = ''
            for indicator in res[station_id]['indicator']:
                if indicator['is_calc_qi']:
                    indicator_str += '<label data-station="%s" class=\'check_public\'>%s&nbsp;%s</label>' % (
                        indicator['station_id'], INPUT(_type="checkbox", _id="%s" % indicator['id'],
                                                       _data_indicator="%s" % indicator['indicator_code'],
                                                       _checked=True),
                        indicator['indicator_code'])
                else:
                    indicator_str += '<label data-station="%s" class=\'check_public\'>%s&nbsp;%s</label>' % (
                        indicator['station_id'], INPUT(_type="checkbox", _id="%s" % indicator['id'],
                                                       _data_indicator="%s" % indicator['indicator_code']),
                        indicator['indicator_code'])

            aaData.append([
                str(iDisplayStart + i),
                res[station_id]['station_name'],
                indicator_str,
                station_id
            ])

        return dict(iTotalRecords=iTotalRecords, iTotalDisplayRecords=iTotalRecords, aaData=aaData, success=True)
    except Exception, ex:
        return dict(iTotalRecords=0, iTotalDisplayRecords=0, aaData=[], message=str(ex), success=False)


@service.json
def get_list_stations_calc_wqi(*args, **kwargs):
    try:
        sometext = request.vars.sometext
        station_id = request.vars.station_id
        station_type = const.STATION_TYPE['SURFACE_WATER']['value']
        iDisplayStart = int(request.vars.iDisplayStart)
        iDisplayLength = int(request.vars.iDisplayLength)
        limitby = (iDisplayStart, iDisplayLength + 1)  # Tuple dung de phan trang (vtri bat dau - chieu dai)
        aaData = []

        conditions = (db.stations.is_qi == True)
        if station_type:
            conditions &= (db.stations.station_type == station_type)
        if station_id:
            conditions &= (db.stations.id == station_id)
        # Get all station_ids which belonged to current login user (group)
        # if not 'admin' in current_user.roles:
        #    station_ids = common.get_stations_belong_current_user()
        #    conditions &= (db.stations.id.belongs(station_ids))
        if current_user:
            if not (auth.has_membership('admin') or auth.has_membership(const.GROUP_MANAGER)):
                list_station_manager = db(db.manager_stations.user_id == current_user.id).select(
                    db.manager_stations.station_id)
                station_ids = [str(item.station_id) for item in list_station_manager]
                conditions &= (db.stations.id.belongs(station_ids))
        stations = db(conditions).select(db.stations.id, db.stations.station_name)
        ids = [item.id for item in stations]

        # Get dict(indicator_id : indicator_name)
        indicators_dict = common.get_indicator_dict()

        # Get all indicators of AQI stations
        # condition_indicator =
        station_indicators = db((db.station_indicator.station_id.belongs(ids,null=True)) & (
                db.station_indicator.status == const.SI_STATUS['IN_USE']['value'])).select(
            db.station_indicator.id,
            db.station_indicator.station_id,
            db.station_indicator.station_name,
            db.station_indicator.station_type,
            db.station_indicator.indicator_id,
            db.station_indicator.is_public,
            db.station_indicator.is_calc_qi,
        )

        # build dict(station_id : {indicator_id: indicator_name,...})
        res, res_1, res_2, res_3, res_4 = {}, {}, {}, {}, {}
        for item in station_indicators:
            if (indicators_dict.get(item.indicator_id) in const.WQI_INDICATOR_I):
                if (not res.has_key(item.station_id)):
                    res[item.station_id] = {}
                    res[item.station_id]['indicator'] = []
                indicator = item.as_dict()
                indicator['indicator_code'] = indicators_dict.get(item.indicator_id)
                res[item.station_id]['indicator'].append(indicator)
                # res[item.station_id]['station_name'] = item.station_name
                for item2 in stations:
                    if str(item2.id) == str(item.station_id):
                        res[item.station_id]['station_name'] = item2.station_name

                if (not res_1.has_key(item.station_id)):
                    res_1[item.station_id] = {}
                    res_1[item.station_id]['indicator'] = []
                indicator = item.as_dict()
                indicator['indicator_code'] = indicators_dict.get(item.indicator_id)
                res_1[item.station_id]['indicator'].append(indicator)
                # res_1[item.station_id]['station_name'] = item.station_name
                for item2 in stations:
                    if str(item2.id) == str(item.station_id):
                        res_1[item.station_id]['station_name'] = item2.station_name

            if (indicators_dict.get(item.indicator_id) in const.WQI_INDICATOR_II):
                if (not res.has_key(item.station_id)):
                    res[item.station_id] = {}
                    res[item.station_id]['indicator'] = []
                indicator = item.as_dict()
                indicator['indicator_code'] = indicators_dict.get(item.indicator_id)
                res[item.station_id]['indicator'].append(indicator)
                # res[item.station_id]['station_name'] = item.station_name
                for item2 in stations:
                    if str(item2.id) == str(item.station_id):
                        res[item.station_id]['station_name'] = item2.station_name

                if (not res_2.has_key(item.station_id)):
                    res_2[item.station_id] = {}
                    res_2[item.station_id]['indicator'] = []
                indicator = item.as_dict()
                indicator['indicator_code'] = indicators_dict.get(item.indicator_id)
                res_2[item.station_id]['indicator'].append(indicator)
                # res_2[item.station_id]['station_name'] = item.station_name
                for item2 in stations:
                    if str(item2.id) == str(item.station_id):
                        res_2[item.station_id]['station_name'] = item2.station_name

            if (indicators_dict.get(item.indicator_id) in const.WQI_INDICATOR_III):
                if (not res.has_key(item.station_id)):
                    res[item.station_id] = {}
                    res[item.station_id]['indicator'] = []
                indicator = item.as_dict()
                indicator['indicator_code'] = indicators_dict.get(item.indicator_id)
                res[item.station_id]['indicator'].append(indicator)
                # res[item.station_id]['station_name'] = item.station_name
                for item2 in stations:
                    if str(item2.id) == str(item.station_id):
                        res[item.station_id]['station_name'] = item2.station_name

                if (not res_3.has_key(item.station_id)):
                    res_3[item.station_id] = {}
                    res_3[item.station_id]['indicator'] = []
                indicator = item.as_dict()
                indicator['indicator_code'] = indicators_dict.get(item.indicator_id)
                res_3[item.station_id]['indicator'].append(indicator)
                # res_3[item.station_id]['station_name'] = item.station_name
                for item2 in stations:
                    if str(item2.id) == str(item.station_id):
                        res_3[item.station_id]['station_name'] = item2.station_name

            if (indicators_dict.get(item.indicator_id) in const.WQI_INDICATOR_IV):
                if (not res.has_key(item.station_id)):
                    res[item.station_id] = {}
                    res[item.station_id]['indicator'] = []
                indicator = item.as_dict()
                indicator['indicator_code'] = indicators_dict.get(item.indicator_id)
                res[item.station_id]['indicator'].append(indicator)
                # res[item.station_id]['station_name'] = item.station_name
                for item2 in stations:
                    if str(item2.id) == str(item.station_id):
                        res[item.station_id]['station_name'] = item2.station_name

                if (not res_4.has_key(item.station_id)):
                    res_4[item.station_id] = {}
                    res_4[item.station_id]['indicator'] = []
                indicator = item.as_dict()
                indicator['indicator_code'] = indicators_dict.get(item.indicator_id)
                res_4[item.station_id]['indicator'].append(indicator)
                # res_4[item.station_id]['station_name'] = item.station_name
                for item2 in stations:
                    if str(item2.id) == str(item.station_id):
                        res_4[item.station_id]['station_name'] = item2.station_name

        # Tong so ban ghi khong thuc hien phan trang
        iTotalRecords = len(res.keys())
        i = 0
        for station_id in sorted(res)[iDisplayStart: iDisplayStart + iDisplayLength + 1]:  # Thuc hien paging
            i += 1
            indicator_str = ''
            if res_1.has_key(station_id):
                indicator_str += '<b>Nhóm 1: </b>'
                for indicator in res_1[station_id]['indicator']:
                    if indicator['is_calc_qi']:
                        indicator_str += '<label data-station="%s" class=\'check_public\'>%s&nbsp;%s</label>' % (
                            indicator['station_id'], INPUT(_type="checkbox", _id="%s" % indicator['id'],
                                                           _data_indicator="%s" % indicator['indicator_code'],
                                                           _checked=True), indicator['indicator_code'])
                    else:
                        indicator_str += '<label data-station="%s" class=\'check_public\'>%s&nbsp;%s</label>' % (
                            indicator['station_id'], INPUT(_type="checkbox", _id="%s" % indicator['id'],
                                                           _data_indicator="%s" % indicator['indicator_code']),
                            indicator['indicator_code'])

            if res_2.has_key(station_id):
                indicator_str += '<br/> <b>Nhóm 2: </b>'
                for indicator in res_2[station_id]['indicator']:
                    if indicator['is_calc_qi']:
                        indicator_str += '<label data-station="%s" class=\'check_public\'>%s&nbsp;%s</label>' % (
                            indicator['station_id'], INPUT(_type="checkbox", _id="%s" % indicator['id'],
                                                           _data_indicator="%s" % indicator['indicator_code'],
                                                           _checked=True), indicator['indicator_code'])
                    else:
                        indicator_str += '<label data-station="%s" class=\'check_public\'>%s&nbsp;%s</label>' % (
                            indicator['station_id'], INPUT(_type="checkbox", _id="%s" % indicator['id'],
                                                           _data_indicator="%s" % indicator['indicator_code']),
                            indicator['indicator_code'])

            if res_3.has_key(station_id):
                indicator_str += '<br/> <b>Nhóm 3: </b>'
                for indicator in res_3[station_id]['indicator']:
                    if indicator['is_calc_qi']:
                        indicator_str += '<label data-station="%s" class=\'check_public\'>%s&nbsp;%s</label>' % (
                            indicator['station_id'], INPUT(_type="checkbox", _id="%s" % indicator['id'],
                                                           _data_indicator="%s" % indicator['indicator_code'],
                                                           _checked=True), indicator['indicator_code'])
                    else:
                        indicator_str += '<label data-station="%s" class=\'check_public\'>%s&nbsp;%s</label>' % (
                            indicator['station_id'], INPUT(_type="checkbox", _id="%s" % indicator['id'],
                                                           _data_indicator="%s" % indicator['indicator_code']),
                            indicator['indicator_code'])

            if res_4.has_key(station_id):
                indicator_str += '<br/> <b>Nhóm 4: </b>'
                for indicator in res_4[station_id]['indicator']:
                    if indicator['is_calc_qi']:
                        indicator_str += '<label data-station="%s" class=\'check_public\'>%s&nbsp;%s</label>' % (
                            indicator['station_id'], INPUT(_type="checkbox", _id="%s" % indicator['id'],
                                                           _data_indicator="%s" % indicator['indicator_code'],
                                                           _checked=True), indicator['indicator_code'])
                    else:
                        indicator_str += '<label data-station="%s" class=\'check_public\'>%s&nbsp;%s</label>' % (
                            indicator['station_id'], INPUT(_type="checkbox", _id="%s" % indicator['id'],
                                                           _data_indicator="%s" % indicator['indicator_code']),
                            indicator['indicator_code'])

            aaData.append([
                str(iDisplayStart + i),
                res[station_id]['station_name'],
                indicator_str,
                station_id
            ])

        return dict(iTotalRecords=iTotalRecords, iTotalDisplayRecords=iTotalRecords, aaData=aaData, success=True)
    except Exception, ex:
        return dict(iTotalRecords=0, iTotalDisplayRecords=0, aaData=[], message=str(ex), success=False)


@service.json
def ajax_save(*args, **kwargs):
    try:
        checked = request.vars.checked.split(',')
        unchecked = request.vars.unchecked.split(',')
        station_public = request.vars.station_public.split(',')
        station_unpublic = request.vars.station_unpublic.split(',')
        db(db.station_indicator.id.belongs(checked)).update(is_calc_qi=True)
        db(db.station_indicator.id.belongs(unchecked)).update(is_calc_qi=False)
        return dict(success=True)
    except Exception as ex:
        logger.error(str(ex))
        return dict(success=False, message=str(ex))


################################################################################
@service.json
def check_mapping_name_indicator(*args, **kwargs):
    from ftplib import FTP
    from StringIO import StringIO
    import ftplib
    res = False
    ftp_ip = request.vars.data_server
    data_folder = request.vars.data_folder
    username = request.vars.username
    password = request.vars.pwd
    ftp_port = request.vars.data_server_port
    station_id = request.vars.station_id
    station_code = request.vars.station_code
    file_mapping = ''

    try:
        station = db(db.stations.id == station_id).select(db.stations.ALL)
        if station:
            file_mapping = station[0].file_mapping

        ftp = FTP()
        ftp.connect(ftp_ip, ftp_port)
        ftp.login(username, password)
        ftp.cwd(data_folder)
        ftp.encoding = 'utf-8'
        ftp.sendcmd('OPTS UTF8 ON')
        count = 0
        content_file = None

        files_c1 = ftp.nlst()
        files_c1 = [str(fi) for fi in files_c1]
        files_c1.sort(reverse=True)
        for file_c1 in files_c1:
            fildir = file_c1.split('.')
            filsize = len(fildir)
            if filsize > 1:
                idx = -1
                try:
                    idx = file_c1.index(station_code)
                except:
                    pass
                if idx == -1:
                    try:
                        idx = file_c1.index(file_mapping)
                    except:
                        pass
                if idx > -1:
                    read_data_in_file = StringIO()
                    ftp.retrbinary('RETR ' + file_c1, read_data_in_file.write)
                    if read_data_in_file:
                        content_file = read_data_in_file.getvalue()
                    read_data_in_file.close()
                    return
            else:
                ftp.cwd(file_c1)
                count += 1
                try:
                    files_c2 = ftp.nlst()
                    files_c2 = [str(fi) for fi in files_c2]
                    files_c2.sort(reverse=True)
                    for file_c2 in files_c2:
                        fildir = file_c2.split('.')
                        filsize = len(fildir)
                        if filsize > 1:
                            idx = -1
                            try:
                                idx = file_c2.index(station_code)
                            except:
                                pass
                            if idx == -1:
                                try:
                                    idx = file_c2.index(file_mapping)
                                except:
                                    pass
                            if idx > -1:
                                read_data_in_file = StringIO()
                                ftp.retrbinary('RETR ' + file_c2, read_data_in_file.write)
                                if read_data_in_file:
                                    content_file = read_data_in_file.getvalue()
                                read_data_in_file.close()
                                return
                        else:
                            ftp.cwd(file_c2)
                            count += 1
                            try:
                                files_c3 = ftp.nlst()
                                files_c3 = [str(fi) for fi in files_c3]
                                files_c3.sort(reverse=True)
                                for file_c3 in files_c3:
                                    fildir = file_c3.split('.')
                                    filsize = len(fildir)
                                    if filsize > 1:
                                        idx = -1
                                        try:
                                            idx = file_c3.index(station_code)
                                        except:
                                            pass
                                        if idx == -1:
                                            try:
                                                idx = file_c3.index(file_mapping)
                                            except:
                                                pass
                                        if idx > -1:
                                            read_data_in_file = StringIO()
                                            ftp.retrbinary('RETR ' + file_c3, read_data_in_file.write)
                                            if read_data_in_file:
                                                content_file = read_data_in_file.getvalue()
                                            read_data_in_file.close()
                                            return
                                    else:
                                        ftp.cwd(file_c3)
                                        count += 1
                                        try:
                                            files_c4 = ftp.nlst()
                                            files_c4 = [str(fi) for fi in files_c4]
                                            files_c4.sort(reverse=True)
                                            for file_c4 in files_c4:
                                                fildir = file_c4.split('.')
                                                filsize = len(fildir)
                                                if filsize > 1:
                                                    idx = -1
                                                    try:
                                                        idx = file_c4.index(station_code)
                                                    except:
                                                        pass
                                                    if idx == -1:
                                                        try:
                                                            idx = file_c4.index(file_mapping)
                                                        except:
                                                            pass
                                                    if idx > -1:
                                                        read_data_in_file = StringIO()
                                                        ftp.retrbinary('RETR ' + file_c4, read_data_in_file.write)
                                                        if read_data_in_file:
                                                            content_file = read_data_in_file.getvalue()
                                                        read_data_in_file.close()
                                                        return
                                                else:
                                                    ftp.cwd(file_c4)
                                                    count += 1
                                                while count > 1:
                                                    ftp.cwd("../")
                                                    count -= 1
                                        except:
                                            pass
                                    while count > 1:
                                        ftp.cwd("../")
                                        count -= 1
                            except:
                                pass

                        while count > 1:
                            ftp.cwd("../")
                            count -= 1
                except:
                    pass
            while count > 0:
                ftp.cwd("../")
                count -= 1
    except:
        pass
    finally:
        try:
            if content_file:
                try:
                    conditions = (db.mapping_name_indicator_stations.station_id == station_id)
                    db(conditions).delete()
                    db.commit()
                except:
                    pass

                for line in content_file.splitlines():
                    if line:
                        line = line.strip()
                        items_temp = line.split()

                    items = []
                    try:
                        if len(items_temp) == 5:  # Theo thông tư 24
                            try:
                                # Case 5.1: Indicator  Value  Unit Date_time Status
                                # Case 5.2: Date_time Indicator  Value  Unit  Status
                                check_time = datetime.strptime(items_temp[3], '%Y%m%d%H%M%S')
                                items = [items_temp[0], items_temp[1], items_temp[2], items_temp[3], items_temp[4]]
                            except:
                                try:
                                    # Case 5.2: Date_time Indicator  Value  Unit  Status
                                    check_time = datetime.strptime(items_temp[0], '%Y%m%d%H%M%S')
                                    items = [items_temp[1], items_temp[2], items_temp[3], items_temp[0], items_temp[4]]
                                except:
                                    items = None
                                    pass
                        elif len(items_temp) == 4:
                            try:
                                # Case 4.1: Indicator  Value  Unit Date_time
                                # Case 4.2: Indicator  Value       Date_time Status
                                # Case 4.3: Date_time  Indicator  Value  Unit
                                check_time = datetime.strptime(items_temp[3], '%Y%m%d%H%M%S')
                                try:
                                    tmp_value = float(items_temp[1])
                                    items = [items_temp[0], items_temp[1], items_temp[2], items_temp[3], 0]
                                except:
                                    items = [items_temp[0], items_temp[1], items_temp[2], items_temp[3], 2]
                            except:
                                try:
                                    # Case 4.2: Date_time Indicator  Value  Unit
                                    check_time = datetime.strptime(items_temp[0], '%Y%m%d%H%M%S')
                                    try:
                                        tmp_value = float(items_temp[2])
                                        items = [items_temp[1], items_temp[2], items_temp[3], items_temp[0], 0]
                                    except:
                                        items = [items_temp[1], items_temp[2], items_temp[3], items_temp[0], 2]
                                except:
                                    try:
                                        # Case 4.3: Indicator  Value  Date_time Status
                                        check_time = datetime.strptime(items_temp[2], '%Y%m%d%H%M%S')
                                        try:
                                            tmp_value = float(items_temp[1])
                                            items = [items_temp[0], items_temp[1], '---', items_temp[2], items_temp[3]]
                                        except:
                                            items = [items_temp[0], items_temp[1], '---', items_temp[2], 2]
                                    except:
                                        items = None
                                        pass
                        elif len(items_temp) == 3:
                            try:
                                # Case 3.1: Indicator  Value  Date_time
                                # Case 3.2: datetime indicator  value
                                check_time = datetime.strptime(items_temp[2], '%Y%m%d%H%M%S')
                                try:
                                    tmp_value = float(items_temp[1])
                                    items = [items_temp[0], items_temp[1], '---', items_temp[2], 0]
                                except:
                                    items = [items_temp[0], items_temp[1], '---', items_temp[2], 2]
                            except:
                                try:
                                    # Case 3.2: datetime indicator  value"
                                    check_time = datetime.strptime(items_temp[0], '%Y%m%d%H%M%S')
                                    try:
                                        tmp_value = float(items_temp[2])
                                        items = [items_temp[1], items_temp[2], '---', items_temp[0], 0]
                                    except:
                                        items = [items_temp[1], items_temp[2], '---', items_temp[0], 2]
                                except:
                                    items = None
                                    pass
                    except:
                        pass

                    if not items:
                        res = False
                        return res

                    try:
                        db.mapping_name_indicator_stations.insert(station_id=station_id,
                                                                  mapping_name_indicator=items[0])
                        db.commit()
                    except:
                        pass
                    res = True
                return res
        except:
            return res
        finally:
            return res


################################################################################
@service.json
def check_ftp(*args, **kwargs):
    station_code = request.vars.station_code
    row = db(db.stations.station_code == station_code).select(db.stations.username,
                                                              db.stations.pwd,
                                                              db.stations.data_folder,
                                                              db.stations.data_server_port,
                                                              db.stations.data_server)
    return dict(aaData=row[0])


@service.json
def check_connect_mqtt(*args, **kwargs):
    try:
        url = 'api/v4/clients/' + kwargs['client_id']
        data = get_mqtt_api(url)
        if data.has_key('data') and len(data['data']) > 0:
            return dict(success=data['data'][0]['connected'])
        return dict(success=False)
    except Exception as e:
        return dict(success=False)


def get_mqtt_api(path):
    try:
        url = '%s/%s' % (myconf.get('mqtt.url', ''), path)
        res = requests.get(url, headers={'Authorization': myconf.get('mqtt.auth_token', '')}, timeout=3)

        rs = dict(success=False)
        if res.status_code == 200:
            rs['success'] = True
            try:
                data = res.json()
                rs['data'] = data['data']
            except:
                pass
        return rs

    except Exception as e:
        return dict(success=False, message=e.message)


def post_mqtt_api(path, params):
    try:
        url = '%s/%s' % (myconf.get('mqtt.url', ''), path)
        res = requests.post(url, json=params, headers={'Authorization': myconf.get('mqtt.auth_token', '')}, timeout=3)
        rs = dict(success=False)
        if res.status_code == 200:
            rs['success'] = True
            try:
                data = res.json()
                rs['data'] = data['data']
            except:
                pass
        return rs
    except Exception as e:
        return dict(success=False, message=e.message)


def ftp_viewer():
    station_id = request.args(0)
    item = db.stations(station_id) or None
    station_name = ''
    data_folder = ''
    if item:
        station_name = item.station_name
        data_folder = item.data_folder
    return dict(station_id=station_id, station_name=station_name, data_folder=data_folder)


def download():
    try:
        import ftplib
        from datetime import datetime
        from cStringIO import StringIO

        TIME_OUT = 15
        vars = request.vars
        station_id = vars.get('station_id')
        folder = vars.get('folder', '')
        station = db.stations(station_id)
        filename = vars['filename']
        ftp_ip = station.data_server
        ftp_port = station.data_server_port
        usr = station.username
        pwd = station.pwd
        ftp = ftplib.FTP(ftp_ip)
        ftp.connect(ftp_ip, ftp_port, TIME_OUT)
        ftp.login(usr, pwd)
        ftp.encoding = 'utf-8'
        ftp.sendcmd('OPTS UTF8 ON')
        ftp.cwd(folder)

        # file_stream = open(filename, "wb")  # read file to send to byte
        # ftp.retrbinary('RETR {}'.format(filename), file_stream.write)
        # file_stream.close()
        # data = open(filename, "rb").read()
        # response.headers['Content-Type'] = 'text/plain'
        # response.headers['Content-Disposition'] = 'attachment;filename=%s' % filename
        # return data

        stringIO = StringIO()

        # gFile = open(filename, "wb")
        ftp.retrbinary('RETR %s' % filename, stringIO.write)
        # gFile.close()
        val = stringIO.getvalue()
        # val = val[1:][:-1]
        stringIO.close()
        ftp.quit()

        # Print the readme file contents
        # gFile = open(filename, "r")
        # buff = gFile.read()
        # gFile.close()
        response.headers['Content-Type'] = 'text/plain'
        response.headers['Content-Disposition'] = 'attachment;filename=%s' % filename
        return val
    except Exception as ex:
        return dict(success=False, message=ex.message)


def popup_ftp_view():
    ftp_id = request.vars.ftp_id
    view_type = request.vars.view_type
    return dict(ftp_id=ftp_id, view_type=view_type)

def popup_edit_thong_so():
    station_id = request.vars.station_id
    qcvn_id = request.vars.qcvn_id
    qcvn_kind_id = request.vars.qcvn_kind_id
    default_qcvn_kind_id = ""
    station_indicator_id=request.vars.station_indicator_id
    record = db.stations(station_id) or None
    indicators, qcvns, equipments, alarm, qcvn_station_kind, qcvn_station_kind_list_by_qcvn, \
        qcvn_const_value_by_qcvn, datalogger, datalogger_command_list, data_send = [], [], [], [], [], [], [], [], [], []
    list_status_data_send =[]
    if station_id:
        # Get all indicators to fill in dropdown
        # indicators = db((db.indicators.id > 0) & (db.indicators.indicator_type == type)).select()
        # Get all QCVN to fill in dropdown
        qcvns = db((db.qcvn.id > 0)).select(db.qcvn.id, db.qcvn.qcvn_code,
                                                                                         db.qcvn.qcvn_const_value)
        province = db.provinces(db.provinces.id == record.province_id)
        agent = db.agents(db.agents.id == record.agents_id)
        data_send_list = db((db.stations_send_data.id > 0) & (db.stations_send_data.station_id == station_id)).select()
        send_file_name = get_send_file_name(record, province, agent, data_send_list)

        if data_send_list:
            data_send = data_send_list[0]
            current_send_status = data_send.status
            if current_send_status == 0:
                curent_send_name = 'In-active'
                list_status_data_send.append({'value': current_send_status, 'name': 'In-active'})
                list_status_data_send.append({'value': 1, 'name': 'Active'})
            elif current_send_status == 1:
                curent_send_name = 'Active'
                list_status_data_send.append({'value': current_send_status, 'name': 'Active'})
                list_status_data_send.append({'value': 0, 'name': 'In-active'})
        else:
            list_status_data_send.append({'value': 0, 'name': 'In-active'})
            list_status_data_send.append({'value': 1, 'name': 'Active'})
        datalogger = None
        datalogger_list = db((db.datalogger.id > 0) & (db.datalogger.station_id == station_id)).select()
        if datalogger_list:
            datalogger = datalogger_list[len(datalogger_list) - 1]
            # Get all command list
            datalogger_command_list = db((db.datalogger_command.id > 0)
                                         & (db.datalogger_command.station_id == station_id)).select()

        # Get all QCVN with qcvn_station_kind
        qcvn_station_kind = db((db.qcvn_station_kind.id > 0) & (db.qcvn_station_kind.station_id == station_id) & (db.qcvn_station_kind.qcvn_id == qcvn_id) & (db.qcvn_station_kind.qcvn_kind_id == qcvn_kind_id)).select()
        if qcvn_station_kind:
            qcvn_details = db.qcvn(qcvn_station_kind[0].qcvn_id) or None
            if qcvn_details:
                qcvn_station_kind[0].qcvn_code = qcvn_details.qcvn_code
            else:
                qcvn_station_kind[0].qcvn_code = '-'

            qcvn_kind_details = db.qcvn_kind(qcvn_station_kind[0].qcvn_kind_id) or None
            if qcvn_kind_details:
                qcvn_station_kind[0].qcvn_kind_name = qcvn_kind_details.qcvn_kind
            else:
                qcvn_station_kind[0].qcvn_kind_name = '---'

            qcvn_station_kind = qcvn_station_kind.first()

            # Get all QCVN kink by qcvn ID
            qcvn_station_kind_list_by_qcvn = db((db.qcvn_kind.id > 0) & (db.qcvn_kind.qcvn_kind_delete_flag == 0) & (
                    db.qcvn_kind.qcvn_id == qcvn_station_kind.qcvn_id)).select(orderby=db.qcvn_kind.qcvn_kind_order)
            if qcvn_station_kind is not None and qcvn_station_kind.qcvn_id != "-999":
                qcvn_const_value_by_qcvn = db((db.qcvn.id > 0) & (db.qcvn.id == int(qcvn_station_kind.qcvn_id))).select()
                for i in range(len(qcvn_station_kind_list_by_qcvn)):
                    qcvn_station_kind_list_by_qcvn[i].id = str(qcvn_station_kind_list_by_qcvn[i].id)
                for i in range(len(qcvn_const_value_by_qcvn)):
                    qcvn_const_value_by_qcvn[i].id = str(qcvn_const_value_by_qcvn[i].id)

        # Get all Equipments to fill in dropdown
        equipments = db(db.equipments.station_id == station_id).select(
            db.equipments.id,
            db.equipments.equipment,
            db.equipments.series,
            db.equipments.lrv,
            db.equipments.urv,
        )
        
    
    station_indicator = db.station_indicator(station_indicator_id) or None
    mapping_name = station_indicator.mapping_name if station_indicator else ''
    indicator_id = station_indicator.indicator_id   if station_indicator else ''
    conditions_kind = (db.qcvn_station_kind.station_id == station_id)
    res_qcvn_id = ""
    res_qcvn_kind_id = ""
    default_qcvn_kind_id = ""
    if qcvn_id != "" or qcvn_id != None:
        res_qcvn_id = qcvn_id
        conditions_kind &= (db.qcvn_station_kind.qcvn_id == qcvn_id)
    if qcvn_kind_id != "":
        res_qcvn_kind_id=qcvn_kind_id
        conditions_kind &= (db.qcvn_station_kind.qcvn_kind_id == qcvn_kind_id)
    if qcvn_station_kind:
        default_qcvn_kind_id = qcvn_station_kind.qcvn_kind_id

    qcvn_station_kind_detail = db.qcvn_station_kind(conditions_kind) or None
    if qcvn_station_kind:
        default_qcvn_kind_id = qcvn_station_kind.qcvn_kind_id

    qcvn_detail_const_area_value_1=qcvn_station_kind_detail.qcvn_detail_const_area_value_1 if qcvn_station_kind_detail else 1
    qcvn_detail_const_area_value_2=qcvn_station_kind_detail.qcvn_detail_const_area_value_2 if qcvn_station_kind_detail else 1
    qcvn_detail_const_area_value_3=qcvn_station_kind_detail.qcvn_detail_const_area_value_3 if qcvn_station_kind_detail else 1
    indicators = []
    if res_qcvn_id != "":
        type_code = db(
            (db.qcvn_detail.id > 0) &
            (db.qcvn_detail.qcvn_id == res_qcvn_id)
        ).select()
        indicator_ids = set()
        for i in range(len(type_code)):
            type_code[i].id = str(type_code[i].id)
            indicator_ids.add(type_code[i].indicator_id)
            indicators = db(db.indicators.id.belongs(indicator_ids)).select()
    if res_qcvn_id == "-999":
        indicators = db((db.indicators.id > 0)).select()
    res = dict(
               station_id=station_id,
               type=type,
               equipments=equipments,
               qcvns=qcvns,
               indicators=indicators,
               qcvn_id=res_qcvn_id,
               qcvn_detail_const_area_value_1=qcvn_detail_const_area_value_1,
               qcvn_detail_const_area_value_2=qcvn_detail_const_area_value_2,
               qcvn_detail_const_area_value_3=qcvn_detail_const_area_value_3,
               qcvn_kind_id=res_qcvn_kind_id,
               qcvn_station_kind=qcvn_station_kind,
               qcvn_station_kind_list_by_qcvn=qcvn_station_kind_list_by_qcvn,
               qcvn_const_value_by_qcvn=qcvn_const_value_by_qcvn,
               mapping_name=mapping_name,
               indicator_id=indicator_id,
               station_indicator_id=station_indicator_id,
                default_qcvn_kind_id=default_qcvn_kind_id,
               )
    return res

def read_file(data_folder_current, filename, is_get_realtime, station_id):
    from StringIO import StringIO
    import ftplib
    
    print "data_folder_current = ", data_folder_current
    stations = db(db.stations.id == station_id).select()
    station = None
    if stations:
        station = stations[0]
    count_read = 0
    ftp_for_read_realtime = None
    ftp_for_import = None
    lines = None
    ftp_ip = None
    ftp_port = None
    ftp_user_name = None
    ftp_password = None
    
    
    if station:
        ftp_ip = station.data_server
        ftp_port = station.data_server_port
        ftp_user_name = station.username
        ftp_password = station.pwd
        try:
            if is_get_realtime:
                ftp_for_read_realtime = ftplib.FTP()
                ftp_for_read_realtime = ftplib.FTP(ftp_ip)
                ftp_for_read_realtime.connect(ftp_ip, ftp_port, 1500)
                ftp_for_read_realtime.login(ftp_user_name, ftp_password)
                ftp_for_read_realtime.cwd(data_folder_current)
                ftp_for_read_realtime.encoding = 'utf-8'
                ftp_for_read_realtime.sendcmd('OPTS UTF8 ON')
            else:
                ftp_for_import = ftplib.FTP()
                ftp_for_import = ftplib.FTP(ftp_ip)
                ftp_for_import.connect(ftp_ip, ftp_port, 1500)
                ftp_for_import.login(ftp_user_name, ftp_password)
                ftp_for_import.cwd(data_folder_current)
                ftp_for_import.encoding = 'utf-8'
                ftp_for_import.sendcmd('OPTS UTF8 ON')
        except Exception as ex:
            traceback.print_exc()
    else:
        return lines
    
    try:
        while count_read <= 5:
            try:
                read_data_in_file = StringIO()
                if is_get_realtime:
                    ftp_for_read_realtime.retrbinary('RETR ' + filename, read_data_in_file.write)
                else:
                    ftp_for_import.retrbinary('RETR ' + filename, read_data_in_file.write)
                    

                if read_data_in_file:
                    lines = read_data_in_file.getvalue()
                read_data_in_file.close()
                break
            except Exception as ex:
                traceback.print_exc()
            try:
                    if read_data_in_file:
                        read_data_in_file.close()
            except Exception as ex:
                traceback.print_exc()

            count_read += 1
            if count_read > 5:
                    break
            else:
                try:
                    if is_get_realtime:
                        ftp_for_read_realtime.quit()
                        ftp_for_read_realtime = None
                    else:
                        ftp_for_import.quit()
                        ftp_for_import = None
                except Exception as ex:
                    traceback.print_exc()

                time.sleep(0.5)

      # End While
    except Exception as ex:
      traceback.print_exc()

    if lines:
      return lines.decode('utf-8', 'ignore').replace(u'\ufeff', '')
    return lines


@service.json
def import_data_thongso(*args, **kwargs):
    station_id = request.vars.station_id
    convert_rate = request.vars.convert_rate
    station_name = request.vars.station_name
    station_type = request.vars.station_type
    
    stations = db(db.stations.id == station_id).select()
    station = None
    day_calculator = None
    if stations:
        station = stations[0]
        ftp_last_file_name_string = ""
        if station.last_file_name:
            ftp_last_file_name_string = station.last_file_name.split("_")[-1]
            day_calculator = datetime.strptime(ftp_last_file_name_string[:8], "%Y%m%d").replace(hour=0, minute=0, second=0)
        data_folder_current = get_data_folder_current(station.data_folder, station.path_format, day_calculator)
        lines = read_file(data_folder_current, station.last_file_name, False, station_id)
        data = dict()
        data_status = dict()
        if lines is None:
            return dict(success=False, message="Không đọc được file")
        for line in lines.splitlines():
            try:
                # Remove whitespace characters like `\n` at the end of each line
                if line:
                    line = line.strip()
                    items_temp = line.split("\t")
                if len(items_temp) < 3:  # Khong phai du lieu thong so do
                    continue
                # else:
                #     continue
            except:
                traceback.print_exc()
                continue

            items = []
            # items[0] = indicator
            # items[1] = value
            # items[2] = unit
            # items[3] = '%Y%m%d%H%M%S'
            # items[4] = status
            try:
                if len(items_temp) == 5:  # Theo thông tư 24
                    try:
                        # Case 5.1: Indicator  Value  Unit Date_time Status
                        # Case 5.2: Date_time Indicator  Value  Unit  Status
                        items = [str(items_temp[0]), items_temp[1], items_temp[2], items_temp[3], items_temp[4]]
                    except:
                        try:
                            # Case 5.2: Date_time Indicator  Value  Unit  Status
                            check_time = datetime.strptime(items_temp[0], '%Y%m%d%H%M%S')
                            items = [str(items_temp[1]), items_temp[2], items_temp[3], items_temp[0], items_temp[4]]
                        except:
                            items = None
                            pass
                elif len(items_temp) == 4:
                    try:
                        # Case 4.1: Indicator  Value  Unit Date_time
                        # Case 4.2: Indicator  Value       Date_time Status
                        # Case 4.3: Date_time  Indicator  Value  Unit
                        check_time = datetime.strptime(items_temp[3], '%Y%m%d%H%M%S')
                        try:
                            tmp_value = float(items_temp[1])
                            items = [str(items_temp[0]), items_temp[1], items_temp[2], items_temp[3], 0]
                        except:
                            items = [str(items_temp[0]), items_temp[1], items_temp[2], items_temp[3], 2]
                    except:
                        try:
                            # Case 4.2: Date_time Indicator  Value  Unit
                            check_time = datetime.strptime(items_temp[0], '%Y%m%d%H%M%S')
                            try:
                                tmp_value = float(items_temp[2])
                                items = [str(items_temp[1]), items_temp[2], items_temp[3], items_temp[0], 0]
                            except:
                                items = [str(items_temp[1]), items_temp[2], items_temp[3], items_temp[0], 2]
                        except:
                            try:
                                # Case 4.3: Indicator  Value  Date_time Status
                                check_time = datetime.strptime(items_temp[2], '%Y%m%d%H%M%S')
                                try:
                                    tmp_value = float(items_temp[1])
                                    items = [str(items_temp[0]), items_temp[1], '---', items_temp[2], items_temp[3]]
                                except:
                                    items = [str(items_temp[0]), items_temp[1], '---', items_temp[2], 2]
                            except:
                                items = None
                                pass
                elif len(items_temp) == 3:
                    try:
                        # Case 3.1: Indicator  Value  Date_time
                        # Case 3.2: datetime indicator  value
                        check_time = datetime.strptime(items_temp[2], '%Y%m%d%H%M%S')
                        try:
                            tmp_value = float(items_temp[1])
                            items = [items_temp[0], items_temp[1], '---', items_temp[2], 0]
                        except:
                            items = [items_temp[0], items_temp[1], '---', items_temp[2], 2]
                    except:
                        try:
                            # Case 3.2: datetime indicator  value"
                            check_time = datetime.strptime(items_temp[0], '%Y%m%d%H%M%S')
                            try:
                                tmp_value = float(items_temp[2])
                                items = [items_temp[1], items_temp[2], '---', items_temp[0], 0]
                            except:
                                items = [items_temp[1], items_temp[2], '---', items_temp[0], 2]
                        except:
                            items = None
                        pass
                
            except:
                traceback.print_exc()
                pass
            
            if not items:
                continue

            # TriNT: Kiem tra indicator da khai bao chua, neu co thi nhan ty le chuyen doi
            # items[0] = indicator
            # items[1] = value
            # items[2] = unit
            # items[3] = '%Y%m%d%H%M%S'
            # items[4] = status

            # check define indicator, and convert unit

        #   # ==================================================
        #   # TriNT: So sanh QCVN
        #   # Chi can 1 chi so vuot nguong la danh dau 'exceed'
            try:
                data[items[0]] = items[1]  # Luu tru du lieu vao data
                data_datetime = items[3]  # datetime trong 1 file se giong het nhau
                # items[0] = indicator
                # items[1] = value
                # items[2] = unit
                # items[3] = '%Y%m%d%H%M%S'
                # items[4] = status = sensor_status

                # "data": {
                #     "pH": 8.21,
                #     "TSS": 65.5,
                #     "Temp": 22.96
                # }
                data_status[items[0]] = {}
                data_status[items[0]]['indicator_name'] = items[0]
                data_status[items[0]]['value'] = items[1]
                data_status[items[0]]['unit'] = items[2]
                
                source_name = items[0].replace('\x00', '').encode('utf-8', errors='ignore')
                indicators = db(db.indicators.source_name == str(source_name)).select()
                qcvn_code = 'Không chọn QCVN'
                qcvn_id = -999
                if indicators and len(indicators) > 0:
                    indicator = indicators[0]
                    status = const.SI_STATUS['NEED_UPDATE']['value']
                    db.station_indicator.update_or_insert(
                        (db.station_indicator.station_id == station_id) & (db.station_indicator.indicator_id == indicator.id),
                        station_id=station_id, station_name=station_name, station_type=station_type,
                        preparing_value=indicator.preparing_value,
                        indicator_id=indicator.id,
                        qcvn_id=qcvn_id,
                        qcvn_code=qcvn_code,
                        unit=indicator.unit,
                        tendency_value=indicator.tendency_value,
                        exceed_value=indicator.exceed_value,
                        status=status,
                        mapping_name=indicator.source_name, convert_rate=convert_rate)
                
            except Exception as ex:
                traceback.print_exc()
                return dict(success=False, message=ex)
        
    return dict(success=True)

def get_data_folder_current(ftp_data_folder, folder_path_format, day_calculator):
    day_calculator_folder = ''
    if folder_path_format == 0:
      day_calculator_folder = '/%0.4d/%0.2d/%0.2d' % (
        day_calculator.year, day_calculator.month,
        day_calculator.day)
    elif folder_path_format == 2:
      day_calculator_folder = '/%0.4d%0.2d%0.2d' % (day_calculator.year, day_calculator.month,
                                                    day_calculator.day)
    elif folder_path_format == 3:
      day_calculator_folder = '/%0.4d/Thang%0.2d/%0.4d%0.2d%0.2d' % (
        day_calculator.year, day_calculator.month,
        day_calculator.year, day_calculator.month,
        day_calculator.day)
    # folder yyyy-mm-dd
    elif folder_path_format == 5:
      day_calculator_folder = '/%0.4d-%0.2d-%0.2d' % (day_calculator.year, day_calculator.month,
                                                      day_calculator.day)
    elif folder_path_format == 6:
      day_calculator_folder = '/%0.4d/Thang%0.2d/%0.2d%0.2d%0.4d' % (
        day_calculator.year, day_calculator.month,
        day_calculator.day, day_calculator.month,
        day_calculator.year)
    elif folder_path_format == 7:
      day_calculator_folder = '/%0.4d_%0.2d_%0.2d' % (
        day_calculator.year, day_calculator.month, day_calculator.day)

    elif folder_path_format == 8:
      day_calculator_folder = '/%0.4d/%0.2d/%0.2d%0.2d%0.4d' % (
        day_calculator.year, day_calculator.month,
        day_calculator.day, day_calculator.month,
        day_calculator.year)
    else:
      day_calculator_folder = '/%0.4d/Thang%0.2d/Ngay%0.2d' % (
        day_calculator.year, day_calculator.month,
        day_calculator.day)

    return '{}{}'.format(ftp_data_folder, day_calculator_folder).replace('//', '/')

    ################################################################################