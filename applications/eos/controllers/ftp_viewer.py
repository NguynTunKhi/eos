# -*- coding: utf-8 -*-
###############################################################################
# Author :
# Date   :
#
# Description :
#
###############################################################################

import ftplib
from datetime import datetime, date
from cStringIO import StringIO
from applications.eos.repo.ftp_repo import FtpRepo
import socket
TIME_OUT = 15

FTP_VIEW_TYPE_DIR = 'directory'
FTP_VIEW_TYPE_FILE = 'file'
FORWARD_SLASH = "/"

def call():
    session.forget()
    response.headers["Access-Control-Allow-Origin"] = '*'
    response.headers['Access-Control-Max-Age'] = 86400
    response.headers['Access-Control-Allow-Headers'] = '*'
    response.headers['Access-Control-Allow-Methods'] = '*'
    response.headers['Access-Control-Allow-Credentials'] = 'true'
    return service()


class FileType:
    Directory = "d"
    File = "f"


def get_ftp_file(ftp_ip, ftp_port, usr, pwd, folder):
    try:
        message = None
        ls = []

        def to_file(f):
            arr = f.split(';')
            if arr[0] == 'type=file':
                ls.append([
                    I(_class='fa fa-file'),
                    arr[3].lstrip(),
                    '%s B' % arr[2].replace('size=', ''),
                    # arr[1].replace('modify=', '')
                    datetime.strptime(arr[1].replace('modify=', ''), '%Y%m%d%H%M%S').strftime('%Y-%m-%d %I:%M:%S %p')
                ])
            if arr[0] == 'type=dir':
                ls.append([
                    I(_class='fa fa-folder'),
                    A(arr[2].lstrip(), _onclick="go_to_folder('{}')".format(arr[2].lstrip())),
                    '',
                    datetime.strptime(arr[1].replace('modify=', ''), '%Y%m%d%H%M%S').strftime('%Y-%m-%d %I:%M:%S %p')
                    # arr[1].replace('modify=', '')  # datetime.strptime(arr[1].replace('modify=', ''), '%Y%m%d%H%M%S')
                ])

        def to_json_window_os(f):
            # format
            # file: 12-01-22  12:59AM                  351 BD_BAUB_NUOBBA_20221201000000.txt
            # folder: 12-01-22  11:00PM       <DIR>          01
            arr = f.split()

            datetime_format = "%m-%d-%y %H:%M%p"

            created_time_start_idx = 0
            created_time_end_idx = 2
            file_size_idx = 2
            file_type_idx = 2
            file_name_start_idx = 3

            created_time_str = " ".join(arr[created_time_start_idx:created_time_end_idx])
            created_time = datetime.strptime(created_time_str, datetime_format)

            file_name = " ".join(arr[file_name_start_idx:])

            file_name = file_name.lstrip()
            file_size = ""

            # take the first element of
            if arr[file_type_idx] == '<DIR>':  # directory
                file_type = FileType.Directory
            else:
                file_type = FileType.File
                file_size = arr[file_size_idx]

            if file_type == FileType.File or file_type == FileType.Directory:
                ls.append({'t': file_type, 'n': file_name,
                           's': file_size,
                           'ts': created_time})

        def to_json_other_os(f):
            # https://www.mkssoftware.com/docs/man1/ls.1.asp
            # folder format: drwxr-xr-x    3 ftp      ftp            96 Feb 18 11:24 hello
            # file format: -rw-r--r--    1 ftp      ftp             0 Feb 18 11:24 abc.txt
            # previous year: drwxr-xr-x  8 mfv-hn-computer-0015  staff   256 Aug 10  2022 transition_asset_demo
            # f = "drwxr-xr-x  8 mfv-hn-computer-0015  staff   256 Aug 10  2022 transition_asset_demo"
            arr = f.split()

            created_time_start_idx = 5
            created_time_end_idx = 8
            file_size_idx = 4
            file_type_idx = 0
            file_name_start_idx = 8

            # current year datetime format: Feb 18 11:24
            cur_year_date_fmt = "%Y %b %d %H:%M"
            previous_year_date_fmt = "%b %d %Y"

            file_name = " ".join(arr[file_name_start_idx:])
            created_time_str = " ".join(arr[created_time_start_idx:created_time_end_idx])

            if ":" in created_time_str:
                create_date_fmt = cur_year_date_fmt
                # adding current year
                created_time_str = str(date.today().year) + " " + created_time_str
            else:
                create_date_fmt = previous_year_date_fmt

            created_time = datetime.strptime(created_time_str, create_date_fmt)

            file_name = file_name.lstrip()
            file_size = ""

            # take the first element of
            if arr[file_type_idx][0] == 'd':  # directory
                file_type = FileType.Directory
            elif arr[file_type_idx][0] == "-":  # regular file
                file_type = FileType.File
                file_size = arr[file_size_idx]

            if file_type == FileType.File or file_type == FileType.Directory:
                ls.append({'t': file_type, 'n': file_name,
                           's': file_size,
                           'ts': created_time})

        ftp = ftplib.FTP()
        ftp.connect(ftp_ip, ftp_port, TIME_OUT)
        ftp.login(usr, pwd)
        ftp.encoding = 'utf-8'
        ftp.sendcmd('OPTS UTF8 ON')
        ftp.cwd(folder)

        os_system = ftp.sendcmd("SYST")
        if "windows" in os_system.lower():
            ftp.retrlines('LIST', to_json_window_os)
        else:
            ftp.retrlines('LIST', to_json_other_os)


    except Exception as ex:
        message = ex.message
    finally:
        ftp.quit()
    return ls, folder, message


