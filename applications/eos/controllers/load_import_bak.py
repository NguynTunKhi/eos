# -*- coding: utf-8 -*-
###############################################################################
# Author :
# Date   :
#
# Description :
#
###############################################################################
from datetime import datetime, timedelta

from applications.eos.modules import const, common
from gluon.tools import prettydate
import json

# Define bread scrumb for each page
# Format [< Bread scrumb name >, < URL when clicked >, < Displayed string >, <Parent name>]
bread_crumbs = [
  ['home', URL('dashboard', 'index'), 'Dashboard', ''],
  ['station', URL('station', 'map'), 'Stations', 'home'],
  ['station_waste', URL('', ''), 'Waste water', 'station'],
  ['station_suface', URL('', ''), 'Surface water', 'station'],
  ['station_under', URL('', ''), 'Underground water', 'station'],
  ['station_stack', URL('', ''), 'Stack emission', 'station'],
  ['station_amb', URL('', ''), 'Ambient air', 'station'],
  ['realtime', URL('camera_links', 'index'), 'Realtime monitor', 'home'],
  ['realtime_cam', URL('camera_links', 'index'), 'Camera list', 'realtime'],
  ['realtime_stack', URL('', ''), 'Stack emission', 'realtime'],
  ['realtime_waste', URL('', ''), 'Waste water', 'realtime'],
  ['realtime_surface', URL('', ''), 'Surface water', 'realtime'],
  ['realtime_air', URL('', ''), 'Ambient air', 'realtime'],
  ['realtime_under', URL('', ''), 'Underground water', 'realtime'],
  ['history', URL('view_logs', 'index', vars={'view_type': 1}), 'Historical data', 'home'],
  ['history_min', URL('', ''), 'Data by minute', 'history'],
  ['history_hour', URL('', ''), 'Data by hour', 'history'],
  ['history_day', URL('', ''), 'Data by day', 'history'],
  ['history_mon', URL('', ''), 'Data by month', 'history'],
  ['adjustments', URL('adjustments', 'index'), 'Station adjustment', 'home'],
  ['adjustments_cal', URL('', ''), 'Calendar', 'adjustments'],
  ['adjustments_list', URL('', ''), 'Adjustments list', 'adjustments'],
  ['commands', URL('commands', 'index'), 'Command get data', 'home'],
  ['commands_list', URL('', ''), 'Commands list', 'commands'],
  ['commands_sche', URL('', ''), 'Commands schedule', 'commands'],
  ['commands_his', URL('', ''), 'Commands history', 'commands'],
  ['commands_res', URL('', ''), 'Commands results', 'commands'],
  ['admin', URL('users', 'index'), 'Administration', 'home'],
  ['admin_batch', URL('tasks', 'index'), 'Schedule batchs', 'admin'],
  ['admin_user', URL('users', 'index'), 'Users list', 'admin'],
  ['admin_user_form', URL('users', 'form'), 'Users list', 'admin_user'],
  ['admin_group', URL('groups', 'index'), 'Groups list', 'admin'],
  ['admin_group_form', URL('groups', 'form'), 'Form', 'admin_group'],
  ['admin_group_form', URL('', ''), 'Priviledges', 'admin_group'],
  ['admin_reset_pwd', URL('', ''), 'Reset password', 'admin'],
  ['master', URL('stations', 'index'), 'Master data', 'home'],
  ['master_pro', URL('provinces', 'index'), 'Provinces list', 'master'],
  ['master_pro_frm', URL('provinces', 'form'), 'Form', 'master_pro'],
  ['master_area', URL('areas', 'index'), 'Areas list', 'master'],
  ['master_sty', URL('station_types', 'index'), 'Station types list', 'master'],
  ['master_sty_frm', URL('station_types', 'form'), 'Form', 'master'],
  ['master_ind', URL('indicators', 'index'), 'Indicators list', 'master'],
  ['master_ind_frm', URL('indicators', 'form'), 'Form', 'master_ind'],
  ['master_sta', URL('stations', 'index'), 'Stations list', 'master'],
  ['master_sta_frm', URL('stations', 'form'), 'Form', 'master_sta'],
  ['master_equ', URL('equipments', 'index'), 'Equipments list', 'master'],
]


################################################################################
# @decor.requires_login()
def graph_detail():
  station_id = request.vars.station_id
  show_by = request.vars.show_by or 1

  conditions = (db.station_indicator.station_id == station_id)
  conditions &= (db.station_indicator.status == const.SI_STATUS['IN_USE']['value'])
  rows = db(conditions).select(db.station_indicator.indicator_id, distinct=True)
  indicators_ids = []
  for row in rows:
    indicators_ids.append(row.indicator_id)

  indicators = db(db.indicators.id.belongs(indicators_ids)).select(db.indicators.ALL)

  return dict(station_id=station_id, indicators=indicators, show_by=show_by)


################################################################################
# @decor.requires_login()
@service.json
def get_chart_for_station(*args, **kwargs):
  try:
    chart_start = request.vars.chart_start or None
    chart_end = request.vars.chart_end or None
    duration = request.vars.duration
    station_id = request.vars.stationId
    show_by = request.vars.show_by or const.VIEW_BY['MINUTE']['value']
    show_by = str(show_by)
    date_now = request.now.replace(microsecond=0)
    try:
      if chart_start:
        chart_start = datetime.strptime(chart_start, '%Y-%m-%d').replace(microsecond=0)
      if chart_end:
        chart_end = datetime.strptime(chart_end, '%Y-%m-%d').replace(microsecond=0)
    except:
      chart_start = None
      chart_end = None
    # Default
    show_by_dict = {
      '1': ['data_min', date_now - timedelta(days=1), T('1 days'), date_now],
      '2': ['data_hour', date_now - timedelta(days=30), T('30 days'), date_now],
      '3': ['data_day', date_now - timedelta(days=30 * 6), T('6 months'), date_now],
      '4': ['data_mon', date_now - timedelta(days=365 * 3), T('3 years'), date_now],
      '5': ['data_hour_8h', date_now - timedelta(days=30), T('30 days'), date_now],
      '6': ['aqi_data_hour', date_now - timedelta(days=30), T('30 days'), date_now],
      '7': ['aqi_data_24h', date_now - timedelta(days=30), T('30 days'), date_now],
      '8': ['wqi_data_hour', date_now - timedelta(days=30), T('30 days'), date_now],
    }

    # Truong hop co truyen vao gioi han cua bieu do
    # co thoi gian bat dau
    if chart_start:
      if not chart_end: chart_end = date_now
    # co thoi gian ket thuc
    if chart_end:
      if not chart_start:
        show_by_dict = {
          '1': ['data_min', chart_end - timedelta(days=1), T('1 days'), chart_end],
          '2': ['data_hour', chart_end - timedelta(days=30), T('30 days'), chart_end],
          '3': ['data_day', chart_end - timedelta(days=30 * 6), T('6 months'), chart_end],
          '4': ['data_mon', chart_end - timedelta(days=365 * 3), T('3 years'), chart_end],
          '5': ['data_hour_8h', chart_end - timedelta(days=30), T('30 days'), chart_end],
          '6': ['aqi_data_hour', chart_end - timedelta(days=30), T('30 days'), chart_end],
          '7': ['aqi_data_24h', chart_end - timedelta(days=30), T('30 days'), chart_end],
          '8': ['wqi_data_hour', chart_end - timedelta(days=30), T('30 days'), chart_end],
        }
    # co ca thoi gian bat dau lan ket thuc
    if chart_start and chart_end:
      show_by_dict = {
        '1': ['data_min', chart_start, T('1 days'), chart_end],
        '2': ['data_hour', chart_start, T('30 days'), chart_end],
        '3': ['data_day', chart_start, T('6 months'), chart_end],
        '4': ['data_mon', chart_start, T('3 years'), chart_end],
        '5': ['data_hour_8h', chart_start, T('30 days'), chart_end],
        '6': ['aqi_data_hour', chart_start, T('30 days'), chart_end],
        '7': ['aqi_data_24h', chart_start, T('30 days'), chart_end],
        '8': ['wqi_data_hour', chart_start, T('30 days'), chart_end],
      }
      # gioi han lai khoang thoi gian neu xuat data_min > 2 thang
      # if chart_end - timedelta(days=60) > chart_start:
      #   show_by_dict = {
      #     '1': ['data_min', chart_end - timedelta(days=60), T('1 days'), chart_end],
      #     '2': ['data_hour', chart_start, T('30 days'), chart_end],
      #     '3': ['data_day', chart_start, T('6 months'), chart_end],
      #     '4': ['data_mon', chart_start, T('3 years'), chart_end],
      #     '5': ['data_hour_8h', chart_start, T('30 days'), chart_end],
      #     '6': ['aqi_data_hour', chart_start, T('30 days'), chart_end],
      #     '7': ['aqi_data_24h', chart_start, T('30 days'), chart_end],
      #     '8': ['wqi_data_hour', chart_start, T('30 days'), chart_end],
      #   }
    # Neu "duration" co gtri thi uu tien khoang tgian :  T1 --- duration --- now
    if duration:
      duration = int(duration)
      show_by_dict = {
        '1': ['data_min', date_now - timedelta(days=duration), T('1 days'), date_now],
        '2': ['data_hour', date_now - timedelta(days=duration), T('7 days'), date_now],
        '3': ['data_day', date_now - timedelta(days=duration), T('15 days'), date_now],
        '4': ['data_day', date_now - timedelta(days=duration), T('3 years'), date_now],  # ko apply cho month --> day
        '5': ['data_hour_8h', date_now - timedelta(days=duration), T('15 days'), date_now],
        '6': ['aqi_data_hour', date_now - timedelta(days=duration), T('15 days'), date_now],
        '7': ['aqi_data_24h', date_now - timedelta(days=duration), T('15 days'), date_now],
        '8': ['wqi_data_hour', date_now - timedelta(days=duration), T('15 days'), date_now],
      }

    charts = dict()
    station = db.stations(station_id)

    if not station:
      return dict(success=True, charts=charts)

    chart = dict()
    chart['title'] = dict(text='<b>%s</b>' % (station.station_name))
    chart['chart'] = {'height': 500}
    # chart['subtitle'] = {'text': T('Quality index in %(dt)s') %dict(dt=show_by_dict[show_by][2])}
    chart['xAxis'] = {'type': 'datetime', 'dateTimeLabelFormats': {'minute': '%H:%M'}}
    chart['subtitle'] = dict(text='')
    chart['series'] = []
    table = show_by_dict[show_by][0]
    if table != 'aqi_data_24h':
      rows = db((db[table].station_id == station_id) &
                (db[table].get_time >= show_by_dict[show_by][1]) &
                (db[table].get_time <= show_by_dict[show_by][3])).select(
        db[table].get_time,
        db[table].data,
        orderby=db[table].get_time)
    else:
      rows = db((db[table].station_id == station_id) &
                (db[table].get_time >= show_by_dict[show_by][1]) &
                (db[table].get_time <= show_by_dict[show_by][3])).select(
        db[table].get_time,
        db[table].data_24h,
        orderby=db[table].get_time)

    conditions2 = (db.station_indicator.station_id == station_id)
    conditions2 &= (db.station_indicator.status == const.SI_STATUS['IN_USE']['value'])
    rows2 = db(conditions2).select(db.station_indicator.indicator_id, distinct=True)
    indicators_id = []
    for row in rows2:
      indicators_id.append(row.indicator_id)
    indicators = db(db.indicators.id.belongs(indicators_id)).select(
      db.indicators.indicator,
      db.indicators.unit)

    data = dict()
    for indicator in indicators:
      data[str(indicator.indicator).decode('utf-8')] = {'unit': indicator.unit, 'data': []}
    if not rows:
      chart['subtitle']['text'] = '<b>%s</b> <br> %s %s %s %s' % (
      T('No data found!'), T('From'), show_by_dict[show_by][1], T('to'), show_by_dict[show_by][3])
    else:
      chart['subtitle']['text'] = '%s %s %s %s' % (
      T('From'), show_by_dict[show_by][1], T('to'), show_by_dict[show_by][3])

    for i, row in enumerate(rows):
      if show_by in ['3', '4']:  # Neu view theo day/month chuyen kieu date --> datetime
        x = 1000 * (datetime.fromordinal(row.get_time.toordinal()) - datetime(1970, 1, 1)).total_seconds()
      else:
        x = 1000 * (row.get_time - datetime(1970, 1, 1)).total_seconds()

      if table != 'aqi_data_24h':
        data_json = row.data
        for k in data_json:
          if data.has_key(k):
            try:
              y = float(str(data_json[k]))
              data[k]['data'].append([x, y])
              pass
            except:
              pass
      else:
        data_json = row.data_24h
        for k in data_json:
          if data.has_key(k):
            try:
              y = float(str(data_json[k]))
              data[k]['data'].append([x, y])
              pass
            except:
              pass

    print data
    for k in data:
      chart['series'].append({
        'name': '%s(%s)' % (k.encode('utf-8'), data[k]['unit']),
        'data': data[k]['data'],
        'tooltip': {'valueDecimals': 2}
      })
    charts['all'] = chart
    return dict(success=True, charts=charts)
  except Exception as ex:
    return dict(success=False, message=str(ex))


