# -*- coding: utf-8 -*-
###############################################################################
# Author : 
# Date   : 
# 
# Description : 
# 
###############################################################################
from datetime import timedelta
from applications.eos.modules import common
from gluon.tools import prettydate

#@auth.requires_membership('manager')
# @decor.requires_login()
# @decor.requires_permission('Administration|notifications|form')
def form():
    record = db.notifications(request.args(0)) or None
    if not record: redirect(URL('notifications', 'index'))
    
    sender = db(db.auth_user.id == record.sender).select(db.auth_user.fullname, db.auth_user.email).first()

    return dict(record = record, sender = sender)

def call():
    return service()

################################################################################
# @decor.requires_login()
def index():
    
    return locals()

################################################################################
@service.json
# @decor.requires_login()
def get_list_notifications(*args, **kwargs):
    iDisplayStart = int(request.vars.iDisplayStart)
    iDisplayLength = int(request.vars.iDisplayLength)
    s_search = request.vars.sSearch
    aaData = []
    limitby = (iDisplayStart, iDisplayLength + 1)  # Tuple dung de phan trang (vtri bat dau - chieu dai)

    # Search conditions

    conditions = (db.notifications.id > 0)

    # Neu chuoi tim kiem khac rong thi them dieu kien truy van voi chuoi tim kiem
    if s_search:
        conditions &= ((db.notifications.title.contains(s_search)) | (db.notifications.content.contains(s_search)))

    list_data = db(conditions).select(db.notifications.id,
                                      db.notifications.title,
                                      db.notifications.content,
                                      db.notifications.receivers,
                                      db.notifications.notify_level,
                                      db.notifications.notify_time,
                                      db.notifications.is_read,
                                      orderby=~db.notifications.notify_time | ~db.notifications.notify_level,
                                      limitby=limitby)
    # Tong so ban ghi khong thuc hien phan trang
    iTotalRecords = db(conditions).count()
    user_dict = common.get_usr_dict()[0]

    # Duyet tung phan tu trong mang du lieu vua truy van duoc
    for i, item in enumerate(list_data):
        # Get & concat all receiver name (from list receivers)
        receiver_name = ''
        if 'receivers' in item and item.receivers is not None:
            for receiver in item.receivers:
                if user_dict.has_key(receiver):
                    receiver_name += '%s, ' % user_dict.get(receiver)
        # Format title by notify_level
        ntf = ''
        if item.notify_level == 0:
            ntf = I(XML("&nbsp;"), _class="fa fa-comment text-success") + SPAN(item.title, _class="text")
        elif item.notify_level == 1:
            ntf = I(XML("&nbsp;"), _class="fa fa-exclamation-circle text-warning") + SPAN(item.title, _class="text")
        else:
            ntf = I(XML("&nbsp;"), _class="fa fa-warning text-danger") + SPAN(item.title, _class="text text-danger")

        aaData.append([
            iDisplayStart + 1 + i,
            A(ntf, _href=URL('form', args=[item.id])),
            XML(item.content),
            receiver_name,
            # item.notify_time.strftime(full_date_format),
            item.notify_time.strftime(datetime_format_vn),
        ])

    return dict(iTotalRecords=iTotalRecords, iTotalDisplayRecords=iTotalRecords, aaData=aaData, success=True)

################################################################################
@service.json
def notify_menu():
    try:
        # Loc nhung notification trong 3 ngay tro lai
        conditions = {'notify_time': {'$gte': request.now - timedelta(days=3)}}

        # conditions = (db.notifications.notify_time >= request.now - timedelta(days=3))
        # loc nhung notify cua nguoi dung dang dang nhap thoi
        # conditions[]
        # conditions &= (db.notifications.receivers.contains(str(current_user.id)))
        # conditions &= (db.notifications.receivers.contains('1'))
                
        # list_data = db(conditions).select(  db.notifications.id,
        #                                     db.notifications.title,
        #                                     db.notifications.notify_level,
        #                                     db.notifications.notify_time,
        #                                     orderby = ~db.notifications.notify_time)
        total = pydb.notifications.count(conditions)
        list_data = pydb.notifications.find(conditions,
                                            {'_id': 1, 'title': 1, 'notify_level': 1, 'notify_time': 1}
                                            ).sort('notify_time', -1)

        html = '''
        <a class="dropdown-toggle count-info" data-toggle="dropdown" href="#"> 
            <div class="div-block-61" style="text-align: center;color: #FFFFFF"><i class="fa fa-envelope" style="font-size: 30px;"></i><div style="color:#FFFFFF;font-weight:bold;" class="text-block-51">Thông báo</div></div> '''
        if total > 0:
            html += '<span class="label label-danger">%s</span>' % total
        html += '''
        </a>
        <ul class="dropdown-menu dropdown-alerts">
        ''' 
        if not list_data:
            html += '''
            <li>
                <a style="text-center">
                    <div class="" >%s</div>
                </a>
            </li>
            <li class="divider"></li>
            ''' % T('No new messages')
        else:
            for item in list_data:
                if item['notify_level'] == 0:
                    icon = '<i class="fa fa-info-circle text-info"></i>'
                elif item['notify_level'] == 1:
                    icon = '<i class="fa fa-warning text-warning"></i>'
                else:
                    icon = '<i class="fa fa-times-circle text-danger"></i>'
                    
                html += '''
                <li>
                    <a href="%s">
                        <div> %s  %s
                            <span class="pull-right text-muted small">%s</span>
                        </div>
                    </a>
                </li>
                <li class="divider"></li>
                ''' % (URL('notifications', 'form', args=[str(item['_id'])]), icon, item['title'], prettydate(item['notify_time'], T))
        html += '''
            <li>
                <div class="text-center link-block">
                    <a href="%s">
                        <strong>%s</strong>&nbsp;&nbsp;<i class="fa fa-angle-double-right"></i>
                    </a>
                </div>
            </li>
        </ul>  ''' % (URL('notifications', 'index'), T('View all'))
       
        return dict(success=True, html=html)
    except Exception as ex:
        return dict(message=ex.message, success=False)
    
        

