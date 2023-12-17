from bson.objectid import ObjectId
from gluon import current

if False:
    from gluon import *

    request = current.request
    response = current.response
    session = current.session
    cache = current.cache
    T = current.T
    db = current.db


class IndicatorService:
    def __init__(self, mongo_client, T):
        self.T = T
        self.current = current
        self.mongo_client = mongo_client

    def get_indicators_id_gt(self, id):
        docs = self.mongo_client.indicators.find({"_id": {"$gt": ObjectId(id)}})
        indicators = []
        for doc in docs:
            indicators.append(self.doc_to_indicator(doc))
        return indicators

    def doc_to_indicator(self, row):
        unit = None
        if "unit" in row:
            unit = row["unit"]
        return {
            'id': str(row["_id"]),
            'indicator': row["indicator"],
            'indicator_type': row["indicator_type"],
            'source_name': row["source_name"],
            'unit': unit,
            'description': row["description"],
            'order_no': row["order_no"],
        }