################################################################################
# @decor.requires_login()
@service.json
def get_chart_for_station_item(*args, **kwargs):
  try:
    chart_start = request.vars.chart_start or None
    chart_end = request.vars.chart_end or None
    duration = request.vars.duration
    indicatorId = request.vars.indicatorId
    station_id = request.vars.stationId
    show_by = request.vars.show_by or const.VIEW_BY['MINUTE']['value']
    show_by = str(show_by)
    date_now = request.now.replace(microsecond=0)
    try:
      if chart_start:
        chart_start = datetime.strptime(chart_start, '%Y-%m-%d').replace(microsecond=0)
      if chart_end:
        chart_end = datetime.strptime(chart_end, '%Y-%m-%d').replace(microsecond=0)
    except:
      chart_start = None
      chart_end = None
    # Default
    show_by_dict = {
      '1': ['data_min', date_now - timedelta(days=1), T('1 days'), date_now],
      '2': ['data_hour', date_now - timedelta(days=30), T('30 days'), date_now],
      '3': ['data_day', date_now - timedelta(days=30 * 6), T('6 months'), date_now],
      '4': ['data_mon', date_now - timedelta(365 * 3), T('3 years'), date_now],
    }

    # Truong hop co truyen vao gioi han cua bieu do
    # co thoi gian bat dau
    if chart_start:
      if not chart_end: chart_end = date_now
    # co thoi gian ket thuc
    if chart_end:
      if not chart_start:
        show_by_dict = {
          '1': ['data_min', chart_end - timedelta(days=1), T('1 days'), chart_end],
          '2': ['data_hour', chart_end - timedelta(days=30), T('30 days'), chart_end],
          '3': ['data_day', chart_end - timedelta(days=30 * 6), T('6 months'), chart_end],
          '4': ['data_mon', chart_end - timedelta(365 * 3), T('3 years'), chart_end],
        }
    # co ca thoi gian bat dau lan ket thuc
    if chart_start and chart_end:
      show_by_dict = {
        '1': ['data_min', chart_start, T('1 days'), chart_end],
        '2': ['data_hour', chart_start, T('30 days'), chart_end],
        '3': ['data_day', chart_start, T('6 months'), chart_end],
        '4': ['data_mon', chart_start, T('3 years'), chart_end],
      }
      # # gioi han lai khoang thoi gian neu xuat data_min > 2 thang
      # if chart_end - timedelta(days=60) > chart_start:
      #     show_by_dict = {
      #         '1': ['data_min', chart_end - timedelta(days=60), T('1 days'), chart_end],
      #         '2': ['data_hour', chart_start, T('30 days'), chart_end],
      #         '3': ['data_day', chart_start, T('6 months'), chart_end],
      #         '4': ['data_mon', chart_start, T('3 years'), chart_end],
      #     }
    # Neu "duration" co gtri thi uu tien khoang tgian :  T1 --- duration --- now
    if duration:
      duration = int(duration)
      show_by_dict = {
        '1': ['data_min', date_now - timedelta(days=duration), T('1 days'), date_now],
        '2': ['data_hour', date_now - timedelta(days=duration), T('7 days'), date_now],
        '3': ['data_day', date_now - timedelta(days=duration), T('15 days'), date_now],
        '4': ['data_day', date_now - timedelta(days=duration), T('3 years'), date_now],
        # ko apply cho month --> day
      }

    station = db.stations(station_id)
    indicator = db.indicators(indicatorId)
    name = str(indicator.indicator)

    charts = dict()
    charts['title'] = dict(text='<b>%s</b>(%s)' % (name, indicator.unit))
    # charts['subtitle'] = {'text': T('Data in %(dt)s') % dict(dt=show_by_dict[show_by][2])}
    charts['yAxis'] = {'title': {'text': indicator.unit}}
    charts['subtitle'] = dict(text='')
    # charts['zoomType'] = 'x'
    actual = []
    adjusted = []
    tendency = []
    preparing = []
    exceed = []

    cmax = []
    cmin = []

    table = show_by_dict[show_by][0]
    rows = db((db[table].station_id == station_id) &
              (db[table].get_time >= show_by_dict[show_by][1]) &
              (db[table].get_time <= show_by_dict[show_by][3])).select(
      db[table].get_time,
      db[table].data,
      orderby=db[table].get_time)

    table = 'data_adjust'
    row_adjusts = db((db[table].station_id == station_id) &
                     (db[table].get_time >= show_by_dict[show_by][1]) &
                     (db[table].get_time <= show_by_dict[show_by][3])).select(
      db[table].get_time,
      db[table].data,
      orderby=db[table].get_time)

    conditions2 = (db.station_indicator.station_id == station_id)
    conditions2 &= (db.station_indicator.indicator_id == indicatorId)
    conditions2 &= (db.station_indicator.status == const.SI_STATUS['IN_USE']['value'])
    station_indicator = db(conditions2).select(db.station_indicator.ALL).first()

    tendency_value = float(station_indicator.tendency_value) if station_indicator else 0
    preparing_value = float(station_indicator.preparing_value) if station_indicator else 0
    exceed_value = float(station_indicator.exceed_value) if station_indicator else 0
    # threshold = exceed_value

    cmax_value = station_indicator.qcvn_detail_max_value if station_indicator else 0
    cmin_value = station_indicator.qcvn_detail_min_value if station_indicator else 0
    threshold = cmax_value

    x_first = 0  # Gtri x dau tien cua chart
    x = 0  # Gtri x cuoi cung cua chart

    for i, row in enumerate(rows):
      if show_by in ['3', '4']:  # Neu view theo day/month chuyen kieu date --> datetime
        x = 1000 * (datetime.fromordinal(row.get_time.toordinal()) - datetime(1970, 1, 1)).total_seconds()
      else:
        x = 1000 * (row.get_time - datetime(1970, 1, 1)).total_seconds()

      if not x_first:
        x_first = x
      data_json = row.data
      if data_json.has_key(name.decode('utf-8')):
        try:
          y = float(data_json[name.decode('utf-8')])
          actual.append([x, y])
          pass
        except:
          pass

    # Neu actual data ko co du lieu,
    if not rows:
      x_first = show_by_dict[show_by][1]
      x = datetime.now()
      if not row_adjusts:
        charts['subtitle']['text'] = T('No data found!')

    exceed.append([x_first, exceed_value])
    exceed.append([x, exceed_value])
    preparing.append([x_first, preparing_value])
    preparing.append([x, preparing_value])
    tendency.append([x_first, tendency_value])
    tendency.append([x, tendency_value])

    cmax.append([x_first, cmax_value])
    cmax.append([x, cmax_value])
    cmin.append([x_first, cmin_value])
    cmin.append([x, cmin_value])
    for i, row in enumerate(row_adjusts):
      x = 1000 * (row.get_time - datetime(1970, 1, 1)).total_seconds()
      data_json = row.data
      if data_json.has_key(name):
        try:
          y = float(data_json[name])
          adjusted.append([x, y])
          pass
        except:
          pass

    charts['rangeSelector'] = {
      'selected': 1,
      'inputEnabled': 'false',
      'inputDateFormat': '%d/%m/%Y %H:%M',
      # 'inputDateFormat': '%d/%m/%Y',
      'inputEditDateFormat': '%d/%m/%Y',
      'buttonTheme': {'visibility': 'hidden'},
      'inputBoxWidth': 150,
      'labelStyle': {'visibility': 'hidden'}
    }

    charts['series'] = [
      {'name': T('Actual'), 'data': actual, 'color': 'red', 'lineWidth': 2, 'negativeColor': '#0088FF',
       'threshold': threshold, 'tooltip': {'valueDecimals': 2}},
      {'name': T('Adjusted'), 'data': adjusted, 'color': 'purple', 'lineWidth': 2, 'dashStyle': 'ShortDot',
       'tooltip': {'valueDecimals': 2}},
      {'name': 'Cmin', 'data': cmin, 'color': 'green', 'lineWidth': 1},
      # {'name': 'Preparing', 'data': preparing, 'color': 'orange', 'lineWidth': 1},
      {'name': 'Cmax', 'data': cmax, 'color': 'red', 'lineWidth': 1},
    ]
    return dict(success=True, charts=charts)
  except Exception as ex:
    return dict(success=False, message=str(ex))


# @decor.requires_login()
def call():
  return service()


################################################################################
def import_bread_crumbs():
  action_name = request.vars.action_name
  title = request.vars.title
  arr = get_item_from_arr(action_name)

  return dict(title=title, arr=arr)


################################################################################
def get_item_from_arr(action_name):
  arr_menu = []
  arr_tmp = []
  for item in bread_crumbs:
    if (item[0] == action_name):
      arr_menu.append(item)
      arr_tmp = get_item_from_arr(item[3])
      if (arr_tmp):
        for item_1 in arr_tmp:
          if (item_1):
            arr_menu.append(item_1)
      break
  return arr_menu


################################################################################
def menu():
  return dict()


################################################################################
def notification():
  return dict()


################################################################################
def user_info():
  return dict()


################################################################################
def import_data_table():
  return dict()


################################################################################
def notification():
  items = []
  conditions = ((db.stations.status == const.STATION_STATUS_OFFLINE))
  # hungdx phan quyen quan ly trạm theo user issue 44
  if current_user:
    if not (auth.has_membership('admin') or auth.has_membership(const.GROUP_MANAGER)):
      list_station_manager = db(db.manager_stations.user_id == current_user.id).select(
        db.manager_stations.station_id)
      station_ids = [str(item.station_id) for item in list_station_manager]
      conditions &= (db.stations.id.belongs(station_ids))

  rows1 = db(conditions).select(db.stations.id, db.stations.station_name, db.stations.station_type)
  for row in rows1:
    item = {
      'id': row.id,
      'station_name': row.station_name,
      'station_type': row.station_type,
    }
    conditions2 = ((db.station_off_log.station_id == row.id) &
                   (db.station_off_log.station_type == row.station_type))
    row2 = db(conditions2).select(db.station_off_log.start_off, orderby=~db.station_off_log.start_off,
                                  limitby=(0, 1)).first()
    # item['start_off'] = row2.start_off.strftime('%Y-%m-%d %H:%M:%S') if row2 else ''
    item['start_off'] = row2.start_off.strftime(datetime_format_vn) if row2 else ''
    items.append(item)
  total = len(items)
  return dict(items=items, total=total)


################################################################################
def station_condition_status():
  province_id = request.vars.province_id
  area_id = request.vars.area_id

  # Select stations to calculate data
  conditions = (db.stations.id > 0)
  if province_id:
    conditions &= (db.stations.province_id == province_id)
  if area_id:
    conditions &= (db.stations.area_id == area_id)

  fields = [
    db.stations.id,
    db.stations.station_name,
    db.stations.station_type,
    db.stations.longitude,
    db.stations.latitude,
    db.stations.status,
    db.stations.last_qty_good,
    db.stations.last_qty_exceed,
    db.stations.last_qty_adjusting,
    db.stations.last_qty_error,
  ]

  # hungdx phan quyen quan ly trạm theo user issue 44
  if current_user:
    if not (auth.has_membership('admin') or auth.has_membership(const.GROUP_MANAGER)):
      list_station_manager = db(db.manager_stations.user_id == current_user.id).select(db.manager_stations.station_id)
      station_ids = [str(item.station_id) for item in list_station_manager]
      conditions &= (db.stations.id.belongs(station_ids))

  stations = db(conditions).select(*fields)
  # Station status (dict) for displaying number of stations group by status
  station_status = dict()
  for item in const.STATION_STATUS:
    station_status[item] = dict()
    station_status[item]['value'] = const.STATION_STATUS[item]['value']
    station_status[item]['name'] = str(T(const.STATION_STATUS[item]['name']))
    station_status[item]['color'] = const.STATION_STATUS[item]['color']
    station_status[item]['qty'] = 0

  # Station type (dict) for displaying number of stations group by type
  # station_type = dict()
  # for item in const.STATION_TYPE:
  #     station_type[item] = dict()
  #     station_type[item]['value'] = const.STATION_TYPE[item]['value']
  #     station_type[item]['name'] = str(T(const.STATION_TYPE[item]['name']))
  #     station_type[item]['qty'] = 0

  total_online, total_adjust, total_offline, total_error = 0, 0, 0, 0
  total_good, total_tendency, total_preparing, total_exceed = 0, 0, 0, 0
  total_rec = len(stations)

  for station in stations:
    if station.status == const.STATION_STATUS['OFFLINE']['value']:
      total_offline += 1
    else:
      total_online += 1
      if station.status == const.STATION_STATUS['GOOD']['value']:
        total_good += 1
      if station.status == const.STATION_STATUS['TENDENCY']['value']:
        total_good += 1
      if station.status == const.STATION_STATUS['PREPARING']['value']:
        total_good += 1
      if station.status == const.STATION_STATUS['EXCEED']['value']:
        total_exceed += 1
      if station.status == const.STATION_STATUS['ERROR']['value']:
        total_error += 1
      if station.status == const.STATION_STATUS['ADJUSTING']['value']:
        total_adjust += 1
      try:
        if station.last_qty_good:
          station_status['GOOD']['qty'] += station.last_qty_good
        if station.last_qty_exceed:
          station_status['EXCEED']['qty'] += station.last_qty_exceed
        if station.last_qty_error:
          station_status['ERROR']['qty'] += station.last_qty_error
        if station.last_qty_adjusting:
          station_status['ADJUSTING']['qty'] += station.last_qty_adjusting
      except:
        pass
      # for item in station_status:
    #     if station.status == station_status[item]['value']:
    #         station_status[item]['qty'] +=
    #         break

  # Calculate percent for each station type
  # for item in station_type:
  #     p = (100.0 * station_type[item]['qty'] / len(stations)) if len(stations) else 0
  #     station_type[item]['percent'] = '%0.2f' %p

  return dict(total_station=len(stations), total_online=total_online, total_good=total_good, total_exceed=total_exceed,
              total_offline=total_offline,
              total_adjust=total_adjust, total_error=total_error,
              station_status=station_status, total_rec=total_rec)


################################################################################
def widget_by_station_type():
  station_type = request.vars.station_type
  # Get stations by station_type
  # stations = db(db.stations.station_type == station_type).select(db.stations.ALL) #hungdx comment issue 44

  # hungdx phan quyen quan ly trạm theo user issue 44
  conditions = db.stations.station_type == station_type
  if current_user:
    if not (auth.has_membership('admin') or auth.has_membership(const.GROUP_MANAGER)):
      list_station_manager = db(db.manager_stations.user_id == current_user.id).select(
        db.manager_stations.station_id)
      station_ids = [str(item.station_id) for item in list_station_manager]
      conditions &= (db.stations.id.belongs(station_ids))

  stations = db(conditions).select(db.stations.ALL)

  return dict(station_type=station_type, stations=stations)


def indicator_block():
  station_id = request.vars.station_id
  station = db.stations(station_id) or None

  # Lay cac Indicator thuoc station
  conditions = (db.station_indicator.station_id == station_id)
  conditions &= (db.station_indicator.status == const.SI_STATUS['IN_USE']['value'])
  station_indicators_rows = db(conditions).select(db.station_indicator.ALL)
  station_indicator = dict()
  indicator_ids = []

  for row in station_indicators_rows:
    indicator_ids.append(row.indicator_id)
    station_indicator[str(row.indicator_id)] = {
      'exceed_value': row.exceed_value,
      'unit': row.unit,
      'qcvn_detail_min_value': row.qcvn_detail_min_value,
      'qcvn_detail_max_value': row.qcvn_detail_max_value
    }

  # Lay ten cac Indicator
  conditions = (db.indicators.id.belongs(indicator_ids))
  rows = db(conditions).select(db.indicators.id, db.indicators.indicator)
  for row in rows:
    station_indicator[str(row.id)]['name'] = row.indicator
    station_indicator[str(row.id)]['color'] = '#EA3223'

  # Lay du lieu cac chi so moi nhat cua station
  conditions = (db.data_lastest.station_id == station_id)
  data_lastest = db(conditions).select(db.data_lastest.data, db.data_lastest.get_time,
                                       limitby=(0, 1),
                                       orderby=~db.data_lastest.get_time).first() or None
  updated_time = '-'
  si_dict = common.get_station_indicator_by_station_2(station_indicators_rows, station_id)

  if data_lastest:
    updated_time = data_lastest.get_time
    # if updated_time > request.now:
    # updated_time = request.now.strftime('%d/%m/%Y %H:%S')
    # updated_time = request.now.strftime(full_date_format)
    for k1 in data_lastest.data:
      for k2 in station_indicator:
        if station_indicator[k2]['name'] == k1.encode('utf-8'):
          if data_lastest.data[k1] is not None:
            try:
              v = float(data_lastest.data[k1])
              station_indicator[k2]['value'] = "{0:.2f}".format(v)
              station_indicator[k2]['color'] = common.getColorByIndicatorQcvn(si_dict, k2, v)
              break
            except:
              break

  # Quet lai cac key xem 'value' co hay ko, neu ko co cho bang rong ''
  for k in station_indicator:
    if not station_indicator[k].has_key('value'):
      station_indicator[k]['value'] = ''

  return dict(station=station, station_indicator=station_indicator, updated_time=updated_time)


