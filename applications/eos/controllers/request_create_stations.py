if False:
    from gluon import *
    from gluon import auth, service
    request = current.request
    response = current.response
    session = current.session
    cache = current.cache
    T = current.T
    db = current.db

from applications.eos.modules import common as common
from applications.eos.modules import const
from datetime import datetime
from applications.eos.repo.ftp_repo import FtpRepo
from applications.eos.services.ftp_services import *
from applications.eos.services import station_service, ftp_services, request_create_station_service
from applications.eos.common import response as http_response
import requests
import sys
import traceback
import time
from applications.eos.common import my_const
# define
def call():
    return service()

@service.json
def get_list_request_create_stations(*args, **kwargs):
    try:
        iDisplayStart = int(request.vars.iDisplayStart)
        iDisplayLength = int(request.vars.iDisplayLength)
        type = request.vars.type
        approve_status = request.vars.approve_status
        sometext = request.vars.sometext
        province_id = request.vars.province_id
        ftp_connection_status = request.vars.ftp_connection_status
        status = request.vars.status

        aaData = []
        limitby = (iDisplayStart, iDisplayLength + 1)

        conditions = (db.request_create_stations.id > 0)

        if sometext:
            conditions &= ((db.request_create_stations.station_code.contains(sometext)) |
                           (db.request_create_stations.station_name.contains(sometext)) |
                           (db.request_create_stations.description.contains(sometext)) |
                           (db.request_create_stations.contact_point.contains(sometext)) |
                           (db.request_create_stations.phone.contains(sometext)) |
                           (db.request_create_stations.email.contains(sometext)) |
                           (db.request_create_stations.address.contains(sometext)))
        if type:
            conditions &= (db.request_create_stations.station_type == type)
        if province_id:
            conditions &= (db.request_create_stations.province_id == province_id)
        if approve_status:
            conditions &= (db.request_create_stations.approve_status == approve_status)
        if ftp_connection_status:
            conditions &= (db.request_create_stations.ftp_connection_status == ftp_connection_status)
        if status:
            conditions &= (db.request_create_stations.status == status)
        if auth is not None and auth.user['type'] == 1:
            conditions &= (db.request_create_stations.created_by == auth.user['id'])
        list_data = db(conditions).select(db.request_create_stations.id,
                                          db.request_create_stations.station_code,
                                          db.request_create_stations.station_name,
                                          db.request_create_stations.station_type,
                                          db.request_create_stations.province_id,
                                          db.request_create_stations.area_id,
                                          db.request_create_stations.address,
                                          db.request_create_stations.phone,
                                          db.request_create_stations.email,
                                          db.request_create_stations.ftp_connection_status,
                                          db.request_create_stations.order_no,
                                          db.request_create_stations.username,
                                          db.request_create_stations.pwd,
                                          db.request_create_stations.data_folder,
                                          db.request_create_stations.data_server_port,
                                          db.request_create_stations.data_server,
                                          db.request_create_stations.approve_status,
                                          db.request_create_stations.approve_reason,
                                          orderby=db.request_create_stations.order_no,
                                          limitby=limitby)
        iTotalRecords = db(conditions).count()
        iRow = iDisplayStart + 1

        provice_dict = common.get_province_dict()

        areas = common.get_area_by_station_dict()
        station_type = dict()
        for item in common.get_station_types():
            station_type[str(item['value'])] = item['name']

        for item in list_data:
            approve_tag = A(I())
            edit_tag = A(I())
            form_url = URL('form', args=[item.id])
            if auth.has_permission('approve', 'request_create_stations') and \
                    item.approve_status == const.REQUEST_CREATE_STATION_WAITING_STATUS:
                approve_tag = A(I(_class="fa fa-edit", _onClick="showApproveModal('" + str(item.id) + "')"))
                edit_tag = A(I(_class='fa fa-edit'), _href=form_url)

            url_ftp = 'ftp://%s:%s@%s:%s%s' % (
                item.username, item.pwd, item.data_server, item.data_server_port, item.data_folder);
            if item.ftp_connection_status:
                text = 'Kết nối'
            else:
                text = 'Không kết nối'
            profile_url = URL('form', args=[item.id])

            approve_status = T('')
            if item.approve_status == const.REQUEST_CREATE_STATION_WAITING_STATUS:
                approve_status = T('Wait Approve')
            elif item.approve_status == const.REQUEST_CREATE_STATION_APPROVED_STATUS:
                approve_status = T('Approved')
            elif item.approve_status == const.REQUEST_CREATE_STATION_REJECTED_STATUS:
                approve_status = T('Rejected')
            aaData.append([
                A(str(iRow), _href=profile_url),
                A(item.station_name, _href=profile_url),
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
                approve_status,
                item.approve_reason,
                # A(I(_class='fa fa-folder'), _style='color: #FBDB79; font-size: 19px;', _onclick="ftp_click('%s')" % (url_ftp)),
                edit_tag,
                approve_tag,
                INPUT(_group='0', _class='select_item', _type='checkbox', _value=item.id),
                item.id
            ])

            iRow += 1
        return dict(iTotalRecords=iTotalRecords, iTotalDisplayRecords=iTotalRecords, aaData=aaData, success=True)
    except Exception as ex:
        return dict(iTotalRecords=0, iTotalDisplayRecords=0, aaData=[], message=str(ex), success=False)


def validate(frm):
    # Check condion
    # Get control value by : frm.vars.ControlName
    # If validate fail : frm.errors.ControlName = some message
    pass

def get_alarm_by_request_create_station_id(request_create_station_id):
    if not request_create_station_id:
        return None
    alarm = db(db.request_create_station_alarm.request_create_station_id == request_create_station_id).select()
    if alarm:
        return alarm.first()
    return None

# index api for request_create_stations
def index():
    conditions = (db.request_create_stations.id > 0)
    row = db(conditions).select(db.request_create_stations.province_id)
    provinces_ids = []
    for it in row:
        if it.province_id:
            provinces_ids.append(str(it.province_id))
    query = db.provinces.id > 0
    query &= db.provinces.id.belongs(provinces_ids)
    provinces = db(query).select()

    return dict(provinces=provinces, message='')


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

