# -*- coding: utf-8 -*-
###############################################################################
# Author : ThuanDoan
# Date   : 2021-03-04
#
# Description : create API for mobile - Dehan
#
###############################################################################

from applications.eos.modules.const import STATION_STATUS, STATION_TYPE
import requests
from pymongo import MongoClient

APP = {'QTDK': 'QTDK', 'QTTD': 'QTTD', 'QLTNN': 'QLTNN', 'AQI': 'AQI', 'WQI': 'WQI'}
#API_QTDK = 'http://qtdk-hg-api.dulieutnmt.vn'
API_QTDK = 'http://192.168.101.31:5377'

TOKEN_QTDK = 'eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpYXQiOjE2MTUzNDcyMzcsImV4cCI6MTY0Njg4MzIzNywic3ViIjoiNWQ2NTRkYWU4YjVhNDY5ZTUzMTVmNDMwIiwicmV2b2tlZCI6IlIxNjE0In0.2eGIproyw5xInLBY77q6MNCz_0om1FdtHr-UNIM9-28'

#rmos = MongoClient('mongodb://192.168.101.35:27702/rmos')['rmos']
rmos = MongoClient('mongodb://hg-mongo/rmos')['rmos']

QTTD_STATION_STATUS = {
  '0': 'GOOD',
  '1': 'TENDENCY',
  '2': 'PREPARING',
  '3': 'EXCEED',
  '4': 'OFFLINE',
  '5': 'ADJUSTING',
  '6': 'ERROR'
}

QTTD_STATION_STATUS_REVERSE = {
  'GOOD': '0',
  'TENDENCY': '1',
  'PREPARING': '2',
  'EXCEED': '3',
  'OFFLINE': '4',
  'ADJUSTING': '5',
  'ERROR': '6'
}

AQI_LEVEL = {
  'GOOD': {'from': 0.0, 'to': 50.5},
  'MODERATE': {'from': 50.5, 'to': 100.5},
  'BAD': {'from': 100.5, 'to': 150.5},
  'UNHEALTHY': {'from': 150.5, 'to': 200.5},
  'VERY_UNHEALTHY': {'from': 200.5, 'to': 300.5},
  'HAZARDOUS': {'from': 300.5, 'to': 500.5}
}

def call():
  session.forget()
  response.headers['Access-Control-Allow-Origin'] = '*'
  response.headers['Access-Control-Max-Age'] = 86400
  response.headers['Access-Control-Allow-Headers'] = '*'
  response.headers['Access-Control-Allow-Methods'] = '*'
  response.headers['Access-Control-Allow-Credentials'] = 'true'
  return service()

def dashboard_qttd():
  stations = db(db.stations.id > 0).select(db.stations.status)
  item_dic = {'GOOD': 0, 'EXCEED': 0, 'OFFLINE': 0, 'ADJUSTING': 0, 'ERROR': 0, 'total': 0}
  for s in stations:
    item_dic['total'] += 1
    if STATION_STATUS['OFFLINE']['value'] == s['status']:
      item_dic['OFFLINE'] += 1
    elif s['status'] in [STATION_STATUS['TENDENCY']['value'], STATION_STATUS['GOOD']['value'],
                         STATION_STATUS['PREPARING']['value']]:
      item_dic['GOOD'] += 1
    elif STATION_STATUS['ADJUSTING']['value'] == s['status']:
      item_dic['ADJUSTING'] += 1
    elif STATION_STATUS['ERROR']['value'] == s['status']:
      item_dic['ERROR'] += 1
    elif STATION_STATUS['EXCEED']['value'] == s['status']:
      item_dic['EXCEED'] += 1
  items = []
  for i_key in item_dic:
    if not i_key is 'total':
      items.append(
        {'status': i_key, 'value': item_dic[i_key],
         'percent': round(float(item_dic[i_key]) / float(item_dic['total']) * 100.0, 2)})

  return {'key': APP['QTTD'], 'total': item_dic['total'], 'items': items,
          'chart': {'current': item_dic['OFFLINE'], 'total': item_dic['total'], 'title': 'OFFLINE'}}

