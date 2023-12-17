# coding=utf-8
# encoding: utf-8
# encoding=utf8
# -*- coding: utf-8 -*-
###############################################################################
# Author :
# Date   :
#
# Description :
#
###############################################################################
import sys

reload(sys)
sys.setdefaultencoding('utf8')
from datetime import datetime, timedelta

from applications.eos.modules import const, common


def call():
  session.forget()
  response.headers["Access-Control-Allow-Origin"] = '*'
  response.headers['Access-Control-Max-Age'] = 86400
  response.headers['Access-Control-Allow-Headers'] = '*'
  response.headers['Access-Control-Allow-Methods'] = '*'
  response.headers['Access-Control-Allow-Credentials'] = 'true'
  return service()


def format_date_time(value, f='%Y-%m-%dT%H:%M:%S.%fZ'):
  try:
    return datetime.strptime(value, f)
  except:
    return None


def to_date_format(value, f='%Y-%m-%dT%H:%M:%S.%fZ'):
  try:
    return value.strftime(f)
  except:
    return None


def create_where_data(table, station_id, last_time, old_qurey):
  c = (db[table]['id'] > 0)
  c &= (db[table]['station_id'] == station_id)
  if last_time:
    c &= (db[table]['get_time'] >= last_time)
  if old_qurey:
    old_qurey |= c
  else:
    old_qurey = c
  return old_qurey


def to_array_dic(table, conds, field_data='data', result={}):
  if conds:
    rows = db(conds).select(
      db[table]['get_time'], db[table][field_data],
      db[table]['station_id'], orderby=db[table]['station_id'] | db[table]['get_time']
    )
    for row in rows:
      k = row.station_id
      d = {
        'time': row.get_time,
        'data': row[field_data]
      }
      if not result.get(k) or (result[k] and d['time'] > result[k]['time']):
        result[k] = d

  return result


