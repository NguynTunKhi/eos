# -*- coding: utf-8 -*-
###############################################################################
# Author : 
# Date   : 
# 
# Description : 
# 
###############################################################################
# encoding=utf8
import sys

reload(sys)
sys.setdefaultencoding('utf8')

from applications.eos.modules import common
from applications.eos.modules.w2pex import date_util
from datetime import datetime, timedelta


def call():
  return service()


################################################################################
# @decor.requires_login()
@auth.requires(lambda: (auth.has_permission('view', 'alarm_log')))
def index():
  lst_data_key = get_all_data_key()
  station_id = request.vars.station_id
  # stations = db(db.stations.id >() 0).select(db.stations.id, db.stations.station_name) #hungdx comment issue 44
  # hungdx phan quyen quan ly trạm theo user issue 44
  conditions = (db.stations.id > 0)
  if current_user:
    if not (auth.has_membership('admin') or auth.has_membership(const.GROUP_MANAGER)):
      list_station_manager = db(db.manager_stations.user_id == current_user.id). \
        select(db.manager_stations.station_id)
      station_ids = [str(item.station_id) for item in list_station_manager]
      conditions &= (db.stations.id.belongs(station_ids))
  stations = db(conditions).select(db.stations.id, db.stations.station_name)

  return dict(data_key=lst_data_key, stations=stations, station_id=station_id)


################################################################################
@auth.requires(lambda: (auth.has_permission('view', 'alarm_log')))
def get_all_data_key(list_data=None):
  if not list_data:
    # data = db(db.station_indicator_exceed.id > 0).select()
    list_data = db(db.station_indicator_exceed.id > 0).select(
      db.station_indicator_exceed.station_indicator_exceed,
      db.station_indicator_exceed.id,
      orderby=~db.station_indicator_exceed.get_time,
      limitby=(0, 100)
    )

  lst_data_key = []
  for item in list_data:
    data = item.station_indicator_exceed if item.station_indicator_exceed else {}
    for ikey in data:
      if ikey not in lst_data_key:
        lst_data_key.append(ikey)
  return lst_data_key


