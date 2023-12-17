# -*- coding: utf-8 -*-

from applications.eos.modules import const


def call():
    return service()

################################################################################
@auth.requires_login()
@auth.requires(lambda: (auth.has_permission('view', 'dashboard')))
def index():
    # common.send_mail('ducva02@gmail.com', 'duc@vtexperts.com', 'this is the subject', 'this is the content')
    # Select provinces to fill in dropdown box
    provinces = common.get_province_have_station_for_envisoft()
    # Select stations to fill in dropdown box
    areas = db(db.areas.id > 0).select()
    conditions = (db.stations.id > 0)
    if current_user:
        if not (auth.has_membership('admin') or auth.has_membership(const.GROUP_MANAGER)):
            list_station_manager = db(db.manager_stations.user_id == current_user.id). \
                select(db.manager_stations.station_id)
            station_ids = [str(item.station_id) for item in list_station_manager]
            conditions &= (db.stations.id.belongs(station_ids))
            row = db(db.stations.id.belongs(station_ids)).select(db.stations.area_id, distinct=True)
            areas_ids = []
            for it in row:
                if it.area_id:
                    areas_ids.append(str(it.area_id))
            areas = db(db.areas.id.belongs(areas_ids)).select(db.areas.area_name,
                                                              db.areas.id)
    default_provinces = db(db.provinces.default == 1).select()
    
    # # Select stations to fill in dropdown box
    # fields = [
    #     db.stations.id,
    #     db.stations.station_name,
    #     db.stations.station_type,
    #     db.stations.longitude,
    #     db.stations.latitude,
    #     db.stations.status,
    # ]
    # stations = db(db.stations.id > 0).select(*fields)
    #
    # # Get qty online/total for each station
    # station_type_online = dict()
    # for st in const.STATION_TYPE:
    #     if not station_type_online.has_key(st):
    #         station_type_online[st] = dict()
    #         station_type_online[st]['value'] = const.STATION_TYPE[st]['value']
    #         station_type_online[st]['name'] = const.STATION_TYPE[st]['name']
    #         station_type_online[st]['image'] = const.STATION_TYPE[st]['image']
    #         station_type_online[st]['online'] = 0
    #         station_type_online[st]['total'] = 0
    #         station_type_online[st]['offline'] = 0
    # total_online = 0
    # total_adjust = 0
    # total_offline = 0
    # for station in stations:
    #     for st in station_type_online:
    #         if station.station_type == station_type_online[st]['value']:
    #             if station.status == const.STATION_STATUS['ADJUSTING']['value']:
    #                 total_adjust += 1
    #             elif station.status == const.STATION_STATUS['OFFLINE']['value']:
    #                 station_type_online[st]['offline'] += 1
    #                 total_offline += 1
    #             else:
    #                 station_type_online[st]['online'] += 1
    #                 total_online += 1
    #
    #             station_type_online[st]['total'] += 1
    #             break
 
    lang = request.args(0)
    defaultLang = myconf.get('langguage.default')
    if lang:
        session.lang = lang
        T.force(lang)
    elif defaultLang != None:
        session.lang = defaultLang
        T.force(defaultLang)
    else:
        session.lang = 'vn-vi'
        T.force('vn-vi')

    # if lang:
    #     session.lang = lang
    #     T.force(lang)
    # else:
    #     session.lang = 'us-en'
    #     T.force('us-en')


    # if lang == 'vn':
    #     session.lang = 'vn-vi'
    #     T.force('vn-vi')
    # else:
    #     session.lang = 'us-en'
    #     T.force('us-en')


    # if lang == 'en':
    #     session.lang = 'us-en'
    #     T.force('us-en')
    # else:
    #     session.lang = 'vn-vi'
    #     T.force('vn-vi')

    return dict(provinces=provinces, areas=areas, default_provinces=default_provinces)
    # return dict(provinces = provinces, areas = areas, stations = stations, station_type_online=station_type_online,
    #             total_station=len(stations), total_online=total_online, total_offline=total_offline, total_adjust=total_adjust)

################################################################################
# @decor.requires_login()
@service.json
@auth.requires(lambda: (auth.has_permission('view', 'dashboard')))
def get_summary_station(*args, **kwargs):       # ham nay cho block 1 cu, ko dung nua
    try:
        area_id = request.vars.area_id
        province_id = request.vars.province_id
        conditions = (db.stations.id > 0)
        if area_id:
            conditions &= (db.stations.area_id == area_id)
        if province_id:
            conditions &= (db.stations.province_id == province_id)
        stations = db(conditions).select(db.stations.id, db.stations.status, db.stations.station_type)

        # Get qty online/total for each station
        station_type_online = dict()
        for st in const.STATION_TYPE:
            if not station_type_online.has_key(st):
                station_type_online[st] = dict()
                station_type_online[st]['value'] = const.STATION_TYPE[st]['value']
                station_type_online[st]['name'] = const.STATION_TYPE[st]['name']
                station_type_online[st]['image'] = const.STATION_TYPE[st]['image']
                station_type_online[st]['online'] = 0
                station_type_online[st]['total'] = 0
                station_type_online[st]['offline'] = 0
        total_online = 0
        total_adjust = 0
        total_offline = 0
        for station in stations:
            for st in station_type_online:
                if station.station_type == station_type_online[st]['value']:
                    if station.status == const.STATION_STATUS['ADJUSTING']['value']:
                        total_adjust += 1
                    elif station.status == const.STATION_STATUS['OFFLINE']['value']:
                        station_type_online[st]['offline'] += 1
                        total_offline += 1
                    else:
                        station_type_online[st]['online'] += 1
                        total_online += 1

                    station_type_online[st]['total'] += 1
                    break
        return dict(success=True, station_type_online=station_type_online, total_station=len(stations), total_online=total_online,
                    total_offline=total_offline, total_adjust=total_adjust)
    except Exception as ex:
        return dict(success=False, message=str(ex))



