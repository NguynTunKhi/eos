# -*- coding: utf-8 -*-
###############################################################################
# Author :
# Date   :
#
# Description :
#
###############################################################################
import datetime
import ast
import requests
import json
import time
import random


# @auth.requires_membership('manager')
# @auth.requires_login()
# @decor.requires_permission()
@auth.requires(lambda: (auth.has_permission('create', 'camera') or auth.has_permission('edit', 'camera')))
def form():
    # If in Update mode, get equivallent record
    record = db.camera_links(request.args(0)) or None
    msg = ''

    frm = SQLFORM(db.camera_links, record, _method='POST', hideerror=True, showid=False, _id='frmMain')

    if frm.process(onvalidation=validate, detect_record_change=True, hideerror=True).accepted:
        session.flash = T('MSG_INFO_SAVE_SUCCESS')
        redirect(URL('index'))
    elif frm.record_changed:
        redirect(URL('home', 'error'))
    elif frm.errors:
        for item in frm.errors:
            msg += '%s: %s<br />' % (item, frm.errors[item])
    else:
        pass
        # response.flash = message.REQUEST_INPUT

    frm.custom.widget.camera_source['_maxlength'] = '128'
    frm.custom.widget.description['_style'] = "width:90%; resize:none"
    frm.custom.widget.description['_maxlength'] = '512'

    return dict(frm=frm, msg=XML(msg))


################################################################################
def validate(frm):
    # Check condion
    # Get control value by : frm.vars.ControlName
    # If validate fail : frm.errors.ControlName = some message
    pass


def call():
    return service()


################################################################################
# @decor.requires_login()
@auth.requires(lambda: (auth.has_permission('view', 'camera')))
def index():
    # stations = db(db.stations.id > 0).select(db.stations.id, db.stations.station_name) #hungdx comment issue 44
    # hungdx phan quyen quan ly trạm theo user issue 44
    conditions = (db.stations.id > 0)
    if current_user:
        if not (auth.has_membership('admin') or auth.has_membership(const.GROUP_MANAGER)):
            list_station_manager = db(db.manager_stations.user_id == current_user.id).select(
                db.manager_stations.station_id)
            station_ids = [str(item.station_id) for item in list_station_manager]
            conditions &= (db.stations.id.belongs(station_ids))
    stations = db(conditions).select(db.stations.id, db.stations.station_name)

    return dict(stations=stations)


#################################################################################
def replace_all(text, dic):
    for i, j in dic.iteritems():
        text = text.replace(i, j)
    return text


##################################################################################
def get_token_with():
    row = db(db.camera_tokens.id > 0).select(db.camera_tokens.ALL).first()
    if not row:
        return None
    iplocal = row['iplocal']
    last_time_access = row['last_time_access']
    last_time_refresh = row['last_time_refresh']
    access_token_expires = row['access_token_expires']
    refresh_token_expires = row['refresh_token_expires']
    access_token = row['access_token']
    refresh_token = row['refresh_token']
    username = row['username']

    if last_time_access and last_time_refresh:
        now = datetime.datetime.utcnow()
        if last_time_access + datetime.timedelta(seconds=access_token_expires - (60 * 60)) > now:
            return access_token
        else:
            if last_time_refresh + datetime.timedelta(seconds=refresh_token_expires - (60 * 15)) > now:
                req = requests.get('{}/zm/api/host/login.json?token={}'.format(iplocal, refresh_token), verify=False, timeout=5)
                content = req.content
                dic = ast.literal_eval(content)
                db(db.camera_tokens.username == username).update(
                    last_time_access=now,
                    access_token_expires=dic['access_token_expires'],
                    access_token=dic['access_token']
                )
                return dic['access_token']
    try:
        username = row['username']
        password = row['password']
        req = requests.get('{}/zm/api/host/login.json?user={}&pass={}'.format(iplocal, username, password),
                           verify=False)
        content = req.content
        dic = ast.literal_eval(content)
        if not dic['access_token']:
            return None
        now = datetime.datetime.utcnow()
        db(db.camera_tokens.username == username).update(
            last_time_access=now,
            last_time_refresh=now,
            access_token_expires=dic['access_token_expires'],
            refresh_token_expires=dic['refresh_token_expires'],
            access_token=dic['access_token'],
            refresh_token=dic['refresh_token']
        )
        return dic['access_token']
    except Exception as ex:
        return dict(message=str(ex), success=False)


