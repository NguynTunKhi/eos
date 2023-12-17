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
import datetime
from datetime import datetime, timedelta

from applications.eos.modules import const


def si():
  session.forget()
  response.headers["Access-Control-Allow-Origin"] = '*'
  response.headers['Access-Control-Max-Age'] = 86400
  response.headers['Access-Control-Allow-Headers'] = '*'
  response.headers['Access-Control-Allow-Methods'] = '*'
  response.headers['Access-Control-Allow-Credentials'] = 'true'
  return service()


def set_where_tb_table(tb, conds, station_id, qi_time):
  cons = db[tb].station_id == station_id
  cons &= db[tb].get_time == qi_time
  if conds is None:
    conds = cons
  else:
    conds |= cons
  return conds


def get_data_by_conds(conds, tb):
  rs = dict()
  if conds is not None:
    rows_tm = db(conds).select(
      db[tb].get_time,
      db[tb].station_id,
      db[tb].data,
      orderby=~db[tb].get_time
    )
    for r in rows_tm:
      rs[r.station_id] = [{'get_time': r['get_time'], 'data': r['data']}]
  return rs
################################################################################
@service.json
def get_stations_for_map(*args, **kwargs):
  try:
    eip_config = db(db.eip_config.name == 'eip_config').select().first()
    try:
      p_now = datetime.now() - timedelta(hours=eip_config.time_public)
    except:
      p_now = datetime.now() - timedelta(hours=3)
    is_qi = True
    is_public = True
    station_type = 4
    stations_dict = {}
    conditions = (db.stations.id > 0)
    if is_qi:
      conditions &= (db.stations.is_qi == is_qi)
    if is_public:
      conditions &= (db.stations.is_public == is_public)
    if station_type:
      conditions &= (db.stations.station_type == station_type)
    conditions &= (db.stations.station_type.belongs(
      [const.STATION_TYPE['STACK_EMISSION']['value'], const.STATION_TYPE['AMBIENT_AIR']['value']]))
    rows = db(conditions).select(db.stations.ALL, orderby=db.stations.order_no)

    dt_format = '%Y-%m-%d %H:%M:%S'
    station_ids = []
    aqi_conds = None
    aqi_adj_conds = None
    for s in rows:
      station_id = str(s['id'])
      try:
        is_public_data_type = s['is_public_data_type']
      except:
        is_public_data_type = 2

      if is_public_data_type == 3:
        if not s.qi_time or s.qi_time < p_now:
          continue
        aqi_conds = set_where_tb_table('aqi_data_hour', aqi_conds, station_id, s.qi_time)
      else:
        if not s.qi_adjsut_time or s.qi_adjsut_time < p_now:
          continue
        aqi_adj_conds = set_where_tb_table('aqi_data_adjust_hour', aqi_adj_conds, station_id, s.qi_adjsut_time)
      station_ids.append(station_id)

    data_aqi = get_data_by_conds(aqi_conds, 'aqi_data_hour')
    data_aqi.update(get_data_by_conds(aqi_adj_conds, 'aqi_data_adjust_hour'))
    # Lay du lieu moi nhat
    r_data_lastest = db(db.data_lastest.station_id.belongs(station_ids)).select(db.data_lastest.data_status,
                                                                                db.data_lastest.station_id,
                                                                                db.data_lastest.get_time)
    dic_data_lastest = dict()
    for dl in r_data_lastest:
      data_status = dl['data_status']
      for key in data_status:
        try:
          value = float(data_status[key]['value'])
          if math.isnan(value) or value == -9999.0:
            value = None
        except:
          value = None
        data_status[key] = {
          'value': value,
          'unit': data_status[key]['unit'],
          'indicator_name': data_status[key]['indicator_name']
        }
      dic_data_lastest[dl['station_id']] = {'data_status': data_status, 'get_time': dl['get_time']}
    for row in rows:
      station_id = str(row['id'])
      try:
        is_public_data_type = row.is_public_data_type
      except:
        is_public_data_type = 2
      if is_public_data_type == 3:
        if not row.qi_time or row.qi_time < p_now:
          continue
        qi = row.qi if row.qi else '-'
        qi_time = row.qi_time.strftime(dt_format) if row.qi_time else ''
      else:
        if not row.qi_adjsut_time or row.qi_adjsut_time < p_now:
          continue
        qi = row.qi_adjust if row.qi_adjust else '-'
        qi_time = row.qi_adjsut_time.strftime(dt_format) if row.qi_adjsut_time else ''

      stations_dict[str(row.id)] = {
        'id': station_id,
        'province_id': row.province_id,
        'station_name': row.station_name,
        'data_aqi': data_aqi[station_id] if data_aqi.has_key(station_id) else [],
        'longitude': row.longitude,
        'latitude': row.latitude,
        'address': row.address,
        'data_source': row.data_source,
        'qi': qi,
        'qi_time': qi_time,
        'off_time': row.off_time.strftime(dt_format) if row.off_time else '',
        'status': row.status,
        'data_lastest': [dic_data_lastest[station_id]] if dic_data_lastest.has_key(station_id) else []
      }
    return dict(success=True, data=stations_dict.values())
  except Exception as ex:
    return dict(success=False, message=str(ex))