def dashboard_qtdk():
  item_ic = {'NOT_YET': 0, 'TOTAL': 0, 'GOOD': 0, 'EXCEEDED': 0}
  items = []
  uri = '%s/data/statistic-by-station-type' % (API_QTDK,)
  rs = requests.post(uri, headers={'authorization': 'bearer %s' % TOKEN_QTDK}, verify=False, timeout=5)
  data = rs.json()
  rows = []
  if data['success']:
    rows = data['data']
  if rows:
    for i in rows:
      item_ic['TOTAL'] = item_ic['TOTAL'] + i['total']
      item_ic['NOT_YET'] = item_ic['NOT_YET'] + i['Not Yet']
      item_ic['GOOD'] = item_ic['GOOD'] + i['Good']
      item_ic['EXCEEDED'] = item_ic['EXCEEDED'] + i['Exceeded']
  for ii in item_ic:
    if ii != 'TOTAL':
       item_tmp = dict()
       item_tmp['status'] = ii
       item_tmp['percent'] = round((float(item_ic[ii]) / float(item_ic['TOTAL'])*100), 2)
       item_tmp['value'] = item_ic[ii]
       items.append(item_tmp)
  return {'key': APP['QTDK'],
          'total': item_ic['TOTAL'],
          'items': items,
          'chart': {'current': item_ic['TOTAL'] - item_ic['NOT_YET'], 'total': item_ic['TOTAL'], 'title': 'DONE_PATTERN'}}

#################################################################################

def dashboard_qltnn():
  stations = rmos.stations.find({})
  item_dic = {'GOOD': 0, 'EXCEED': 0, 'OFFLINE': 0, 'ADJUSTING': 0, 'ERROR': 0, 'total': 0}
  for s in stations:
    item_dic['total'] += 1
    if STATION_STATUS['OFFLINE']['value'] == s['status']:
      item_dic['OFFLINE'] += 1
    elif s['status'] in [STATION_STATUS['TENDENCY']['value'], STATION_STATUS['GOOD']['value'],
                         STATION_STATUS['PREPARING']['value']]:
      item_dic['GOOD'] += 1
    elif STATION_STATUS['ADJUSTING']['value'] == s['status']:
      item_dic['ADJUSTING'] += 1
    elif STATION_STATUS['ERROR']['value'] == s['status']:
      item_dic['ERROR'] += 1
    elif STATION_STATUS['EXCEED']['value'] == s['status']:
      item_dic['EXCEED'] += 1
  items = []
  for i_key in item_dic:
    if not i_key is 'total':
      items.append(
        {'status': i_key, 'value': item_dic[i_key],
         'percent': round(float(item_dic[i_key]) / float(item_dic['total']) * 100.0, 2)})

  return {'key': APP['QLTNN'], 'total': item_dic['total'], 'items': items,
          'chart': {'current': item_dic['OFFLINE'], 'total': item_dic['total'], 'title': 'OFFLINE'}}

################################################################################

@service.json
def dashboard(*args, **kwargs):
  data = []
  # Lấy thông tin quan trắc tự động
  qttd = dashboard_qttd()
  data.append(qttd)
  # QTDK
  qtdk = dashboard_qtdk()
  data.append(qtdk)
  # Quan ly tai nguyen nuoc
  ttn = dashboard_qltnn()
  data.append(ttn)
  return dict(success=True, data=data)

@service.json
def details(*args, **kwargs):
  key = kwargs.get('key', '')
  station_types = kwargs.get('station_types', [])
  data_types = kwargs.get('data_types', [])
  page_size = kwargs.get('page_size', 10)
  page = kwargs.get('page', 1)
  item_start = (page - 1) * page_size

  total = 0
  current = 0
  items = []

  if key == APP['QTTD']:
    total, current, items = detail_qttd(item_start, page_size, station_types, data_types)
  elif key == APP['QTDK']:
    total, current, items = detail_qtdk(item_start, page_size, station_types, data_types)
  return dict(success=True, data=items, page_info={'total': total, 'current': current, 'page': page, 'page_size': page_size})

def detail_qtdk(item_start, page_size, station_types, data_types):
  params = {'item_start': item_start, 'page_size': page_size, 'station_types': station_types, 'data_types': data_types}
  total = 0
  current = 0
  items = []
  uri = '%s/data/details' % (API_QTDK,)
  rs = requests.post(uri, headers={'authorization': 'bearer %s' % TOKEN_QTDK}, json=params, verify=False, timeout=5)
  data = rs.json()

  if data['success']:
    items = data['data']
  current = len(data['data'])
  return total, current, items