###############################################################################
@service.json
def load_data_for_wbst(*args, **kwargs):
  try:
    area_id = request.vars.area_id
    province_id = request.vars.province_id
    station_type = request.vars.station_type
    station_status = request.vars.station_status
    aaData = []
    conditions = (db.stations.id > 0)
    if area_id:
      conditions &= (db.stations.area_id == area_id)
    if province_id:
      conditions &= (db.stations.province_id == province_id)
    if station_type:
      conditions &= (db.stations.station_type == station_type)
    if station_status:
      if station_status in ['1', '2', '0']:
        conditions &= (db.stations.status.belongs([1, 2, 0]))
      else:
        conditions &= (db.stations.status == station_status)

    # hungdx phan quyen quan ly trạm theo user issue 44
    if current_user:
      if not (auth.has_membership('admin') or auth.has_membership(const.GROUP_MANAGER)):
        list_station_manager = db(db.manager_stations.user_id == current_user.id).select(
          db.manager_stations.station_id)
        station_ids = [str(item.station_id) for item in list_station_manager]
        conditions &= (db.stations.id.belongs(station_ids))

    list_data = db(conditions).select(db.stations.id, db.stations.station_name, db.stations.status,
                                      db.stations.off_time)
    iTotalRecords = len(list_data)

    if iTotalRecords:
      iRow = 1
      # Duyet tung phan tu trong mang du lieu vua truy van duoc
      for item in list_data:
        status = const.STATION_STATUS['GOOD']
        for ss in const.STATION_STATUS:
          if item.status == const.STATION_STATUS[ss]['value']:
            status = const.STATION_STATUS[ss]
        off_text = ''
        # Lay du lieu cac chi so moi nhat cua station

        if item.status == const.STATION_STATUS['OFFLINE']['value']:
          # off_text = '(%s)' %(item.off_time.strftime('%d-%m-%Y %H:%M')) if item.off_time else ''
          conditions_data = (db.data_lastest.station_id == item.id)
          data_lastest = db(conditions_data).select(db.data_lastest.data, db.data_lastest.get_time, limitby=(0, 1),
                                                    orderby=~db.data_lastest.get_time).first() or None
          if data_lastest and not item.off_time is None:
            if item.off_time > data_lastest.get_time:
              item.off_time = data_lastest.get_time
          off_text = '(%s)' % (item.off_time.strftime(datetime_format_vn)) if item.off_time else ''

        listA = [
          XML(item.station_name) + SPAN(off_text, _class='off_text'),
          I(_class=status['icon'], _style='color: %s' % (status['color']), _title=T(status['name'])),
          str(item.id),
        ]
        aaData.append(listA)
        iRow += 1
    return dict(iTotalRecords=iTotalRecords, iTotalDisplayRecords=iTotalRecords, aaData=aaData, success=True)
  except Exception as ex:
    return dict(iTotalRecords=0, iTotalDisplayRecords=0, aaData=[], message=str(ex), success=False)


# def widget_data_collect():
#     from  w2pex import date_util
#     from  datetime import datetime, date
#
#     area_id = request.vars.area_id
#     province_id = request.vars.province_id
#
#     conditions = (db.stations.id > 0)
#     if area_id:
#         conditions &= (db.stations.area_id == area_id)
#     if province_id:
#         conditions &= (db.stations.province_id == province_id)
#     # hungdx phan quyen quan ly trạm theo user issue 44
#     if current_user:
#         if not (auth.has_membership('admin') or auth.has_membership(const.GROUP_MANAGER)):
#             list_station_manager = db(db.manager_stations.user_id == current_user.id).select(
#                 db.manager_stations.station_id)
#             station_ids = [str(item.station_id) for item in list_station_manager]
#             conditions &= (db.stations.id.belongs(station_ids))
#
#     # station_ids = []
#     # if area_id or province_id:
#     ids = db(conditions).select(db.stations.id)
#     station_ids = [str(item.id) for item in ids]
#
#     first_date_in_this_month = date_util.get_first_day_current_month(date.today())
#     first_date_in_this_month = datetime.combine(first_date_in_this_month, datetime.min.time())
#     first_date_in_last_month = date_util.get_first_day_last_month(date.today())
#     first_date_in_last_month = datetime.combine(first_date_in_last_month, datetime.min.time())
#     first_date_in_next_month = date_util.get_first_day_next_month(date.today())
#     first_date_in_next_month = datetime.combine(first_date_in_next_month, datetime.min.time())
#     # alarm_level
#     if True:
#         alarm_level_this_month = dict()
#         alarm_level_last_month = dict()
#         for item in const.ALARM_LEVEL:
#             alarm_level_this_month[item] = dict()
#             alarm_level_this_month[item]['value'] = const.ALARM_LEVEL[item]['value']
#             alarm_level_this_month[item]['name'] = str(T(const.ALARM_LEVEL[item]['name']))
#             alarm_level_this_month[item]['color'] = const.ALARM_LEVEL[item]['color']
#             alarm_level_this_month[item]['icon'] = const.ALARM_LEVEL[item]['icon']
#             alarm_level_this_month[item]['qty'] = 0
#
#             alarm_level_last_month[item] = dict()
#             alarm_level_last_month[item]['value'] = const.ALARM_LEVEL[item]['value']
#             alarm_level_last_month[item]['name'] = str(T(const.ALARM_LEVEL[item]['name']))
#             alarm_level_last_month[item]['color'] = const.ALARM_LEVEL[item]['color']
#             alarm_level_last_month[item]['icon'] = const.ALARM_LEVEL[item]['icon']
#             alarm_level_last_month[item]['qty'] = 0
#     # station_type
#     if True:
#         station_type_this_month = dict()
#         station_type_last_month = dict()
#         for item in const.STATION_TYPE:
#             station_type_this_month[item] = dict()
#             station_type_this_month[item]['value'] = const.STATION_TYPE[item]['value']
#             station_type_this_month[item]['name'] = str(T(const.STATION_TYPE[item]['name']))
#             station_type_this_month[item]['qty'] = 0
#
#             station_type_last_month[item] = dict()
#             station_type_last_month[item]['value'] = const.STATION_TYPE[item]['value']
#             station_type_last_month[item]['name'] = str(T(const.STATION_TYPE[item]['name']))
#             station_type_last_month[item]['qty'] = 0
#
#     # Count number records of data_min in this month
#     if True:
#         # get_chart_for_station = db((db.data_min.get_time >= first_date_in_this_month) & (db.data_min.station_id.belongs(station_ids))).count(db.data_min.id)
#         # n_this_month = db((db.data_min.get_time >= first_date_in_this_month) & (db.data_min.station_id.belongs(station_ids))).count(db.data_min.id)
#         n_this_month = db((db.data_min_collect.year == first_date_in_this_month.year) &
#                           (db.data_min_collect.month == first_date_in_this_month.month) &
#                           (db.data_min_collect.station_id.belongs(station_ids))).select(db.data_min_collect.total.sum().with_alias('total')).first()
#         n_this_month = n_this_month['total'] if n_this_month['total'] else 0
#         # Get number of days in this mon
#         days_this_month = (first_date_in_this_month.replace(month = first_date_in_this_month.month % 12 +1, day = 1)-timedelta(days=1)).day
#         # Tinh theo %
#         n_this_month = round(n_this_month / (12.0*24*days_this_month*len(station_ids)) * 100, 2) if station_ids else 0
#         # n_this_month = "{:,}".format(n_this_month)
#
#         conditions = (db.data_alarm.get_time >= first_date_in_this_month)
#         conditions &= (db.data_alarm.get_time < first_date_in_next_month)
#         conditions &= (db.data_alarm.station_id.belongs(station_ids))
#         rows = db(conditions).select(db.data_alarm.alarm_level.with_alias('alarm_level'),
#                                      db.data_alarm.id.count().with_alias('count'),
#                                      groupby = db.data_alarm.alarm_level)
#         t1 = 0
#         for row in rows:
#             t1 += row['count']
#             for item in alarm_level_this_month:
#                 if row['alarm_level'] == alarm_level_this_month[item]['value']:
#                     alarm_level_this_month[item]['qty'] += row['count']
#                     break
#         for item in alarm_level_this_month:
#             alarm_level_this_month[item]['percent'] = round(100.0 * alarm_level_this_month[item]['qty'] / t1, 2) if t1 > 0 else 0
#
#         # KH no yeu cau hide cai PREPARING --> add vao cai TENDENCY
#         alarm_level_this_month['TENDENCY']['percent'] += alarm_level_this_month['PREPARING']['percent']
#         alarm_level_this_month.pop('PREPARING')
#         alarm_level_this_month['TENDENCY']['name'] = T('Good')
#     # Count number records of data_min in last month
#     if True:
#         n_last_month = db((db.data_min_collect.year == first_date_in_last_month.year) &
#                           (db.data_min_collect.month == first_date_in_last_month.month) &
#                           (db.data_min_collect.station_id.belongs(station_ids))).select(db.data_min_collect.total.sum().with_alias('total')).first()
#         n_last_month = n_last_month['total'] if n_last_month['total'] else 0
#         # Get number of days in last mon
#         days_last_month = (first_date_in_last_month.replace(month=first_date_in_last_month.month % 12 + 1, day=1) - timedelta(days=1)).day
#         # Tinh theo %
#         n_last_month = round(n_last_month / (12.0 * 24 * days_last_month * len(station_ids)) * 100, 2) if station_ids else 0
#         # n_last_month = "{:,}".format(n_last_month)
#
#         conditions = (db.data_alarm.get_time >= first_date_in_last_month)
#         conditions &= (db.data_alarm.get_time < first_date_in_this_month)
#         conditions &= (db.data_alarm.station_id.belongs(station_ids))
#         rows = db(conditions).select(db.data_alarm.alarm_level.with_alias('alarm_level'),
#                                      db.data_alarm.id.count().with_alias('count'),
#                                      groupby = db.data_alarm.alarm_level)
#         t2 = 0
#         for row in rows:
#             t2 += row['count']
#             for item in alarm_level_last_month:
#                 if row['alarm_level'] == alarm_level_last_month[item]['value']:
#                     alarm_level_last_month[item]['qty'] += row['count']
#                     break
#
#         for item in alarm_level_last_month:
#             alarm_level_last_month[item]['percent'] = round(100.0 * alarm_level_last_month[item]['qty'] / t2, 2) if t2 > 0 else 0
#
#         # KH no yeu cau hide cai PREPARING --> add vao cai TENDENCY
#         alarm_level_last_month['TENDENCY']['percent'] += alarm_level_last_month['PREPARING']['percent']
#         alarm_level_last_month.pop('PREPARING')
#         alarm_level_last_month['TENDENCY']['name'] = T('Good')
#
#     # So sanh gtri collect tong cong
#     collect_icon = 'fa fa-arrow-up text-info'
#     if t1 < t2:
#         collect_icon = 'fa fa-arrow-down text-info'
#     elif t1 == t2:
#         collect_icon = 'fa fa-pause text-warning'
#
#     # So sanh gtri 3 nguong thang nay va thang truoc de display Icon len/xuong cho dung
#     for item in alarm_level_last_month:
#         if alarm_level_this_month[item]['percent'] > alarm_level_last_month[item]['percent']:
#             alarm_level_this_month[item]['icon'] = 'fa fa-arrow-up text-danger'
#         if alarm_level_this_month[item]['percent'] < alarm_level_last_month[item]['percent']:
#             alarm_level_this_month[item]['icon'] = 'fa fa-arrow-down text-info'
#         else:
#             alarm_level_this_month[item]['icon'] = 'fa fa-pause text-warning'
#
#     # Count number records of station_off_log in this month
#     if True:
#         conditions = (db.station_off_log.start_off >= first_date_in_this_month)
#         conditions &= (db.station_off_log.station_id.belongs(station_ids))
#         n2_this_month = db(conditions).count(db.station_off_log.id)
#         n2_this_month = "{:,}".format(n2_this_month)
#
#         conditions = (db.station_off_log.start_off >= first_date_in_this_month)
#         conditions &= (db.station_off_log.station_id.belongs(station_ids))
#         rows = db(conditions).select(db.station_off_log.id, db.station_off_log.station_type)
#         t1 = len(rows)
#         for row in rows:
#             for item in station_type_this_month:
#                 if row.station_type == station_type_this_month[item]['value']:
#                     station_type_this_month[item]['qty'] += 1
#                     break
#
#     # Count number records of station_off_log in last month
#     if True:
#         conditions = (db.station_off_log.start_off >= first_date_in_last_month)
#         conditions &= (db.station_off_log.start_off < first_date_in_this_month)
#         conditions &= (db.station_off_log.station_id.belongs(station_ids))
#         n2_last_month = db(conditions).count(db.station_off_log.id)
#         n2_last_month = "{:,}".format(n2_last_month)
#
#         conditions = (db.station_off_log.start_off >= first_date_in_last_month)
#         conditions &= (db.station_off_log.start_off < first_date_in_this_month)
#         conditions &= (db.station_off_log.station_id.belongs(station_ids))
#         rows = db(conditions).select(db.station_off_log.id, db.station_off_log.station_type)
#         t2 = len(rows)
#         for row in rows:
#             for item in station_type_last_month:
#                 if row.station_type == station_type_last_month[item]['value']:
#                     station_type_last_month[item]['qty'] += 1
#                     break
#
#     # So sanh gtri offline cua station
#     offline_icon = 'fa fa-arrow-up text-danger'
#     if t1 < t2:
#         collect_icon = 'fa fa-arrow-down text-info'
#     elif t1 == t2:
#         collect_icon = 'fa fa-pause text-warning'
#
#     return dict(n_this_month=n_this_month, n_last_month=n_last_month, collect_icon = collect_icon, offline_icon = offline_icon,
#                 alarm_level_this_month=alarm_level_this_month, alarm_level_last_month=alarm_level_last_month,
#                 n2_this_month=n2_this_month, n2_last_month=n2_last_month,
#                 station_type_this_month=station_type_this_month, station_type_last_month=station_type_last_month
#                 )