# ################################################################################
# @service.json
# @auth.requires(lambda: (auth.has_permission('view', 'camera')))
# def search_camera(*args, **kwargs):
#     try:
#         page = request.vars.page
#         try:
#             page = int(page)
#         except:
#             page = 1
#         num_on_page = 20
#         station_type = request.vars.type
#         station_id = request.vars.station_id
#         # Search conditions
#         conditions = (db.camera_links.is_visible == True)
#         if station_type:
#             conditions &= (db.camera_links.station_type == station_type)
#         if station_id:
#             conditions &= (db.camera_links.station_id == station_id)
#
#         if current_user:
#             if not (auth.has_membership('admin') or auth.has_membership(const.GROUP_MANAGER)):
#                 list_station_manager = db(db.manager_stations.user_id == current_user.id).select(
#                     db.manager_stations.station_id)
#                 station_ids = [str(item.station_id) for item in list_station_manager]
#                 conditions &= (db.camera_links.station_id.belongs(station_ids))
#
#         limitby = ((page - 1) * num_on_page, num_on_page + 1)
#         cameras = db(conditions).select(db.camera_links.id,
#                                         db.camera_links.camera_id,
#                                         db.camera_links.station_id,
#                                         db.camera_links.camera_source,
#                                         db.camera_links.camera_source_zm,
#                                         db.camera_links.station_name,
#                                         db.camera_links.description,
#                                         orderby=db.camera_links.order_no,
#                                         limitby=limitby)
#         total = db(conditions).count(db.camera_links.id)
#         total_page = total / num_on_page
#         if total > total_page * num_on_page:
#             total_page += 1
#         html = ''
#         access_token = None
#         for i in cameras:
#             if not access_token:
#                 access_token = get_token_with()
#             camera_source = str(i.camera_source_zm)
#             description = i.description
#             id = i.id
#             station_name = i.station_name
#             camera_id = i.camera_id
#             station_id = i.station_id
#
#             if not access_token:
#                 continue
#             camera_source = "{}&token={}".format(camera_source, access_token)
#             item = " \
#                                 <div class='item col-sm-3' style = 'padding:0px'> \
#                                     <div class = 'camera' > \
#                                         <a> \
#                                             <img id='camera_links_%s' class='bg-video1' src='%s'></img> \
#                                         </a> \
#                                     </div> \
#                                     <div class= 'title_camera' style = 'background-color: black'> \
#                                         <span class='camera_title'> \
#                                         <img class = 'camera_img' src='/eos/static/images/icons8-video-camera-152.png' style = 'margin-right:10px'><span style = 'color:white' class = 'setup' >%s</span></img> \
#                                                         <div class = 'myOption' id = 'options_%s'  style = 'text-align:right;display:none'> \
#                                                                     <select name='forma' onchange = 'test(this)'> \
#                                                                         <option value='' selected disabled hidden>Tùy chọn</option> \
#                                                                         <option class = 'camera_option' id = '0'  value = %s >Ghi hình</option> \
#                                                                         <option class = 'camera_option' id = '1'  value = history/%s > Video đã lưu </option> \
#                                                                     </select> \
#                                                             </div> \
#                                         <button onclick = 'showOptions(%s)'  class = 'camera_setting' ><i class='fa fa-cog' aria-hidden='true' style = 'color: white'></i></button> \
#                                         </span> \
#                                     </div> \
#                                 </div> \
#                              "
#             des = ' ' + description if description else ''
#             html += item % (id, camera_source, station_name + des ,camera_id ,camera_id,  camera_id , camera_id)
#
#         next_page = page
#         if page < total_page:
#             next_page = page + 1
#             html += "<div class='text-center' style='clear: both;'><a class='btn btn-primary btnShowMore'><i class='fa fa-more'></i>&nbsp;%s</div>" % (
#                 str(T('Show more...')));
#
#         return dict(success=True, html=html, next_page=next_page)
#     except Exception as ex:
#         return dict(message=str(ex), success=False)