def detail_qttd(item_start, page_size, station_types, data_types):
  items = []
  new_data_types = []
  current = 0
  limitby = (item_start, page_size + 1)
  conditions = db.stations.id > 0

  if station_types:
    conditions &= db.stations.station_type.belongs(station_types)

  if data_types:
    for data_type in data_types:
      new_data_types.append(QTTD_STATION_STATUS_REVERSE[str(data_type)])
    conditions &= db.stations.status.belongs(new_data_types)

  stations = db(conditions).select(db.stations.ALL, orderby=db.stations.station_name,limitby=limitby)

  ids = [str(s.id) for s in stations]

  conditions_data_lastest = db.data_lastest.station_id.belongs(ids)

  data_lastest = db(conditions_data_lastest).select(db.data_lastest.data_status,
                                                          db.data_lastest.station_id,
                                                          db.data_lastest.get_time)
  total = db(conditions).count()

  data_lastest_dict = dict()
  for d in data_lastest:
    if not data_lastest_dict.has_key(str(d['station_id'])):
      data_lastest_dict[str(d['station_id'])] = {'get_time': d['get_time'], 'indicators': []}
      for in_key in d['data_status']:
        s_key = str(d['data_status'][in_key]['status'])
        data_lastest_dict[str(d['station_id'])]['indicators'].append({
          'name': in_key,
          'code': in_key,
          'value': d['data_status'][in_key]['value'],
          'status': QTTD_STATION_STATUS[s_key] if QTTD_STATION_STATUS.has_key(s_key) else ''
        })
  for s in stations:
    item = {
      'name': s['station_name'],
      'code': s['station_code'],
      'indicators': None,
    }
    try:
      s_key = str(s['status'])
      item['status'] = QTTD_STATION_STATUS[s_key] if QTTD_STATION_STATUS.has_key(s_key) else ''
      if data_lastest_dict.has_key(str(s['id'])):
        item['get_time'] = data_lastest_dict[str(s['id'])]['get_time']
        item['indicators'] = data_lastest_dict[str(s['id'])]['indicators']
    except:
      pass
    if item['indicators']:
      current += 1
      items.append(item)
  return total, current, items

# '''
#   MAPS API
# '''

def map_aqi(data_types):
  conditions = db.stations.id > 0
  conditions &= db.stations.is_qi == True
  # conditions &= db.stations.is_public == True
  conditions &= db.stations.station_type == STATION_TYPE['AMBIENT_AIR']['value']
  if data_types:
    conditions_data_types = None #(db.stations.qi_adjust >= AQI_LEVEL[data_types[0]['from']]) & (db.stations.qi_adjust <= AQI_LEVEL[data_types[0]['to']])
    for data_type in data_types:
      _to = AQI_LEVEL[data_type]['to']
      _from = AQI_LEVEL[data_type]['from']
      if conditions_data_types is None:
        conditions_data_types = (db.stations.qi_adjust >= _from) & (db.stations.qi_adjust < _to)
      else:
        conditions_data_types |= (db.stations.qi_adjust >= _from) & (db.stations.qi_adjust < _to)

    if not conditions_data_types is None:
      conditions &= conditions_data_types
  rows = db(conditions).select(db.stations.ALL, orderby=~db.stations.qi_adjsut_time | db.stations.qi_adjust)

  items = []
  total = 0
  for row in rows:
    total += 1
    items.append({
      'id': str(row.id),
      'name': row['station_name'],
      'code': row['station_code'],
      'address': row['address'],
      'value': round(row['qi_adjust'], 0),
      'get_time': row['qi_adjsut_time'],
      'longitude': row['longitude'],
      'latitude': row['latitude']
    })

  return {
    'total': total,
    'items': items
  }


def to_obj_value(obj, keys):
  value = obj
  try:
    for k in keys:
      if value and k in value:
        value = value[k]
  except:
    value = None
    pass
  if isinstance(value, dict):
    return ''
  return value


def map_wqi():
  uri = '%s/wqi/data-map' % (API_QTDK,)
  items = []
  total = 0
  rs = requests.post(uri, headers={'authorization': 'bearer %s' % TOKEN_QTDK}, verify=False, timeout=5)
  data = rs.json()
  rows = []
  if data['success']:
    rows = data['data']

  for row in rows:
    total += 1
    tmp = {
      'id': str(row['_id']),
      'name': to_obj_value(row, ['station', 'name']),
      'code': to_obj_value(row, ['key']),
      'address': row['address'],
      'value': round(row['value'], 0),
      'get_time': to_obj_value(row, ['plan', 'years']),
      'longitude': round(to_obj_value(row, ['coordinate', 'long']), 6),
      'latitude': round(to_obj_value(row, ['coordinate', 'lat']), 6),
    }
    # tmp['name'] = ''

    # tmp['name'] = ''
    items.append(tmp)

  return {
    'total': total,
    'items': items
  }


