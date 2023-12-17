# -*- coding: utf-8 -*-
###############################################################################
# Author : 
# Date   : 
# 
# Description : 
# 
###############################################################################
from applications.eos.modules import common
 
#@auth.requires_login() 
@auth.requires(lambda: (auth.has_permission('create', 'agents') or auth.has_permission('edit', 'agents')))
def form():
    # If in Update mode, get equivallent record
    record = db.agents(request.args(0)) or None
    msg = ''
    
    frm = SQLFORM(db.agents, record, _method = 'POST', hideerror = True, showid = False, _id = 'frmMain')
    
    if frm.process(onvalidation = validate, detect_record_change = True, hideerror = True).accepted:
        session.flash = T('MSG_INFO_SAVE_SUCCESS')
        redirect(URL('index'))
    elif frm.record_changed:
        redirect(URL('home', 'error'))
    elif frm.errors:
        for item in frm.errors:
            msg += '%s: %s<br />' %(item, frm.errors[item])
    else:
        pass
        #response.flash = message.REQUEST_INPUT

    # Get list agents to fill in dropdown
    if not record:
        conditions = (db.agents.id > 0)
    else:
        conditions = (db.agents.id != record.id)

    agents = db(conditions).select(db.agents.id, db.agents.agent_name)

    return dict(frm = frm, agents = agents, msg = XML(msg))

################################################################################
def validate(frm):
    #Check condion
    #Get control value by : frm.vars.ControlName
    #If validate fail : frm.errors.ControlName = some message
    pass

def call():
    return service()

################################################################################
# @decor.requires_login()
@auth.requires(lambda: (auth.has_permission('view', 'agents')))
def index():
    return locals()

################################################################################
@service.json
@auth.requires(lambda: (auth.has_permission('view', 'agents')))
def get_list_station_by_agent(*args, **kwargs):
    try:
        agent_id = request.vars.agent_id
        aaData = []
        list_data = db(db.agent_station.agent_id == agent_id).select(db.agent_station.ALL)
        iTotalRecords = len(list_data)

        if iTotalRecords:
            station_type = dict()
            for key, item in const.STATION_TYPE.iteritems():
                station_type[str(item['value'])] = item['name']
            # Duyet tung phan tu trong mang du lieu vua truy van duoc
            for i, item in enumerate(list_data):
                station_type_str = []
                if str(item.station_type) in station_type:
                    station_type_str = station_type[str(item.station_type)]
                aaData.append([
                    str(i + 1),
                    item.station_name,
                    station_type_str,
                    INPUT(_name = 'select_item', _class = 'select_item', _type = 'checkbox', _value = item.id,
                        data = dict(value = item.id, display = item.station_name), _group=0),
                    item.id,
                ])
        return dict(iTotalRecords = iTotalRecords, iTotalDisplayRecords = iTotalRecords, aaData = aaData, success = True)
    except Exception as ex:
        return dict(iTotalRecords = 0, iTotalDisplayRecords = 0, aaData = [], message = str(ex), success = False)

################################################################################
def render_nestable(root, all_rows):
    # Get childs of node
    child = []
    for item in all_rows:
        if item.manage_agent == str(root.id):
            child.append(item)

    html = '<li class="dd-item">';
    html += '    <div class="dd-handle"  data-id="%s"> \
                     <span class="pull-right"><a href="%s" ><i class="fa fa-edit"></i></a></span> \
                     %s \
                 </div>' % (root.id, URL('form', args=[root.id]), root.agent_name)


    if child:
        for item in child:
            html += '    <ol class="dd-list">'
            html += '        ' + render_nestable(item, all_rows)
            html += '    </ol>'

    html += '</li>'

    return html

################################################################################
@auth.requires(lambda: (auth.has_permission('view', 'agents')))
def get_list_agents():
    try:
        conditions = (db.agents.id > 0)
        list_data = db(conditions).select(  db.agents.id, 
                                            db.agents.agent_name,
                                            db.agents.manage_agent,
                                            orderby = db.agents.order_number)
        root = None
        # Find the root to Build nestable list
        # html = '<div class="dd" id="nestable">'
        # html += '<ol class="dd-list">'
        # for item in list_data:
        #     check_root = True
        #     for item2 in list_data:
        #         root = item
        #         if item.manage_agent == str(item2.id):
        #             check_root = False
        #         # break

        #
        #     if check_root:
        #         html += render_nestable(root, list_data)
        # html += '</ol>'
        # html += '</div>'
        # Find the root to Build nestable list
        for item in list_data:
            if item.manage_agent == '':     # chi duy nhat co 1 row co manage_agent = ''
                root = item
                break

        html = '<div class="dd" id="nestable">'
        html += '<ol class="dd-list">'
        html += render_nestable(root, list_data)
        html += '</ol>'
        html += '</div>'

        return dict(success = True, html = html)
    except Exception as ex:
        return dict(message = str(ex), success = False, html = '')