def widget_data_collect():
  from w2pex import date_util
  from datetime import datetime, date

  # calc_station_distribution_widget()
  area_id = request.vars.area_id
  province_id = request.vars.province_id
  n_qty_this_month = 0
  expected_this_month = 0
  n_qty_last_month = 0
  expected_last_month = 0
  conditions = (db.stations.id > 0)
  if province_id:
    conditions &= (db.stations.province_id == province_id)
  else:
    if area_id:
      conditions &= (db.stations.area_id == area_id)
  # hungdx phan quyen quan ly trạm theo user issue 44
  if current_user:
    if not (auth.has_membership('admin') or auth.has_membership(const.GROUP_MANAGER)):
      list_station_manager = db(db.manager_stations.user_id == current_user.id).select(
        db.manager_stations.station_id)
      station_ids = [str(item.station_id) for item in list_station_manager]
      conditions &= (db.stations.id.belongs(station_ids))

  # station_ids = []
  # if area_id or province_id:
  ids = db(conditions).select(db.stations.id)
  station_ids = [str(item.id) for item in ids]

  first_date_in_this_month = date_util.get_first_day_current_month(date.today())
  first_date_in_this_month = datetime.combine(first_date_in_this_month, datetime.min.time())
  first_date_in_last_month = date_util.get_first_day_last_month(date.today())
  first_date_in_last_month = datetime.combine(first_date_in_last_month, datetime.min.time())
  first_date_in_next_month = date_util.get_first_day_next_month(date.today())
  first_date_in_next_month = datetime.combine(first_date_in_next_month, datetime.min.time())

  t1 = 0
  t2 = 0
  n_this_month = 0
  n_last_month = 0
  # alarm_level
  if True:
    alarm_level_this_month = dict()
    alarm_level_last_month = dict()
    for item in const.STATION_STATUS:
      alarm_level_this_month[item] = dict()
      alarm_level_this_month[item]['value'] = const.STATION_STATUS[item]['value']
      alarm_level_this_month[item]['name'] = str(T(const.STATION_STATUS[item]['name']))
      alarm_level_this_month[item]['color'] = const.STATION_STATUS[item]['color']
      alarm_level_this_month[item]['icon'] = const.STATION_STATUS[item]['icon']
      alarm_level_this_month[item]['qty'] = 0
      alarm_level_this_month[item]['percent'] = 0

      alarm_level_last_month[item] = dict()
      alarm_level_last_month[item]['value'] = const.STATION_STATUS[item]['value']
      alarm_level_last_month[item]['name'] = str(T(const.STATION_STATUS[item]['name']))
      alarm_level_last_month[item]['color'] = const.STATION_STATUS[item]['color']
      alarm_level_last_month[item]['icon'] = const.STATION_STATUS[item]['icon']
      alarm_level_last_month[item]['qty'] = 0
      alarm_level_last_month[item]['percent'] = 0
  # station_type
  if True:
    station_type_this_month = dict()
    station_type_last_month = dict()
    # for item in const.STATION_TYPE:
    for item in common.get_station_types():
      _key = str(item['value'])
      # This month
      station_type_this_month[_key] = dict()
      station_type_this_month[_key]['value'] = item['value']  # const.STATION_TYPE[item]['value']
      station_type_this_month[_key]['name'] = T(item['name'])  # str(T(const.STATION_TYPE[item]['name']))
      station_type_this_month[_key]['qty'] = 0
      # Last month
      station_type_last_month[_key] = dict()
      station_type_last_month[_key]['value'] = item['value']  # const.STATION_TYPE[item]['value']
      station_type_last_month[_key]['name'] = T(item['name'])  # str(T(const.STATION_TYPE[item]['name']))
      station_type_last_month[_key]['qty'] = 0

  alarm_level_this_month.pop('PREPARING')
  alarm_level_last_month.pop('PREPARING')
  alarm_level_this_month.pop('TENDENCY')
  alarm_level_last_month.pop('TENDENCY')

  stations = db(db.stations.id.belongs(station_ids)).select()
  ## tinh lượng datamin phải nhận trong tháng này
  conditions = (db.data_min_month_collect.station_id.belongs(station_ids))
  conditions &= (db.data_min_month_collect.date_month >= first_date_in_this_month)
  conditions &= (db.data_min_month_collect.date_month < first_date_in_next_month)
  data_min_month_this_month = db(conditions).select(db.data_min_month_collect.station_id,
                                                    db.data_min_month_collect.actual_datamin)
  data_min_month_this_month_dict = dict()
  for item in data_min_month_this_month:
    data_min_month_this_month_dict[item.station_id] = item
  expected_this_month = 0.0
  # số ngày trong tháng
  # days_this_month = (
  #         first_date_in_this_month.replace(month=first_date_in_this_month.month % 12 + 1, day=1) - timedelta(
  #     days=1)).day
  days_this_month = datetime.now().day - 1
  days_this_month += 1.0 / 24.0 * datetime.now().hour
  for row in stations:
    # tần suất nhận dữ liệu
    freq = row['frequency_receiving_data']
    # freq = 5
    indicator_number = db(db.station_indicator.station_id == row.id).count(db.station_indicator.indicator_id)
    if not indicator_number:
      indicator_number = 0
    if (not freq) or (freq == 0):
      freq = 5
    expected_this_month_each = (indicator_number * days_this_month * 24 * 60 / freq)
    if data_min_month_this_month_dict.has_key(str(row.id)):
      actual_this_month = data_min_month_this_month_dict[str(row.id)].actual_datamin

      if actual_this_month:
        if expected_this_month_each < actual_this_month:
          expected_this_month_each = actual_this_month
    expected_this_month += expected_this_month_each
  # Count number records of data_min in this month
  if data_min_month_this_month:
    # conditions = (db.data_min_month_collect.station_id.belongs(station_ids))
    # conditions &= (db.data_min_month_collect.date_month >= first_date_in_this_month)
    # conditions &= (db.data_min_month_collect.date_month < first_date_in_next_month)
    data = db(conditions).select(
      db.data_min_month_collect.actual_datamin.sum().with_alias('actual_datamin'),
      db.data_min_month_collect.qty_good.sum().with_alias('qty_good'),
      db.data_min_month_collect.qty_exceed.sum().with_alias('qty_exceed'),
      db.data_min_month_collect.qty_adjusting.sum().with_alias('qty_adjusting'),
      db.data_min_month_collect.qty_error.sum().with_alias('qty_error'),
    ).first()
    n_this_month = data['actual_datamin'] if data['actual_datamin'] else 0
    t1 = n_this_month
    n_qty_this_month = data['actual_datamin'] if data['actual_datamin'] else 0
    # Tinh theo %
    if expected_this_month and expected_this_month > 0:
      n_this_month = round(100 * data['actual_datamin'] / expected_this_month, 2) if data['actual_datamin'] else 0
    else:
      n_this_month = 0
    # n_this_month = "{:,}".format(n_this_month)
    alarm_level_this_month['GOOD']['qty'] = moneyfmt(data['qty_good'])
    alarm_level_this_month['GOOD']['percent'] = round(
      100.0 * data['qty_good'] / expected_this_month if expected_this_month > 0 and data['qty_good'] else 0, 2)

    alarm_level_this_month['EXCEED']['qty'] = moneyfmt(data['qty_exceed'])
    alarm_level_this_month['EXCEED']['percent'] = round(
      100.0 * data['qty_exceed'] / expected_this_month if expected_this_month > 0 and data['qty_exceed'] else 0,
      2)

    alarm_level_this_month['ADJUSTING']['qty'] = moneyfmt(data['qty_adjusting'])
    alarm_level_this_month['ADJUSTING']['percent'] = round(
      100.0 * data['qty_adjusting'] / expected_this_month if expected_this_month > 0 and data['qty_adjusting'] else 0,
      2)
    alarm_level_this_month['ERROR']['qty'] = moneyfmt(data['qty_error'])
    alarm_level_this_month['ERROR']['percent'] = round(
      100.0 * data['qty_error'] / expected_this_month if expected_this_month > 0 and data['qty_error'] else 0,
      2)

    offline_count = expected_this_month - data['qty_good'] - data['qty_exceed'] - data['qty_adjusting'] - data[
      'qty_error']
    alarm_level_this_month['OFFLINE']['qty'] = moneyfmt(offline_count)
    alarm_level_this_month['OFFLINE']['percent'] = round(
      100.0 * offline_count / expected_this_month if expected_this_month > 0 and offline_count else 0,
      2)

  conditions = (db.data_min_month_collect.station_id.belongs(station_ids))
  conditions &= (db.data_min_month_collect.date_month >= first_date_in_last_month)
  conditions &= (db.data_min_month_collect.date_month < first_date_in_this_month)
  data_min_month_last_month = db(conditions).select(db.data_min_month_collect.station_id,
                                                    db.data_min_month_collect.actual_datamin)
  data_min_month_last_month_dict = dict()
  for item in data_min_month_last_month:
    data_min_month_last_month_dict[item.station_id] = item
  expected_last_month = 0.0
  # số ngày trong tháng
  days_last_month = (
      first_date_in_last_month.replace(month=first_date_in_last_month.month % 12 + 1, day=1) - timedelta(
    days=1)).day
  for row in stations:
    # tần suất nhận dữ liệu
    freq = row['frequency_receiving_data']
    # freq = 5
    indicator_number = db(db.station_indicator.station_id == row.id).count(db.station_indicator.indicator_id)
    if not indicator_number:
      indicator_number = 0
    if (not freq) or (freq == 0):
      freq = 5
    expected_last_month_each = (indicator_number * days_last_month * 24 * 60 / freq)
    # Trường hợp data nhận được nhiều hơn dự kiến (expected)
    if data_min_month_last_month_dict.has_key(str(row.id)):
      actual_last_month = data_min_month_last_month_dict[str(row.id)].actual_datamin
      if actual_last_month:
        if expected_last_month_each < actual_last_month:
          expected_last_month_each = actual_last_month
      expected_last_month += expected_last_month_each

  # Count number records of data_min in last month
  if data_min_month_last_month:
    # conditions = (db.data_min_month_collect.station_id.belongs(station_ids))
    # conditions &= (db.data_min_month_collect.date_month >= first_date_in_last_month)
    # conditions &= (db.data_min_month_collect.date_month < first_date_in_this_month)
    data = db(conditions).select(
      db.data_min_month_collect.actual_datamin.sum().with_alias('actual_datamin'),
      db.data_min_month_collect.qty_good.sum().with_alias('qty_good'),
      db.data_min_month_collect.qty_exceed.sum().with_alias('qty_exceed'),
      db.data_min_month_collect.qty_adjusting.sum().with_alias('qty_adjusting'),
      db.data_min_month_collect.qty_error.sum().with_alias('qty_error'),
    ).first()
    n_last_month = data['actual_datamin'] if data['actual_datamin'] else 0
    t2 = n_last_month
    n_qty_last_month = data['actual_datamin'] if data['actual_datamin'] else 0
    if expected_last_month and expected_last_month > 0:
      n_last_month = round(100 * data['actual_datamin'] / expected_last_month, 2) if data['actual_datamin'] else 0
    else:
      n_last_month = 0

    # alarm_level_last_month['TENDENCY']['qty'] = data['qty_good']
    # alarm_level_last_month['TENDENCY']['percent'] = round(
    #     100.0 * data['qty_good'] / data['actual_datamin'] if data['actual_datamin'] and data['qty_good'] else 0, 2)
    # alarm_level_last_month['TENDENCY']['name'] = T('Good')
    # alarm_level_last_month['EXCEED']['qty'] = data['qty_exceed']
    # alarm_level_last_month['EXCEED']['percent'] = round(
    #     100.0 * data['qty_exceed'] / data['actual_datamin'] if data['actual_datamin'] and data['qty_exceed'] else 0, 2)
    alarm_level_last_month['GOOD']['qty'] = moneyfmt(data['qty_good'])
    alarm_level_last_month['GOOD']['percent'] = round(
      100.0 * data['qty_good'] / expected_last_month if expected_last_month > 0 and data['qty_good'] else 0, 2)

    alarm_level_last_month['EXCEED']['qty'] = moneyfmt(data['qty_exceed'])
    alarm_level_last_month['EXCEED']['percent'] = round(
      100.0 * data['qty_exceed'] / expected_last_month if expected_last_month > 0 and data['qty_exceed'] else 0,
      2)

    alarm_level_last_month['ADJUSTING']['qty'] = moneyfmt(data['qty_adjusting'])
    alarm_level_last_month['ADJUSTING']['percent'] = round(
      100.0 * data['qty_adjusting'] / expected_last_month if expected_last_month > 0 and data[
        'qty_adjusting'] else 0,
      2)
    alarm_level_last_month['ERROR']['qty'] = moneyfmt(data['qty_error'])
    alarm_level_last_month['ERROR']['percent'] = round(
      100.0 * data['qty_error'] / expected_last_month if expected_last_month > 0 and data['qty_error'] else 0,
      2)

    offline_count = expected_last_month - data['qty_good'] - data['qty_exceed'] - data['qty_adjusting'] - data[
      'qty_error']
    alarm_level_last_month['OFFLINE']['qty'] = moneyfmt(offline_count)
    alarm_level_last_month['OFFLINE']['percent'] = round(
      100.0 * offline_count / expected_last_month if expected_last_month > 0 and offline_count else 0,
      2)
  # So sanh gtri collect tong cong
  collect_icon = 'fa fa-arrow-up text-info'
  if t1 < t2:
    collect_icon = 'fa fa-arrow-down text-info'
  elif t1 == t2:
    collect_icon = 'fa fa-pause text-warning'

  # So sanh gtri 3 nguong thang nay va thang truoc de display Icon len/xuong cho dung
  for item in alarm_level_last_month:
    if alarm_level_this_month[item]['percent'] > alarm_level_last_month[item]['percent']:
      alarm_level_this_month[item]['icon'] = 'fa fa-arrow-up text-danger'
    if alarm_level_this_month[item]['percent'] < alarm_level_last_month[item]['percent']:
      alarm_level_this_month[item]['icon'] = 'fa fa-arrow-down text-info'
    else:
      alarm_level_this_month[item]['icon'] = 'fa fa-pause text-warning'

  # Count number records of station_off_log in this month
  if True:
    conditions = (db.data_min_month_collect.station_id.belongs(station_ids))
    conditions &= (db.data_min_month_collect.date_month >= first_date_in_this_month)
    conditions &= (db.data_min_month_collect.date_month < first_date_in_next_month)
    conditions &= (db.data_min_month_collect.number_off_log > 0)
    rows = db(conditions).select(
      db.data_min_month_collect.id,
      db.data_min_month_collect.station_type,
      db.data_min_month_collect.number_off_log
    )
    n2_this_month = 0
    for row in rows:
      n2_this_month += row.number_off_log
      for item in station_type_this_month:
        if row.station_type == station_type_this_month[item]['value']:
          station_type_this_month[item]['qty'] += row.number_off_log
          break
    for item in station_type_this_month:
      if station_type_this_month[item]['qty']:
        station_type_this_month[item]['qty'] = moneyfmt(station_type_this_month[item]['qty'])
    t1 = n2_this_month
    n2_this_month = "{:,}".format(n2_this_month)

  # Count number records of station_off_log in last month
  if True:
    conditions = (db.data_min_month_collect.station_id.belongs(station_ids))
    conditions &= (db.data_min_month_collect.date_month >= first_date_in_last_month)
    conditions &= (db.data_min_month_collect.date_month < first_date_in_this_month)
    conditions &= (db.data_min_month_collect.number_off_log > 0)
    rows = db(conditions).select(
      db.data_min_month_collect.id,
      db.data_min_month_collect.station_type,
      db.data_min_month_collect.number_off_log
    )
    n2_last_month = 0
    for row in rows:
      n2_last_month += row.number_off_log
      for item in station_type_last_month:
        if row.station_type == station_type_last_month[item]['value']:
          station_type_last_month[item]['qty'] += row.number_off_log
          break
    for item in station_type_last_month:
      if station_type_last_month[item]['qty']:
        station_type_last_month[item]['qty'] = moneyfmt(station_type_last_month[item]['qty'])
    t2 = n2_last_month
    n2_last_month = "{:,}".format(n2_last_month)

  # So sanh gtri offline cua station
  offline_icon = 'fa fa-arrow-up text-danger'
  if t1 < t2:
    collect_icon = 'fa fa-arrow-down text-info'
  elif t1 == t2:
    collect_icon = 'fa fa-pause text-warning'

  return dict(n_this_month=n_this_month, n_last_month=n_last_month, collect_icon=collect_icon,
              offline_icon=offline_icon,
              alarm_level_this_month=alarm_level_this_month, alarm_level_last_month=alarm_level_last_month,
              n2_this_month=n2_this_month, n2_last_month=n2_last_month,
              station_type_this_month=station_type_this_month, station_type_last_month=station_type_last_month,
              n_qty_this_month=moneyfmt(n_qty_this_month), expected_this_month=moneyfmt(expected_this_month),
              n_qty_last_month=moneyfmt(n_qty_last_month), expected_last_month=moneyfmt(expected_last_month),
              )