def form():
    db = current.db
    ftp_repo = FtpRepo(db)
    # If in Update mode, get equivallent record
    request_create_station_id = request.vars.request_create_station_id
    last_time = request.vars.last_time
    last_file_name = request.vars.last_file_name
    province = ""
    ftp_last_file_name = request.vars.ftp_file_name
    ftp_folder_path = request.vars.ftp_folder_path
    ftp_path_format = request.vars.path_format
    ftp_id = request.vars.ftp_id
    
    if ftp_last_file_name != None and ftp_path_format != None:
        ftp_folder_path, ftp_last_file_name, last_time = get_ftp_file_from_data(ftp_last_file_name, ftp_path_format)
        
    data_request_create_station_id = request.args(0)
    record = db.request_create_stations(data_request_create_station_id) or None
    request_create_station_id = request.args(0) or None
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
    qi_adjust_time = None
    qi_adjust = None
    item_stations_qi = db(db.request_create_stations.id == request_create_station_id).select(db.request_create_stations.qi_adjust)
    item_stations_qi_time = db(db.request_create_stations.id == request_create_station_id).select(db.request_create_stations.qi_adjsut_time)

    ftp_list = ftp_repo.get_all(auth)
    agents = db(db.agents.id > 0).select()
    # get the last qi_adjust and qi_adjsut_time in
    if item_stations_qi:
        for i in item_stations_qi:
            qi_adjust = i.qi_adjust
    if item_stations_qi_time:
        for i in item_stations_qi_time:
            qi_adjust_time = i.qi_adjsut_time
    approve_status = const.REQUEST_CREATE_STATION_WAITING_STATUS if record is None else record.approve_status
    frm = SQLFORM(db.request_create_stations, record, _method='POST', hideerror=True, showid=False, _id='frmMain')
    # if request.vars.last_time != None:
    # frm.vars.last_time =  datetime.now()
    # frm.vars.last_time = datetime.strptime(request.vars.last_time, '%Y/%m/%d %H:%M')
    if frm.process(onvalidation=validate, detect_record_change=False, hideerror=True).accepted:
        # update history
        # newName = db.stations(request.args(0)).station_name or None
        new_request_create_station_id = frm.vars.id


        # add station id if new stations is created
        if record is None:
            db(db.request_create_stations.id == new_request_create_station_id).update(approve_status=const.REQUEST_CREATE_STATION_WAITING_STATUS, request_create_station_id=new_request_create_station_id, area_ids=frm.vars.area_ids)
        if record:
            record.update_record(approve_status=approve_status)
        # Update FTP information
        if ftp_id != "":
            ftp_info = ftp_repo.get_ftp_by_id(ftp_id)
            db(db.request_create_stations.id == new_request_create_station_id).update(
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
            update_lastlog_reafile_ftp(last_time, data_request_create_station_id, type)

        if qi_adjust:
            db(db.request_create_stations.id == request_create_station_id).update(qi_adjust=qi_adjust)
        if qi_adjust_time:
            db(db.request_create_stations.id == request_create_station_id).update(qi_adjsut_time=qi_adjust_time)

        if request.vars.transfer_type == 'mqtt':
            res = station_service.check_mqtt_status(request.vars, record)
        else:
            res = ftp_services.check_ftp_status(request.vars)

        if record:
            description = 'Thay_doi_noi_dung_thong_tin_tram.'
            # handle later if need
            # db.manager_stations_history.insert(station_id=data_request_create_station_id,
            #                                    action='Update',
            #                                    username=current_user.fullname or None,
            #                                    description=description,
            #                                    update_time=datetime.now())
            if record.order_no is None:
                record.update_record(order_no=0)
            if qi_adjust:
                db(db.request_create_stations.id == request_create_station_id).update(qi_adjust=qi_adjust)
            if qi_adjust_time:
                db(db.request_create_stations.id == request_create_station_id).update(qi_adjsut_time=qi_adjust_time)

            db(db.request_create_stations.id == request_create_station_id).update(ftp_connection_status=res)
            session.flash = T('MSG_INFO_SAVE_SUCCESS')
            redirect(URL('index'))
        else:
            new_record = db(db.request_create_stations.id > 0).select().last() or None
            # db.manager_stations_history.insert(station_id=newrecord.id,
            #                                    station_name=newrecord.station_name,
            #                                    action='Create',
            #                                    username=current_user.fullname or None,
            #                                    description='',
            #                                    update_time=datetime.now())
            db(db.request_create_stations.id == new_record.id).update(ftp_connection_status=res)
            # if current_user:
            #     if not (auth.has_membership('admin') or auth.has_membership(const.GROUP_MANAGER)):
            #         data_user = db(db.manager_areas.areas_id == str(newrecord.area_id)).select(db.manager_areas.user_id)
            #         user_ids = [str(it.user_id) for it in data_user]
            #         if user_ids:
            #             for i in user_ids:
            #                 db.manager_stations.insert(user_id=i,
            #                                            station_id=str(newrecord.id))
        # update_ftp_status(data_request_create_station_id)
        ###
            session.flash = T('MSG_INFO_SAVE_SUCCESS')
            redirect(URL('form', args=[new_record.id])) # redirect to edit form
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

    indicators, qcvns, equipments, alarm, request_create_station_qcvn_station_kind, qcvn_station_kind_list_by_qcvn, \
        qcvn_const_value_by_qcvn, datalogger, datalogger_command_list, data_send = [], [], [], [], [], [], [], [], [], []
    # Get Station alarm info
    list_status_data_send = []
    current_send_status = 0
    curent_send_name = ''
    send_file_name = ''
    alarm = get_alarm_by_request_create_station_id(request_create_station_id)

    if request_create_station_id:
        # Get all indicators to fill in dropdown
        # indicators = db((db.indicators.id > 0) & (db.indicators.indicator_type == type)).select()
        # Get all QCVN to fill in dropdown
        qcvns = db((db.qcvn.id > 0) & (db.qcvn.qcvn_type == record.station_type)).select(db.qcvn.id, db.qcvn.qcvn_code,
                                                                                         db.qcvn.qcvn_const_value)
        province = db.provinces(db.provinces.id == record.province_id)
        agent = db.agents(db.agents.id == record.agents_id)

        data_send_list = None
        data_send_list = db((db.request_create_station_send_data.id > 0) & (db.request_create_station_send_data.request_create_station_id == request_create_station_id)).\
            select()
        send_file_name = station_service.get_send_file_name(record, province, agent, data_send_list)

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
        datalogger_list = db((db.request_create_station_datalogger.id > 0) & (db.request_create_station_datalogger.request_create_station_id == request_create_station_id)).\
            select()
        if datalogger_list:
            datalogger = datalogger_list[len(datalogger_list) - 1]
            # Get all command list
            datalogger_command_list = db((db.request_create_station_datalogger_command.id > 0)
                                         & (db.request_create_station_datalogger_command.request_create_station_id == request_create_station_id)).select()

        # Get all QCVN with qcvn_station_kind
        request_create_station_qcvn_station_kind = db((db.request_create_station_qcvn_station_kind.id > 0) & (db.request_create_station_qcvn_station_kind.request_create_station_id == request_create_station_id)).\
            select()
        if request_create_station_qcvn_station_kind:
            qcvn_details = db.qcvn(request_create_station_qcvn_station_kind[0].qcvn_id) or None
            if qcvn_details:
                request_create_station_qcvn_station_kind[0].qcvn_code = qcvn_details.qcvn_code
            else:
                request_create_station_qcvn_station_kind[0].qcvn_code = '-'

            qcvn_kind_details = db.qcvn_kind(request_create_station_qcvn_station_kind[0].qcvn_kind_id) or None
            if qcvn_kind_details:
                request_create_station_qcvn_station_kind[0].qcvn_kind_name = qcvn_kind_details.qcvn_kind
            else:
                request_create_station_qcvn_station_kind[0].qcvn_kind_name = '---'

            request_create_station_qcvn_station_kind = request_create_station_qcvn_station_kind.first()

            # Get all QCVN kink by qcvn ID
            qcvn_station_kind_list_by_qcvn = db((db.qcvn_kind.id > 0) & (db.qcvn_kind.qcvn_kind_delete_flag == 0) & (
                    db.qcvn_kind.qcvn_id == request_create_station_qcvn_station_kind.qcvn_id)).\
                select(orderby=db.qcvn_kind.qcvn_kind_order)
            qcvn_const_value_by_qcvn = db((db.qcvn.id > 0) & (db.qcvn.id == request_create_station_qcvn_station_kind.qcvn_id)).select()
            for i in range(len(qcvn_station_kind_list_by_qcvn)):
                qcvn_station_kind_list_by_qcvn[i].id = str(qcvn_station_kind_list_by_qcvn[i].id)
            for i in range(len(qcvn_const_value_by_qcvn)):
                qcvn_const_value_by_qcvn[i].id = str(qcvn_const_value_by_qcvn[i].id)

        # # Get all Equipments to fill in dropdown
        equipments = db(db.request_create_station_equipments.request_create_station_id == request_create_station_id).select(
            db.request_create_station_equipments.id,
            db.request_create_station_equipments.equipment,
            db.request_create_station_equipments.series,
            db.request_create_station_equipments.lrv,
            db.request_create_station_equipments.urv,
        )
    
    res_ftp_folder_path = ""
    if request_create_station_id:
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
               request_create_station_id=request_create_station_id,
               station_id=None,
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
               qcvn_station_kind=request_create_station_qcvn_station_kind,
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

def update_lastlog_reafile_ftp(last_time, request_create_station_id, type):
    last_time_update = datetime.strptime(datetime.strftime(datetime.strptime(last_time, '%Y-%m-%d'), '%Y-%m-%dT%H:%M'),
                                         '%Y-%m-%dT%H:%M')

    item_data_hour_lastest = db(db.request_create_station_data_hour_lastest.request_create_station_id == request_create_station_id).\
        select(db.request_create_station_data_hour_lastest.request_create_station_id)
    if item_data_hour_lastest:
        db(db.request_create_station_data_hour_lastest.request_create_station_id == request_create_station_id).update(last_time=last_time_update)

    item_data_month_lastest = db(db.request_create_station_data_month_lastest.request_create_station_id == request_create_station_id).select(
        db.request_create_station_data_month_lastest.request_create_station_id)
    if item_data_month_lastest:
        db(db.request_create_station_data_month_lastest.request_create_station_id == request_create_station_id).update(last_time=last_time_update)

    item_data_day_lastest = db(db.request_create_station_data_day_lastest.request_create_station_id == request_create_station_id).\
        select(db.request_create_station_data_day_lastest.last_time)
    if item_data_day_lastest:
        db(db.request_create_station_data_day_lastest.request_create_station_id == request_create_station_id).update(last_time=last_time_update)


    item_data_lastest = db(db.request_create_station_data_lastest.request_create_station_id == request_create_station_id).\
        select(db.request_create_station_data_lastest.request_create_station_id)
    if item_data_lastest:
        db(db.request_create_station_data_lastest.request_create_station_id == request_create_station_id).update(get_time=last_time_update)

    item_last_data_files = db(db.request_create_station_last_data_files.request_create_station_id == request_create_station_id).\
        select(db.request_create_station_last_data_files.request_create_station_id)
    if item_last_data_files:
        db(db.request_create_station_last_data_files.request_create_station_id == request_create_station_id).\
            update(lasttime=last_time_update, filename='', file_name='')

    if type == 4:
        item_data_aqi_hour_lastest = db(db.request_create_station_data_aqi_hour_lastest.request_create_station_id == request_create_station_id).\
            select(db.request_create_station_data_aqi_hour_lastest.request_create_station_id)
        if item_data_aqi_hour_lastest:
            db(db.request_create_station_data_aqi_hour_lastest.request_create_station_id == request_create_station_id).\
                update(last_time=last_time_update)

        item_data_aqi_24h_lastest = db(db.request_create_station_data_aqi_24h_lastest.request_create_station_id == request_create_station_id).\
            select(db.request_create_station_data_aqi_24h_lastest.request_create_station_id)
        if item_data_aqi_24h_lastest:
            db(db.request_create_station_data_aqi_24h_lastest.request_create_station_id == request_create_station_id).\
                update(last_time=last_time_update)

def profile():
    request_create_station_id = request.args(0) or None
    if not request_create_station_id:
        return dict()

    request_create_station = db.request_create_stations(request_create_station_id) or None
    name = request_create_station.station_name if request_create_station else ''

    province = db.provinces(db.provinces.id == request_create_station.province_id)
    agent = db.agents(db.agents.id == request_create_station.agents_id)
    area = db.areas(db.areas.id == request_create_station.area_id)
    type = db.station_types(db.station_types.code == request_create_station.station_type)

    frm = SQLFORM(db.request_create_stations, request_create_station, _id='frmMain')

    data_send_list = db((db.request_create_station_send_data.id > 0) & (db.request_create_station_send_data.request_create_station_id == request_create_station_id)).select()
    data_send = data_send_list[0] if data_send_list else None

    send_file_name = station_service.get_send_file_name(request_create_station, province, agent, data_send_list)
    send_data_status = station_service.get_send_data_status(data_send_list)

    alarm = get_alarm_by_request_create_station_id(request_create_station_id)

    status = {}
    for item in const.STATION_STATUS.values():
        if request_create_station.status == item['value']:
            status = {'value': item['value'], 'name': item['name']}

    return dict(frm=frm, request_create_station_id=request_create_station_id, name=name, request_create_station=request_create_station, data_send=data_send,
                type=type, province=province, area=area, agent=agent, status=status,
                send_data_status=send_data_status, send_file_name=send_file_name,
                alarm=alarm)


@service.json
def get_list_indicators_for_request_create_station(*args, **kwargs):
    try:
        iDisplayStart = int(request.vars.iDisplayStart)
        iDisplayLength = int(request.vars.iDisplayLength)
        request_create_station_id = request.vars.request_create_station_id
        aaData = []
        limitby = (iDisplayStart, iDisplayLength + 1)
        view_only = request.vars.view_only
        conditions = (db.request_create_station_indicator.id > 0)
        if request_create_station_id:
            conditions &= (db.request_create_station_indicator.request_create_station_id == request_create_station_id) & ((
                                                                                     db.request_create_station_indicator.status ==
                                                                                     const.SI_STATUS['IN_USE']['value']) | (
                                                                                         db.request_create_station_indicator.status ==
                                                                                         const.SI_STATUS['NEED_UPDATE'][
                                                                                             'value']))
        list_data = db(conditions).select(db.request_create_station_indicator.id,
                                          db.request_create_station_indicator.indicator_id,
                                          db.request_create_station_indicator.tendency_value,
                                          db.request_create_station_indicator.preparing_value,
                                          db.request_create_station_indicator.exceed_value,
                                          db.request_create_station_indicator.qcvn_code,
                                          db.request_create_station_indicator.qcvn_detail_type_code,
                                          db.request_create_station_indicator.qcvn_detail_min_value,
                                          db.request_create_station_indicator.qcvn_detail_max_value,
                                          db.request_create_station_indicator.qcvn_detail_const_area_value,
                                          db.request_create_station_indicator.equipment_name,
                                          db.request_create_station_indicator.equipment_lrv,
                                          db.request_create_station_indicator.equipment_urv,
                                          db.request_create_station_indicator.mapping_name,
                                          db.request_create_station_indicator.convert_rate,
                                          db.request_create_station_indicator.status,
                                          db.request_create_station_indicator.qcvn_id,
                                          db.request_create_station_indicator.qcvn_detail_id,
                                          db.request_create_station_indicator.qcvn_kind_id,
                                          db.request_create_station_indicator.request_create_station_id,
                                          )
        # limitby = limitby)
        # Tong so ban ghi khong thuc hien phan trang
        iTotalRecords = db(conditions).count()
        indicator_dict = common.get_indicator_dict()
        status = dict(db.request_create_station_indicator.status.requires.options())
        # Thu tu ban ghi
        iRow = iDisplayStart + 1
        hide_class = "" if (request.vars.preview is None or request.vars.preview == 'None') else "hide"
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
            conditions_kind = (db.request_create_station_qcvn_station_kind.request_create_station_id == request_create_station_id)
            if item.qcvn_id != "" or item.qcvn_id != None:
                qcvn_id = str(item.qcvn_id)
                conditions_kind &= (db.request_create_station_qcvn_station_kind.qcvn_id == item.qcvn_id)
            if item.qcvn_kind_id != "" or item.qcvn_kind_id != None:
                qcvn_kind_id = str(item.qcvn_kind_id)
                conditions_kind &= (db.request_create_station_qcvn_station_kind.qcvn_kind_id == item.qcvn_kind_id)

            qcvn_station_kind = db.request_create_station_qcvn_station_kind(conditions_kind) or None

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
                round(qcvn_detail_const_area_value_1, 2) if qcvn_detail_const_area_value_1 > 0 else None,
                round(qcvn_detail_const_area_value_2, 2) if qcvn_detail_const_area_value_2 > 0 else None,
                round(qcvn_detail_const_area_value_3, 2) if qcvn_detail_const_area_value_3 > 0 else None,
                TD(text, _class="qcvn_detail_type_code", _value=str(item.qcvn_detail_type_code)),
                round(item.qcvn_detail_min_value, 6) if item.qcvn_detail_min_value else None,
                round(item.qcvn_detail_max_value, 6) if item.qcvn_detail_max_value else None,
                # item.qcvn_detail_const_area_value,
                status[str(item.status)] if item.status else '',
                A(I(_class='fa fa-edit ' + hide_class), data={
                    'url': '/eos/request_create_stations/popup_edit_thong_so?request_create_station_id=' + request_create_station_id + '&qcvn_id=' + qcvn_id + '&qcvn_kind_id=' + qcvn_kind_id + '&station_indicator_id=' + str(
                        idd)}, _class="edit_thong_so_btn btnAddNew", _href="javascript: {};")
            ]

            if not view_only:
                listA.append(INPUT(_group='1', _class='select_item ' + hide_class, _type='checkbox', _value=item.id))
            listA.append(item.id)

            aaData.append(listA)
            iRow += 1
        return dict(iTotalRecords=iTotalRecords, iTotalDisplayRecords=iTotalRecords, aaData=aaData, success=True)
    except Exception as ex:
        return dict(iTotalRecords=0, iTotalDisplayRecords=0, aaData=[], message=str(ex), success=False)