@service.json
def get_list(*args, **kwargs):
    # ftp_ip = kwargs.get('ftp_ip', '')  # 'ftp.envisoft.gov.vn'
    # ftp_port = int(kwargs.get('ftp_port', '21'))
    # usr = kwargs.get('usr', '')
    # pwd = kwargs.get('pwd', '')  # 'hn_khi556@123'
    # folder = kwargs.get('folder', '')  # 'hn_khi556@123'
    station_id = kwargs.get('station_id')
    search = kwargs.get('vFolder', '')
    folder = kwargs.get('folder', '')
    station = db.stations(station_id)
    if station:
        ftp_ip = station.data_server
        ftp_port = station.data_server_port
        usr = station.username
        pwd = station.pwd
        if search == '':
            folder = station.data_folder
        else:
            if search == '..':
                folder = '/'.join(folder.split('/')[:-1])
            else:
                folder = os.path.join(folder, search)

        if len(folder) < len(station.data_folder):
            folder = station.data_folder
        ls, folder, message = get_ftp_file(ftp_ip, ftp_port, usr, pwd, folder)
        iTotalRecords = len(ls)
        return dict(success=False if message is None else True, data=ls, folder=folder,
                    iTotalRecords=iTotalRecords, iTotalDisplayRecords=iTotalRecords
                    )
    return dict(success=False, message='Kh�ng c� th�ng tin',
                # iTotalRecords=0, iTotalDisplayRecords=0,
                data=[])

@service.json
def get_list_for_request_create_station(*args, **kwargs):
    # ftp_ip = kwargs.get('ftp_ip', '')  # 'ftp.envisoft.gov.vn'
    # ftp_port = int(kwargs.get('ftp_port', '21'))
    # usr = kwargs.get('usr', '')
    # pwd = kwargs.get('pwd', '')  # 'hn_khi556@123'
    # folder = kwargs.get('folder', '')  # 'hn_khi556@123'
    request_create_station_id = kwargs.get('request_create_station_id')
    search = kwargs.get('vFolder', '')
    folder = kwargs.get('folder', '')
    request_create_station = db.request_create_stations(request_create_station_id)
    if request_create_station:
        ftp_ip = request_create_station.data_server
        ftp_port = request_create_station.data_server_port
        usr = request_create_station.username
        pwd = request_create_station.pwd
        if search == '':
            folder = request_create_station.data_folder
        else:
            if search == '..':
                folder = '/'.join(folder.split('/')[:-1])
            else:
                folder = os.path.join(folder, search)

        if len(folder) < len(request_create_station.data_folder):
            folder = request_create_station.data_folder
        ls, folder, message = get_ftp_file(ftp_ip, ftp_port, usr, pwd, folder)
        iTotalRecords = len(ls)
        return dict(success=False if message is None else True, data=ls, folder=folder,
                    iTotalRecords=iTotalRecords, iTotalDisplayRecords=iTotalRecords
                    )
    return dict(success=False, message='Kh�ng c� th�ng tin',
                # iTotalRecords=0, iTotalDisplayRecords=0,
                data=[])