@service.json
@auth.requires(lambda: (auth.has_permission('view', 'alarm_log')))
def get_list_data_alarm(*args, **kwargs):
  try:
    s_search = request.vars.sSearch
    # sometext = request.vars.sometext
    from_date = request.vars.from_date
    to_date = request.vars.to_date
    station_id = request.vars.station_id
    added_columns = request.vars.added_columns or ''
    if added_columns:
      added_columns = added_columns.split(',')
    iDisplayStart = int(request.vars.iDisplayStart)
    iDisplayLength = int(request.vars.iDisplayLength)
    aaData = []
    limitby = (iDisplayStart, iDisplayLength + 1)  # Tuple dung de phan trang (vtri bat dau - chieu dai)

    conditions = (db.station_indicator_exceed.id > 0)
    # Neu chuoi tim kiem khac rong thi them dieu kien truy van voi chuoi tim kiem
    # if sometext:
    # conditions &= (db.data_alarm.station_id.contains(sometext))
    if from_date:
      conditions &= (db.station_indicator_exceed.get_time >= date_util.string_to_datetime(from_date))
    if to_date:
      conditions &= (db.station_indicator_exceed.get_time < date_util.string_to_datetime(to_date) + timedelta(days=1))
    if station_id:
      conditions &= (db.station_indicator_exceed.station_id == station_id)
    # hungdx phan quyen quan ly trạm theo user issue 44
    if current_user:
      if not (auth.has_membership('admin') or auth.has_membership(const.GROUP_MANAGER)):
        list_station_manager = db(db.manager_stations.user_id == current_user.id). \
          select(db.manager_stations.station_id)
        station_ids = [str(item.station_id) for item in list_station_manager]
        conditions &= (db.station_indicator_exceed.station_id.belongs(station_ids))
    if added_columns:
      or_conditions =[]
      for column in added_columns:
        column_name = str(column)
        or_conditions.append({('station_indicator_exceed.'+column_name+'.is_exceed'): True})
      conditions &= {'$or': or_conditions}
    list_data = db(conditions).select(db.station_indicator_exceed.id,
                                      db.station_indicator_exceed.station_id,
                                      db.station_indicator_exceed.get_time,
                                      db.station_indicator_exceed.station_indicator_exceed,
                                      orderby=~db.station_indicator_exceed.get_time,
                                      limitby=limitby)
    # Tong so ban ghi khong thuc hien phan trang
    iTotalRecords = db(conditions).count()
    iRow = iDisplayStart + 1
    # indicators = db(db.indicators.id > 0).select(db.indicators.id, db.indicators.indicator, db.indicators.unit)
    # lst_data_key = get_all_data_key(list_data)
    lst_data_key = added_columns
    # Duyet tung phan tu trong mang du lieu vua truy van duoc
    stations_dict = common.get_station_dict()[0]
    levels = dict(db.alarm_logs.alarm_level.requires.options())

    for i, item in enumerate(list_data):
      # Check status to assign alert badge
      bg_color = '#EA3223'
      color = '#FFFFFF'
      # for al_key in const.ALARM_LOG_LEVEL:
      # if item.alarm_level == const.ALARM_LOG_LEVEL[al_key]['value']:
      # bg_color = const.ALARM_LOG_LEVEL[al_key]['color']
      # color = const.ALARM_LOG_LEVEL[al_key]['color2']
      # break
      # for al_key in const.ALARM_LEVEL:
      #     if item.alarm_level == const.ALARM_LEVEL[al_key]['value']:
      #         bg_color = const.ALARM_LEVEL[al_key]['color']
      #         color = const.ALARM_LEVEL[al_key]['color2']
      #         break
      row = [
        str(iDisplayStart + 1 + i),
        # A(item.station_id, _href = URL('', args = [item.id])),
        stations_dict[str(item.station_id)] if stations_dict.has_key(str(item.station_id)) else '',
        SPAN(T('High')
             , _style="background:%s; color:%s" % (bg_color, color), _class="badge"),
        item.get_time
      ]
      added_item = dict()
      if item.station_indicator_exceed:
        if added_columns:
          for data_key in lst_data_key:
            # i_id = str(indicator.id)
            i_name = str(data_key)
            current_indicator = item.station_indicator_exceed[i_name] if item.station_indicator_exceed.has_key(
              i_name) else ''
            if not current_indicator:
              added_item[i_name] = SPAN('-')
            else:
              try:
                v = float(current_indicator['value'])
                qcvn_detail_min_value = current_indicator['station_qcvn_min']
                qcvn_detail_max_value = current_indicator['station_qcvn_max']

                if qcvn_detail_min_value and qcvn_detail_max_value:
                  # So sanh <= ... <=
                  title = 'QCVN Min: %s' % qcvn_detail_min_value
                  title = title + ' - QCVN Max: %s' % qcvn_detail_max_value
                else:
                  if qcvn_detail_max_value:
                    title = 'QCVN Max: %s' % qcvn_detail_max_value
                  elif qcvn_detail_min_value:
                    title = 'QCVN Min: %s' % qcvn_detail_min_value
                  # c = getColorByIndicator(si_dict, i_id, v)
                c = common.getColorByIndicatorQcvn2(v, qcvn_detail_min_value, qcvn_detail_max_value)
                added_item[i_name] = SPAN("{0:.2f}".format(v), _style="background:%s; color:white" % c, _class="badge",
                                          _title=title)
              except:
                added_item[i_name] = SPAN('-')
      for column in added_columns:
        # for column in lst_data_key:
        if column and added_item.has_key(column):
          row.append(added_item[column])
      aaData.append(row)

    return dict(iTotalRecords=iTotalRecords, iTotalDisplayRecords=iTotalRecords, aaData=aaData, success=True)
  except Exception as ex:
    return dict(iTotalRecords=0, iTotalDisplayRecords=0, aaData=[], message=str(ex), success=False)