def popup_edit_thong_so():
    request_create_station_id = request.vars.request_create_station_id
    qcvn_id = request.vars.qcvn_id
    qcvn_kind_id = request.vars.qcvn_kind_id
    station_indicator_id = request.vars.station_indicator_id
    record = db.request_create_stations(request_create_station_id) or None
    indicators, qcvns, equipments, alarm, qcvn_station_kind, qcvn_station_kind_list_by_qcvn, \
        qcvn_const_value_by_qcvn, datalogger, datalogger_command_list, data_send = [], [], [], [], [], [], [], [], [], []
    list_status_data_send = []
    if request_create_station_id:
        # Get all indicators to fill in dropdown
        # indicators = db((db.indicators.id > 0) & (db.indicators.indicator_type == type)).select()
        # Get all QCVN to fill in dropdown
        qcvns = db((db.qcvn.id > 0)).select(db.qcvn.id, db.qcvn.qcvn_code,
                                            db.qcvn.qcvn_const_value)
        province = db.provinces(db.provinces.id == record.province_id)
        agent = db.agents(db.agents.id == record.agents_id)
        data_send_list = db((db.request_create_station_send_data.id > 0) & (db.request_create_station_send_data.request_create_station_id == request_create_station_id)).select()

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
        datalogger_list = db((db.request_create_station_datalogger.id > 0) & (db.request_create_station_datalogger.request_create_station_id == request_create_station_id)).select()
        if datalogger_list:
            datalogger = datalogger_list[len(datalogger_list) - 1]
            # Get all command list
            datalogger_command_list = db((db.request_create_station_datalogger.id > 0)
                                         & (db.request_create_station_datalogger_command.request_create_station_id == request_create_station_id)).select()

        # Get all QCVN with qcvn_station_kind
        qcvn_station_kind = db((db.request_create_station_qcvn_station_kind.id > 0)
                               & (db.request_create_station_qcvn_station_kind.request_create_station_id == request_create_station_id)
                               & (db.request_create_station_qcvn_station_kind.qcvn_id == qcvn_id)
                               & (db.request_create_station_qcvn_station_kind.qcvn_kind_id == qcvn_kind_id)
                               ).select()

        db((db.qcvn_station_kind.id > 0) & (db.qcvn_station_kind.station_id == station_id) & (
                    db.qcvn_station_kind.qcvn_id == qcvn_id) & (
                       db.qcvn_station_kind.qcvn_kind_id == qcvn_kind_id)).select()
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
                qcvn_const_value_by_qcvn = db(
                    (db.qcvn.id > 0) & (db.qcvn.id == int(qcvn_station_kind.qcvn_id))).select()
                for i in range(len(qcvn_station_kind_list_by_qcvn)):
                    qcvn_station_kind_list_by_qcvn[i].id = str(qcvn_station_kind_list_by_qcvn[i].id)
                for i in range(len(qcvn_const_value_by_qcvn)):
                    qcvn_const_value_by_qcvn[i].id = str(qcvn_const_value_by_qcvn[i].id)

        # Get all Equipments to fill in dropdown
        equipments = db(db.request_create_station_equipments.request_create_station_id == request_create_station_id).select(
            db.request_create_station_equipments.id,
            db.request_create_station_equipments.equipment,
            db.request_create_station_equipments.series,
            db.request_create_station_equipments.lrv,
            db.request_create_station_equipments.urv,
        )

    station_indicator = db.request_create_station_indicator(station_indicator_id) or None
    mapping_name = station_indicator.mapping_name if station_indicator else ''
    indicator_id = station_indicator.indicator_id if station_indicator else ''
    conditions_kind = (db.request_create_station_qcvn_station_kind.request_create_station_id == request_create_station_id)
    res_qcvn_id = ""
    res_qcvn_kind_id = ""
    default_qcvn_kind_id = ""
    if qcvn_id != "" or qcvn_id != None:
        res_qcvn_id = qcvn_id
        conditions_kind &= (db.request_create_station_qcvn_station_kind.qcvn_id == qcvn_id)
    if qcvn_kind_id != "":
        res_qcvn_kind_id = qcvn_kind_id
        conditions_kind &= (db.request_create_station_qcvn_station_kind.qcvn_kind_id == qcvn_kind_id)
    if qcvn_station_kind:
        default_qcvn_kind_id = qcvn_station_kind.qcvn_kind_id

    qcvn_station_kind_detail = db.request_create_station_qcvn_station_kind(conditions_kind) or None

    qcvn_detail_const_area_value_1 = qcvn_station_kind_detail.qcvn_detail_const_area_value_1 if qcvn_station_kind_detail else 1
    qcvn_detail_const_area_value_2 = qcvn_station_kind_detail.qcvn_detail_const_area_value_2 if qcvn_station_kind_detail else 1
    qcvn_detail_const_area_value_3 = qcvn_station_kind_detail.qcvn_detail_const_area_value_3 if qcvn_station_kind_detail else 1
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
        station_id=request_create_station_id,
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