def moneyfmt(value, places=0, curr='', sep=',', dp='.', pos='', neg='(', trailneg=''):
  # """Convert Decimal to a money formatted string.
  #
  # places:  required number of places after the decimal point
  # curr:    optional currency symbol before the sign (may be blank)
  # sep:     optional grouping separator (comma, period, space, or blank)
  # dp:      decimal point indicator (comma or period)
  #          only specify as blank when places is zero
  # pos:     optional sign for positive numbers: '+', space or blank
  # neg:     optional sign for negative numbers: '-', '(', space or blank
  # trailneg:optional trailing minus indicator:  '-', ')', space or blank
  #
  # >>> d = Decimal('-1234567.8901')
  # >>> moneyfmt(d, curr='$')
  # '-$1,234,567.89'
  # >>> moneyfmt(d, places=0, sep='.', dp='', neg='', trailneg='-')
  # '1.234.568-'
  # >>> moneyfmt(d, curr='$', neg='(', trailneg=')')
  # '($1,234,567.89)'
  # >>> moneyfmt(Decimal(123456789), sep=' ')
  # '123 456 789.00'
  # >>> moneyfmt(Decimal('-0.02'), neg='<', trailneg='>')
  # '<0.02>'
  #
  # """
  from decimal import Decimal
  q = Decimal(10) ** -places  # 2 places --> '0.01'
  sign, digits, exp = Decimal(value).quantize(q).as_tuple()
  result = []
  digits = map(str, digits)
  build, next = result.append, digits.pop

  if places == 0:
    dp = ''

  if sign:
    build(trailneg)
  for i in range(places):
    build(next() if digits else '0')

  build(dp)
  if not digits:
    build('0')

  i = 0
  while digits:
    build(next())
    i += 1
    if i == 3 and digits:
      i = 0
      build(sep)
  build(curr)
  build(neg if sign else pos)
  return ''.join(reversed(result))


###############################################################################
def station_distribution():
  # total_station = db(db.stations.id > 0).count(db.stations.id) #hungdx comment issue 44
  # hungdx phan quyen quan ly trạm theo user issue 44
  conditions_station = (db.stations.id > 0)
  if current_user:
    if not (auth.has_membership('admin') or auth.has_membership(const.GROUP_MANAGER)):
      list_station_manager = db(db.manager_stations.user_id == current_user.id).select(
        db.manager_stations.station_id)
      station_ids = [str(item.station_id) for item in list_station_manager]
      conditions_station &= (db.stations.id.belongs(station_ids))
  total_station = db(conditions_station).count(db.stations.id)

  # By Province
  # total_provinces = db(db.provinces.id > 0).count(db.provinces.id)#hungdx comment issue 44
  # hungdx phan quyen quan ly trạm theo user issue 44
  conditions_provinces = (db.stations.id > 0)
  if current_user:
    if not (auth.has_membership('admin') or auth.has_membership(const.GROUP_MANAGER)):
      list_station_manager = db(db.manager_stations.user_id == current_user.id).select(
        db.manager_stations.station_id)
      station_ids = [str(item.station_id) for item in list_station_manager]
      conditions_provinces &= (db.stations.id.belongs(station_ids))
  total_provinces = db(conditions_provinces).count(db.stations.id)

  conditions = (db.stations.id > 0)
  # hungdx phan quyen quan ly trạm theo user issue 44
  if current_user:
    if not (auth.has_membership('admin') or auth.has_membership(const.GROUP_MANAGER)):
      list_station_manager = db(db.manager_stations.user_id == current_user.id).select(
        db.manager_stations.station_id)
      station_ids = [str(item.station_id) for item in list_station_manager]
      conditions &= (db.stations.id.belongs(station_ids))

  conditions &= (db.stations.province_id != None)
  total_provinces_station = db(conditions).count(db.stations.province_id)
  pp = round(100 * total_provinces_station / total_provinces, 2) if total_provinces > 0 else 0
  # Equiments
  conditions = (db.equipments.id > 0)
  total_equipments = db(conditions).count(db.equipments.id)
  conditions &= (db.equipments.status == 1)
  total_equipments_in_use = db(conditions).count(db.equipments.id)
  percent_total_equipments_in_use = 100 * total_equipments_in_use / total_equipments if total_equipments else 0
  return dict(total_station=total_station,
              pp=pp,
              total_provinces_station=total_provinces_station,
              total_equipments=total_equipments,
              percent_total_equipments_in_use=percent_total_equipments_in_use)


###############################################################################
@service.json
def get_station_distribution_by_province(*args, **kwargs):
  try:
    data = dict()
    data['categories'] = []
    data['series'] = [{
      'name': T('Good'),
      'color': const.STATION_STATUS['GOOD']['color'],
      'data': [],
    }
      , {
        'name': T('Exceed'),
        'color': const.STATION_STATUS['EXCEED']['color'],
        'data': [],
      }
      , {
        'name': T('Offline'),
        'color': const.STATION_STATUS['OFFLINE']['color'],
        'data': [],
      }
      , {
        'name': T('Adjusting'),
        'color': const.STATION_STATUS['ADJUSTING']['color'],
        'data': [],
      }
      , {
        'name': T('Sensor error'),
        'color': const.STATION_STATUS['ERROR']['color'],
        'data': [],
      }]
    data['title'] = T('Stations distributed by Province')
    data['subtitle'] = ''
    rows = db(db.provinces.id > 0).select(db.provinces.id, db.provinces.province_name, orderby=db.provinces.order_no)
    provinces = dict()
    for row in rows:
      provinces[str(row.id)] = row.province_name

    conditions = (db.stations.id > 0)
    # hungdx phan quyen quan ly trạm theo user issue 44
    if current_user:
      if not (auth.has_membership('admin') or auth.has_membership(const.GROUP_MANAGER)):
        list_station_manager = db(db.manager_stations.user_id == current_user.id).select(
          db.manager_stations.station_id)
        station_ids = [str(item.station_id) for item in list_station_manager]
        conditions &= (db.stations.id.belongs(station_ids))

    conditions &= (db.stations.province_id != None)
    rows = db(conditions).select(db.stations.province_id, db.stations.status, limitby=(0, 100))
    categories = dict()
    if not rows:
      data['subtitle'] = T('No data found!')
    for row in rows:
      province_id = str(row.province_id)
      if provinces.has_key(province_id):
        if not categories.has_key(province_id):
          categories[province_id] = {
            'name': provinces[province_id],
            'qty': 0,
            'qty_good': 0,
            'qty_exceed': 0,
            'qty_offline': 0,
            'qty_adjust': 0,
            'qty_error': 0
          }
        categories[province_id]['qty'] += 1
        if row.status == const.STATION_STATUS['EXCEED']['value']:
          categories[province_id]['qty_exceed'] += 1
          pass
        elif row.status == const.STATION_STATUS['GOOD']['value'] or \
            row.status == const.STATION_STATUS['TENDENCY']['value'] or \
            row.status == const.STATION_STATUS['PREPARING']['value']:
          categories[province_id]['qty_good'] += 1
        elif row.status == const.STATION_STATUS['OFFLINE']['value']:
          categories[province_id]['qty_offline'] += 1
        elif row.status == const.STATION_STATUS['ADJUSTING']['value']:
          categories[province_id]['qty_adjust'] += 1
        elif row.status == const.STATION_STATUS['ERROR']['value']:
          categories[province_id]['qty_error'] += 1

    for item in categories:
      data['categories'].append(categories[item]['name'])
      data['series'][0]['data'].append(categories[item]['qty_good'])
      data['series'][1]['data'].append(categories[item]['qty_exceed'])
      data['series'][2]['data'].append(categories[item]['qty_offline'])
      data['series'][3]['data'].append(categories[item]['qty_adjust'])
      data['series'][4]['data'].append(categories[item]['qty_error'])

    return dict(data=data)
  except Exception as ex:
    return dict(data=data)


###############################################################################
@service.json
def get_station_distribution_by_area(*args, **kwargs):
  try:
    data = dict()
    data['categories'] = []
    data['series'] = [{
      'name': T('Good'),
      'color': const.STATION_STATUS['GOOD']['color'],
      'data': [],
    }
      , {
        'name': T('Exceed'),
        'color': const.STATION_STATUS['EXCEED']['color'],
        'data': [],
      }
      , {
        'name': T('Offline'),
        'color': const.STATION_STATUS['OFFLINE']['color'],
        'data': [],
      }
      , {
        'name': T('Adjusting'),
        'color': const.STATION_STATUS['ADJUSTING']['color'],
        'data': [],
      }
      , {
        'name': T('Sensor error'),
        'color': const.STATION_STATUS['ERROR']['color'],
        'data': [],
      }]
    data['title'] = T('Stations distributed by Area')
    data['subtitle'] = ''
    rows = db(db.areas.id > 0).select(db.areas.id, db.areas.area_name, orderby=db.areas.order_no)
    areas = dict()
    for row in rows:
      areas[str(row.id)] = row.area_name
    conditions = (db.stations.id > 0)
    # hungdx phan quyen quan ly trạm theo user issue 44
    if current_user:
      if not (auth.has_membership('admin') or auth.has_membership(const.GROUP_MANAGER)):
        list_station_manager = db(db.manager_stations.user_id == current_user.id).select(
          db.manager_stations.station_id)
        station_ids = [str(item.station_id) for item in list_station_manager]
        conditions &= (db.stations.id.belongs(station_ids))

    conditions &= (db.stations.area_id != None)
    rows = db(conditions).select(db.stations.area_id, db.stations.status, limitby=(0, 100))
    categories = dict()
    if not rows:
      data['subtitle'] = T('No data found!')
    for row in rows:
      area_id = str(row.area_id)
      if areas.has_key(area_id):
        if not categories.has_key(area_id):
          categories[area_id] = {
            'name': areas[area_id],
            'qty': 0,
            'qty_good': 0,
            'qty_exceed': 0,
            'qty_offline': 0,
            'qty_adjust': 0,
            'qty_error': 0
          }
        categories[area_id]['qty'] += 1
        if row.status == const.STATION_STATUS['EXCEED']['value']:
          categories[area_id]['qty_exceed'] += 1
          pass
        elif row.status == const.STATION_STATUS['GOOD']['value'] or \
            row.status == const.STATION_STATUS['TENDENCY']['value'] or \
            row.status == const.STATION_STATUS['PREPARING']['value']:
          categories[area_id]['qty_good'] += 1
        elif row.status == const.STATION_STATUS['OFFLINE']['value']:
          categories[area_id]['qty_offline'] += 1
        elif row.status == const.STATION_STATUS['ADJUSTING']['value']:
          categories[area_id]['qty_adjust'] += 1
        elif row.status == const.STATION_STATUS['ERROR']['value']:
          categories[area_id]['qty_error'] += 1

    for item in categories:
      data['categories'].append(categories[item]['name'])
      data['series'][0]['data'].append(categories[item]['qty_good'])
      data['series'][1]['data'].append(categories[item]['qty_exceed'])
      data['series'][2]['data'].append(categories[item]['qty_offline'])
      data['series'][3]['data'].append(categories[item]['qty_adjust'])
      data['series'][4]['data'].append(categories[item]['qty_error'])

    return dict(data=data)
  except Exception as ex:
    return dict(data=data)


###############################################################################
# STATION_STATUS = {
#     'GOOD': {'value': 0, 'name': 'Good', 'color': '#1dce6c', 'icon': 'fa fa-circle'},              # fa fa-spinner fa-spin
#     # 'TENDENCY': {'value': 1, 'name': 'Tendency', 'color': '#F1D748', 'icon': 'fa fa-circle'},
#     'TENDENCY': {'value': 1, 'name': 'Good', 'color': '#1dce6c', 'icon': 'fa fa-circle'},
#     # 'PREPARING': {'value': 2, 'name': 'Preparing', 'color': '#F08432', 'icon': 'fa fa-circle'},
#     'PREPARING': {'value': 2, 'name': 'Good', 'color': '#1dce6c', 'icon': 'fa fa-circle'},
#     'EXCEED': {'value': 3, 'name': 'Exceed', 'color': '#EA3223', 'icon': 'fa fa-circle'},
#     'OFFLINE':  {'value': 4, 'name': 'Offline', 'color': '#999999', 'icon': 'fa fa-stop'},
#     'ADJUSTING': {'value': 5, 'name': 'Adjusting', 'color': 'purple', 'icon': 'fa fa-pause'},
#     'ERROR':  {'value': 6, 'name': 'Sensor error', 'color': 'red', 'icon': 'fa fa-times-circle-o'},
# }
@service.json
def get_station_data_by_province(*args, **kwargs):
  try:
    province_id = request.vars.province_id

    data = dict()
    data['categories'] = []
    data['series'] = [{
      'name': T(const.STATION_STATUS['OFFLINE']['name']),
      'color': const.STATION_STATUS['OFFLINE']['color'],
      'data': [],
    }, {
      'name': T(const.STATION_STATUS['GOOD']['name']),
      'color': const.STATION_STATUS['GOOD']['color'],
      'data': [],
    }, {
      'name': T(const.STATION_STATUS['EXCEED']['name']),
      'color': const.STATION_STATUS['EXCEED']['color'],
      'data': [],
    }, {
      'name': T(const.STATION_STATUS['ADJUSTING']['name']),
      'color': const.STATION_STATUS['ADJUSTING']['color'],
      'data': [],
    }, {
      'name': T(const.STATION_STATUS['ERROR']['name']),
      'color': const.STATION_STATUS['ERROR']['color'],
      'data': [],
    }]

    if not province_id:
      data['title'] = T('No Province choosen!')
      return dict(data=data)

    # Get stations by province
    # stations = db(db.stations.province_id == province_id).select( #hungdx comment issue 44
    #     db.stations.id,
    #     db.stations.station_name,
    #     limitby=(0, 100)
    # )

    # hungdx phan quyen quan ly trạm theo user issue 44
    conditions = (db.stations.id > 0)
    conditions &= (db.stations.province_id == province_id)
    if current_user:
      if not (auth.has_membership('admin') or auth.has_membership(const.GROUP_MANAGER)):
        list_station_manager = db(db.manager_stations.user_id == current_user.id).select(
          db.manager_stations.station_id)
        station_ids = [str(item.station_id) for item in list_station_manager]
        conditions &= (db.stations.id.belongs(station_ids))

    stations = db(conditions).select(
      db.stations.id,
      db.stations.station_name,
      limitby=(0, 100)
    )

    station_dict = {}
    for item in stations:
      station_dict[str(item.id)] = item.station_name

    province = db.provinces(province_id)
    province = province.province_name if province else ''
    data['title'] = province
    if not stations:
      data['subtitle'] = T('No data found!')
    data['subtitle'] = T('Data in recent 30 days')

    # check = db(db.data_min_station_collect.station_id > 0).select()
    # calc_data_min_station_collect()
    # calc_station_distribution_widget()
    # Count all data_min in lastest 30 days

    for item in stations:
      qty_offline = 0
      qty_good = 0
      qty_exceed = 0
      qty_adjusting = 0
      qty_error = 0
      have_data = False

      conditions = (db.data_min_day_collect.station_id == item.id)
      conditions &= (db.data_min_day_collect.date_day >= (datetime.now() - timedelta(days=60)))
      series_data = db(conditions).select()

      if series_data:
        have_data = True
        for row in series_data:
          qty_offline += row['qty_offline']
          qty_good += row['qty_good']
          qty_exceed += row['qty_exceed']
          qty_adjusting += row['qty_adjusting']
          qty_error += row['qty_error']

      conditions = (
            (db.station_off_log.end_off >= datetime.now() - timedelta(days=30)) | (db.station_off_log.duration == 0))
      conditions &= (db.station_off_log.station_id == item.id)
      off_log = db(conditions).select(db.station_off_log.start_off, db.station_off_log.station_id,
                                      db.station_off_log.end_off)

      if off_log:
        have_data = True
        station_id = item.id
        freq_data = db(db.stations.id == station_id).select(db.stations.frequency_receiving_data)
        frequency = 60
        if freq_data:
          itemfreq = freq_data.first()['frequency_receiving_data']
          if itemfreq:
            frequency = round(itemfreq * 60)
        for row in off_log:
          station_id = row['station_id']
          start_time = row['start_off']
          if start_time < datetime.now(): start_time = datetime.now() - timedelta(days=30)
          end_time = row['end_off']
          if not end_time: end_time = datetime.now()
          duration = end_time - start_time
          qty_offline += round(duration.total_seconds() / frequency)

      if have_data:
        data['categories'].append(item.station_name)
        data['series'][0]['data'].append(qty_offline)
        data['series'][1]['data'].append(qty_good)
        data['series'][2]['data'].append(qty_exceed)
        data['series'][3]['data'].append(qty_adjusting)
        data['series'][4]['data'].append(qty_error)

    return dict(data=data)
  except Exception as ex:
    return dict(msg=str(ex), data=data)


