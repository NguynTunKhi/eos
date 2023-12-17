import logging

from applications.eos.package import request_indicator_pack
from applications.eos.exception import http
from applications.eos.enums import request_indicator as enums
from applications.eos.common import condition_tree
from applications.eos.adapters import eos_tw
from bson.objectid import ObjectId
from gluon import current

# TODO indicator_type for now validate from 1->4, need move to ref station_types.code
# TODO move add http.HttpException to use T

if False:
    from gluon import *

    request = current.request
    response = current.response
    session = current.session
    cache = current.cache
    T = current.T
    db = current.db


class RequestIndicatorService:
    def __init__(self, mongo_client, T):
        self.T = T
        self.current = current
        self.approve_statuses = enums.RequestIndicatorApproveStatus()
        self.mongo_client = mongo_client

    def get_request_indicator(self, request_indicator_id  # type: str
                              ):
        doc = self.mongo_client.request_indicators.find_one({"_id": ObjectId(request_indicator_id)})
        if not doc:
            return False, http.HttpException(
                message=self.T('Missing id for get request indicator'),
                http_code=400,
            )
        request_indicator = self.doc_to_request_indicator(doc)
        return request_indicator

    def create_request_indicator(self, request_pack  # type: request_indicator_pack.CreateRequestIndicator
                                 ):
        valid, ex = request_pack.validate()
        if not valid:
            raise ex
        valid2, ex2 = self.validate_create_refs(request_pack)
        if not valid2:
            raise ex2
        model = self.create_request_indicator_request_to_model(request_pack)
        id = self.create(model)
        return id

    def validate_create_refs(self, request_pack  # type: request_indicator_pack.CreateRequestIndicator
                             ):
        db = current.db
        # validate record in request indicators
        query_ri = db.request_indicators.indicator == request_pack.indicator
        query_ri |= db.request_indicators.source_name == request_pack.source_name
        query_ri &= db.request_indicators.approve_status == enums.RequestIndicatorApproveStatus.WAITING
        exist_request_indicators = db(query_ri).select()
        if len(exist_request_indicators) != 0:
            return False, http.HttpException(
                message=self.T('Exist an request indicator with the same name or source name ') +
                        str(db._adapter.object_id(exist_request_indicators.first().id)),
                http_code=400,
            )
        # validate record in indicators
        query_i = db.indicators.indicator == request_pack.indicator
        query_i |= db.indicators.source_name == request_pack.source_name
        exist_indicators = db(query_i).select()
        if len(exist_indicators) != 0:
            return False, http.HttpException(
                message=self.T('Exist an indicator with the same name or source name ') +
                        str(db._adapter.object_id(exist_indicators.first().id)),
                http_code=400,
            )
        return True, None

    def update_request_indicator(self, request_pack  # type: request_indicator_pack.UpdateRequestIndicator
                                 ):
        valid, ex = request_pack.validate()
        if not valid:
            raise ex
        valid2, ex2 = self.validate_update_refs(request_pack)
        if not valid2:
            raise ex2
        set_update_fields = self.update_request_indicator_pack_to_set_update_fields(request_pack)
        self.update(request_pack.id, set_update_fields)

    def validate_update_refs(self, request_pack  # type request_indicator_pack.UpdateRequestIndicator
                             ):
        doc = self.mongo_client.request_indicators.find_one({"_id": ObjectId(request_pack.id)})
        if not doc:
            return False, http.HttpException(
                message=self.T('Missing id for update request indicator'),
                http_code=400,
            )
        request_indicator = self.doc_to_request_indicator(doc)
        if request_indicator["approve_status"] == enums.RequestIndicatorApproveStatus.APPROVED:
            return False, http.HttpException(
                message=self.T('Can not update approved request indicator'),
                http_code=400,
            )
        if request_indicator["approve_status"] == enums.RequestIndicatorApproveStatus.REJECTED:
            return False, http.HttpException(
                message=self.T('Can not update rejected request indicator'),
                http_code=400,
            )
        return True, None

    def approve_request_indicator(self, request_pack  # type: request_indicator_pack.ApproveRequestIndicator
                                  ):
        # validate permission will be validate from controller with line
        # @auth.requires(lambda: (auth.has_permission('approve', 'request_indicators')))
        valid, ex = request_pack.validate()
        if not valid:
            raise ex
        request_indicator, valid2, ex = self.validate_approve_indicator_refs(request_pack)
        if not valid2:
            raise ex
        new_indicator_id = ''
        approve_status = ''
        if request_pack.action == enums.RequestIndicatorApproveAction.APPROVE:
            approve_status = enums.RequestIndicatorApproveStatus.APPROVED
            indicator = self.request_indicator_to_indicator(request_indicator)
            new_indicator_id = self.mongo_client.indicators.insert(indicator)
        elif request_pack.action == enums.RequestIndicatorApproveAction.REJECT:
            approve_status = enums.RequestIndicatorApproveStatus.REJECTED

        set_update_fields = {
            'approve_status': approve_status,
            'reason': request_pack.reason,
        }
        if new_indicator_id:
            set_update_fields['indicator_id'] = new_indicator_id
        self.update(request_pack.request_indicator_id, set_update_fields)
        return

    def validate_approve_indicator_refs(self, request_pack  # type: request_indicator_pack.ApproveRequestIndicator
                                        ):
        doc = self.mongo_client.request_indicators.find_one({"_id": ObjectId(request_pack.request_indicator_id)})
        if not doc:
            return None, False, http.HttpException(
                message=self.T('Not Found'),
                http_code=400,
            )
        request_indicator = self.doc_to_request_indicator(doc)
        if request_indicator["approve_status"] == enums.RequestIndicatorApproveStatus.APPROVED:
            return request_indicator, False, http.HttpException(
                message=self.T('Can not approve approved request indicator'),
                http_code=400,
            )
        if request_indicator["approve_status"] == enums.RequestIndicatorApproveStatus.REJECTED:
            return request_indicator, http.HttpException(
                message=self.T('Can not approve rejected request indicator'),
                http_code=400,
            )
        if request_indicator["indicator_id"]:
            return request_indicator, False, http.HttpException(
                message=self.T('Can not approve approved request indicator'),
                http_code=400,
            )
        return request_indicator, True, None

    def create_request_indicator_request_to_model(self, request_pack
                                                  # type: request_indicator_pack.CreateRequestIndicator
                                                  ):
        return {
            'indicator': request_pack.indicator,
            'indicator_type': request_pack.indicator_type,
            'source_name': request_pack.source_name,
            'unit': request_pack.unit,
            'description': request_pack.description,
            'order_no': request_pack.order_no,
            'approve_status': self.approve_statuses.WAITING,
            'reason': '',
            'indicator_id': None,
        }

    def update_request_indicator_pack_to_set_update_fields(self, request_pack
                                                           # type: request_indicator_pack.UpdateRequestIndicator
                                                           ):
        return {
            'indicator': request_pack.indicator,
            'indicator_type': request_pack.indicator_type,
            'source_name': request_pack.source_name,
            'unit': request_pack.unit,
            'description': request_pack.description,
            'order_no': request_pack.order_no,
        }

    def update(self, request_indicator_id, set_update_fields):
        self.mongo_client.request_indicators.update_one(
            {"_id": ObjectId(request_indicator_id)},
            {
                "$set": set_update_fields,
            }
        )

    def create(self, model):
        db = current.db
        return db.request_indicators.insert(**model)

    def list_request_indicators(self, request_pack  # type: request_indicator_pack.RequestListRequestIndicator
                                ):
        condition = condition_tree.ExpressionTree(None)
        if request_pack.indicator_type is not None:
            condition.And({
                "indicator_type": request_pack.indicator_type
            })
        if request_pack.keyword:
            condition.And(
                condition_tree.ExpressionTree(None).Or(
                    {
                        "indicator": request_pack.keyword,
                    },
                    {
                        "unit": request_pack.keyword
                    },
                    {
                        "description": request_pack.keyword
                    }
                )
            )
        if request_pack.approve_status is not None:
            condition.And({
                "approve_status": request_pack.approve_status,
            })
        docs = self.mongo_client.request_indicators.find(condition.dict). \
            sort("order_no", -1).skip((request_pack.page - 1) * request_pack.page_size). \
            limit(request_pack.page_size)
        count = docs.count()
        request_indicators = []
        for doc in docs:
            request_indicators.append(self.doc_to_request_indicator(doc))
        return request_indicator_pack.ResponseListRequestIndicator(request_pack.page, request_pack.page_size, count,
                                                                   request_indicators)

    def doc_to_request_indicator(self, row):
        indicator_id = ''
        if "indicator_id" in row and row["indicator_id"]:
            indicator_id = row["indicator_id"]
        reason = None
        if "reason" in row and row["reason"]:
            reason = row["reason"]
        approve_status = None
        if "approve_status" in row:
            approve_status = row["approve_status"]
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
            'approve_status': approve_status,
            'reason': reason,
            'indicator_id': str(indicator_id)
        }

    def request_indicator_to_indicator(self, request_indicator):
        return {
            'indicator': request_indicator["indicator"],
            'indicator_type': request_indicator["indicator_type"],
            'source_name': request_indicator["source_name"],
            'unit': request_indicator["unit"],
            'description': request_indicator["description"],
            'order_no': request_indicator["order_no"],
        }

    # list_request_indicators_local_dp handle list request indicator on local dp
    def list_request_indicators_local_dp(self, request_pack  # type: request_indicator_pack.RequestListRequestIndicator
                                         ):
        twapi = eos_tw.TWAPI()
        response_body, err = twapi.get_list_request_indicators(request_pack)

        if err:
            logging.error(err)
            raise http.HttpException(
                message=err,
                http_code=500,
            )

        return response_body

    def get_request_indicators_local_dp(self, request_indicator_id  # type: str
                                        ):
        twapi = eos_tw.TWAPI()
        response_body, err = twapi.get_request_indicator_by_id(request_indicator_id)
        if err:
            logging.error(err)
            raise http.HttpException(
                message=err,
                http_code=500,
            )

        return response_body

    def update_request_indicator_local_dp(self, request_pack  # type: request_indicator_pack.UpdateRequestIndicator
                                          ):
        valid, ex = request_pack.validate()
        if not valid:
            raise ex
        twapi = eos_tw.TWAPI()
        response_body, err = twapi.update_request_indicator(request_pack)
        if err:
            logging.error(err)
            raise http.HttpException(
                message=err,
                http_code=500,
            )

        return response_body

    def create_request_indicator_local_dp(self, request_pack  # type: request_indicator_pack.CreateRequestIndicator
                                          ):
        valid, ex = request_pack.validate()
        if not valid:
            raise ex
        twapi = eos_tw.TWAPI()
        response_body, err = twapi.create_request_indicator(request_pack)
        if err:
            logging.error(err)
            raise http.HttpException(
                message=response_body['meta']['message'],
                http_code=response_body['meta']['code'],
            )

        return response_body