@service.json
def get_list_indicators_auto_adjust(*args, **kwargs):
    try:
        request_create_station_id = request.vars.request_create_station_id
        view_only = request.vars.view_only
        aaData = []

        conditions = (db.request_create_station_indicator.id > 0)
        if request_create_station_id:
            conditions &= (db.request_create_station_indicator.request_create_station_id == request_create_station_id)

        list_data = db(conditions).select()
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

        for item in list_data:
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

            typeCompareValue = [">", "<", "=", "<=", ">="]
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
                '%s %s' % (INPUT(_class='', _name='extraordinary_value_check', _type='checkbox',
                                 _checked=item.extraordinary_value_check, _disabled=view_only),
                           textbox2,
                           ),
                '%s %s' % (
                INPUT(_class='', _name='compare_value_check', _type='checkbox', _checked=item.compare_value_check,
                      _disabled=view_only),
                textbox3,
                ),
                '%s' % (textbox4),
                '%s' % (textbox5),
                str(item.id)
            ])
        return dict(iTotalRecords=iTotalRecords, iTotalDisplayRecords=iTotalRecords, aaData=aaData, success=True)
    except Exception as ex:
        return dict(iTotalRecords=0, iTotalDisplayRecords=0, aaData=[], message=str(ex), success=False)


@service.json
def edit_station_indicator(*args, **kwargs):
    try:
        table = 'request_create_station_indicator'
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