def calc_data_min_station_collect():
  try:
    logger.info('Start calculate data min station collect')
    field = [
      db.stations.id,
      db.stations.station_code
    ]
    conditions = (db.stations.id > 0)
    # get all datamin
    rows = db(conditions).select(*field)

    conditions = (db.data_min.get_time >= datetime.now() - timedelta(days=30))
    qty_all = db(conditions).select(db.data_min.station_id, db.data_min.data_status)

    categories = {}
    for row in qty_all:
      station_id = row['station_id']
      if not categories.has_key(station_id):
        categories[station_id] = {
          'qty': 0,
          'qty_offline': 0,
          'qty_good': 0,
          'qty_exceed': 0,
          'qty_adjusting': 0,
          'qty_error': 0,
        }
      for item in row.data_status:
        data = row.data_status[item]
        if (data['status'] == 0 and not data['is_exceed']): categories[station_id]['qty_good'] += 1
        if (data['status'] == 0 and data['is_exceed']): categories[station_id]['qty_exceed'] += 1
        if (data['status'] == 1): categories[station_id]['qty_adjusting'] += 1
        if (data['status'] == 2): categories[station_id]['qty_error'] += 1
    conditions = (
          (db.station_off_log.end_off >= datetime.now() - timedelta(days=30)) | (db.station_off_log.duration == 0))
    off_log = db(conditions).select(db.station_off_log.start_off, db.station_off_log.station_id,
                                    db.station_off_log.end_off)
    for row in off_log:
      station_id = row['station_id']
      if not categories.has_key(station_id):
        categories[station_id] = {
          'qty': 0,
          'qty_offline': 0,
          'qty_good': 0,
          'qty_exceed': 0,
          'qty_adjusting': 0,
          'qty_error': 0,
        }
      start_time = row['start_off']
      if start_time < datetime.now(): start_time = datetime.now() - timedelta(days=30)
      end_time = row['end_off']
      if not end_time: end_time = datetime.now()
      duration = end_time - start_time
      freq_data = db(db.stations.id == station_id).select(db.stations.frequency_receiving_data)
      frequency = 60
      if freq_data:
        item = freq_data.first()['frequency_receiving_data']
        if item:
          frequency = item * 60
      qty_offline = duration.total_seconds() / frequency
      categories[station_id]['qty_offline'] += qty_offline

    for item in categories:
      station_id = str(item)
      conditions_station_id = (db.data_min_station_collect.station_id == station_id)
      db.data_min_station_collect.update_or_insert(conditions_station_id,
                                                   station_id=station_id,
                                                   qty_offline=categories[item]['qty_offline'],
                                                   qty_good=categories[item]['qty_good'],
                                                   qty_exceed=categories[item]['qty_exceed'],
                                                   qty_adjusting=categories[item]['qty_adjusting'],
                                                   qty_error=categories[item]['qty_error'],
                                                   )
    db.commit()
  except Exception as ex:
    logger.error(str(ex))
  finally:
    logger.info('End calculate data min station collect')

  return


# def get_station_data_by_province(*args, **kwargs):
#     try:
#         province_id = request.vars.province_id
#
#         data = dict()
#         data['categories'] = []
#         data['series'] = [{
#             'name': T('Exceed'),
#             'color': '#EA3223',
#             'data': [],
#         }, {
#             'name': T('Preparing'),
#             'color': '#F08432',
#             'data': [],
#         }, {
#             'name': T('Tendency'),
#             'color': '#F1D748',
#             'data': [],
#         }, {
#             'name': T('Good'),
#             'color': '#1dce6c',
#             'data': [],
#         }]
#
#         if not province_id:
#             data['title'] = T('No Province choosen!')
#             return dict(data = data)
#
#         # Get stations by province
#         # stations = db(db.stations.province_id == province_id).select( #hungdx comment issue 44
#         #     db.stations.id,
#         #     db.stations.station_name,
#         #     limitby=(0, 100)
#         # )
#
#         # hungdx phan quyen quan ly trạm theo user issue 44
#         conditions = (db.stations.id > 0)
#         conditions &= (db.stations.province_id == province_id)
#         if current_user:
#             if not (auth.has_membership('admin') or auth.has_membership(const.GROUP_MANAGER)):
#                 list_station_manager = db(db.manager_stations.user_id == current_user.id).select(
#                     db.manager_stations.station_id)
#                 station_ids = [str(item.station_id) for item in list_station_manager]
#                 conditions &= (db.stations.id.belongs(station_ids))
#
#         stations = db(conditions).select(
#             db.stations.id,
#             db.stations.station_name,
#             limitby=(0, 100)
#         )
#
#         station_dict = {}
#         for item in stations:
#             station_dict[str(item.id)] = item.station_name
#
#         province = db.provinces(province_id)
#         province = province.province_name if province else ''
#         data['title'] = province
#         if not stations:
#             data['subtitle'] = T('No data found!')
#         data['subtitle'] = T('Data in recent 30 days')
#
#         # Count all data_min in lastest 30 days
#         conditions = (db.data_min.station_id.belongs(station_dict.keys()))
#         conditions &= (db.data_min.get_time >= request.now - timedelta(days=30))
#         qty_all = db(conditions).select(
#             db.data_min.station_id.with_alias('station_id'),
#             db.data_min.station_id.count().with_alias('station_id_count'),
#             groupby = db.data_min.station_id
#         )
#
#         # Count data_alarm by station_id | alarm_level
#         conditions = (db.data_alarm.station_id.belongs(station_dict.keys()))
#         conditions &= (db.data_alarm.get_time >= request.now - timedelta(days=30))   # Lay du lieu 30 ngay gan nhat
#         data_alarms = db(conditions).select(
#             db.data_alarm.station_id.with_alias('station_id'),
#             db.data_alarm.alarm_level.with_alias('alarm_level'),
#             db.data_alarm.alarm_level.count().with_alias('alarm_level_count'),
#             groupby = db.data_alarm.station_id | db.data_alarm.alarm_level
#         )
#         categories = {}
#         for row in data_alarms:
#             station_id = row['station_id']
#             if not categories.has_key(station_id):
#                 categories[station_id] = {
#                     'name': station_dict[station_id],
#                     'qty': 0,
#                     'qty_good': 0,
#                     'qty_tendency': 0,
#                     'qty_preparing': 0,
#                     'qty_exceed': 0,
#                     'qty_total': 0,
#                 }
#
#             if row['alarm_level'] == const.ALARM_LEVEL['TENDENCY']['value']:
#                 categories[station_id]['qty_tendency'] = row['alarm_level_count']
#             elif row['alarm_level'] == const.ALARM_LEVEL['PREPARING']['value']:
#                 categories[station_id]['qty_preparing'] = row['alarm_level_count']
#             elif row['alarm_level'] == const.ALARM_LEVEL['EXCEED']['value']:
#                 categories[station_id]['qty_exceed'] = row['alarm_level_count']
#
#             categories[station_id]['qty_total'] += row['alarm_level_count']
#
#         # Tinh so luong record Good
#         for item in qty_all:
#             for station_id in categories:
#                 if item['station_id'] == station_id:
#                     categories[station_id]['qty_good'] = item['station_id_count'] - categories[station_id]['qty_total']
#                     break
#
#         for item in categories:
#             data['categories'].append(categories[item]['name'])
#             data['series'][0]['data'].append(categories[item]['qty_exceed'])
#             data['series'][1]['data'].append(categories[item]['qty_preparing'])
#             data['series'][2]['data'].append(categories[item]['qty_tendency'])
#             data['series'][3]['data'].append(categories[item]['qty_good'])
#
#         return dict(data=data)
#     except Exception as ex:
#         return dict(msg=str(ex), data=data)
###############################################################################


@service.json
def get_station_data_by_area(*args, **kwargs):
  try:
    area_id = request.vars.area_id

    data = dict()
    data['categories'] = []
    data['series'] = [{
      'name': T(const.STATION_STATUS['OFFLINE']['name']),
      'color': const.STATION_STATUS['OFFLINE']['color'],
      'data': [],
    }, {
      'name': T(const.STATION_STATUS['GOOD']['name']),
      'color': const.STATION_STATUS['GOOD']['color'],
      'data': [],
    }, {
      'name': T(const.STATION_STATUS['EXCEED']['name']),
      'color': const.STATION_STATUS['EXCEED']['color'],
      'data': [],
    }, {
      'name': T(const.STATION_STATUS['ADJUSTING']['name']),
      'color': const.STATION_STATUS['ADJUSTING']['color'],
      'data': [],
    }, {
      'name': T(const.STATION_STATUS['ERROR']['name']),
      'color': const.STATION_STATUS['ERROR']['color'],
      'data': [],
    }]

    if not area_id:
      data['title'] = T('No Area choosen!')
      return dict(data=data)

    # Get stations by province
    # stations = db(db.stations.province_id == province_id).select( #hungdx comment issue 44
    #     db.stations.id,
    #     db.stations.station_name,
    #     limitby=(0, 100)
    # )

    # hungdx phan quyen quan ly trạm theo user issue 44
    conditions = (db.stations.id > 0)
    conditions &= (db.stations.area_id == area_id)
    if current_user:
      if not (auth.has_membership('admin') or auth.has_membership(const.GROUP_MANAGER)):
        list_station_manager = db(db.manager_stations.user_id == current_user.id).select(
          db.manager_stations.station_id)
        station_ids = [str(item.station_id) for item in list_station_manager]
        conditions &= (db.stations.id.belongs(station_ids))

    stations = db(conditions).select(
      db.stations.id,
      db.stations.station_name,
      limitby=(0, 100)
    )

    station_dict = {}
    for item in stations:
      station_dict[str(item.id)] = item.station_name

    area = db.areas(area_id)
    area = area.area_name if area else ''
    data['title'] = area
    if not stations:
      data['subtitle'] = T('No data found!')
      data['subtitle'] = T('Data in recent 30 days')

    # check = db(db.data_min_station_collect.station_id > 0).select()
    # calc_data_min_station_collect()
    # Count all data_min in lastest 30 days
    for item in stations:
      qty_offline = 0
      qty_good = 0
      qty_exceed = 0
      qty_adjusting = 0
      qty_error = 0
      have_data = False

      conditions = (db.data_min_day_collect.station_id == item.id)
      conditions &= (db.data_min_day_collect.date_day >= (datetime.now() - timedelta(days=60)))
      series_data = db(conditions).select()

      if series_data:
        have_data = True
        for row in series_data:
          qty_offline += row['qty_offline']
          qty_good += row['qty_good']
          qty_exceed += row['qty_exceed']
          qty_adjusting += row['qty_adjusting']
          qty_error += row['qty_error']

      conditions = ((db.station_off_log.end_off >= datetime.now() - timedelta(days=30)) | (
          db.station_off_log.duration == 0))
      conditions &= (db.station_off_log.station_id == item.id)
      off_log = db(conditions).select(db.station_off_log.start_off, db.station_off_log.station_id,
                                      db.station_off_log.end_off)

      if off_log:
        have_data = True
        station_id = item.id
        freq_data = db(db.stations.id == station_id).select(db.stations.frequency_receiving_data)
        frequency = 60
        if freq_data:
          itemfreq = freq_data.first()['frequency_receiving_data']
          if itemfreq:
            frequency = round(itemfreq * 60)
        for row in off_log:
          station_id = row['station_id']
          start_time = row['start_off']
          if start_time < datetime.now(): start_time = datetime.now() - timedelta(days=30)
          end_time = row['end_off']
          if not end_time: end_time = datetime.now()
          duration = end_time - start_time
          qty_offline += round(duration.total_seconds() / frequency)

      if have_data:
        data['categories'].append(item.station_name)
        data['series'][0]['data'].append(qty_offline)
        data['series'][1]['data'].append(qty_good)
        data['series'][2]['data'].append(qty_exceed)
        data['series'][3]['data'].append(qty_adjusting)
        data['series'][4]['data'].append(qty_error)
    return dict(data=data)
  except Exception as ex:
    return dict(msg=str(ex), data=data)


# def get_station_data_by_area(*args, **kwargs):
#     try:
#         area_id = request.vars.area_id
#
#         data = dict()
#         data['categories'] = []
#         data['series'] = [{
#             'name': T('Exceed'),
#             'color': '#EA3223',
#             'data': [],
#         }, {
#             'name': T('Preparing'),
#             'color': '#F08432',
#             'data': [],
#         }, {
#             'name': T('Tendency'),
#             'color': '#F1D748',
#             'data': [],
#         }, {
#             'name': T('Good'),
#             'color': '#1dce6c',
#             'data': [],
#         }]
#
#         if not area_id:
#             data['title'] = T('No Area choosen!')
#             return dict(data = data)
#
#         # Get stations by province
#         # stations = db(db.stations.area_id == area_id).select( #hungdx comment issue 44
#         #     db.stations.id,
#         #     db.stations.station_name,
#         #     limitby=(0, 100)
#         # )
#
#         # hungdx phan quyen quan ly trạm theo user issue 44
#         conditions = (db.stations.id > 0)
#         conditions &= (db.stations.area_id == area_id)
#         if current_user:
#             if not (auth.has_membership('admin') or auth.has_membership(const.GROUP_MANAGER)):
#                 list_station_manager = db(db.manager_stations.user_id == current_user.id).select(
#                     db.manager_stations.station_id)
#                 station_ids = [str(item.station_id) for item in list_station_manager]
#                 conditions &= (db.stations.id.belongs(station_ids))
#
#         stations = db(conditions).select(
#             db.stations.id,
#             db.stations.station_name,
#             limitby=(0, 100)
#         )
#
#         station_dict = {}
#         for item in stations:
#             station_dict[str(item.id)] = item.station_name
#
#         area = db.areas(area_id)
#         area = area.area_name if area else ''
#         data['title'] = area
#         if not stations:
#             data['subtitle'] = T('No data found!')
#         data['subtitle'] = T('Data in recent 30 days')
#
#         # Count all data_min in lastest 30 days
#         conditions = (db.data_min.station_id.belongs(station_dict.keys()))
#         conditions &= (db.data_min.get_time  >= request.now - timedelta(days=30))
#         qty_all = db(conditions).select(
#             db.data_min.station_id.with_alias('station_id'),
#             db.data_min.station_id.count().with_alias('station_id_count'),
#             groupby = db.data_min.station_id
#         )
#
#         # Count data_alarm by station_id | alarm_level
#         conditions = (db.data_alarm.station_id.belongs(station_dict.keys()))
#         conditions &= (db.data_alarm.get_time >= request.now - timedelta(days=30))   # Lay du lieu 30 ngay gan nhat
#         data_alarms = db(conditions).select(
#             db.data_alarm.station_id.with_alias('station_id'),
#             db.data_alarm.alarm_level.with_alias('alarm_level'),
#             db.data_alarm.alarm_level.count().with_alias('alarm_level_count'),
#             groupby = db.data_alarm.station_id | db.data_alarm.alarm_level
#         )
#
#         categories = {}
#         for row in data_alarms:
#             total = 0
#             station_id = row['station_id']
#             if not categories.has_key(station_id):
#                 categories[station_id] = {
#                     'name': station_dict[station_id],
#                     'qty_good': 0,
#                     'qty_tendency': 0,
#                     'qty_preparing': 0,
#                     'qty_exceed': 0,
#                     'qty_total': 0
#                 }
#
#             if row['alarm_level'] == const.ALARM_LEVEL['TENDENCY']['value']:
#                 categories[station_id]['qty_tendency'] = row['alarm_level_count']
#             elif row['alarm_level'] == const.ALARM_LEVEL['PREPARING']['value']:
#                 categories[station_id]['qty_preparing'] = row['alarm_level_count']
#             elif row['alarm_level'] == const.ALARM_LEVEL['EXCEED']['value']:
#                 categories[station_id]['qty_exceed'] = row['alarm_level_count']
#
#             categories[station_id]['qty_total'] += row['alarm_level_count']
#
#         # Tinh so luong record Good
#         for item in qty_all:
#             for station_id in categories:
#                 if item['station_id'] == station_id:
#                     categories[station_id]['qty_good'] = item['station_id_count'] - categories[station_id]['qty_total']
#                     break
#
#         for item in categories:
#             data['categories'].append(categories[item]['name'])
#             data['series'][0]['data'].append(categories[item]['qty_exceed'])
#             data['series'][1]['data'].append(categories[item]['qty_preparing'])
#             data['series'][2]['data'].append(categories[item]['qty_tendency'])
#             data['series'][3]['data'].append(categories[item]['qty_good'])
#
#         return dict(data=data)
#     except Exception as ex:
#         return dict(msg=str(ex), data=data)

