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


def get_token_with():
    row = db(db.camera_tokens.id > 0).select(db.camera_tokens.ALL).first()
    if not row:
        return None
    url = row['url']
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
                req = requests.get('{}?token={}'.format(url, refresh_token), verify=False)
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
        req = requests.get('{}?user={}&pass={}'.format(url, username, password), verify=False)
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
        camera_token = db().select(db.camera_tokens.ALL).first()

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
                                        db.camera_links.camera_source,
                                        db.camera_links.station_name,
                                        db.camera_links.description,
                                        orderby=db.camera_links.order_no,
                                        limitby=limitby)
        total = db(conditions).count(db.camera_links.id)
        total_page = total / num_on_page
        if total > total_page * num_on_page:
            total_page += 1
        html = ''
        data = db(conditions).select(db.camera_links.ALL)
        access_token = None
        for i in cameras:
            if not access_token:
                access_token = get_token_with()
            camera_source = str(i.camera_source)
            description = i.description
            id = i.id
            station_name = i.station_name
            if camera_source.startswith('zm_'):
                camera_source = camera_source[3:]

                if not access_token:
                    continue
                camera_source = "{}&token={}".format(camera_source, access_token)
                item = " \
                                <div class='item col-sm-3'> \
                                    <div > \
                                        <div class='panel-body bg-video1'> \
                                            <img id='camera_links_%s' class='bg-video1' src='%s'></img> \
                                        </div> \
                                        <div class='panel-footer'>%s</div> \
                                    </div> \
                                </div> \
                             "
                des = ' ' + description if description else ''
                html += item % (id, camera_source, station_name + des)
            else:
                item = " \
                                <div class='item col-sm-3'> \
                                    <div class='panel panel-default m-xxs'> \
                                        <div class='panel-body bg-video'> \
                                            <div id='camera_links_%s'  class='camera_links' data-url='%s'></div> \
                                        </div> \
                                        <div class='panel-footer' style = ' height: 56px'> \
                                            <div class = 'camera' >%s</div> \
                                        </div> \
                                    </div> \
                                </div> \
                            "
                des = ' ' + description if description else ''
                html += item % (id, camera_source, station_name + des)

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
    try:
        station_id = request.vars.station_id
        name = request.vars.name
        station_type = request.vars.type
        aaData = []

        conditions = (db.camera_links.station_id == station_id)
        # hungdx phan quyen quan ly trạm theo user issue 44
        if current_user:
            if not (auth.has_membership('admin') or auth.has_membership(const.GROUP_MANAGER)):
                list_station_manager = db(db.manager_stations.user_id == current_user.id).select(
                    db.manager_stations.station_id)
                station_ids = [str(item.station_id) for item in list_station_manager]
                conditions &= (db.camera_links.station_id.belongs(station_ids))

        list_data = db(conditions).select(db.camera_links.id,
                                          db.camera_links.camera_source,
                                          db.camera_links.is_visible,
                                          db.camera_links.order_no,
                                          db.camera_links.description)
        iTotalRecords = len(list_data)

        # Duyet tung phan tu trong mang du lieu vua truy van duoc
        for i, item in enumerate(list_data):
            url = URL('camera_links', 'popup_add_camera', args=[item.id],
                      vars={'station_id': station_id, 'type': station_type, 'name': name})

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
    # update history
    db.manager_stations_history.insert(station_id=station_id,
                                       action='Update',
                                       username=current_user.fullname or None,
                                       description='Thay_doi_camera_giam_sat',
                                       update_time=datetime.datetime.now())

    ###
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