@service.json
def add_request_create_station_datalogger_command(*args, **kwargs):
    try:
        request_create_station_id = request.vars.request_create_station_id
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
        datalogger = db(db.request_create_station_datalogger.request_create_station_id == request_create_station_id).select().first()
        if datalogger:
            if data['type_logger'] != datalogger.type_logger or data['type_logger'] != datalogger.type_logger or data[
                'logger_name'] != datalogger.logger_name:
                datalogger.logger_id = data['logger_id']
                datalogger.type_logger = data['type_logger']
                datalogger.logger_name = data['logger_name']
                datalogger.update_record()
                # try:
                #     db.manager_stations_history.insert(request_create_station_id=request_create_station_id,
                #                                        action='Update',
                #                                        username=current_user.fullname or None,
                #                                        description='Thay_doi_noi_dung_truyen_du_lieu',
                #                                        update_time=datetime.now())
                # except:
                #     pass
        else:
            db.request_create_station_datalogger.insert(**data)
            # try:
            #     db.manager_stations_history.insert(station_id=request_create_station_id,
            #                                        action='Add',
            #                                        username=current_user.fullname or None,
            #                                        description='Thay_doi_noi_dung_truyen_du_lieu',
            #                                        update_time=datetime.now())
            # except:
            #     pass
        if not data.has_key('command_id'):
            data['command_id'] = data['command_name']
        conditions = (db.request_create_station_datalogger_command.request_create_station_id == request_create_station_id)
        conditions &= (db.request_create_station_datalogger_command.command_name == data['command_name'])
        c = db(conditions).count()
        if c > 0:
            db(conditions).update(**data)
        else:
            db.request_create_station_datalogger_command.insert(**data)

        return dict(success=True)
    except Exception as ex:
        return dict(success=False, message=str(ex))