# def get_list_data_alarm(*args, **kwargs):
#     try:
#         s_search = request.vars.sSearch
#         # sometext = request.vars.sometext
#         from_date = request.vars.from_date
#         to_date = request.vars.to_date
#         station_id = request.vars.station_id
#         added_columns = request.vars.added_columns or ''
#         if added_columns:
#             added_columns = added_columns.split(',')
#         iDisplayStart = int(request.vars.iDisplayStart)
#         iDisplayLength = int(request.vars.iDisplayLength)
#         aaData = []
#         limitby = (iDisplayStart, iDisplayLength + 1)  # Tuple dung de phan trang (vtri bat dau - chieu dai)
#
#         conditions = (db.data_alarm.id > 0) and (db.data_alarm.alarm_level<2)
#         # Neu chuoi tim kiem khac rong thi them dieu kien truy van voi chuoi tim kiem
#         # if sometext:
#         # conditions &= (db.data_alarm.station_id.contains(sometext))
#         if from_date:
#             conditions &= (db.data_alarm.get_time >= date_util.string_to_datetime(from_date))
#         if to_date:
#             conditions &= (db.data_alarm.get_time < date_util.string_to_datetime(to_date) + timedelta(days=1))
#         if station_id:
#             conditions &= (db.data_alarm.station_id == station_id)
#         # hungdx phan quyen quan ly trạm theo user issue 44
#         if current_user:
#             if not (auth.has_membership('admin') or auth.has_membership(const.GROUP_MANAGER)):
#                 list_station_manager = db(db.manager_stations.user_id == current_user.id). \
#                     select(db.manager_stations.station_id)
#                 station_ids = [str(item.station_id) for item in list_station_manager]
#                 conditions &= (db.data_alarm.station_id.belongs(station_ids))
#
#         list_data = db(conditions).select(db.data_alarm.id,
#                                           db.data_alarm.station_id,
#                                           db.data_alarm.get_time,
#                                           db.data_alarm.alarm_level,
#                                           db.data_alarm.data,
#                                           orderby=~db.data_alarm.get_time,
#                                           limitby=limitby)
#         # Tong so ban ghi khong thuc hien phan trang
#         iTotalRecords = db(conditions).count()
#         iRow = iDisplayStart + 1
#         # indicators = db(db.indicators.id > 0).select(db.indicators.id, db.indicators.indicator, db.indicators.unit)
#         # lst_data_key = get_all_data_key(list_data)
#         lst_data_key = get_all_data_key()
#         # Duyet tung phan tu trong mang du lieu vua truy van duoc
#         stations_dict = common.get_station_dict()[0]
#         levels = dict(db.alarm_logs.alarm_level.requires.options())
#         for i, item in enumerate(list_data):
#             # Check status to assign alert badge
#             bg_color = '#FF9900'
#             color = '#FFFFFF'
#             # for al_key in const.ALARM_LOG_LEVEL:
#             # if item.alarm_level == const.ALARM_LOG_LEVEL[al_key]['value']:
#             # bg_color = const.ALARM_LOG_LEVEL[al_key]['color']
#             # color = const.ALARM_LOG_LEVEL[al_key]['color2']
#             # break
#             for al_key in const.ALARM_LEVEL:
#                 if item.alarm_level == const.ALARM_LEVEL[al_key]['value']:
#                     bg_color = const.ALARM_LEVEL[al_key]['color']
#                     color = const.ALARM_LEVEL[al_key]['color2']
#                     break
#             row = [
#                 str(iDisplayStart + 1 + i),
#                 # A(item.station_id, _href = URL('', args = [item.id])),
#                 stations_dict[str(item.station_id)] if stations_dict.has_key(str(item.station_id)) else '',
#                 SPAN(levels[str(item.alarm_level)]
#                      , _style="background:%s; color:%s" % (bg_color, color), _class="badge"),
#                 item.get_time
#             ]
#             added_item = dict()
#             if item.data:
#                 if added_columns:
#                     for data_key in lst_data_key:
#                         # i_id = str(indicator.id)
#                         i_name = str(data_key)
#                         v = ''
#                         v = item.data[i_name] if item.data.has_key(i_name) else ''
#                         if not v:
#                             added_item[i_name] = '-'
#                         else:
#                             try:
#                                 v = float(v)
#                                     #c = getColorByIndicator(si_dict, i_id, v)
#                                 c ="#99CC00"
#                                 added_item[i_name] = SPAN("{0:.2f}".format(v), _style="background:%s; color:white" %c, _class="badge")
#                             except:
#                                 added_item[i_name] = '-'
#             for column in added_columns:
#                 # for column in lst_data_key:
#                 if column and added_item.has_key(column):
#                     row.append(added_item[column])
#             aaData.append(row)
#
#         return dict(iTotalRecords=iTotalRecords, iTotalDisplayRecords=iTotalRecords, aaData=aaData, success=True)
#     except Exception as ex:
#         return dict(iTotalRecords=0, iTotalDisplayRecords=0, aaData=[], message=str(ex), success=False)
def export_excel_old():
  import os.path, openpyxl
  # get search parameters
  station_id = request.vars.station_id
  from_date = request.vars.from_date
  to_date = request.vars.to_date
  added_columns = request.vars.added_columns
  if added_columns:
    added_columns = added_columns.split(',')

  aaData = []

  conditions = (db.station_indicator_exceed.id > 0)
  if from_date:
    conditions &= (db.station_indicator_exceed.get_time >= date_util.string_to_datetime(from_date))
  if to_date:
    conditions &= (db.station_indicator_exceed.get_time < date_util.string_to_datetime(to_date) + timedelta(days=1))
  if station_id:
    conditions &= (db.station_indicator_exceed.station_id == station_id)
  if current_user:
    if not (auth.has_membership('admin') or auth.has_membership(const.GROUP_MANAGER)):
      list_station_manager = db(db.manager_stations.user_id == current_user.id). \
        select(db.manager_stations.station_id)
      station_ids = [str(item.station_id) for item in list_station_manager]
      conditions &= (db.station_indicator_exceed.station_id.belongs(station_ids))
  if added_columns:
    or_conditions =[]
    for column in added_columns:
      column_name = str(column)
      or_conditions.append({('station_indicator_exceed.'+column_name+'.is_exceed'): True})
    conditions &= {'$or': or_conditions}
  list_data = db(conditions).select(db.station_indicator_exceed.id,
                                    db.station_indicator_exceed.station_id,
                                    db.station_indicator_exceed.get_time,
                                    db.station_indicator_exceed.station_indicator_exceed,
                                    )

  stations_dict = common.get_station_dict()[0]
  iTotalRecords = db(conditions).count()
  lst_data_key = added_columns
  # write data
  for i, item in enumerate(list_data):
    # Check status to assign alert badge
    row = [
      str(1 + i),
      stations_dict[str(item.station_id)] if stations_dict.has_key(str(item.station_id)) else '',
      # SPAN(T('High')),
      'Vượt qui chuẩn',
      item.get_time,
    ]
    added_item = dict()
    if item.station_indicator_exceed:
      if added_columns:
        for data_key in lst_data_key:
          # i_id = str(indicator.id)
          i_name = str(data_key)
          current_indicator = item.station_indicator_exceed[i_name] if item.station_indicator_exceed.has_key(
            i_name) else ''
          if not current_indicator:
            added_item[i_name] = ('-')
          else:
            try:
              v = float(current_indicator['value'])
              qcvn_detail_min_value = current_indicator['station_qcvn_min']
              qcvn_detail_max_value = current_indicator['station_qcvn_max']

              if qcvn_detail_min_value and qcvn_detail_max_value:
                # So sanh <= ... <=
                title = 'QCVN Min: %s' % qcvn_detail_min_value
                title = title + ' - QCVN Max: %s' % qcvn_detail_max_value
              else:
                if qcvn_detail_max_value:
                  title = 'QCVN Max: %s' % qcvn_detail_max_value
                elif qcvn_detail_min_value:
                  title = 'QCVN Min: %s' % qcvn_detail_min_value
                # c = getColorByIndicator(si_dict, i_id, v)
              c = common.getColorByIndicatorQcvn2(v, qcvn_detail_min_value, qcvn_detail_max_value)
              added_item[i_name] = ("{0:.2f}".format(v))
            except:
              added_item[i_name] = ('-')
    for column in added_columns:
      # for column in lst_data_key:
      if column and added_item.has_key(column):
        row.append(added_item[column])
    aaData.append(row)

  wb2 = openpyxl.Workbook(write_only=True)
  ws2 = wb2.create_sheet()
  temp_headers = []
  headers = []
  temp_headers.append('#')
  temp_headers.append('Tên Trạm')
  temp_headers.append('Mức cảnh báo')
  temp_headers.append('Ngày giờ')
  for item in added_columns:
    temp_headers.append(str(item))
  headers.append(temp_headers)
  for header in headers:
    ws2.append(header)
  for row in aaData:
    ws2.append(row)

  file_name = request.now.strftime('Danh sách vượt qui chuẩn' + '_%Y%m%d_%H%M%S.xlsx')
  file_path = os.path.join(request.folder, 'static', 'export', file_name)
  # wb.save(file_path)
  wb2.save(file_path)

  data = open(file_path, "rb").read()
  os.unlink(file_path)
  response.headers['Content-Type'] = 'application/vnd.ms-excel'
  response.headers['Content-Disposition'] = 'attachment;filename=%s' % file_name

  return data


