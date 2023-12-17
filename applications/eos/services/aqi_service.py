import logging
from applications.eos.enums import aqi
from applications.eos.common import condition_tree
from applications.eos.modules import common, manh_test


class AqiService:
    def __init__(self, mongo_client, T, pydal_db):
        self.mongo_client = mongo_client
        self.T = T
        self.db = pydal_db

    def get_report_aqi_day_in_time(self, station_id, data_type, start_date, end_date):
        if data_type == aqi.AQIDataType.RAW:
            return self.get_report_raw_aqi_day_in_time(station_id, start_date, end_date)
        elif data_type == aqi.AQIDataType.ADJUST:
            return self.get_report_adjust_aqi_day_in_time(station_id, start_date, end_date)

        return None

    def get_report_raw_aqi_day_in_time(self, station_id, start_date, end_date):
        common_cond = condition_tree.ExpressionTree(None)
        common_cond.And({
            "station_id": station_id,
            "get_time": {
                "$gte": start_date,
                "$lte": end_date
            },
        })
        condLv1 = condition_tree.ExpressionTree(None)
        condLv1.And({
            "data_24h.aqi": {
                "$gte": aqi.AQIReportLevel.LEVEL1[0],
                "$lte": aqi.AQIReportLevel.LEVEL1[1],
            },
        }).And(common_cond)
        count_level1 = len(self.mongo_client.aqi_data_24h.distinct("get_time", condLv1.dict))

        condLv2 = condition_tree.ExpressionTree(None)
        condLv2.And({
            "data_24h.aqi": {
                "$gt": aqi.AQIReportLevel.LEVEL2[0],
                "$lte": aqi.AQIReportLevel.LEVEL2[1],
            },
        }).And(common_cond)

        count_level2 = len(self.mongo_client.aqi_data_24h.distinct("get_time", condLv2.dict))

        condLv3 = condition_tree.ExpressionTree(None)
        condLv3.And({
            "data_24h.aqi": {
                "$gt": aqi.AQIReportLevel.LEVEL3[0],
                "$lte": aqi.AQIReportLevel.LEVEL3[1],
            },
        }).And(common_cond)
        count_level3 = len(self.mongo_client.aqi_data_24h.distinct("get_time", condLv3.dict))

        condLv4 = condition_tree.ExpressionTree(None)
        condLv4.And({
            "data_24h.aqi": {
                "$gt": aqi.AQIReportLevel.LEVEL4[0],
                "$lte": aqi.AQIReportLevel.LEVEL4[1],
            },
        }).And(common_cond)
        count_level4 = len(self.mongo_client.aqi_data_24h.distinct("get_time", condLv4.dict))

        condLv5 = condition_tree.ExpressionTree(None)
        condLv5.And({
            "data_24h.aqi": {
                "$gt": aqi.AQIReportLevel.LEVEL5[0],
                "$lte": aqi.AQIReportLevel.LEVEL5[1],
            },
        }).And(common_cond)
        count_level5 = len(self.mongo_client.aqi_data_24h.distinct("get_time", condLv5.dict))

        condLv6 = condition_tree.ExpressionTree(None)
        condLv6.And({
            "data_24h.aqi": {
                "$gt": aqi.AQIReportLevel.LEVEL6[0],
            },
        }).And(common_cond)
        count_level6 = len(self.mongo_client.aqi_data_24h.distinct("get_time", condLv6.dict))

        count_all = len(self.mongo_client.aqi_data_24h.distinct("get_time", common_cond.dict))
        if count_all == 0:
            return [
                [aqi.AQIReportLevel.RANGE_TEXT_LEVEL1, self.T('AQI Quality Good Level 1'), count_level1, 0],
                [aqi.AQIReportLevel.RANGE_TEXT_LEVEL2, self.T('AQI Quality Good Level 2'), count_level2, 0],
                [aqi.AQIReportLevel.RANGE_TEXT_LEVEL3, self.T('AQI Quality Good Level 3'), count_level3, 0],
                [aqi.AQIReportLevel.RANGE_TEXT_LEVEL4, self.T('AQI Quality Good Level 4'), count_level4, 0],
                [aqi.AQIReportLevel.RANGE_TEXT_LEVEL5, self.T('AQI Quality Good Level 5'), count_level5, 0],
                [aqi.AQIReportLevel.RANGE_TEXT_LEVEL6, self.T('AQI Quality Good Level 6'), count_level6, 0],
            ]
        else:
            return [
                [aqi.AQIReportLevel.RANGE_TEXT_LEVEL1, self.T('AQI Quality Good Level 1'), count_level1,
                 common.convert_data(float(100 * count_level1) / count_all)],
                [aqi.AQIReportLevel.RANGE_TEXT_LEVEL2, self.T('AQI Quality Good Level 2'), count_level2,
                 common.convert_data(float(100 * count_level2) / count_all)],
                [aqi.AQIReportLevel.RANGE_TEXT_LEVEL3, self.T('AQI Quality Good Level 3'), count_level3,
                 common.convert_data(float(100 * count_level3) / count_all)],
                [aqi.AQIReportLevel.RANGE_TEXT_LEVEL4, self.T('AQI Quality Good Level 4'), count_level4,
                 common.convert_data(float(100 * count_level4) / count_all)],
                [aqi.AQIReportLevel.RANGE_TEXT_LEVEL5, self.T('AQI Quality Good Level 5'), count_level5,
                 common.convert_data(float(100 * count_level5) / count_all)],
                [aqi.AQIReportLevel.RANGE_TEXT_LEVEL6, self.T('AQI Quality Good Level 6'), count_level6,
                 common.convert_data(float(100 * count_level6) / count_all)],
            ]

    def get_report_adjust_aqi_day_in_time(self, station_id, start_date, end_date):
        common_cond = condition_tree.ExpressionTree(None)
        common_cond.And({
            "station_id": station_id,
            "get_time": {
                "$gte": start_date,
                "$lte": end_date
            },
        })
        condLv1 = condition_tree.ExpressionTree(None)
        condLv1.And({
            "data_24h.aqi": {
                "$gte": aqi.AQIReportLevel.LEVEL1[0],
                "$lte": aqi.AQIReportLevel.LEVEL1[1],
            },
        }).And(common_cond)
        count_level1 = len(self.mongo_client.aqi_data_adjust_24h.distinct("get_time", condLv1.dict))

        condLv2 = condition_tree.ExpressionTree(None)
        condLv2.And({
            "data_24h.aqi": {
                "$gt": aqi.AQIReportLevel.LEVEL2[0],
                "$lte": aqi.AQIReportLevel.LEVEL2[1],
            },
        }).And(common_cond)

        count_level2 = len(self.mongo_client.aqi_data_adjust_24h.distinct("get_time", condLv2.dict))

        condLv3 = condition_tree.ExpressionTree(None)
        condLv3.And({
            "data_24h.aqi": {
                "$gt": aqi.AQIReportLevel.LEVEL3[0],
                "$lte": aqi.AQIReportLevel.LEVEL3[1],
            },
        }).And(common_cond)
        count_level3 = len(self.mongo_client.aqi_data_adjust_24h.distinct("get_time", condLv3.dict))

        condLv4 = condition_tree.ExpressionTree(None)
        condLv4.And({
            "data_24h.aqi": {
                "$gt": aqi.AQIReportLevel.LEVEL4[0],
                "$lte": aqi.AQIReportLevel.LEVEL4[1],
            },
        }).And(common_cond)
        count_level4 = len(self.mongo_client.aqi_data_adjust_24h.distinct("get_time", condLv4.dict))

        condLv5 = condition_tree.ExpressionTree(None)
        condLv5.And({
            "data_24h.aqi": {
                "$gt": aqi.AQIReportLevel.LEVEL5[0],
                "$lte": aqi.AQIReportLevel.LEVEL5[1],
            },
        }).And(common_cond)
        count_level5 = len(self.mongo_client.aqi_data_adjust_24h.distinct("get_time", condLv5.dict))

        condLv6 = condition_tree.ExpressionTree(None)
        condLv6.And({
            "data_24h.aqi": {
                "$gt": aqi.AQIReportLevel.LEVEL6[0],
            },
        }).And(common_cond)
        count_level6 = len(self.mongo_client.aqi_data_adjust_24h.distinct("get_time", condLv6.dict))

        count_all = len(self.mongo_client.aqi_data_adjust_24h.distinct("get_time", common_cond.dict))
        if count_all == 0:
            return [
                [aqi.AQIReportLevel.RANGE_TEXT_LEVEL1, self.T('AQI Quality Good Level 1'), count_level1, 0],
                [aqi.AQIReportLevel.RANGE_TEXT_LEVEL2, self.T('AQI Quality Good Level 2'), count_level2, 0],
                [aqi.AQIReportLevel.RANGE_TEXT_LEVEL3, self.T('AQI Quality Good Level 3'), count_level3, 0],
                [aqi.AQIReportLevel.RANGE_TEXT_LEVEL4, self.T('AQI Quality Good Level 4'), count_level4, 0],
                [aqi.AQIReportLevel.RANGE_TEXT_LEVEL5, self.T('AQI Quality Good Level 5'), count_level5, 0],
                [aqi.AQIReportLevel.RANGE_TEXT_LEVEL6, self.T('AQI Quality Good Level 6'), count_level6, 0],
            ]
        else:
            return [
                [aqi.AQIReportLevel.RANGE_TEXT_LEVEL1, self.T('AQI Quality Good Level 1'), count_level1,
                 common.convert_data(float(100 * count_level1) / count_all)],
                [aqi.AQIReportLevel.RANGE_TEXT_LEVEL2, self.T('AQI Quality Good Level 2'), count_level2,
                 common.convert_data(float(100 * count_level2) / count_all)],
                [aqi.AQIReportLevel.RANGE_TEXT_LEVEL3, self.T('AQI Quality Good Level 3'), count_level3,
                 common.convert_data(float(100 * count_level3) / count_all)],
                [aqi.AQIReportLevel.RANGE_TEXT_LEVEL4, self.T('AQI Quality Good Level 4'), count_level4,
                 common.convert_data(float(100 * count_level4) / count_all)],
                [aqi.AQIReportLevel.RANGE_TEXT_LEVEL5, self.T('AQI Quality Good Level 5'), count_level5,
                 common.convert_data(float(100 * count_level5) / count_all)],
                [aqi.AQIReportLevel.RANGE_TEXT_LEVEL6, self.T('AQI Quality Good Level 6'), count_level6,
                 common.convert_data(float(100 * count_level6) / count_all)],
            ]

    def get_report_public_aqi_station(self, start_date, end_date):
        result = []
        provinces = self.db(self.db.provinces.id > 0).select()
        count_stations_all = 0
        count_public_stations_all = 0
        for province in provinces:
            count_stations = self.db(self.db.stations.province_id == province.id).count()
            conditions = {
                'province_id': str(province.id),
                'is_public': True,
                'public_time': {'$gte': start_date, "$lte": end_date},
            }
            count_public_stations = self.mongo_client["stations"].count(conditions)
            count_stations_all += count_stations
            count_public_stations_all += count_public_stations
            result.append([
                province.province_name,
                count_stations,
                count_public_stations,
                count_stations - count_public_stations,
            ])
        result.insert(0, [
            self.T('Total All Station'),
            count_stations_all,
            count_public_stations_all,
            count_stations_all - count_public_stations_all,
        ])
        return result