################################################################################
@service.json
@auth.requires(lambda: (auth.has_permission('view', 'camera')))
def search_camera(*args, **kwargs):
    try:
        page = request.vars.page
        try:
            page = int(page)
        except:
            page = 1
        num_on_page = 20
        station_type = request.vars.type
        station_id = request.vars.station_id
        # Search conditions
        conditions = (db.camera_links.is_visible == True)
        if station_type:
            conditions &= (db.camera_links.station_type == station_type)
        if station_id:
            conditions &= (db.camera_links.station_id == station_id)

        if current_user:
            if not (auth.has_membership('admin') or auth.has_membership(const.GROUP_MANAGER)):
                list_station_manager = db(db.manager_stations.user_id == current_user.id).select(
                    db.manager_stations.station_id)
                station_ids = [str(item.station_id) for item in list_station_manager]
                conditions &= (db.camera_links.station_id.belongs(station_ids))

        limitby = ((page - 1) * num_on_page, num_on_page + 1)
        cameras = db(conditions).select(db.camera_links.id,
                                        db.camera_links.camera_id,
                                        db.camera_links.station_id,
                                        db.camera_links.camera_source,
                                        db.camera_links.camera_source_zm,
                                        db.camera_links.station_name,
                                        db.camera_links.description,
                                        orderby=db.camera_links.order_no,
                                        limitby=limitby)
        total = db(conditions).count(db.camera_links.id)
        total_page = total / num_on_page
        if total > total_page * num_on_page:
            total_page += 1
        html = ''
        access_token = None
        if not access_token:
            access_token = get_token_with()
        row = db(db.camera_tokens.id > 0).select(db.camera_tokens.ALL).first()
        iplocal = row['iplocal']
        list_camera = requests.get('{}/zm/api/{}?token={}'.format(iplocal, 'monitors.json', access_token), verify=False)
        content = list_camera.content
        dic = json.loads(content)['monitors']
        status_camera = dict()
        for idx in dic:
            idx_camera = idx['Monitor_Status']['MonitorId'].encode("utf-8")
            sts_camera = idx['Monitor_Status']['Status'].encode("utf-8")
            status_camera[idx_camera] = sts_camera
        for i in cameras:
            camera_source = str(i.camera_source_zm)
            description = i.description
            id = i.id
            station_name = i.station_name
            camera_id = i.camera_id
            if status_camera.has_key(str(camera_id)):
                status = status_camera[str(camera_id)]
            camera_source = "{}&token={}".format(camera_source, access_token)
            if status == 'Connected':
                item = " \
                                    <div class='item col-sm-3' style = 'padding:0px'> \
                                        <div class = 'camera' > \
                                            <a> \
                                                <img id='camera_links_%s' class='bg-video1' src='%s'></img> \
                                            </a> \
                                        </div> \
                                        <div class= 'title_camera' style = 'background-color: black'> \
                                            <span class='camera_title'> \
                                            <img class = 'camera_img' src='/eos/static/images/icons8-video-camera-152.png' style = 'margin-right:10px'><span style = 'color:white' class = 'setup' >%s</span></img> \
                                                            <div class = 'myOption' id = 'options_%s'  style = 'text-align:right;display:none'> \
                                                                <div class='dropdown-content'> \
                                                                    <a  data-url='/eos/camera_links/popup_record_camera?station_id=%s' class='btnAddNew' data-for='#hfCameraId' >%s</a> \
                                                                    <a onclick=changeCamera(%s)>%s</a> \
                                                                    <a  href = '/eos/camera_links/history/%s'>%s</a> \
                                                                </div>\
                                                            </div> \
                                            <button onclick = 'showOptions(%s)'  class = 'camera_setting' ><i class='fa fa-cog' aria-hidden='true' style = 'color: white'></i></button> \
                                            </span> \
                                        </div> \
                                    </div> \
                                 "
                des = ' ' + description if description else ''
                html += item % (
                id, camera_source, station_name + des, camera_id, camera_id,T('Camera Record'), camera_id,T('Auto Record'), camera_id, T('Camera History'),camera_id)
            else:
                item = " \
                                                    <div class='item col-sm-3' style = 'padding:0px'> \
                                                        <div class = 'camera' > \
                                                            <a> \
                                                                <img id='camera_links_%s' class='bg-video1' src='%s'></img> \
                                                            </a> \
                                                        </div> \
                                                        <div class= 'title_camera' style = 'background-color: black'> \
                                                            <span class='camera_title'> \
                                                            <img class = 'camera_img' src='/eos/static/images/icons8-video-camera-152.png' style = 'margin-right:10px'><span style = 'color:white' class = 'setup' >%s</span></img> \
                                                            <div class = 'myOption' id = 'options_%s'  style = 'text-align:right;display:none'> \
                                                                <div class='dropdown-content'> \
                                                                    <a  data-url='/eos/camera_links/popup_record_camera?station_id=%s' class='btnAddNew' data-for='#hfCameraId' >%s</a> \
                                                                    <a onclick=changeCamera(%s)>%s</a> \
                                                                    <a href = '/eos/camera_links/history/%s'>%s</a> \
                                                                </div>\
                                                            </div> \
                                                            <button onclick = 'showOptions(%s)'  class = 'camera_setting' ><i class='fa fa-cog' aria-hidden='true' style = 'color: white'></i></button> \
                                                            </span> \
                                                        </div> \
                                                    </div> \
                                                 "
                des = ' ' + description if description else ''
                html += item % (id, '/eos/static/images/video_error.png', station_name + des , camera_id,camera_id,T('Camera Record'),camera_id, T('Auto Record'),camera_id,T('Camera History'),camera_id)

        next_page = page
        if page < total_page:
            next_page = page + 1
            html += "<div class='text-center' style='clear: both;'><a class='btn btn-primary btnShowMore'><i class='fa fa-more'></i>&nbsp;%s</div>" % (
                str(T('Show more...')));

        return dict(success=True, html=html, next_page=next_page)
    except Exception as ex:
        return dict(message=str(ex), success=False)