################################################################################
@service.json
def stations(*args, **kwargs):
  try:
    station_type = request.vars.station_type
    if station_type is None:
      station_type = const.STATION_TYPE['AMBIENT_AIR']['value']
    time_public = common.get_public_time_air()
    stations_dict = {}
    conditions = (db.stations.id > 0)
    conditions &= (db.stations.is_public == True)
    if station_type == const.STATION_TYPE['AMBIENT_AIR']['value']:
      conditions &= (db.stations.station_type == const.STATION_TYPE['AMBIENT_AIR']['value'])
      if time_public:
        conditions &= (db.stations.qi_adjsut_time >= time_public)
    else:
      conditions &= (db.stations.station_type == station_type)
    rows = db(conditions).select(db.stations.ALL, orderby=db.stations.order_no)
    where = None
    aqi_day_dic = dict()
    station_ind_dic = dict()
    if station_type == const.STATION_TYPE['AMBIENT_AIR']['value']:
      for row in rows:
        if row.qi_adjsut_time:
          last_time_end = datetime(year=row.qi_adjsut_time.year, month=row.qi_adjsut_time.month,
                                   day=row.qi_adjsut_time.day) - timedelta(days=1)
          where = create_where_data('aqi_data_adjust_24h', str(row.id), last_time_end, where)

      aqi_day_dic = to_array_dic('aqi_data_adjust_24h', where, 'data_24h')

    station_ids = [str(it.id) for it in rows]
    #
    data_lastest_dic = dict()
    if const.STATION_TYPE['SURFACE_WATER']['value'] == station_type:
      data_lastest = db(db.data_lastest.station_id.belongs(station_ids)).select(
        db.data_lastest.station_id, db.data_lastest.get_time)
      for dl in data_lastest:
        if not data_lastest_dic.has_key(dl.station_id):
          data_lastest_dic[dl.station_id] = dl.get_time
    # if station_type != const.STATION_TYPE['AMBIENT_AIR']['value']:
    indicators = db(db.indicators.id > 0).select(db.indicators.ALL, orderby=db.indicators.indicator)
    indicators_dic = dict()
    for t in indicators:
      indicators_dic[str(t.id)] = t
    conds = db.station_indicator.station_id.belongs(station_ids)
    conds &= db.station_indicator.status == 1
    conds &= db.station_indicator.is_public == True
    station_inds = db(conds).select(db.station_indicator.ALL, orderby=db.station_indicator.station_id)
    for sd in station_inds:
      if not station_ind_dic.has_key(str(sd.station_id)):
        station_ind_dic[str(sd.station_id)] = []
      item_tmp = {'key': sd.mapping_name, 'name': sd.mapping_name,
                  'qcvn_detail_type_code': sd.qcvn_detail_type_code,
                  'qcvn_code': sd.qcvn_code, 'unit': sd.unit,
                  'qcvn_min_value': sd.qcvn_detail_min_value,
                  'qcvn_max_value': sd.qcvn_detail_max_value}

      if indicators_dic.has_key(str(sd.indicator_id)):
        item_tmp['name'] = indicators_dic[str(sd.indicator_id)]['indicator']

      station_ind_dic[str(sd.station_id)].append(item_tmp)

    for row in rows:
      try:
        is_public_data_type = row.is_public_data_type
      except:
        is_public_data_type = 2

      if is_public_data_type == 3:
        qi = round(row.qi) if row.qi else '-'
        qi_time = to_date_format(row.qi_time) if row.qi_time else ''
      else:
        qi = int(round(row.qi_adjust, 0)) if row.qi_adjust else '-'
        qi_time = to_date_format(row.qi_adjsut_time) if row.qi_adjsut_time else ''

      qi_day, qi_day_time = None, None
      try:
        qi_day_time = to_date_format(aqi_day_dic[str(row.id)]['time'])
        qi_day = round(aqi_day_dic[str(row.id)]['data']['aqi'])
      except:
        pass

      data_tmp = {
        'indicators': station_ind_dic[str(row.id)] if station_ind_dic.has_key(str(row.id)) else [],
        'id': str(row.id),
        'station_code': row.station_code,
        'station_name': row.station_name,
        'last_time': to_date_format(row.last_time) if row.last_time else '',
        'qi': qi,
        'qi_time': qi_time,
        'longitude': row.longitude,
        'latitude': row.latitude,
        'address': row.address,
        'is_public_data_type': is_public_data_type,
        'order_no': row.order_no,
        'qi_day': qi_day,
        'qi_day_time': qi_day_time,
        'status': row.status,
      }
      if const.STATION_TYPE['SURFACE_WATER']['value'] == station_type:
        if data_lastest_dic.has_key(str(row.id)):
          data_tmp['last_time'] = to_date_format(data_lastest_dic[str(row.id)])

      stations_dict[str(row.id)] = data_tmp
    ls = stations_dict.values()



    if station_type == const.STATION_TYPE['AMBIENT_AIR']['value']:
      new_list = []

      def myFunc(e):
        return e['qi']

      ls.sort(key=myFunc, reverse=True)
      inx = 0
      qi_old = -1
      for item in ls:
        rank = None
        if item.has_key('qi') and item['qi'] != '-':
          if qi_old != item['qi']:
            qi_old = item['qi']
            inx += 1
          rank = inx
        item['rank'] = rank
        new_list.append(item)
    else:
      new_list = ls

    return dict(success=True, data=new_list)
  except Exception as ex:
    return dict(success=False, message=str(ex))


@service.json
def data(*args, **kwargs):
  try:
    station_id = request.vars.get('station_id', None)
    indicators = request.vars.get('indicators', [])
    if station_id is None:
      return dict(success=False, message='Station Id Is Null')

    time_now = datetime.now() - timedelta(days=90)
    station = db(db.stations.id == station_id).select(db.stations.last_time).first()
    if station:
      last_t = station.last_time
      last_t = datetime(year=last_t.year, month=last_t.month, day=last_t.day, hour=23, minute=59)
      time_now = last_t - timedelta(days=90)
    conditions = db.data_adjust.id > 0
    conditions &= db.data_adjust.station_id == station_id
    conditions &= db.data_adjust.get_time > time_now
    rows = db(conditions).select(db.data_adjust.get_time, db.data_adjust.data, orderby=~db.data_adjust.get_time,
                                 limitby=(0, 121))

    data = []
    for row in rows:
      tmp = dict()
      try:
        tmp['time'] = to_date_format(row.get_time)
        for ind in indicators:
          try:
            if row.data and row.data.has_key(ind):
              tmp[ind] = row.data.get(ind)
          except:
            tmp[ind] = 'errr'
            pass
        data.append(tmp)
      except:
        pass

    return dict(success=True, data=data)
  except Exception as ex:
    return dict(success=False, message=str(ex))