@service.json
def maps(*args, **kwargs):
  key = kwargs.get('key', '')
  station_types = kwargs.get('station_types', [])
  data_types = kwargs.get('data_types', [])
  data = {'items': [], 'total': 0}
  if key == APP['AQI']:
    data = map_aqi(data_types)
  elif key == APP['WQI']:
    data = map_wqi()
  elif key == APP['QLTNN']:
    pass  # TODO tai nguyen nước

  return dict(success=True, data=data['items'], total=data['total'])


# '''
#   Notification API
# '''

@service.json
def notifications_info(*args, **kwargs):
  data = [{'key': APP['QTTD'], 'unread': 0},
              {'key': APP['QLTNN'], 'unread': 4}]
  data.append(get_notifications_info_qtdk())
  return dict(success=True, data=data)

# @service.json
def get_notifications_info_qtdk():
  dict_info = dict()
  dict_info['key'] = APP['QTDK']
  dict_info['unread'] = len(get_notifications_data_qtdk())
  return dict_info

def get_notifications_data_qtdk():

  uri = '%s/data/notifications' % (API_QTDK,)
  # uri = 'http://localhost:5003/data/notifications'
  rs = requests.post(uri, headers={'authorization': 'bearer %s' % TOKEN_QTDK}, verify=False, timeout=5)
  data = rs.json()
  rows = []
  if data['success']:
    rows = data['data']
  return rows

@service.json
def notifications_by(*args, **kwargs):
  key = kwargs.get('key', '')
  data = {
    'unread': 1,
    'items': [
      {
        "id": 'id-record',
        'title': 'Trạm mất kết nối',
        'content': 'Trạm không khí Cửa khẩu Thanh Thủy (KK)',
        'is_read': True,
        'time': '2020-08-31 00:00:00.000Z'
      }
    ]
  }
  if key == APP['QTTD']:
    pass
  elif key == APP['QTDK']:
    data = get_notifications_data_qtdk()
  elif key == APP['QLTNN']:
    pass

  return dict(success=True, data=data)

'''
Station types QTDK - QTDK
'''
@service.json
def station_types_qttd():
  station_types = {}
  rows= []
  rows = db().select(db.station_types.code,db.station_types.station_type)

  for row in rows:
    station_types[row['code']] = row['station_type']

  return station_types

#######################################################################################################

def station_types_qtdk():
  uri = '%s/station-types' % (API_QTDK,)
  station_types = {}
  rs = requests.get(uri, headers={'authorization': 'bearer %s' % TOKEN_QTDK}, verify=False, timeout=5)
  data = rs.json()
  rows = []

  if data['success']:
    rows = data['data']

  for row in rows:
    station_types[row['key']] = row['name']

  return station_types

'''
Settings API
'''

