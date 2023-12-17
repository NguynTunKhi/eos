from applications.eos.modules import const

if False:
    from gluon import *

    request = current.request
    response = current.response
    session = current.session
    cache = current.cache
    T = current.T
    db = current.db


class StationIndicator:
    def __init__(self, pydal, T):
        self.pydal = pydal
        self.T = T

    def get_station_indicators_by(self, station_id, indicator_ids, station_type, station_indicator_status):
        station_indicators = self.pydal(
            (self.pydal.station_indicator.station_id == station_id) &
            (self.pydal.station_indicator.indicator_id.belongs(indicator_ids)) &
            (self.pydal.station_indicator.status == station_indicator_status) &
            (self.pydal.station_indicator.station_type == station_type)). \
            select()
        return station_indicators
    def filter_unlinked_indicators(self, indicators, station):
        indicator_ids = []
        for indi in indicators:
            indicator_ids.append(indi.id)

        station_type = station.station_type or const.STATION_TYPE['WASTE_WATER']['value']
        linked_station_indicators = self.get_station_indicators_by(station.id, indicator_ids, station_type, const.SI_STATUS['IN_USE']['value'])
        linked_indicator_ids_str = []
        for row in linked_station_indicators:
            linked_indicator_ids_str.append(str(row.indicator_id))
        unlinked_indicators = []
        for indicator in indicators:
            if indicator.id not in linked_indicator_ids_str:
                unlinked_indicators.append(indicator)
        return unlinked_indicators