###############################################################################
def inactive_station():
  from w2pex import date_util
  # rows = db(db.stations.status == const.STATION_STATUS['OFFLINE']['value']).select(db.stations.id) #hungdx comment issue 44
  # hungdx phan quyen quan ly trạm theo user issue 44
  conditions = (db.stations.id > 0)
  conditions &= (db.stations.status == const.STATION_STATUS['OFFLINE']['value'])
  if current_user:
    if not (auth.has_membership('admin') or auth.has_membership(const.GROUP_MANAGER)):
      list_station_manager = db(db.manager_stations.user_id == current_user.id).select(
        db.manager_stations.station_id)
      station_ids = [str(item.station_id) for item in list_station_manager]
      conditions &= (db.stations.id.belongs(station_ids))
  rows = db(conditions).select(db.stations.id)

  total = len(rows)
  station_ids = []
  for row in rows:
    station_ids.append(str(row.id))
  conditions = (db.station_off_log.id > 0)
  # conditions &= (db.station_off_log.station_id.belongs(station_ids)) # Todo: Review this line
  rows = db(conditions).select(db.station_off_log.ALL, orderby=db.station_off_log.start_off)
  items = []
  for row in rows:
    item = [
      row.station_name,
      # row.start_off.strftime('%Y-%m-%d %H:%M:%S'),
      row.start_off.strftime(datetime_format_vn),
      date_util.pretty_date(row.start_off),
    ]
    items.append(item)
  return dict(total=total, items=items)


###############################################################################
def aqi_wqi():
  return dict()


###############################################################################
@service.json
def get_aqi_wqi(*args, **kwargs):
  try:

    province_id = request.vars.province_id
    area_id = request.vars.area_id
    aaData = []

    conditions = (db.stations.is_qi == True)
    # Todo : lay 30 tram co chi so QI cao nhat --> xem ve sau cho ra Setting
    conditions &= (db.stations.station_type.belongs([const.STATION_TYPE['STACK_EMISSION']['value'],
                                                     const.STATION_TYPE['AMBIENT_AIR']['value']]))
    if area_id:
      conditions &= (db.stations.area_id == area_id)
    if province_id:
      conditions &= (db.stations.province_id == province_id)

    # hungdx phan quyen quan ly trạm theo user issue 44
    if current_user:
      if not (auth.has_membership('admin') or auth.has_membership(const.GROUP_MANAGER)):
        list_station_manager = db(db.manager_stations.user_id == current_user.id).select(
          db.manager_stations.station_id)
        station_ids = [str(item.station_id) for item in list_station_manager]
        conditions &= (db.stations.id.belongs(station_ids))

    fields = ['id', 'station_name', 'qi', 'qi_time', 'status', 'qi_adjust', 'qi_adjsut_time']
    fields = [db.stations[field] for field in fields]

    rows = db(conditions).select(*fields, orderby=db.stations.order_no, limitby=(0, 30))
    total1 = len(rows)

    # status = dict()
    # for k in const.STATION_STATUS:
    #     status[str(const.STATION_STATUS[k]['value'])] = const.STATION_STATUS[k]['name']

    for row in rows:
      # status_icon = []
      status_icon = const.STATION_STATUS['GOOD']
      for ss in const.STATION_STATUS:
        if row.status == const.STATION_STATUS[ss]['value']:
          status_icon = const.STATION_STATUS[ss]

      status_station = {}
      for key in sorted(const.AQI_COLOR):
        if row.qi_adjust <= key:
          status_station['name'] = const.AQI_COLOR[key]['text']
          status_station['color'] = const.AQI_COLOR[key]['bgColor']
          break
      print(status_icon)
      print(status_station)
      aaData.append([
        row.station_name,
        '%s %s' % (
        I(_class="fa fa-clock-o"), row.qi_adjsut_time.strftime("%H:%M %m/%d") if row.qi_adjsut_time else '-'),
        "{0:.0f}".format(row.qi_adjust) if row.qi_adjust else '-',
        # status[str(row.status)],
        I(T(status_station['name']), _style='color: %s' % (status_station['color']), _title=T(status_station['name'])),
        str(row.id)
      ])
    return dict(iTotalRecords=len(rows), iTotalDisplayRecords=len(rows), aaData=aaData, success=True)
  except Exception as ex:
    return dict(iTotalRecords=0, iTotalDisplayRecords=0, aaData=[], message=str(ex), success=False)


################################################################################
def aqi_detail():
  station_id = request.vars.station_id

  stations = db.stations(station_id) or None
  aqi_detail_info = {}
  aqi_value = ''
  station_name = ''
  qi_time_1, qi_time_2 = '', ''
  is_public_data_type = 2
  qis = []

  if stations:
    aqi_value = int(round(stations.qi)) if stations.qi else '-'
    station_name = stations.station_name
    qi_time_1 = prettydate(stations.qi_time, T) if stations.qi_time else '-'
    # qi_time_2 = stations.qi_time.strftime('%d/%m/%Y %H:%S') if stations.qi_time else '-'
    qi_time_2 = stations.qi_time.strftime(datetime_format_vn) if stations.qi_time else '-'
    for key in sorted(const.AQI_COLOR):
      if stations.qi <= key:
        aqi_detail_info = const.AQI_COLOR[key]
        break

    try:
      is_public_data_type = stations.is_public_data_type
    except:
      is_public_data_type = 2

    if (stations.station_type != 4):
      if is_public_data_type == 3:
        conditions = (db.wqi_data_hour.station_id == station_id)
        qis = db(conditions).select(
          db.wqi_data_hour.get_time,
          db.wqi_data_hour.data,
          orderby=~db.wqi_data_hour.get_time,
          limitby=(0, 48)
        )
      else:
        conditions = (db.wqi_data_adjust_hour.station_id == station_id)
        qis = db(conditions).select(
          db.wqi_data_adjust_hour.get_time,
          db.wqi_data_adjust_hour.data,
          orderby=~db.wqi_data_adjust_hour.get_time,
          limitby=(0, 48)
        )
    else:
      if is_public_data_type == 3:
        conditions = (db.aqi_data_hour.station_id == station_id)
        qis = db(conditions).select(
          db.aqi_data_hour.get_time,
          db.aqi_data_hour.data,
          orderby=~db.aqi_data_hour.get_time,
          limitby=(0, 48)
        )
      else:
        conditions = (db.aqi_data_adjust_hour.station_id == station_id)
        qis = db(conditions).select(
          db.aqi_data_adjust_hour.get_time,
          db.aqi_data_adjust_hour.data,
          orderby=~db.aqi_data_adjust_hour.get_time,
          limitby=(0, 48)
        )

  ### Lay phan du lieu chi so AQI detail
  # conditions = (db.aqi_data_hour.station_id == station_id)
  # aqis = db(conditions).select(
  #     db.aqi_data_hour.get_time,
  #     db.aqi_data_hour.data,
  #     orderby = ~db.aqi_data_hour.get_time,
  #     limitby = (0, 48),
  # )

  ### Lay phan du lieu chi so AQI detail
  # conditions = (db.aqi_data_24h.station_id == station_id)
  # aqis = db(conditions).select(
  #     db.aqi_data_24h.get_time,
  #     db.aqi_data_24h.data_24h,
  #     orderby=~db.aqi_data_24h.get_time,
  #     limitby=(0, 48),
  # )

  conditions = (db.station_indicator.station_id == station_id) & (db.station_indicator.is_public == False)
  rows2 = db(conditions).select(db.station_indicator.indicator_id, distinct=True)
  indicators_id = []
  for row in rows2:
    indicators_id.append(row.indicator_id)
  indicators = db(db.indicators.id.belongs(indicators_id)).select(db.indicators.indicator)

  res = {}
  for item in qis:
    data = item.data

    for i in indicators:
      if data.has_key(i.indicator):
        del data[i.indicator]

    for indicator in data:
      if indicator == 'aqi': continue
      if indicator == 'wqi': continue
      if not res.has_key(indicator):
        res[indicator] = {
          'values': [],
          'values_hf': [],
          'min': data[indicator],
          'max': data[indicator],
          'current': data[indicator]
        }
      # O day mang 'values' dang duoc luu gtri theo tgian tu gan --> xa
      # nen tren html se phai dao nguoc lai (reversed)
      res[indicator]['values_hf'].append(
        {str(int(round(data[indicator]))): item.get_time.strftime(datetime_format_vn_2)})
      res[indicator]['values'].append(str(int(round(data[indicator]))))
      if res[indicator]['min'] > data[indicator]:
        res[indicator]['min'] = data[indicator]
      if res[indicator]['max'] < data[indicator]:
        res[indicator]['max'] = data[indicator]

  # Lay bang dinh nghia Color cho AQI, de buil colorMap cho client co format:
  # '0 : 50' : 'color1', '51 : 100' : 'color2', ....
  colors = const.AQI_COLOR
  keys = sorted(colors)  # keys    = [50, 100, 150, 200, 300, 999]
  shift_keys = [-1] + keys[:len(keys) - 1]  # shift_keys = [-1, 50, 100, 150, 200, 300]
  # color_map = ''
  color_map = {}
  for i, key in enumerate(keys):
    # color_map += "'%s : %s' : '%s', " % (shift_keys[i] + 1, keys[i], colors[key]['bgColor'])
    color_map['%s : %s' % (shift_keys[i] + 1, keys[i])] = '%s' % (colors[key]['bgColor'])
  color_map = json.dumps(color_map)
  return dict(aqi_value=aqi_value, station_name=station_name, res=res, color_map=color_map,
              qi_time_1=qi_time_1, qi_time_2=qi_time_2, aqi_detail_info=aqi_detail_info, res_json=json.dumps(res))


###############################################################################
def widget_notification():
  # Lay thong tin nguoi dung he thong (ten, avatar)
  user_name_dict, user_avatar_dict = common.get_usr_dict()

  # Get du lieu tu bang "notifications",
  # Todo : lay 10 cai moi nhat --> dua ra setting
  conditions = (db.notifications.id > 0)
  conditions &= (db.notifications.receivers.contains(str(current_user.id)))
  rows = db(conditions).select(
    db.notifications.ALL,
    orderby=~db.notifications.notify_time,
    limitby=(0, 10)
  )
  total = len(rows)
  items = []

  for item in rows:
    # avatar
    if user_avatar_dict[item.sender]:
      avatar = IMG(_src='%s' % URL('default', 'download', args=[user_avatar_dict[item.sender]]), _alt='image',
                   _class='img-circle')
    else:
      # avatar = IMG(_src='%s' % URL('static', 'img/black-linen.png'), _alt='image', _class='img-circle')
      avatar = IMG(_src='%s' % URL('static', 'img/a3.jpg'), _alt='image', _class='img-circle')

    items.append([
      avatar,
      prettydate(item.notify_time, T),  # time ago
      user_name_dict.get(item.sender),  # sender name
      item.title,  # brief title
      item.notify_time.strftime("%H:%S %d/%m") if item.notify_time else '',
      URL('notifications', 'form', args=[item.id])  # link
    ])

  # Get du lieu tu bang "adjustments",
  # Todo : lay nhung cai tao 3 ngay gan nhat, toi da 10 --> Setting
  conditions = (db.adjustments.id > 0)
  conditions &= (
        (db.adjustments.submit_to == str(current_user.id)) | (db.adjustments.created_by == str(current_user.id)))
  conditions &= (db.adjustments.created_date >= request.now - timedelta(days=3))

  fields = ['id', 'created_by', 'created_date', 'title']
  fields = [db.adjustments[field] for field in fields]
  rows = db(conditions).select(
    *fields,
    orderby=~db.adjustments.created_date,
    limitby=(0, 10)
  )

  for item in rows:
    # avatar
    if user_avatar_dict.has_key(item.created_by) and user_avatar_dict[item.created_by]:
      avatar = IMG(_src='%s' % URL('default', 'download', args=[user_avatar_dict[item.created_by]]), _alt='image',
                   _class='img-circle')
    else:
      # avatar = IMG(_src='%s' % URL('static', 'img/black-linen.png'), _alt='image', _class='img-circle')
      avatar = IMG(_src='%s' % URL('static', 'img/a3.jpg'), _alt='image', _class='img-circle')

    items.append([
      avatar,
      prettydate(item.created_date, T),  # time ago
      user_name_dict.get(item.created_by),  # sender name
      item.title,  # brief title
      item.created_date.strftime("%H:%S %d/%m") if item.created_date else '',
      URL('adjustments', 'form', args=[item.id])  # link
    ])

  return dict(total=total, items=items)


###############################################################################
def widget_aqi():
  conditions = (db.stations.id > 0)
  conditions &= (db.stations.is_qi == True)
  # hungdx phan quyen quan ly trạm theo user issue 44
  if current_user:
    if not (auth.has_membership('admin') or auth.has_membership(const.GROUP_MANAGER)):
      list_station_manager = db(db.manager_stations.user_id == current_user.id).select(
        db.manager_stations.station_id)
      station_ids = [str(item.station_id) for item in list_station_manager]
      conditions &= (db.stations.id.belongs(station_ids))

  conditions &= (db.stations.station_type.belongs(
    [const.STATION_TYPE['STACK_EMISSION']['value'], const.STATION_TYPE['AMBIENT_AIR']['value']]))
  stations = db(conditions).select(db.stations.ALL)
  report_at = datetime.now()
  return dict(stations=stations, report_at=report_at)