@service.json
def settings(*args, **kwargs):
  vi = {
    'AQI': {
      'title': 'Chỉ số chất lượng không khí',
      'data_types': {
        'GOOD': {
          'name': 'Tốt',
          'color': '#00E400',
          'content': 'Chất lượng không khí tốt, không ảnh hưởng tới sức khỏe'
        },
        'MODERATE': {
          'name': 'Trung bình',
          'color': '#FFFF00',
          'content': 'Chất lượng không khí ở mức chấp nhận được. Tuy nhiên, đối với những người nhạy cảm (Người già, trẻ em, người mắc các bệnh hô hấp tim mạnh...) có thể chịu những tác động nhất định tới sức khỏe.'
        },
        'BAD': {
          'name': 'Kém',
          'color': '#FF7E00',
          'content': 'Những người nhạy cảm gặp phải các vấn đề về sức khỏe, những người bình thường ít ảnh hưởng.'
        },
        'UNHEALTHY': {
          'name': 'Xấu',
          'color': '#FF0000',
          'content': 'Những người bình thường bắt đầu có các ảnh hưởng tới sức khỏe, nhóm người nhạy cảm có thể gặp những vấn đề về sức khỏe nghiêm trọng hơn'
        },
        'VERY_UNHEALTHY': {
          'name': 'Rất xấu',
          'color': '#8F3F97',
          'content': 'Cảnh báo hưởng tới sức khỏe: mọi người bị ảnh hưởng tới sức khỏe nghiêm trọng hơn.'
        },
        'HAZARDOUS': {
          'name': 'Nguy hại',
          'color': '#7E0000',
          'content': 'Cảnh báo khẩn cấp về sức khỏe: Toàn bộ dân số bị ảnh hưởng tới sức khỏe nghiêm trọng.'
        }
      }
    },
    'WQI': {
      'title': 'Chỉ số chất lượng nước',
      'data_types': {
        'VERRY_GOOD': {
          'name': 'Rất tốt',
          'content': 'Sử dụng tốt cho mục đích cấp nước sinh hoạt',
          'color': '#3333FF',
          'text_color': '#FFFFFF'
        },
        'GOOD': {
          'name': 'Tốt',
          'content': 'Sử dụng cho mục đích cấp nước sinh hoạt nhưng cần các biện pháp xử lý phù hợp',
          'color': '#00FF00',
          'text_color': '#FFFFFF'
        },
        'NORMAL': {
          'name': 'Trung bình',
          'content': 'Sử dụng cho mục đích tưới tiêu và các mục đích tương đương khác',
          'color': '#FFFF00',
          'text_color': '#3F3A3A'
        },
        'POOR': {
          'name': 'Kém',
          'content': 'Sử dụng cho giao thông thủy và các mục đích tương đương khác',
          'color': '#FF7E00',
          'text_color': '#FFFFFF'
        },
        'HEAVY_POLLUTION': {
          'name': 'Ô nhiễm nặng',
          'content': 'Nước ô nhiễm nặng, cần các biện pháp xử lý trong tương lai',
          'color': '#FF0000',
          'text_color': '#FFFFFF'
        },
        'VERRY_HEAVY_POLLUTION': {
          'name': 'Ô nhiễm rất nặng',
          'content': 'Nước nhiễm độc, cần có biện pháp khắc phục, xử lý',
          'color': '#7E0023',
          'text_color': '#FFFFFF'
        }
      }
    },
    'QTTD': {
      'title': 'Quan Trắc tự động',
      'station_types': station_types_qttd(),
      'data_types': {
        'GOOD': {
          'name': 'Hoạt động tốt',
          'color': '#1dce6c'
        },
        'TENDENCY': {
          'name': 'Xu hướng vượt',
          'color': '#FFF954'
        },
        'PREPARING': {
          'name': 'Chuẩn bị vượt',
          'color': '#F08432'
        },
        'EXCEED': {
          'name': 'Vượt quy chuẩn',
          'color': '#EA3223'
        },
        'OFFLINE': {
          'name': 'Mất kết nối',
          'color': '#999999'
        },
        'ADJUSTING': {
          'name': 'Hiệu chuẩn',
          'color': '#6A0DAD'
        },
        'ERROR': {
          'name': 'Lỗi thiết bị',
          'color': '#ff7e00'
        }
      }
    },
    'QTDK': {
      'title': 'Quan Trắc Định Kỳ',
      'station_types': station_types_qtdk(),
      'data_types': {
        'GOOD': {
          'name': 'Đạt quy chuẩn',
          'color': '#1dce6c'
        },
        'EXCEEDED': {
          'name': 'Vượt quy chuẩn',
          'color': '#EA3223'
        },
        'NOT_YET': {
          'name': 'Chưa thực hiện',
          'color': '#999999'
        }
      }
    },
    'QLTNN': {
      'title': 'Quản lý tài nguyên nước',
      'data_types': {
        'GOOD': {
          'name': 'Hoạt động tốt',
          'color': '#1dce6c'
        },
        'EXCEED': {
          'name': 'Vượt quy chuẩn',
          'color': '#EA3223'
        },
        'OFFLINE': {
          'name': 'Mất kết nối',
          'color': '#999999'
        },
        'ADJUSTING': {
          'name': 'Hiệu chuẩn',
          'color': '#6A0DAD'
        },
        'ERROR': {
          'name': 'Lỗi thiết bị',
          'color': '#ff7e00'
        }
      }
    },
    'MAPS': {
      'AQI': True,
      'WQI': True,
      'QLTNN': True
    },
    'NOTIFICATION': {
      'plan': 'kế hoạch',
      'station': 'điểm quan trắc',
      'data': 'mẫu quan trắc',
      'import': 'nhập từ file',
      'add': 'thêm mới',
      'update': 'chỉnh sửa',
      'delete': 'xóa',
    }
  }
  data = {'vi': vi, 'en': vi}
  return dict(success=True, data=data)