################################################################################
@service.json
def get_aqi_by_station(*args, **kwargs):
  try:
    station_id = request.vars.station_id
    from_date = request.vars.from_date
    to_date = request.vars.to_date
    type_time = int(request.vars.type_time)  # co 2 loai la NGAY va GIO (0 - la GIO, 1 la NGAY)
    from_date = datetime.strptime(from_date, '%Y-%m-%d %H:%M:%S')
    to_date = datetime.strptime(to_date, '%Y-%m-%d %H:%M:%S')

    queryIndicatorIsCal = (db.station_indicator.station_id == station_id)
    queryIndicatorIsCal &= (db.station_indicator.is_public == True)
    queryIndicatorIsCal &= (db.station_indicator.is_calc_qi == True)
    indicatorCal = db(queryIndicatorIsCal).select(db.station_indicator.is_public, db.station_indicator.is_calc_qi,
                                                  db.station_indicator.indicator_id, db.station_indicator.mapping_name)

    indicatorISCal = []
    for item in indicatorCal:
      indicatorId = item.indicator_id
      soureNameIndicator = db(db.indicators._id == indicatorId).select(db.indicators.source_name,
                                                                       db.indicators.indicator)
      indicatorISCal.append({
        'indicator_id': item.indicator_id,
        'mapping_name': item.mapping_name,
        'source_name': soureNameIndicator[0].source_name,
        'indicator': soureNameIndicator[0].indicator
      })

    data_return = dict()
    count = 0
    count_in_page = 0

    if type_time == 0:  # aqi adjust hour
      conditons_aqi_hour = (db.aqi_data_adjust_hour.station_id == station_id)
      conditons_aqi_hour &= (db.aqi_data_adjust_hour.get_time >= from_date)
      conditons_aqi_hour &= (db.aqi_data_adjust_hour.get_time <= to_date)
      data_return = db(conditons_aqi_hour).select(db.aqi_data_adjust_hour.get_time, db.aqi_data_adjust_hour.data,
                                                  orderby=~db.aqi_data_adjust_hour.get_time)
      count = db(conditons_aqi_hour).count()

    elif type_time == 1:  # aqi adjust day
      conditons_aqi_day = (db.aqi_data_adjust_24h.station_id == station_id)
      conditons_aqi_day &= (db.aqi_data_adjust_24h.get_time >= from_date)
      conditons_aqi_day &= (db.aqi_data_adjust_24h.get_time <= to_date)
      data_return = db(conditons_aqi_day).select(db.aqi_data_adjust_24h.get_time, db.aqi_data_adjust_24h.data_24h,
                                                 orderby=~db.aqi_data_adjust_24h.get_time)
      count = db(conditons_aqi_day).count()
    else:
      conditons_aqi_hour = (db.aqi_data_adjust_hour.station_id == station_id)
      conditons_aqi_hour &= (db.aqi_data_adjust_hour.get_time >= from_date)
      conditons_aqi_hour &= (db.aqi_data_adjust_hour.get_time <= to_date)
      data_return = db(conditons_aqi_hour).select(db.aqi_data_adjust_hour.get_time,
                                                  db.aqi_data_adjust_hour.data,
                                                  orderby=~db.aqi_data_adjust_hour.get_time)
      count = db(conditons_aqi_hour).count()

    if data_return:
      count_in_page = len(data_return)
    page_info = dict()
    page_info['count_all_item'] = count_in_page
    return dict(success=True, data=data_return, page_info=page_info, indicatorISCal=indicatorISCal)
  except Exception as ex:
    return dict(success=False, message=str(ex))


################################################################################