@service.json
def get_datalogger_command_by_request_create_station(*args, **kwargs):
    try:
        iDisplayStart = int(request.vars.iDisplayStart)
        iDisplayLength = int(request.vars.iDisplayLength)
        request_create_station_id = request.vars.request_create_station_id
        logger_type = request.vars.type
        aaData = []
        limitby = (iDisplayStart, iDisplayLength + 1)
        conditions = (db.request_create_station_datalogger_command.id > 0)
        if request_create_station_id:
            conditions &= (db.request_create_station_datalogger_command.request_create_station_id == request_create_station_id)
        if logger_type:
            conditions &= (db.request_create_station_datalogger_command.type_logger == logger_type)

        list_data = db(conditions).select(db.request_create_station_datalogger_command.ALL,
                                          limitby=limitby,
                                          orderby=~db.request_create_station_datalogger_command.id)
        iTotalRecords = db(conditions).count()
        rowsKind = db(db.request_create_station_datalogger_command.id > 0).select()
        resKind = {}
        for item in rowsKind:
            resKind[str(item.id)] = item.id
        iRow = iDisplayStart + 1
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


@service.json
def link_indicator_to_request_create_station(*args, **kwargs):
    try:
        request_create_station_id = request.vars.request_create_station_id
        indicator_id = request.vars.indicator
        station_name = request.vars.station_name
        qcvn_id = request.vars.qcvn_id
        qcvn_code = request.vars.qcvn_code if qcvn_id else ''
        qcvn_kind_id = request.vars.qcvn_kind_id
        qcvn_detail_type_code = request.vars.qcvn_detail_type_code
        qcvn_detail_const_area_value_1 = request.vars.qcvn_detail_const_area_value_1
        qcvn_detail_const_area_value_2 = request.vars.qcvn_detail_const_area_value_2
        qcvn_detail_const_area_value_3 = request.vars.qcvn_detail_const_area_value_3
        indicator_name_mapping = request.vars.indicator_name_mapping

        indicator = db.indicators(indicator_id) or None
        request_create_station = db.request_create_stations(request_create_station_id) or None
        qcvn_detail = get_qcvn_detail_by_indicator_and_qcvn(indicator_id, qcvn_id, qcvn_kind_id)
        if not request_create_station:
            return dict(success=False, message=T('Station does not exist!'))
        station_type = request_create_station.station_type or const.STATION_TYPE['WASTE_WATER']['value']
        if not indicator:
            return dict(success=False, message=T('Indicator does not exist!'))
        unit = indicator.unit
        conditions = ((db.request_create_station_indicator.request_create_station_id == request_create_station_id) &
                      (db.request_create_station_indicator.indicator_id == indicator_id) &
                      (db.request_create_station_indicator.status == const.SI_STATUS['IN_USE']['value']) &
                      (db.request_create_station_indicator.station_type == station_type))
        existed = db(conditions).count(db.request_create_station_indicator.id)
        if existed:
            return dict(success=False, message=T('Indicator is existed!'))
        qcvn_min, qcvn_max = get_station_indicator_min_max_value(
            qcvn_detail, qcvn_detail_const_area_value_1, qcvn_detail_const_area_value_2,
            qcvn_detail_const_area_value_3)

        db.request_create_station_indicator.update_or_insert(
            (db.request_create_station_indicator.request_create_station_id == request_create_station_id) & (db.request_create_station_indicator.indicator_id == indicator_id),
            request_create_station_id=request_create_station_id, station_name=station_name,
            station_type=station_type,
            indicator_id=indicator_id,
            unit=unit, qcvn_id=qcvn_id,
            qcvn_code=qcvn_code,
            status=const.SI_STATUS['IN_USE']['value'],
            qcvn_detail_type_code=qcvn_detail_type_code,
            qcvn_detail_min_value=qcvn_min,
            qcvn_detail_max_value=qcvn_max,
            qcvn_kind_id=qcvn_kind_id,
            mapping_name=indicator_name_mapping,
        )

        db.request_create_station_qcvn_station_kind.update_or_insert(
            (db.request_create_station_qcvn_station_kind.request_create_station_id == request_create_station_id) & (db.request_create_station_qcvn_station_kind.qcvn_id == qcvn_id) & (
                        db.request_create_station_qcvn_station_kind.qcvn_kind_id == qcvn_kind_id),
            request_create_station_id=request_create_station_id, station_name=station_name, qcvn_id=qcvn_id,
            station_type=station_type,
            qcvn_kind_id=qcvn_kind_id,
            qcvn_detail_const_area_value_1=qcvn_detail_const_area_value_1,
            qcvn_detail_const_area_value_2=qcvn_detail_const_area_value_2,
            qcvn_detail_const_area_value_3=qcvn_detail_const_area_value_3,
        )

        # # update history
        # db.manager_stations_history.insert(station_id=request_create_station_id,
        #                                    action='Update',
        #                                    username=current_user.fullname or None,
        #                                    description='Them_Thong_So',
        #                                    update_time=datetime.now())
        ###
        return dict(success=True)
    except Exception as ex:
        return dict(success=False, message=str(ex))