################################################################################


@service.json
@auth.requires(lambda: (auth.has_permission('view', 'camera')))
def get_list_camera_by_station(*args, **kwargs):
    import requests
    try:
        station_id = request.vars.station_id
        name = request.vars.name
        station_type = request.vars.type
        aaData = []

        conditions = (db.camera_links.station_id == station_id)
        list_data = db(conditions).select(db.camera_links.id,
                                          db.camera_links.camera_source,
                                          db.camera_links.station_name,
                                          db.camera_links.camera_id,
                                          db.camera_links.is_visible,
                                          db.camera_links.order_no,
                                          db.camera_links.description)
        list_id = db(conditions).select(db.camera_links.camera_id)
        list_all_camera = db().select(db.camera_links.camera_id)
        list_all_camera_id = []
        for i in list_all_camera:
            id = i.camera_id
            list_all_camera_id.append(id)
        if list_all_camera_id:
            max_all_camera_id = max(list_all_camera_id)
        list = []
        if list_id:
            for i in list_id:
                i = i['camera_id']
                list.append(i)
            x = max(list)
        iTotalRecords = len(list_data)
        row = db(db.camera_tokens.id > 0).select(db.camera_tokens.ALL).first()
        access_token = None
        if not access_token:
            access_token = get_token_with()
        url_camera = row['url']
        iplocal = row['iplocal']
        try:
            list_camera = requests.get('{}/zm/api/{}?token={}'.format(iplocal, 'monitors.json', access_token), verify=False, timeout=5)
            content = list_camera.content
            dic = json.loads(content)
            try:
                a = dic['monitors']
            except:
                a = None
            if a:
                list_camera_id = []
                for j in a:
                    b = j['Monitor_Status']['MonitorId']
                    if b:
                        c = b.encode("utf-8")
                        d = int(c)
                        list_camera_id.append(d)
                id_max = max(list_camera_id)
        except:
            pass
        camera_port = random.randint(30000, 30200)
        # Duyet tung phan tu trong mang du lieu vua truy van duoc
        for i, item in enumerate(list_data):
            url = URL('camera_links', 'popup_add_camera', args=[item.id],
                      vars={'station_id': station_id, 'type': station_type, 'name': name})
            if item.camera_id == 0:
                camera_name = item.description
                station_name = item.station_name
                d = {"à": "a", "á": "a", "ạ": "a", "ả": "a", "ã": "a", "â": "a", "ầ": "a", "ấ": "a", "ậ": "a", "ẩ": "a",
                     "ẫ": "a", "ă": "a", "ằ": "a", "ắ": "a", "ặ": "a", "ẳ": "a", "ẵ": "a",
                     "è": "e", "é": "e", "ẻ": "e", "ẹ": "e", "ẽ": "e", "ê": "e", "ề": "e", "ế": "e", "ệ": "e", "ể": "e",
                     "ễ": "e",
                     "ò": "o", "ó": "o", "ọ": "o", "ỏ": "o", "õ": "o", "ô": "o", "ồ": "o", "ố": "o", "ộ": "o", "ổ": "o",
                     "ỗ": "o", "ơ": "o", "ờ": "o", "ớ": "o", "ợ": "o", "ở": "o", "ỡ": "o",
                     "í": "i", "ì": "i", "ĩ": "i", "ỉ": "i", "ị" : "i",
                     "ủ": "u", "ù": "u", "ú": "u", "ụ": "u", "ũ": "u", "ứ": "u", "ừ": "u", "ử": "u", "ự": "u", "ữ": "u",
                     "ư": "u",
                     "ý": "y", "ỳ": "y", "ỷ": "y", "ỹ": "y", "ỵ": "y",
                     "đ": "d",
                     "Ấ": "A", "Ầ": "A", "Ẩ": "A", "Ẫ": "A", "Ậ": "A", "Â": "A", "Á": "", "À": "A", "Ã": "A", "Ạ": "A",
                     "Ả": "A", "Ắ": "A", "Ằ": "A", "Ẳ": "A", "Ặ": "A", "Ẵ": "A", "Ă": "A",
                     "Ò": "O", "Ó": "O", "Ỏ": "O", "Õ": "O", "Ọ": "O", "Ớ": "O", "Ờ": "O", "Ỡ": "O", "Ơ": "O", "Ợ": "O",
                     "Ở": "O", "Ố": "O", "Ồ": "O", "Ổ": "O", "Ỗ": "O", "Ộ": "O", "Ô": "O",
                     "É": "E", "È": "E", "Ẻ": "E", "Ẽ": "E", "Ẹ": "E", "Ế": "E", "Ề": "E", "Ể": "E", "Ệ": "E", "Ễ": "E",
                     "Ê": "E",
                     "Í": "I", "Ì": "I", "Ỉ": "I", "Ĩ": "I", "Ị": "I",
                     "Ú": "U", "Ù": "U", "Ủ": "U", "Ũ": "U", "Ụ": "U", "Ư": "U", "Ứ": "U", "Ừ": "U", "Ử": "U", "Ữ": "U",
                     "Ự": "U",
                     "Ý": "Y", "Ỳ": "Y", "Ỷ": "Y", "Ỵ": "Y", "Ỹ": "Y",
                     "Đ": "D",
                     }
                camera_name = replace_all(camera_name, d)
                camera_name = camera_name.upper()
                station_name = replace_all(station_name, d)
                station_name = station_name.upper()
                if max_all_camera_id > id_max:
                    continue
                else:
                    payload = {'Monitor[Name]': station_name + '-' + camera_name,
                               'Monitor[Function]': 'Nodect',
                               'Monitor[Path]': item.camera_source,
                               'Monitor[Width]': '1280',
                               'Monitor[Height]': '720',
                               'Monitor[Type]': 'Ffmpeg',
                               'Monitor[Colours]': '4',
                               'Monitor[Method]': 'Nodect',
                               'Monitor[Id]': id_max + 1,
                               'token': access_token}
                    url_post = "{host}/zm/api/monitors.json".format(host=iplocal)
                    post_api_create_camera = requests.post(url_post, data=payload, verify=False, timeout=5)

                    source_url = '{host}:{port}/cgi-bin-zm/nph-zms?scale=auto&mode=jpeg&maxfps=100&monitor={id}' #cu
                    #source_url = '{host}:{port}/zm/cgi-bin/nph-zms?scale=auto&mode=jpeg&maxfps=100&monitor={id}'  # moi
                    source_zm = source_url.format(host=url_camera, port=camera_port, id=id_max + 1)
                    db(db.camera_links.camera_id == 0).update(
                        camera_id=id_max + 1,
                        camera_source_zm=source_zm
                    )
            aaData.append([
                str(i + 1),
                I(_class='fa fa-eye') if item.is_visible else I(_class='fa fa-eye-slash'),
                item.description,
                item.camera_source,
                item.order_no,
                "%s%s%s%s%s" % ( \
                    "<a href='javascript: void(0);' class='btnAddNew' title='{{=T('Camera information')}}' \
                        data-for='#hfEquipmentId'  data-callback='reloadDatatable_Camera()' \
                        data-url='", url, "'> ",
                    I(_class='fa fa-edit'),
                    "</a>"),
                INPUT(_group='3', _class='select_item', _type='checkbox', _value=item.id),
                item.id
            ])

        return dict(iTotalRecords=iTotalRecords, iTotalDisplayRecords=iTotalRecords, aaData=aaData, success=True)
    except Exception, ex:
        return dict(iTotalRecords=0, iTotalDisplayRecords=0, aaData=[], message=str(ex), success=False)