def get_data(tb, station_id, time_now, field=None):
  try:
    conditions = db[tb].station_id == station_id
    conditions &= db[tb].get_time <= time_now
    conditions &= db[tb].get_time >= time_now - timedelta(hours=24)
    rs = db(conditions).select(db[tb].ALL, orderby=~db[tb].get_time, limitby=(0, 1)).first()
    if rs is None:
      return dict()

    if field:
      return rs.get(field, dict)
    return rs
  except:
    return dict()


@service.json
def aqi_day(*args, **kwargs):
  try:
    station_id = request.vars.get('station_id', None)
    if station_id is None:
      return dict(success=False, message='Station Id Is Null')
    time_now = datetime.now()
    station = db(db.stations.id == station_id).select(db.stations.last_time).first()
    if station:
      last_t = station.last_time
      last_t = datetime(year=last_t.year, month=last_t.month, day=last_t.day, hour=time_now.hour,
                        minute=time_now.minute)
      time_now = last_t

    aqi_day = get_data('aqi_data_adjust_24h', station_id, datetime(year=last_t.year, month=last_t.month,
                                                                   day=last_t.day, hour=0, minute=0))
    data_min = get_data('data_adjust', station_id, time_now, 'data')
    aqi_hour = get_data('aqi_data_adjust_hour', station_id, time_now, 'data')
    data = aqi_day
    if aqi_day is None:
      data = dict(station_id=station_id)
    data['data_min'] = data_min
    data['aqi_hour'] = aqi_hour
    if data.has_key('get_time'):
      data['get_time'] = to_date_format(data.get_time)

    return dict(success=True, data=data)
  except Exception as ex:
    return dict(success=False, message=str(ex))


@service.json
def data_hour_of_day(*args, **kwargs):
  try:
    station_id = request.vars.get('station_id', None)
    if station_id is None:
      return dict(success=False, message='Station Id Is Null')

    time_now = datetime.now() - timedelta(hours=32)
    station = db(db.stations.id == station_id).select(db.stations.last_time).first()
    if station:
      last_t = station.last_time
      last_t = datetime(year=last_t.year, month=last_t.month, day=last_t.day, hour=time_now.hour,
                        minute=time_now.minute)
      time_now = last_t - timedelta(hours=32)
    conditions = db.data_hour_adjust.id > 0
    conditions &= db.data_hour_adjust.station_id == station_id
    conditions &= db.data_hour_adjust.get_time > time_now
    rows = db(conditions).select(db.data_hour_adjust.get_time, db.data_hour_adjust.data,
                                 orderby=db.data_hour_adjust.get_time, limitby=(0, 25))
    data = []
    for r in rows:
      if r.get_time:
        r['get_time'] = to_date_format(r.get_time)
      data.append(r)

    return dict(success=True, data=data)
  except Exception as ex:
    return dict(success=False, message=str(ex))


@service.json
def v2_data_hour_of_day(*args, **kwargs):
  try:
    station_id = request.vars.get('station_id', None)
    if station_id is None:
      return dict(success=False, message='Station Id Is Null')

    time_end = datetime.now()
    if request.vars.get('time', None) is not None:
      time_end = format_date_time(request.vars.get('time'))
    time_s = datetime(year=time_end.year, month=time_end.month, day=time_end.day, hour=0, minute=0)
    conditions = db.data_hour_adjust.id > 0
    conditions &= db.data_hour_adjust.station_id == station_id
    conditions &= db.data_hour_adjust.get_time <= time_end
    conditions &= db.data_hour_adjust.get_time > time_s

    rows = db(conditions).select(db.data_hour_adjust.get_time, db.data_hour_adjust.data,
                                 orderby=db.data_hour_adjust.get_time, limitby=(0, 25))
    data = []
    for r in rows:
      if r.get_time:
        r['get_time'] = to_date_format(r.get_time)
      data.append(r)

    return dict(success=True, data=data, a=len(data))
  except Exception as ex:
    return dict(success=False, message=str(ex))