@service.json
def elink_indicator_to_request_create_station(*args, **kwargs):
    try:
        request_create_station_id = request.vars.request_create_station_id
        indicator_id = request.vars.indicator_id
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
        request_create_station = db.request_create_stations(request_create_station_id) or None
        qcvn_detail = get_qcvn_detail_by_indicator_and_qcvn(indicator_id, qcvn_id, qcvn_kind_id)
        if not request_create_station:
            return dict(success=False, message=T('request_create_station does not exist!'))
        station_type = request_create_station.station_type or const.STATION_TYPE['WASTE_WATER']['value']
        if not indicator:
            return dict(success=False, message=T('Indicator does not exist!'))
        unit = indicator.unit
        conditions = ((db.request_create_station_indicator.request_create_station_id == request_create_station_id) &
                      (db.request_create_station_indicator.indicator_id == indicator_id) &
                      (db.request_create_station_indicator.status == const.SI_STATUS['IN_USE']['value']) &
                      (db.request_create_station_indicator.station_type == station_type))
        qcvn_min, qcvn_max = get_station_indicator_min_max_value(
            qcvn_detail, qcvn_detail_const_area_value_1, qcvn_detail_const_area_value_2,
            qcvn_detail_const_area_value_3)

        db.request_create_station_indicator.update_or_insert(
            (db.request_create_station_indicator.id == station_indicator_id),
            request_create_station_id=request_create_station_id, station_name=station_name,
            station_type=station_type,
            indicator_id=indicator_id,
            unit=unit, qcvn_id=qcvn_id,
            qcvn_code=qcvn_code,
            status=const.SI_STATUS['IN_USE']['value'],
            qcvn_detail_type_code=qcvn_detail_type_code,
            qcvn_detail_min_value=qcvn_min,
            qcvn_detail_max_value=qcvn_max,
            qcvn_kind_id=qcvn_kind_id,
            mapping_name=indicator_name_mapping,
        )

        db.request_create_station_qcvn_station_kind.update_or_insert(
            (db.request_create_station_qcvn_station_kind.request_create_station_id == request_create_station_id) & (db.request_create_station_qcvn_station_kind.qcvn_id == qcvn_id) & (
                        db.request_create_station_qcvn_station_kind.qcvn_kind_id == qcvn_kind_id),
            request_create_station_id=request_create_station_id, station_name=station_name, qcvn_id=qcvn_id,
            station_type=station_type,
            qcvn_kind_id=qcvn_kind_id,
            qcvn_detail_const_area_value_1=qcvn_detail_const_area_value_1,
            qcvn_detail_const_area_value_2=qcvn_detail_const_area_value_2,
            qcvn_detail_const_area_value_3=qcvn_detail_const_area_value_3,
        )

        # # update history
        # db.manager_stations_history.insert(station_id=request_create_station_id,
        #                                    action='Update',
        #                                    username=current_user.fullname or None,
        #                                    description='Them_Thong_So',
        #                                    update_time=datetime.now())
        ###
        return dict(success=True)
    except Exception as ex:
        return dict(success=False, message=str(ex))

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

def get_station_indicator_min_max_value(qcvn_detail,
                                        qcvn_detail_const_area_value_1,
                                        qcvn_detail_const_area_value_2, qcvn_detail_const_area_value_3):
    qcvn_min_value_indicator = qcvn_max_value_indicator = None
    if qcvn_detail is None:
        return qcvn_min_value_indicator, qcvn_max_value_indicator
    if qcvn_detail.have_factor_qcvn == 1:
        if qcvn_detail.qcvn_min_value:
            qcvn_min_value_indicator = float(qcvn_detail.qcvn_min_value) * float(
                qcvn_detail_const_area_value_1) * float(qcvn_detail_const_area_value_2) * float(qcvn_detail_const_area_value_3)
        if qcvn_detail.qcvn_max_value:
            qcvn_max_value_indicator = float(qcvn_detail.qcvn_max_value) * float(
                qcvn_detail_const_area_value_1) * float(qcvn_detail_const_area_value_2)* float(qcvn_detail_const_area_value_3)
    else:
        if qcvn_detail.qcvn_min_value:
            qcvn_min_value_indicator = float(qcvn_detail.qcvn_min_value)
        if qcvn_detail.qcvn_max_value:
            qcvn_max_value_indicator = float(qcvn_detail.qcvn_max_value)

    return qcvn_min_value_indicator, qcvn_max_value_indicator

@service.json
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
    try:
        record = db.request_create_station_send_data(request.args(0)) or None
        request_create_station_id = request.vars.request_create_station_id
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

        count = db(db.request_create_station_send_data.request_create_station_id == request_create_station_id).count()
        if count:
            db(db.request_create_station_send_data.request_create_station_id == request_create_station_id). \
                update(status=status, time_send_data=time_send_data, from_date=from_date, file_format=file_format,
                       file_name=file_name, ftp_path=ftp_path, ftp_ip=ftp_ip, ftp_port=ftp_port, ftp_user=ftp_user,
                       ftp_password=ftp_password)
            db(db.request_create_stations.id == request_create_station_id).update(ftp_connection_status=res)
        else:
            db.request_create_station_send_data.insert(request_create_station_id=request_create_station_id, status=status, time_send_data=time_send_data,
                                         from_date=from_date, file_format=file_format, file_name=file_name,
                                         ftp_path=ftp_path, ftp_ip=ftp_ip, ftp_port=ftp_port, ftp_user=ftp_user,
                                         ftp_password=ftp_password)
            db(db.request_create_stations.id == request_create_station_id).update(ftp_connection_status=res)
        # update history
        # db.manager_stations_history.insert(station_id=request_create_station_id,
        #                                    action='Update',
        #                                    username=current_user.fullname or None,
        #                                    description='Thay_doi_noi_dung_truyen_du_lieu',
        #                                    update_time=datetime.now())
        ###
        return dict(success=True, res=res)
    except Exception as ex:
        return dict(success=False, message=str(ex), res=res)

@service.json
def ajax_save_auto_adjust(*args, **kwargs):
    try:
        import json
        data = request.vars.data
        data = json.loads(data)

        for request_create_station_indicator_id in data:
            db(db.request_create_station_indicator.id == request_create_station_indicator_id).update(**data[request_create_station_indicator_id])

        return dict(success=True)
    except Exception as ex:
        return dict(message=str(ex), success=False)