@service.json
def download(*args, **kwargs):
    try:
        station_id = kwargs.get('station_id')
        folder = kwargs.get('folder', '')
        station = db.stations(station_id)
        filename = kwargs['filename']
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
        ftp.retrbinary('RETR %s' % filename, stringIO.write)
        val = stringIO.getvalue()
        stringIO.close()
        ftp.quit()
        response.headers['Content-Type'] = 'text/plain'
        response.headers['Content-Disposition'] = 'attachment;filename=%s' % filename
        return val
    except Exception as ex:
        return dict(success=False, message=ex.message)


@service.json
def download_1(*args, **kwargs):
    try:
        station_id = kwargs.get('station_id')
        folder = kwargs.get('folder', '')
        station = db.stations(station_id)
        filename = kwargs['filename']
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
        # file_stream = StringIO()
        _path = os.path.join(request.folder, 'static', 'export', filename)
        file_stream = open(_path, "wb")  # read file to send to byte
        ftp.retrbinary('RETR {}'.format(filename), file_stream.write)
        file_stream.close()
        response.headers['Content-Type'] = 'text/plain'
        response.headers['Content-Disposition'] = 'attachment;filename=%s' % filename
        data = open(_path, "rb").read()
        # ftp.storbinary("RETR " + filename, open(filename, 'wb').write)
        # response.headers['Content-Type'] = 'text/plain'
        response.headers['Content-Disposition'] = 'attachment;filename=%s' % filename
        # values = file_stream.getvalue()
        return data  # file_stream #values#response #.stream(file_stream)
    except Exception as ex:
        return dict(success=False, message=ex.message)


@service.json
def get_list_by_ftp_id(*args, **kwargs):
    ftp_id = request.vars.ftp_id
    view_type = request.vars.view_type
    search = kwargs.get('vFolder', '')
    folder = kwargs.get('folder', '')

    if ftp_id:
        ftp_repo = FtpRepo(db)
        ftp_info = ftp_repo.get_ftp_by_id(ftp_id)
        ftp_ip = ftp_info.ftp_ip
        ftp_port = ftp_info.ftp_port
        usr = ftp_info.ftp_user
        pwd = ftp_info.ftp_password
        if search == '':
            folder = FORWARD_SLASH
        else:
            if search == '..':
                folder = FORWARD_SLASH.join(folder.split(FORWARD_SLASH)[:-1])
            else:
                folder = os.path.join(folder, search)
        if folder == "":
            folder = FORWARD_SLASH
        ls, folder, message = get_ftp_file(ftp_ip, ftp_port, usr, pwd, folder)

        directory_filter = []
        for data in ls:
            data['file_path'] = os.path.join(folder, data['n'])
            data['file_name'] = data['n']
            data['view_type'] = view_type
            if data['t'] == FileType.Directory:
                directory_filter.append(data)

        if view_type == FTP_VIEW_TYPE_DIR:
            if len(directory_filter) == 0:
                message = "Không có thông tin"
            ls = directory_filter

        iTotalRecords = len(ls)
        return dict(success=False if message is None else True, data=ls, folder=folder,
                    iTotalRecords=iTotalRecords, iTotalDisplayRecords=iTotalRecords)

    return dict(success=False, message='Kh�ng c� th�ng tin', data=[])