def export_excel():
  import os.path, openpyxl
  # get search parameters
  station_id = request.vars.station_id
  from_date = request.vars.from_date
  to_date = request.vars.to_date
  added_columns = request.vars.added_columns
  if added_columns:
    added_columns = added_columns.split(',')

  aaData = []

  conditions = (db.station_indicator_exceed.id > 0)
  if from_date:
    conditions &= (db.station_indicator_exceed.get_time >= date_util.string_to_datetime(from_date))
  if to_date:
    conditions &= (db.station_indicator_exceed.get_time < date_util.string_to_datetime(to_date) + timedelta(days=1))
  if station_id:
    conditions &= (db.station_indicator_exceed.station_id == station_id)
  if current_user:
    if not (auth.has_membership('admin') or auth.has_membership(const.GROUP_MANAGER)):
      list_station_manager = db(db.manager_stations.user_id == current_user.id). \
        select(db.manager_stations.station_id)
      station_ids = [str(item.station_id) for item in list_station_manager]
      conditions &= (db.station_indicator_exceed.station_id.belongs(station_ids))
  if added_columns:
    or_conditions =[]
    for column in added_columns:
      column_name = str(column)
      or_conditions.append({('station_indicator_exceed.'+column_name+'.is_exceed'): True})
    conditions &= {'$or': or_conditions}
  list_data = db(conditions).select(db.station_indicator_exceed.id,
                                    db.station_indicator_exceed.station_id,
                                    db.station_indicator_exceed.get_time,
                                    db.station_indicator_exceed.station_indicator_exceed,
                                    )

  stations_dict = common.get_station_dict()[0]
  iTotalRecords = db(conditions).count()
  lst_data_key = added_columns
  # write data

  # Print Headers
  headers = []
  header_arr = ['#', 'Tên Trạm', 'Mức cảnh báo', 'Ngày giờ'] + added_columns

  cols_dic = dict()
  start_row = 2
  col_d = []
  for i, m in enumerate(header_arr):
    if m in added_columns:
      cols_dic[u'{}'.format(m)] = i + 1
    col_d.append('-')
    headers.append(m)

  wb2 = openpyxl.Workbook()
  ws2 = wb2.active
  ws2.append(headers)
  if added_columns:
    for i, item in enumerate(list_data):
      row_ind = start_row + i
      ws2.append(col_d)
      ws2.cell(row_ind, 1, str(1+i))
      ws2.cell(row_ind, 2, stations_dict[str(item.station_id)] if stations_dict.has_key(str(item.station_id)) else '')
      ws2.cell(row_ind, 3, 'Vượt qui chuẩn')
      ws2.cell(row_ind, 4, item.get_time)
      # Check status to assign alert badge

      if item.station_indicator_exceed:
        for data_key in lst_data_key:
          # i_id = str(indicator.id)
          i_name = str(data_key)
          current_indicator = item.station_indicator_exceed[i_name] if item.station_indicator_exceed.has_key(i_name) else ''
          if current_indicator:
            try:
              v = float(current_indicator['value'])
              if cols_dic.has_key(u'{}'.format(i_name)):
                col_inx = cols_dic.get(u'{}'.format(i_name))
                ws2.cell(row_ind, col_inx, "{0:.2f}".format(v))
            except:
              pass

  file_name = request.now.strftime('Danh sách vượt qui chuẩn' + '_%Y%m%d_%H%M%S.xlsx')
  file_path = os.path.join(request.folder, 'static', 'export', file_name)
  wb2.save(file_path)

  data = open(file_path, "rb").read()
  os.unlink(file_path)
  response.headers['Content-Type'] = 'application/vnd.ms-excel'
  response.headers['Content-Disposition'] = 'attachment;filename=%s' % file_name

  return data