################################################################################
@service.json
@auth.requires(lambda: (auth.has_permission('view', 'agents')))
def link_agent_to_station(*args, **kwargs):
    try:
        agentId = request.vars.agentId
        agent = db.agents(agentId)
        if not agent or not agentId:
            return dict(message = T('Record not found!'), success = False)
        stationIds = request.vars.stationId.split(',')
        rows = db(db.stations.id.belongs(stationIds)).select(db.stations.ALL)
        for row in rows:
            conditions = (db.agent_station.agent_id == str(agent.id))
            conditions &= (db.agent_station.station_id == str(row.id))
            fields = {
                'agent_id': str(agent.id),
                'agent_name': agent.agent_name,
                'order_no': 1,
                'station_id': str(row.id),
                'station_name': row.station_name,
                'station_type': row.station_type,
            }
            db.agent_station.update_or_insert(conditions, **fields)
        return dict(success = True)
    except Exception as ex:
        return dict(message = str(ex), success = False)

################################################################################
@service.json
@auth.requires(lambda: (auth.has_permission('view', 'agents')))
def get_list_agents_by_agent(*args, **kwargs):
    try:
        agent_id = request.vars.agent_id
        aaData = []
        list_data = db(db.agent_details.agent_id == agent_id).select(
            db.agent_details.id,
            db.agent_details.agent_detail_id,
            db.agent_details.agent_detail_name,
            db.agent_details.data_server,
            db.agent_details.data_server_port,
            db.agent_details.directory_format,
            db.agent_details.file_format,
        )
        iTotalRecords = len(list_data)

        if iTotalRecords:
            # Duyet tung phan tu trong mang du lieu vua truy van duoc
            for i, item in enumerate(list_data):
                aaData.append([
                    str(i + 1),
                    item.agent_detail_name,
                    item.data_server,
                    item.data_server_port,
                    item.directory_format,
                    item.file_format,
                    INPUT(_name = 'select_item', _class = 'select_item', _type = 'checkbox', _value = item.id, _group=0),
                    item.id,
                ])
        return dict(iTotalRecords = iTotalRecords, iTotalDisplayRecords = iTotalRecords, aaData = aaData, success = True)
    except Exception as ex:
        return dict(iTotalRecords = 0, iTotalDisplayRecords = 0, aaData = [], message = str(ex), success = False)

################################################################################
# # @decor.requires_login()
@auth.requires(lambda: (auth.has_permission('view', 'agents')))
def popup_add_agent():
    agent_id = request.vars.agent_id

    agents = db(db.agents.id != agent_id).select(db.agents.id, db.agents.agent_name)

    # record = db.agents(agent_id) or None
    #
    # frm = SQLFORM(db.agents, record, _method = 'POST', hideerror = True, showid = False)

    return  dict(agent_id = agent_id, agents = agents)

################################################################################
@service.json
@auth.requires(lambda: (auth.has_permission('view', 'agents')))
def get_agent_detail(*args, **kwargs):
    try:
        agent_id = request.vars.agent_id
        agent = db.agents(agent_id)

        return dict(success=True, agent = agent)
    except Exception as ex:
        return dict(success=False, message=str(ex))

################################################################################
@service.json 
@auth.requires(lambda: (auth.has_permission('create', 'agents')))
def ajax_save_agent_detail(*args, **kwargs):
    try:
        # data_server = request.vars.data_server
        # data_server_port = request.vars.data_server_port
        # directory_format = request.vars.directory_format
        # file_format = request.vars.file_format
        # username = request.vars.username
        # pwd = request.vars.pwd

        agent_id = request.vars.agent_id
        receive_agent = request.vars.receive_agent

        agent = db.agents(agent_id)
        agent_detail = db.agents(receive_agent)

        db.agent_details.insert(
            agent_id = agent_id,
            agent_name = agent.agent_name,
            agent_detail_id = receive_agent,
            agent_detail_name = agent_detail.agent_name,
            data_server = agent_detail.data_server,
            data_server_port = agent_detail.data_server_port,
            directory_format = agent_detail.directory_format,
            file_format = agent_detail.file_format,
            username = agent_detail.username,
            pwd = agent_detail.pwd,
        )
            
        return dict(success = True)
    except Exception as ex:
        logger.error(str(ex))
        return dict(success = False, message = str(ex))