@service.json
def ajax_save_station_alarm(*args, **kwargs):
    try:
        request_create_station_id = request.vars.request_create_station_id
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
        exceed_emails_header = request.vars.exceed_emails_header
        frequency_notify = request.vars.frequency_notify

        # Check if record existed
        count = db(db.request_create_station_alarm.request_create_station_id == request_create_station_id).count()
        if count:
            db(db.request_create_station_alarm.request_create_station_id == request_create_station_id).update(
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
                exceed_emails_header=exceed_emails_header,

            )

        else:
            db.request_create_station_alarm.insert(
                request_create_station_id=request_create_station_id,
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
                exceed_emails_header=exceed_emails_header,
            )
        if frequency_notify:
            db(db.request_create_station_alarm.request_create_station_id == request_create_station_id).update(frequency_notify=frequency_notify)

        # update history
        # db.manager_stations_history.insert(station_id=request_create_station_id,
        #                                    action='Update',
        #                                    username=current_user.fullname or None,
        #                                    description='Thay_doi_canh_bao',
        #                                    update_time=datetime.now())
        ###
        return dict(success=True)
    except Exception as ex:
        return dict(success=False, message=str(ex))


def ftp_viewer():
    request_create_station_id = request.args(0)
    item = db.request_create_stations(request_create_station_id) or None
    station_name = ''
    data_folder = ''
    if item:
        station_name = item.station_name
        data_folder = item.data_folder
    return dict(request_create_station_id=request_create_station_id, station_name=station_name, data_folder=data_folder)


def read_file(data_folder_current, filename, is_get_realtime, station_id):
    from StringIO import StringIO
    import ftplib

    print
    "data_folder_current = ", data_folder_current
    stations = db(db.request_create_stations.id == station_id).select()
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
                print
                "data_folder_current = ", data_folder_current
                print
                "ftp_for_read_realtime.cwd(data_folder_current): start ..."
                ftp_for_read_realtime.cwd(data_folder_current)
                ftp_for_read_realtime.encoding = 'utf-8'
                ftp_for_read_realtime.sendcmd('OPTS UTF8 ON')
                print
                "ftp_for_read_realtime.cwd(data_folder_current): ok"
            else:
                ftp_for_import = ftplib.FTP()
                ftp_for_import = ftplib.FTP(ftp_ip)
                ftp_for_import.connect(ftp_ip, ftp_port, 1500)
                ftp_for_import.login(ftp_user_name, ftp_password)
                print
                "data_folder_current = ", data_folder_current
                print
                "ftp_for_import.cwd(data_folder_current): start ..."
                ftp_for_import.cwd(data_folder_current)
                ftp_for_import.encoding = 'utf-8'
                ftp_for_import.sendcmd('OPTS UTF8 ON')
                print
                "ftp_for_import.cwd(data_folder_current): ok"
        except Exception as ex:
            if '{}'.format(ex.message).startswith('550 CWD'):
                time.sleep(0.5)
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

@service.json
def import_data_thongso_request_sync(*args, **kwargs):
    station_id = request.vars.station_id
    convert_rate = request.vars.convert_rate
    station_name = request.vars.station_name
    station_type = request.vars.station_type

    stations = db(db.request_create_stations.id == station_id).select()
    station = None
    day_calculator = None
    if stations:
        station = stations[0]
        ftp_last_file_name_string = ""
        if station.last_file_name:
            ftp_last_file_name_string = station.last_file_name.split("_")[-1]
            day_calculator = datetime.strptime(ftp_last_file_name_string[:8], "%Y%m%d").replace(hour=0, minute=0,
                                                                                                second=0)
        data_folder_current = get_data_folder_current(station.data_folder, station.path_format, day_calculator)
        lines = read_file(data_folder_current, station.last_file_name, False, station_id)

        data = dict()
        data_status = dict()
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

                source_name = items[0].replace('\x00', '').decode('utf-8', errors='ignore')
                indicators = db(db.indicators.source_name == str(source_name)).select()
                qcvn_code = 'Không chọn QCVN'
                qcvn_id = -999
                if indicators and len(indicators) > 0:
                    indicator = indicators[0]
                    status = const.SI_STATUS['NEED_UPDATE']['value']
                    db.request_create_station_indicator.update_or_insert(
                        (db.request_create_station_indicator.request_create_station_id == station_id) & (
                                    db.request_create_station_indicator.indicator_id == indicator.id),
                        request_create_station_id=station_id, station_name=station_name, station_type=station_type,
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
                # self.station_import_logger.error(
                #     'import-->Have error when call process data. Exception =   %s',
                #     ex.message)
        # End for line in lines.splitlines():

    return dict(success=True)


@service.json
def approve_request_create_station(*args, **kwargs):
    request_create_station_id_str = request.vars.request_create_station_id
    request_create_station_id = int(request_create_station_id_str)
    approve_action_str = request.vars.approve_action
    approve_action = int(approve_action_str)
    reason = request.vars.reason

    # validate
    if approve_action != const.APPROVE_ACTION and approve_action != const.REJECT_ACTION:
        return http_response.BadRequest.to_dict()
    request_create_station = db.request_create_stations(request_create_station_id) or None
    if not request_create_station:
        return http_response.BadRequest.to_dict()
    if request_create_station.approve_status != const.REQUEST_CREATE_STATION_WAITING_STATUS:
        if request_create_station.approve_status == const.REQUEST_CREATE_STATION_REJECTED_STATUS:
            return http_response.Response(
                code=400,
                message=T('Can not approve request create station in rejected status'),
                data=None
            ).to_dict()
        if request_create_station.approve_status == const.REQUEST_CREATE_STATION_APPROVED_STATUS:
            return http_response.Response(
                code=400,
                message=T('Can not approve request create station in approved status'),
                data=None
            ).to_dict()

    # update request create station
    if approve_action == const.REJECT_ACTION:
        request_create_station_service.RequestCreateStationService(db, T).handle_reject(request_create_station, reason)
    elif approve_action == const.APPROVE_ACTION:
        request_create_station_service.RequestCreateStationService(db, T).handle_approve(request_create_station, reason)
    return http_response.Response(
        code=200,
        message=T('Success'),
        data=None
    ).to_dict()

@service.json
def del_request_create_stations(*args, **kwargs):
    try:
        array_data = request.vars.ids
        list_ids = array_data.split(',')
        # update history
        # for id in list_ids:
        #     db(db.manager_stations.station_id == id).delete()
        #     station_name = db.stations(id).station_name
        #     db.manager_stations_history.insert(station_id=id,
        #                                        station_name=station_name,
        #                                        action='Delete',
        #                                        username=current_user.fullname or None,
        #                                        description='',
        #                                        update_time=datetime.now())
        ######
        db(db.request_create_stations.id.belongs(list_ids)).delete()
        return dict(success=True)
    except Exception as ex:
        return dict(success=False, message=str(ex))