@service.json
def share_qi_data(*args, **kwargs):
  try:
    conds = db.stations.id > 0
    conds &= db.stations.is_public == True
    conds &= db.stations.station_type == 4
    conds &= db.stations.is_qi == True
    stations_public = db(conds).select(db.stations.ALL, orderby=db.stations.order_no)
    station_dic = {}

    conds_data_lastest = None

    query_aqi = None
    for station in stations_public:
      station_id = str(station.id)
      station_dic[station_id] = {
        'id': station_id,
        'key': station.station_code,
        'name': station.station_name,
        'coordinate': {
          'latitude': station.latitude,
          'longitude': station.longitude
        },
        'address': station['address'],
        'description': station['description'],
        'data_source': station['data_source'],
        'last_time': station['last_time']
      }

      if station['last_time']:
        last_time = station['last_time']
      elif station['qi_adjsut_time']:
        last_time = station['qi_adjsut_time']
      else:
        last_time = datetime.now() - timedelta(days=1)
      last_time = datetime(last_time.year, last_time.month, last_time.day, hour=0, minute=0)
      if station['qi_adjsut_time']:
        last_time = last_time.replace(hour=station['qi_adjsut_time'].hour)
      c = (db.data_lastest.id > 0)
      c &= (db.data_lastest.station_id == station_id)
      c &= (db.data_lastest.get_time >= last_time)
      if conds_data_lastest:
        conds_data_lastest |= c
      else:
        conds_data_lastest = c

      if station['qi_adjsut_time']:
        station_dic[str(station.id)]['qi'] = {
          'value': station['qi_adjust'],
          'time': station['qi_adjsut_time'],
        }
        qc = (db.aqi_data_adjust_hour.station_id == station_id)
        qc &= (db.aqi_data_adjust_hour.get_time == station.qi_adjsut_time)
        if query_aqi:
          query_aqi |= qc
        else:
          query_aqi = qc

    data = []
    data_lastest = None
    if conds_data_lastest:
      data_lastest = db(conds_data_lastest).select(db.data_lastest.get_time, db.data_lastest.data_status,
                                                   db.data_lastest.station_id,
                                                   orderby=db.data_lastest.station_id | ~db.data_lastest.get_time)
    data_lastest_dic = {}
    if data_lastest:
      for row in data_lastest:
        k = row.station_id
        d = {
          'time': row.get_time,
          'data': row.data_status
        }
        if not data_lastest_dic.get(k) or (data_lastest_dic[k] and d['time'] > data_lastest_dic[k]['time']):
          data_lastest_dic[k] = d

    aqi_dic = {}
    if query_aqi:
      rows = db(query_aqi).select(db.aqi_data_adjust_hour.get_time, db.aqi_data_adjust_hour.data,
                                  db.aqi_data_adjust_hour.station_id)
      for r in rows:
        d_tmp = {
          'time': r.get_time,
          'data': r.data
        }
        if not aqi_dic.get(r.station_id) or (aqi_dic[r.station_id] and d_tmp['time'] > aqi_dic[r.station_id]['time']):
          aqi_dic[r.station_id] = d_tmp
    for key in station_dic:
      if data_lastest_dic.get(key):
        station_dic[key]['data_realtime'] = data_lastest_dic[key]['data']
        station_dic[key]['last_time'] = data_lastest_dic[key]['time']
      if aqi_dic.get(key):
        station_dic[key]['qi_data_hour'] = aqi_dic[key]['data']
      data.append(station_dic[key])
    return dict(success=True, data=data)
  except Exception as e:
    print e.message
    return dict(message=e.message, success=False)


# --------- Thuan.Doan --------------- UPDATE API MOBILE ----------------------

def to_station_dict(station):
  return {
    'id': str(station.id),
    'province_id': station.province_id,
    'station_name': station.station_name,
    'longitude': station.longitude,
    'latitude': station.latitude,
    'address': station.address,
    'data_source': station.data_source,
    'status': station.status,
    'description': station.description,
    'last_time': station.last_time,
  }


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


@service.json
def get_stations_v2(*args, **kwargs):
  try:
    is_qi = True
    is_public = True
    station_type = 4
    stations = []
    conditions = (db.stations.id > 0)
    if is_qi:
      conditions &= (db.stations.is_qi == is_qi)
    if is_public:
      conditions &= (db.stations.is_public == is_public)
    if station_type:
      conditions &= (db.stations.station_type == station_type)
    rows = db(conditions).select(db.stations.ALL, orderby=db.stations.order_no)

    station_dic = {}
    realtime_dic = {}
    aqi_dic = {}

    cond_aqi = None
    cond_aqi_adjust = None

    cond_realtime = None

    # to station dict
    for row in rows:
      station_id = str(row.id)
      item = to_station_dict(row)
      if row.is_public_data_type == 3:  # data origin
        item['qi'] = row.qi
        item['qi_time'] = row.qi_time
        cond_aqi = create_where_data('aqi_data_hour', station_id, item['qi_time'], cond_aqi)
      else:  # data adjust
        item['qi'] = row.qi_adjust
        item['qi_time'] = row.qi_adjsut_time
        cond_aqi_adjust = create_where_data('aqi_data_adjust_hour', station_id, item['qi_time'], cond_aqi_adjust)
      station_dic[station_id] = item
      cond_realtime = create_where_data('data_lastest', station_id, item['qi_time'], cond_realtime)

    aqi_dic = to_array_dic('aqi_data_adjust_hour', cond_aqi_adjust, result=aqi_dic)
    aqi_dic = to_array_dic('aqi_data_hour', cond_aqi, result=aqi_dic)
    realtime_dic = to_array_dic('data_lastest', cond_realtime, result=realtime_dic, field_data='data_status')
    # station dict to list
    for key in station_dic:
      if aqi_dic.get(key):
        station_dic[key]['aqi_data_hour'] = aqi_dic[key]['data']
        station_dic[key]['aqi_time'] = aqi_dic[key]['time']

      if realtime_dic.get(key):
        station_dic[key]['data_lastest'] = realtime_dic[key]['data']
        station_dic[key]['time_lastest'] = realtime_dic[key]['time']
      stations.append(station_dic[key])
    return dict(success=True, data=stations)
  except Exception as ex:
    return dict(success=False, message=ex.message)