################################################################################
# # @decor.requires_login()
# @decor.requires_permission('eos|areas|form')
@auth.requires(lambda: (auth.has_permission('view', 'camera')))
def popup_add_camera():
    record = db.camera_links(request.args(0)) or None
    station_id = request.vars.station_id
    station_type = request.vars.type
    name = request.vars.name

    frm = SQLFORM(db.camera_links, record, _method='POST', hideerror=True, showid=False)
    # frm.custom.widget.description['_rows'] = '2'

    return dict(frm=frm, station_id=station_id, type=station_type, name=name)
#################################################################
@auth.requires(lambda: (auth.has_permission('view', 'camera')))
def popup_record_camera():
    record = db.camera_links(request.args(0)) or None
    station_id = request.vars.station_id
    station_type = request.vars.type
    name = request.vars.name

    frm = SQLFORM(db.camera_record, record, _method='POST', hideerror=True, showid=False)
    # frm.custom.widget.description['_rows'] = '2'

    return dict(frm=frm, station_id=station_id, type=station_type, name=name)

################################################################################
@service.json
# # @decor.requires_login()
# @decor.requires_permission('eos|areas|form')
@auth.requires(lambda: (auth.has_permission('create', 'camera') or auth.has_permission('edit', 'camera')))
def ajax_save_camera(*args, **kwargs):
    try:
        if not request.vars.is_visible: request.vars.is_visible = False

        if not request.vars.id:
            db.camera_links.insert(**dict(request.vars))
        else:
            db(db.camera_links.id == request.vars.id).update(**dict(request.vars))

        return dict(success=True)
    except Exception as ex:
        logger.error(str(ex))
        return dict(success=False, message=str(ex))