@service.json
def idh_data(*args, **kwargs):
  try:
    station_id = request.vars.get('station_id', None)
    if station_id is None:
      return dict(success=False, message='Station Id Is Null')
    data_lastest = db(db.data_lastest.station_id == station_id).select().first()
    time_end = datetime.now()

    data_type = request.vars.get('data_type', 2)
    tb = 'data_adjust'
    if data_type == 2:
      tb = 'data_hour_adjust'

    if data_lastest:
      time_s = data_lastest.get_time
    else:
      time_s = datetime(year=time_end.year, month=time_end.month, day=time_end.day, hour=23, minute=59)
    time_end = time_s - timedelta(hours=12)
    conditions = db[tb].id > 0
    conditions &= db[tb].station_id == station_id
    conditions &= db[tb].get_time > time_end

    rows = db(conditions).select(db[tb].get_time, db[tb].data, orderby=db[tb].get_time)
    data = []
    for r in rows:
      if r.get_time:
        r['get_time'] = to_date_format(r.get_time)
      data.append(r)
    return dict(success=True, data=data)
  except Exception as ex:
    return dict(success=False, message=str(ex))


def is_exceed(item):
  if isinstance(item['value'], str):
    return False
  if item['min'] is not None and item['max'] is not None:
    return item['max'] < item['value'] or item['value'] < item['min']
  elif item['max'] is not None:
    return item['max'] < item['value']
  elif item['min'] is not None:
    return item['value'] < item['min']
  return False


@service.json
def idh_data_lastest(*args, **kwargs):
  try:
    station_id = request.vars.get('station_id', None)
    if station_id is None:
      return dict(success=False, message='Station Id Is Null')

    conds = db.station_indicator.station_id == station_id
    conds &= db.station_indicator.status == 1
    conds &= db.station_indicator.is_public == True
    station_inds = db(conds).select(db.station_indicator.ALL, orderby=db.station_indicator.station_id)
    station_ind_ids = []
    indicators_dic = dict()
    for r in station_inds:
      station_ind_ids.append(r.indicator_id)
      indicators_dic[str(r.indicator_id)] = {
        'min': r.qcvn_detail_min_value, 'max': r.qcvn_detail_max_value,
        'qcvn': r.qcvn_code, 'qcvn_code': r.qcvn_detail_type_code,
        'unit': r.unit, 'name': r.mapping_name, 'value': '-',
        'exceed': False
      }
    indicators = db(db.indicators.id.belongs(station_ind_ids)).select(db.indicators.ALL,
                                                                      orderby=db.indicators.indicator)

    for t in indicators:
      if indicators_dic.has_key(str(t.id)):
        indicators_dic[str(t.id)]['name'] = u'{}'.format(t.indicator.encode('utf-8'))

    data_lastest = db(db.data_lastest.station_id == station_id).select().first()
    time_end = datetime.now()

    data_type = request.vars.get('data_type', 2)
    tb = 'data_adjust'
    if data_type == 2:
      tb = 'data_hour_adjust'

    if data_lastest:
      time_s = data_lastest.get_time
    else:
      time_s = datetime(year=time_end.year, month=time_end.month, day=time_end.day, hour=23, minute=59)
    time_end = time_s - timedelta(hours=12)
    conditions = db[tb].id > 0
    conditions &= db[tb].station_id == station_id
    conditions &= db[tb].get_time > time_end

    rows = db(conditions).select(db[tb].get_time, db[tb].data, orderby=~db[tb].get_time).first()
    if rows:
      for ind_id in indicators_dic:
        ind_tmp = indicators_dic[ind_id]
        indicator = ind_tmp['name']
        if rows.data.has_key(indicator):
          indicators_dic[ind_id]['value'] = rows.data[indicator]
          indicators_dic[ind_id]['exceed'] = is_exceed(indicators_dic[ind_id])  # rows.data[ind_tmp['name']]

    return dict(success=True, data=indicators_dic.values())
  except Exception as ex:
    return dict(success=False, message=str(ex))
