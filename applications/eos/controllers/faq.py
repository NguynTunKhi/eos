# -*- coding: utf-8 -*-
###############################################################################
from applications.eos.modules.plugin_ckeditor import CKEditor
# Author : 
# Date   : 
# 
# Description : 
# 
###############################################################################
@auth.requires(lambda: (auth.has_permission('create', 'faq') or auth.has_permission('edit', 'faq')))
def form():

    # If in Update mode, get equivallent record
    msg = ''
    record = db.eip_faq(request.args(0)) or None

    frm = SQLFORM(db.eip_faq, record, _method='POST', hideerror=True, showid=False, _id='frmMain')

    if frm.process(onvalidation=validate, detect_record_change=True, hideerror=True).accepted:
        session.flash = T('MSG_INFO_SAVE_SUCCESS')
        redirect(URL('index'))
    elif frm.record_changed:
        redirect(URL('home', 'error'))
    elif frm.errors:
        for item in frm.errors:
            msg += '%s: %s<br />' % (T('provinces_' + item), frm.errors[item])
    else:
        pass
        # response.flash = message.REQUEST_INPUT
    if record:
        frm.custom.widget.content = CKEditor.widget
    #frm.custom.widget.content = CKEditor

    return dict(frm = frm, msg = XML(msg))


################################################################################
def validate(frm):
    # Check condion
    # Get control value by : frm.vars.ControlName
    # If validate fail : frm.errors.ControlName = some message
    pass

#################################################################################
def call():
    return service()

#################################################################################
def index():
    return dict()

##################################################################################
@service.json
@auth.requires(lambda: (auth.has_permission('view', 'faq')))
def get_list_faq(*args, **kwargs):
    try:
        iDisplayStart = int(request.vars.iDisplayStart)  # Vi tri bat dau lay du lieu
        iDisplayLength = int(request.vars.iDisplayLength)  # So luong ban ghi se lay toi da
        limitby = (iDisplayStart, iDisplayLength + 1)  # Tuple dung de phan trang (vtri bat dau - chieu dai)

        s_search = request.vars.sSearch

        sometext = request.vars.sometext
        aaData = []

        conditions = (db.eip_faq.id > 0)
        # Neu chuoi tim kiem khac rong thi them dieu kien truy van voi chuoi tim kiem
        if sometext:
            conditions &= (db.eip_faq.content.contains(sometext) |
                           db.eip_faq.title.contains(sometext))
        # if type:
        #     conditions &= (db.indicators.indicator_type == type)

        list_data = db(conditions).select(db.eip_faq.id,
                                          db.eip_faq.order_no,
                                          db.eip_faq.title,
                                          limitby=limitby)
        # Tong so ban ghi khong thuc hien phan trang
        iTotalRecords = db(conditions).count()
        iRow = iDisplayStart + 1

        # Duyet tung phan tu trong mang du lieu vua truy van duoc
        for i, item in enumerate(list_data):
            aaData.append([
                str(iRow),
                # A(item.title, _href=URL('form', args=[item.id])),
                A(item.title),
                item.order_no,
                INPUT(_group='0', _class='select_item', _type='checkbox', _value=item.id),
                item.id,
            ])
            iRow += 1

        return dict(iTotalRecords=iTotalRecords, iTotalDisplayRecords=iTotalRecords, aaData=aaData, success=True)
    except Exception, ex:
        return dict(iTotalRecords=0, iTotalDisplayRecords=0, aaData=[], message=str(ex), success=False)
############################################################################
@service.json
@auth.requires(lambda: (auth.has_permission('delete', 'station_types')))
def del_faq(*args, **kwargs):
    try:
        array_data = request.vars.ids
        list_ids = array_data.split(',')
        db(db.eip_faq.id.belongs(list_ids)).delete()
        return dict(success = True)
    except Exception as ex:
        return dict(success = False, message = str(ex))