####################################################
@service.json
@auth.requires(lambda: (auth.has_permission('create', 'camera') or auth.has_permission('edit', 'camera')))
def ajax_save_content_record(*args, **kwargs):
    try:
        content = request.vars.content
        time = request.vars.time
        camera_id  = request.vars.station_id
        get_time = datetime.datetime.now()
        db.camera_record.insert(camera_id =camera_id,content = content,time = time,get_time=get_time,event_id = None)
        record()
        return dict(success=True,message=T('Record updated successful!'))
    except Exception as ex:
        logger.error(str(ex))
        return dict(success=False, message='Lỗi khi lưu.vui lòng kiểm tra lại các trường')

####################################################

def history():
    return dict(success=True)


#############################
@service.json
@auth.requires(lambda: (auth.has_permission('view', 'camera')))
def record(*args, **kwargs):
    try:
        id = request.vars.station_id
        time_record = int(request.vars.time)
        access_token = get_token_with()
        row_camera = db(db.camera_tokens.id > 0).select(db.camera_tokens.ALL).first()
        iplocal = row_camera['iplocal']
        row = db(db.camera_links.camera_id == id).select(db.camera_links.station_id)
        for i in row:
            station_id = i.station_id
        url_start = '{host}/zm/api/monitors/alarm/id:{id}/command:on.json?token={access_token}'.format(host=iplocal,
                                                                                                       id=id,
                                                                                                       access_token=access_token)
        url_stop = '{host}/zm/api/monitors/alarm/id:{id}/command:off.json?token={access_token}'.format(host=iplocal,
                                                                                                       id=id,
                                                                                                       access_token=access_token)

        row = db(db.camera_record.id > 0).select(orderby=~db.camera_record.get_time).first()
        record_start = requests.get(url_start, verify = False)
        respone = record_start.text
        dic = ast.literal_eval(respone)
        status = dic['status']
        arr = status.split(':')
        event_id = int(arr[1])
        db(db.camera_record.get_time == row['get_time']).update(event_id = event_id+1)
        time.sleep(time_record)
        record_stop = requests.get(url_stop, verify = False)
        return dict(success=True,message=T('Record updated successful!'))
    except Exception as ex:
        return dict(success=False, message=str(ex))