###############################################################################
@service.json
def get_chart_for_widget_aqi(*args, **kwargs):
  try:
    chart = dict()
    aqi = ''
    at_time = ''
    at_date = ''
    station_id = request.vars.station_id
    from_public = request.vars.from_public
    get_time = datetime.now()

    # Create blank data for chart
    chart['categories'] = []
    station = db.stations(station_id) or None
    chart['title'] = dict(text='<b>%s</b>' % (station.station_name if station else ''))
    chart['chart'] = {'height': 500}
    chart['xAxis'] = {'type': 'datetime', 'dateTimeLabelFormats': {'minute': '%H:%M'}}
    chart['subtitle'] = dict(text='')
    chart['series'] = [dict(data=[])]
    if station:
      # Get indicator
      conditions = (db.station_indicator.station_id == station_id)
      conditions &= (db.station_indicator.status == const.SI_STATUS['IN_USE']['value'])
      conditions &= (db.station_indicator.is_public == True)

      rows2 = db(conditions).select(db.station_indicator.indicator_id, distinct=True)
      indicators_id = []
      for row in rows2:
        indicators_id.append(row.indicator_id)
      indicators = db(db.indicators.id.belongs(indicators_id)).select(db.indicators.indicator)
      # Build data for all indicators
      data = dict()
      for indicator in indicators:
        data[str(indicator.indicator)] = {'value': 0}
      # Get data from db (table aqi_data_hour)
      try:
        is_public_data_type = station.is_public_data_type
      except:
        is_public_data_type = 2

      qi_value = ''
      qi_time = ''
      aqis = None
      if (station.station_type == 4):
        if is_public_data_type == 3:
          conditionsaqi = (db.aqi_data_hour.station_id == station_id)
          aqis = db(conditionsaqi).select(
            db.aqi_data_hour.ALL,
            orderby=~db.aqi_data_hour.get_time,
            limitby=(0, 2)
          ).first()
        else:
          conditionsaqi = (db.aqi_data_adjust_hour.station_id == station_id)
          aqis = db(conditionsaqi).select(
            db.aqi_data_adjust_hour.ALL,
            orderby=~db.aqi_data_adjust_hour.get_time,
            limitby=(0, 2)
          ).first()
      else:
        if is_public_data_type == 3:
          conditionsaqi = (db.wqi_data_hour.station_id == station_id)
          aqis = db(conditionsaqi).select(
            db.wqi_data_hour.ALL,
            orderby=~db.wqi_data_hour.get_time,
            limitby=(0, 2)
          ).first()
        else:
          conditionsaqi = (db.wqi_data_adjust_hour.station_id == station_id)
          aqis = db(conditionsaqi).select(
            db.wqi_data_adjust_hour.ALL,
            orderby=~db.wqi_data_adjust_hour.get_time,
            limitby=(0, 2)
          ).first()
      # aqi_data_hour = db(db.aqi_data_hour.station_id == station_id).select(db.aqi_data_hour.ALL, limitby=(0, 2),
      #                                                                      orderby=~db.aqi_data_hour.get_time).first()

      if not aqis:
        chart['subtitle']['text'] = T('No data found!')
        for k in data:
          chart['categories'].append(k)
          chart['series'][0]['data'].append(0)
      else:
        # get_time
        get_time = aqis.get_time
        # at_time = '%s %s' %(T('Updated time:'), get_time.strftime('%d/%m/%Y %H:%M'))
        at_time = '%s %s' % (T('Updated time:'), get_time.strftime(datetime_format_vn))
        at_date = get_time.strftime('%Y-%m-%d')
        data_json = aqis.data

        # for i in indicators:
        #     if data_json.has_key(i.indicator):
        #         del data_json[i.indicator]

        for k in data_json:
          try:
            y = float(data_json[k])
            if data.has_key(k):
              data[k]['value'] = y
            if k == 'aqi':
              aqi = int(round(y))
            if k == 'wqi':
              aqi = int(round(y))
          except:
            pass
        for k in data:
          chart['categories'].append(k)
          chart['series'][0]['data'].append(int(round(data[k]['value'])))
    else:
      chart['subtitle']['text'] = T('No data found!')

    return dict(success=True, chart=chart, aqi=aqi, at_time=at_time, at_date=at_date)
  except Exception as ex:
    return dict(success=False, message=str(ex), chart=dict(), aqi='', at_time=at_time, at_date=at_date)


###############################################################################
@service.json
def get_station_offline(*args, **kwargs):
  try:
    province_id = request.vars.province_id
    condition = request.vars.condition
    area_id = request.vars.area_id
    sometext = request.vars.sometext

    aaData = []
    conditions = (db.stations.status.belongs([4, 5, 6]))  # Chi lay status OFF
    if area_id:
      conditions &= (db.stations.area_id == area_id)
    if province_id:
      conditions &= (db.stations.province_id == province_id)
    if sometext:
      conditions &= (db.stations.station_name.contains(sometext))
    if condition:
      conditions &= (db.stations.status == condition)

      # hungdx phan quyen quan ly trạm theo user issue 44
    if current_user:
      if not (auth.has_membership('admin') or auth.has_membership(const.GROUP_MANAGER)):
        list_station_manager = db(db.manager_stations.user_id == current_user.id).select(
          db.manager_stations.station_id)
        station_ids = [str(item.station_id) for item in list_station_manager]
        conditions &= (db.stations.id.belongs(station_ids))

    list_data = db(conditions).select(db.stations.id,
                                      db.stations.station_name,
                                      db.stations.status,
                                      db.stations.off_time,
                                      limitby=(0, 30))

    station_dict = dict()
    data_lastest = db(db.data_lastest.id > 0).select(db.data_lastest.station_id, db.data_lastest.data_status)
    for item in data_lastest:
      station_dict[str(item.station_id)] = item

    for item in list_data:
      for key in const.STATION_STATUS:
        if const.STATION_STATUS[key]['value'] == item.status:
          status = const.STATION_STATUS[key]
          break
      off_text = ''
      if item.off_time and status == const.STATION_STATUS['OFFLINE']:
        off_text = '%s %s %s - %s' % (
          T('Offline'), T('From'), item.off_time.strftime(datetime_format_vn), prettydate(item.off_time, T))
      if station_dict.has_key(str(item.id)):
        datalastest = station_dict[str(item.id)]
        count_exceed = 0
        list_exceed = '('
        count_adjust = 0
        list_adjust = '('
        count_error = 0
        list_error = '('
        if datalastest.data_status:
          for i in datalastest.data_status:
            data = datalastest.data_status[i]
            if data['status'] == 0 and data['is_exceed']:
              count_exceed += 1;
              if count_exceed > 1: list_exceed += ', '
              list_exceed += data['indicator_name'].encode('utf-8')
            if data['status'] == 1:
              count_adjust += 1;
              if count_adjust > 1: list_adjust += ', '
              list_adjust += data['indicator_name'].encode('utf-8')
            if data['status'] == 2:
              count_error += 1;
              if count_error > 1: list_error += ', '
              list_error += data['indicator_name'].encode('utf-8')
          list_exceed += ')'
          list_adjust += ')'
          list_error += ')'
          if count_exceed > 0:
            # if off_text != '': off_text += '<br />'
            if off_text != '': off_text += ", "
            off_text += '%s: %s %s' % (T('Exceed'), str(count_exceed), list_exceed)
          if count_adjust > 0:
            # if off_text != '': off_text += '<br />'
            if off_text != '': off_text += ", "
            off_text += '%s: %s %s' % (T('Adjusting'), str(count_adjust), list_adjust)
          if count_error > 0:
            # if off_text != '': off_text += '<br />'
            if off_text != '': off_text += ", "
            off_text += '%s: %s %s' % (T('Sensor error'), str(count_error), list_error)

      aaData.append([
        XML(item.station_name) + SPAN(off_text, _class='off_text'),
        I(_class=status['icon'], _style='color: %s' % (status['color']), _title=T(status['name'])),
        str(item.id),
      ])
    return dict(iTotalRecords=len(list_data), iTotalDisplayRecords=len(list_data), aaData=aaData, success=True)
  except Exception as ex:
    return dict(iTotalRecords=0, iTotalDisplayRecords=0, aaData=[], message=str(ex), success=False)


###############################################################################
@service.json
def get_station_online(*args, **kwargs):
  try:
    province_id = request.vars.province_id
    area_id = request.vars.area_id
    sometext = request.vars.sometext
    status = request.vars.status

    aaData = []
    conditions = (db.stations.status.belongs([0, 1, 2, 3]))  # Ko lay status OFF, ADJUST, ERROR
    if area_id:
      conditions &= (db.stations.area_id == area_id)
    if province_id:
      conditions &= (db.stations.province_id == province_id)
    if sometext:
      conditions &= (db.stations.station_name.contains(sometext))
    if status:
      if status == '1':  # Exceed
        conditions &= (db.stations.status == 3)
      elif status == '2':  # Active
        conditions &= (db.stations.status.belongs([0, 1, 2]))
      # hungdx phan quyen quan ly trạm theo user issue 44
    if current_user:
      if not (auth.has_membership('admin') or auth.has_membership(const.GROUP_MANAGER)):
        list_station_manager = db(db.manager_stations.user_id == current_user.id).select(
          db.manager_stations.station_id)
        station_ids = [str(item.station_id) for item in list_station_manager]
        conditions &= (db.stations.id.belongs(station_ids))

    list_data = db(conditions).select(db.stations.id,
                                      db.stations.station_name,
                                      db.stations.status,
                                      limitby=(0, 30))
    station_dict = dict()
    data_lastest = db(db.data_lastest.id > 0).select(db.data_lastest.station_id, db.data_lastest.data_status)
    for item in data_lastest:
      station_dict[str(item.station_id)] = item

    for item in list_data:
      status = const.STATION_STATUS['GOOD']
      for ss in const.STATION_STATUS:
        if item.status == const.STATION_STATUS[ss]['value']:
          status = const.STATION_STATUS[ss]
      # xu ly text phia duoi
      off_text = ''
      if status == const.STATION_STATUS['EXCEED'] and station_dict.has_key(str(item.id)):
        datalastest = station_dict[str(item.id)]
        count_exceed = 0;
        list_exceed = '('
        if datalastest.data_status:
          for i in datalastest.data_status:
            data = datalastest.data_status[i]
            if data['status'] == 0 and data['is_exceed']:
              count_exceed += 1;
              if count_exceed > 1: list_exceed += ', '
              list_exceed += data['indicator_name'].encode('utf-8')
          list_exceed += ')'
          off_text += '%s: %s %s' % (T('Exceed'), str(count_exceed), list_exceed)

      aaData.append([
        XML(item.station_name) + SPAN(off_text, _class='off_text'),
        I(_class=status['icon'], _style='color: %s' % (status['color']), _title=T(status['name'])),
        str(item.id),
      ])
    return dict(iTotalRecords=len(list_data), iTotalDisplayRecords=len(list_data), aaData=aaData, success=True)
  except Exception as ex:
    return dict(iTotalRecords=0, iTotalDisplayRecords=0, aaData=[], message=str(ex), success=False)


###############################################################################
def station_type():
  area_id = request.vars.area_id
  province_id = request.vars.province_id

  # Select stations to fill in dropdown box
  fields = [
    db.stations.id,
    db.stations.station_name,
    db.stations.station_type,
    db.stations.status,
  ]

  conditions = (db.stations.id > 0)
  if area_id:
    conditions &= (db.stations.area_id == area_id)
  if province_id:
    conditions &= (db.stations.province_id == province_id)
  # stations = db(conditions).select(db.stations.id, db.stations.status, db.stations.station_type)

  # hungdx phan quyen quan ly trạm theo user issue 44
  if current_user:
    if not (auth.has_membership('admin') or auth.has_membership(const.GROUP_MANAGER)):
      list_station_manager = db(db.manager_stations.user_id == current_user.id).select(
        db.manager_stations.station_id)
      station_ids = [str(item.station_id) for item in list_station_manager]
      conditions &= (db.stations.id.belongs(station_ids))

  stations = db(conditions).select(*fields)
  station_types = common.get_station_types()

  # Get qty online/total for each station
  station_type_online = dict()
  for row in station_types:
    st = row['value']
    if not station_type_online.has_key(st):
      station_type_online[st] = dict()
      station_type_online[st]['value'] = row['value']  # const.STATION_TYPE[st]['value']
      station_type_online[st]['name'] = row['name']  # const.STATION_TYPE[st]['name']
      station_type_online[st]['image'] = row['image']  # const.STATION_TYPE[st]['image']
      station_type_online[st]['online'] = 0
      station_type_online[st]['good'] = 0
      station_type_online[st]['exceed'] = 0
      station_type_online[st]['total'] = 0
      station_type_online[st]['offline'] = 0
      station_type_online[st]['adjust'] = 0
      station_type_online[st]['error'] = 0
  # for st in const.STATION_TYPE:
  #     if not station_type_online.has_key(st):
  #         station_type_online[st] = dict()
  #         station_type_online[st]['value'] = const.STATION_TYPE[st]['value']
  #         station_type_online[st]['name'] = const.STATION_TYPE[st]['name']
  #         station_type_online[st]['image'] = const.STATION_TYPE[st]['image']
  #         station_type_online[st]['online'] = 0
  #         station_type_online[st]['good'] = 0
  #         station_type_online[st]['exceed'] = 0
  #         station_type_online[st]['total'] = 0
  #         station_type_online[st]['offline'] = 0
  #         station_type_online[st]['adjust'] = 0
  #         station_type_online[st]['error'] = 0

  total_online, total_adjust, total_offline, total_error, total_good, total_exceed = 0, 0, 0, 0, 0, 0

  for station in stations:
    for st in station_type_online:
      if station.station_type == station_type_online[st]['value']:
        if station.status == const.STATION_STATUS['OFFLINE']['value']:
          station_type_online[st]['offline'] += 1
          total_offline += 1
        else:
          station_type_online[st]['online'] += 1
          total_online += 1
          if station.status == const.STATION_STATUS['GOOD']['value']:
            station_type_online[st]['good'] += 1
            total_good += 1
          if station.status == const.STATION_STATUS['TENDENCY']['value']:
            station_type_online[st]['good'] += 1
            total_good += 1
          if station.status == const.STATION_STATUS['PREPARING']['value']:
            station_type_online[st]['good'] += 1
            total_good += 1
          if station.status == const.STATION_STATUS['EXCEED']['value']:
            station_type_online[st]['exceed'] += 1
            total_exceed += 1
          if station.status == const.STATION_STATUS['ERROR']['value']:
            station_type_online[st]['error'] += 1
            total_error += 1
          if station.status == const.STATION_STATUS['ADJUSTING']['value']:
            station_type_online[st]['adjust'] += 1
            total_adjust += 1
        station_type_online[st]['total'] += 1
        # if station.status == const.STATION_STATUS['ADJUSTING']['value']:
        #     station_type_online[st]['adjust'] += 1
        #     total_adjust += 1
        # elif station.status == const.STATION_STATUS['OFFLINE']['value']:
        #     station_type_online[st]['offline'] += 1
        #     total_offline += 1
        # elif station.status == const.STATION_STATUS['ERROR']['value']:
        #     station_type_online[st]['error'] += 1
        #     total_error += 1
        # else:
        #     station_type_online[st]['online'] += 1
        #     total_online += 1
        #
        # station_type_online[st]['total'] += 1
        # break
  return dict(station_type_online=station_type_online, total_error=total_error, total_good=total_good,
              total_exceed=total_exceed,
              total_station=len(stations), total_online=total_online, total_offline=total_offline,
              total_adjust=total_adjust)


def get_file_lastest():
  try:
    station_id = request.args[0] or None
    item = db(db.data_lastest.station_id == station_id).select(db.data_lastest.latest_file_content,
                                                               db.data_lastest.latest_file_name).first()
    content = item.latest_file_content
    file_name = item.latest_file_name or "file.txt"
    filename = os.path.join(request.folder, 'static', 'export', file_name)
    f = open(filename, "w+")
    f.write(content);
    f.close()
    response.headers['Content-Type'] = 'text/plain'
    response.headers['Content-Disposition'] = 'attachment;filename=%s' % file_name
    data = open(filename, "rb").read()
    return data
  except Exception as ex:
    return T('Error text export')
