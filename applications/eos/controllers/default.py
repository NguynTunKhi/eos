# -*- coding: utf-8 -*-

################################################################################
# # @decor.requires_login()
def index():
    # db(db.camera_links.id > 0).delete()
    #sts = db(db.stations.id > 0).select(db.stations.id, db.stations.station_type, db.stations.station_name)
    #for item in sts:
        # Camera
    #    db.camera_links.insert(station_id = item.id, station_name = item.station_name, station_type = item.station_type, description='Camera 1', camera_source = 'http://27.118.20.209:1935/CAM/CAMTEST6.stream/playlist.m3u8')
    #    db.camera_links.insert(station_id = item.id, station_name = item.station_name, station_type = item.station_type, description='Camera 2', camera_source = 'http://27.118.20.209:1935/CAM/CAMTEST7.stream/playlist.m3u8')
    #    db.camera_links.insert(station_id = item.id, station_name = item.station_name, station_type = item.station_type, description='Camera 3', camera_source = 'http://27.118.20.209:1935/CAM/CAMTEST8.stream/playlist.m3u8')

    # if current_user.username == 'admin':
    redirect(URL('dashboard', 'index'))
    # else:
    #     redirect(URL('adjustmentscompany', 'index'))
    return dict()

def login():
    frm = auth.login()
    frm.custom.widget.username['_placeholder'] = T('Enter username')
    frm.custom.widget.username['_tabindex'] = 1
    frm.custom.widget.username['_autofocus'] = True
    frm.custom.widget.password['_placeholder'] = T('Enter password')
    frm.custom.widget.password['_tabindex'] = 2
    return dict(form = frm)


################################################################################
def user():
    """
    exposes:
    http://..../[app]/default/user/login
    http://..../[app]/default/user/logout
    http://..../[app]/default/user/register
    http://..../[app]/default/user/profile
    http://..../[app]/default/user/retrieve_password
    http://..../[app]/default/user/change_password
    http://..../[app]/default/user/bulk_register
    use @auth.requires_login()
        @auth.requires_membership('group name')
        @auth.requires_permission('read','table name',record_id)
    to decorate functions that need access control
    also notice there is http://..../[app]/appadmin/manage/auth to allow administrator to manage users
    """
    form = auth()
    if request.args(0) == 'login':
        form.custom.widget.username['_placeholder'] = T('Enter username')
        form.custom.widget.username['_tabindex'] = 1
        form.custom.widget.username['_autofocus'] = True
        form.custom.widget.password['_placeholder'] = T('Enter password')
        form.custom.widget.password['_tabindex'] = 2

    return dict(form=form)

################################################################################
@cache.action()
def download():
    """
    allows downloading of uploaded files
    http://..../[app]/default/download/[filename]
    """
    return response.download(request, db)

################################################################################
def call():
    """
    exposes services. for example:
    http://..../[app]/default/call/jsonrpc
    decorate with @services.jsonrpc the functions to expose
    supports xml, json, xmlrpc, jsonrpc, amfrpc, rss, csv
    """
    return service()

def test():
    db(db.station_indicator.id > 0).update(status = const.SI_STATUS['IN_USE']['value'])
    return dict()