################################################################################
@service.json
@auth.requires(lambda: (auth.has_permission('view', 'camera')))
def history_camera(*args, **kwargs):
    try:
        page = request.vars.page
        try:
            page = int(page)
        except:
            page = 1
        a = request.env.http_referer
        list = a.split("/")
        id = list[6]
        # Search conditions
        conditions = (db.camera_links.camera_id == id)
        if current_user:
            if not (auth.has_membership('admin') or auth.has_membership(const.GROUP_MANAGER)):
                list_station_manager = db(db.manager_stations.user_id == current_user.id).select(
                    db.manager_stations.station_id)
                station_ids = [str(item.station_id) for item in list_station_manager]
                conditions &= (db.camera_links.station_id.belongs(station_ids))

        cameras = db(conditions).select(db.camera_links.id,
                                        db.camera_links.camera_id,
                                        db.camera_links.station_id,
                                        db.camera_links.camera_source,
                                        db.camera_links.camera_source_zm,
                                        db.camera_links.station_name,
                                        db.camera_links.description,
                                        orderby=db.camera_links.order_no,
                                        )

        html = ''
        data = db(conditions).select(db.camera_links.ALL)
        access_token = None
        for i in cameras:
            if not access_token:
                access_token = get_token_with()
            camera_source = str(i.camera_source_zm)
            description = i.description
            id = i.id
            station_name = i.station_name

            if not access_token:
                continue
            #### get event camera:
            row = db(db.camera_tokens.id > 0).select(db.camera_tokens.ALL).first()
            url = row['iplocal']
            list_camera = requests.get(
                '{}/zm/api/events/index/MonitorId:{}.json?token={}'.format(url, i.camera_id, access_token), verify=False, timeout=5)
            content = list_camera.content
            dic = json.loads(content)
            dic_event = dic['events']
            list_camera_id = []
            list_camera_time = []
            for i in dic_event:
                id_event_camera = i['Event']['Id']
                if id_event_camera:
                    id_event_camera_convert = id_event_camera.encode("utf-8")
                    camera_event = int(id_event_camera_convert)
                    list_camera_id.append(camera_event)
                time_event_camera = i['Event']['StartTime']
                if time_event_camera:
                    time_event_camera_convert = time_event_camera.encode("utf-8")
                    list_camera_time.append(time_event_camera_convert)
            list_camera_events = zip(list_camera_id, list_camera_time)
            camera_source = "{}&token={}".format(camera_source, access_token)
            item = " \
                                <div class='item col-sm-3> \
                                    <div > \
                                        <div class='panel-body bg-video1'> \
                                            <img id='camera_links_%s' class='bg-video1' src='%s'></img> \
                                        </div> \
                                        <div class='panel-footer'>%s</div> \
                                    </div> \
                                </div> \
                                <div><h2>Danh sách video đã lưu</h2></div>\
                             "
            des = ' ' + description if description else ''
            html += item % (id, camera_source, des)
            for list_camera_event in list_camera_events:
                id_event = list_camera_event[0]
                time_event = list_camera_event[1]
                row = db(db.camera_record.event_id == id_event).select(db.camera_record.ALL).first()
                if row:
                    content = row['content']
                else:
                    content = ''
                camera_source = '{host}/zm/index.php?eid={id}&fid=snapshot&view=image&token={access_token}'
                title1 = '{host}/zm/cgi-bin/nph-zms?mode=jpeg&scale=auto&maxfps=30&replay=none&source=event&event={id}&token={access_token}' #moi
                title1 = '{host}/cgi-bin-zm/nph-zms?mode=jpeg&scale=auto&maxfps=30&replay=none&source=event&event={id}&token={access_token}' #cu
                title = title1.format(host=url, id=id_event, access_token=access_token)
                camera_source1 = camera_source.format(host=url, id=id_event, access_token=access_token)
                item = " \
                                                <div class='item col-sm-3'> \
                                                    <div > \
                                                        <div class='panel-body bg-video1'> \
                                                            <img id='camera_links_%s' class='bg-video2' src='%s' title = '%s' ></img> \
                                                        </div> \
                                                        <div class='panel-footer'><div>Thời gian : %s</div><div>Nội dung : %s </div></div> \
                                                    </div> \
                                                </div> \
                                             "
                html += item % (id, camera_source1, title, time_event,content)

        return dict(success=True, html=html)
    except Exception as ex:
        return dict(message=str(ex), success=False)

################################################################################
#############################
@service.json
@auth.requires(lambda: (auth.has_permission('view', 'camera')))
def change(*args, **kwargs):
    try:
        id = request.vars.id
        row = db(db.camera_tokens.id > 0).select(db.camera_tokens.ALL).first()
        iplocal = row['iplocal']
        access_token = None
        if not access_token:
            access_token = get_token_with()
        payload = {'Monitor[Function]': 'Modect',
                   'token': access_token}
        url_post = "{host}/zm/api/monitors/{id}.json".format(host=iplocal, id=id)
        post_api_create_camera = requests.post(url_post, data=payload, verify=False, timeout=5)
        return dict(success=True)
    except Exception as ex:
        return dict(success=False, message=str(ex))


################################################################################