@service.json
def register_token_fcm(*args, **kwargs):
  try:
    body = request.vars
    data = None
    if body and body.has_key('token_fcm'):
      db.vnair_fcm_token.update_or_insert(db.vnair_fcm_token.token_fcm == body.token_fcm, **body)
      data = db(db.vnair_fcm_token.token_fcm == body.token_fcm).select(db.vnair_fcm_token.ALL).first()
    return dict(success=True, data=data)
  except Exception as ex:
    return dict(success=False, message=ex.message)


@service.json
def update_notify_status(*args, **kwargs):
  try:
    body = request.vars
    data = None
    if body and body.has_key('token_fcm'):
      db(db.vnair_fcm_token.token_fcm == body.token_fcm).update(is_notify=body.is_notify)
      data = db(db.vnair_fcm_token.token_fcm == body.token_fcm).select(db.vnair_fcm_token.ALL).first()
    return dict(success=True, data=data)
  except Exception as ex:
    return dict(success=False, message=ex.message)


@service.json
def aqi_station_favourites(*args, **kwargs):
  try:
    body = request.vars
    station_id = body.get('station_id')
    fcm = body.get('fcm')
    is_subscribe = body.get('is_subscribe')
    row = db(db.vnair_favourites.fcm == fcm).select(db.vnair_favourites.station_id).first()
    station_ids = []
    if row:
      station_ids = row.station_id
      station_ids = station_ids.split(";")
      if station_id and station_id in station_ids:
        station_ids.remove(station_id)

    if is_subscribe and station_id:
      station_ids.append(station_id)
    else:
      if station_id and station_id in station_ids:
        station_ids.remove(station_id)
    data = station_ids
    station_ids = ";".join(station_ids)
    if len(station_ids) > 0:
      db.vnair_favourites.update_or_insert(db.vnair_favourites.fcm == fcm, station_id=station_ids, fcm=fcm)
    else:
      db(db.vnair_favourites.fcm == fcm).delete()
    return dict(success=True, data=data)
  except Exception as ex:
    return dict(success=False, message=ex.message)


@service.json
def share_data_for_qtdk(*args, **kwargs):
  try:
    data = None
    station_code = request.vars.key
    date_time = datetime.strptime(request.vars.data_time, '%Y-%m-%d %H:%M')
    distance = 61
    table = 'data_adjust'
    if request.vars.data_type == 1:
      distance = 60
      table = 'data_hour_adjust'
    if request.vars.data_type == 2:
      date_time = datetime.strptime(request.vars.data_time, '%Y-%m-%d %H:%M').date()
      distance = 60 * 24
      table = 'data_day_adjust'
    from_time = date_time - timedelta(minutes=distance)
    to_time = date_time + timedelta(minutes=distance)
    cond_stations = (db.stations.id > 0)
    cond_stations &= (db.stations.station_code == station_code)
    station = db(cond_stations).select(db.stations.id).first()
    if station:
      station_id = str(station.id)
      conds = (db[table].id > 0)
      conds &= (db[table].station_id == station_id)
      conds &= (db[table].get_time >= from_time)
      conds &= (db[table].get_time <= to_time)
      rows = db(conds).select(db[table].get_time, db[table].data, orderby=~db[table].get_time)

      # Lấy phần tử gần nhất
      tmp = None

      for row in rows:
        if row.get_time >= date_time:
          dist = row.get_time - date_time
        else:
          dist = date_time - row.get_time
        if tmp is None or (dist.days <= tmp.days and dist.seconds <= tmp.seconds):
          tmp = dist
          data = row
    rs = None
    if data:
      rs = {'get_time': data['get_time'], 'data': {}}
      indicators = '{}'.format(request.vars['indicators']).split(',')
      for k in indicators:
        ind = u'{}'.format(k)
        try:
          if data['data'] and data['data'][ind] is not None:
            rs['data'][ind] = data['data'][ind]
        except:
          print ind

    return dict(success=True, data=rs)
  except Exception as ex:
    return dict(success=False, message=str(ex))
