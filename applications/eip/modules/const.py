# coding: utf8

from gluon import current

GROUP_MANAGER = 'managers'

STATION_TYPE = {
    'WASTE_WATER': {'value': 0, 'name': 'Waste water', 'image': 'waste_water2.png'},
    'SURFACE_WATER': {'value': 1, 'name': 'Surface water', 'image': 'surface_water2.png'},
    'UNDERGROUND_WATER': {'value': 2, 'name': 'Underground water', 'image': 'underground_water2.png'},
    'STACK_EMISSION': {'value': 3, 'name': 'Stack emission', 'image': 'stack_emission.png'},
    'AMBIENT_AIR': {'value': 4, 'name': 'Ambient air', 'image': 'ambient_air2.png'},
}

STATION_STATUS = {
    'GOOD': {'value': 0, 'name': 'Good', 'color': '#1dce6c', 'icon': 'fa fa-circle'},              # fa fa-spinner fa-spin
    # 'TENDENCY': {'value': 1, 'name': 'Tendency', 'color': '#F1D748', 'icon': 'fa fa-circle'},
    'TENDENCY': {'value': 1, 'name': 'Good', 'color': '#1dce6c', 'icon': 'fa fa-circle'},
    # 'PREPARING': {'value': 2, 'name': 'Preparing', 'color': '#F08432', 'icon': 'fa fa-circle'},
    'PREPARING': {'value': 2, 'name': 'Good', 'color': '#1dce6c', 'icon': 'fa fa-circle'},
    'EXCEED': {'value': 3, 'name': 'Exceed', 'color': '#EA3223', 'icon': 'fa fa-circle'},
    'OFFLINE':  {'value': 4, 'name': 'Offline', 'color': '#999999', 'icon': 'fa fa-stop'},
    'ADJUSTING': {'value': 5, 'name': 'Adjusting', 'color': 'purple', 'icon': 'fa fa-pause'},
    'ERROR':  {'value': 6, 'name': 'Sensor error', 'color': 'red', 'icon': 'fa fa-times-circle-o'},
}

ALARM_LEVEL = {
    'TENDENCY': {'value': 0, 'name': 'Tendency', 'color': '#F1D748', 'icon': 'fa fa-arrow-down text-info'},
    'PREPARING': {'value': 1, 'name': 'Preparing', 'color': '#F08432', 'icon': 'fa fa-arrow-up text-danger'},
    'EXCEED': {'value': 2, 'name': 'Exceed', 'color': '#EA3223', 'icon': 'fa fa-pause text-warning'},
}

ALARM_LOG_LEVEL = {
    'Immediate': {'value': 0, 'name': 'Immediate', 'color': '#EA3223', 'color2': '#FFFFFF', 'icon': 'fa fa-arrow-down text-info'},
    'High': {'value': 1, 'name': 'High', 'color': '#F08432', 'color2': '#FFFFFF', 'icon': 'fa fa-arrow-up text-danger'},
    'Medium': {'value': 2, 'name': 'Medium', 'color': '#F1D748', 'color2': '#FFFFFF', 'icon': 'fa fa-pause text-warning'},
    'Low': {'value': 3, 'name': 'Low', 'color': '#f7fbd7', 'color2': '#898989', 'icon': 'fa fa-pause text-warning'},
}

VIEW_BY = {
    'MINUTE': {'value': 1, 'name': 'by minute', 'table': 'data_min'},
    'HOUR': {'value': 2, 'name': 'by hour', 'table': 'data_hour'},
    'DAY': {'value': 3, 'name': 'by day', 'table': 'data_day'},
    'MONTH': {'value': 4, 'name': 'by month', 'table': 'data_mon'},
}

DATA_TYPE = {
    'YET_APPROVED': {'value': 1, 'name': 'Yet Approved'},
    'APPROVED': {'value': 2, 'name': 'Approved'},
    'ORIGINAL_DATA': {'value': 3, 'name': 'Original Data'},
}

DATA_FILTER_BY = {
    'NEGATIVE': {'value': 1, 'name': 'Negative'},
    'IS_ZERO': {'value': 2, 'name': 'Is Zero'},
    'OUT_OF_RANGE': {'value': 3, 'name': 'Out of range'},
}

ADJUSTMENT_TYPE = {
    'REPLACE': {'value': 0, 'name': 'Replace'},
    'MAINTAINANCE': {'value': 1, 'name': 'Maintainance'},
    'IMPLEMENT': {'value': 2, 'name': 'Implement'},
    'CHECKING': {'value': 3, 'name': 'Checking'},
}

ADJUSTMENT_STATUS = {
    'DRAFT': {'value': 0, 'name': 'Draft'},
    'CREATED': {'value': 1, 'name': 'Created'},
    'WAIT_FOR_APPROVE': {'value': 2, 'name': 'Wait for approve'},
    'REJECTED': {'value': 3, 'name': 'Rejected'},
    'ACCEPTED': {'value': 4, 'name': 'Accepted'},
    'CANCELLED': {'value': 5, 'name': 'Cancelled'},
}

T = current.T
AQI_COLOR = {
    50  :       {'from': 0,   'to': 50,   'text' : 'Index - Good',    'bgColor' : '#008000', 'color' : '#ffffff', 'description': 'effect_to_the_health_50'},
    100 :       {'from': 51,  'to': 100,  'text' : 'Index - Medium',  'bgColor' : '#ffff00', 'color' : '#333333', 'description': 'effect_to_the_health_100'},
    200 :       {'from': 101, 'to': 200,  'text' : 'Index - Low',     'bgColor' : '#099099', 'color' : '#efa216', 'description': 'effect_to_the_health_200'},
    300 :       {'from': 201, 'to': 300,  'text' : 'Index - Bad',     'bgColor' : '#ff0000', 'color' : '#ffffff', 'description': 'effect_to_the_health_300'},
    999999999 : {'from': 301, 'to': None, 'text' : 'Index - Serious', 'bgColor' : '#800080', 'color' : '#ffffff', 'description': 'effect_to_the_health_other'},
}

AQI_COLOR_TCMT = {
    50 :  {'text' : T('Excellent'),           'bgColor' : '#00b9e7', 'color' : '#666'},
    100 : {'text' : T('Good'),                'bgColor' : '#ffec60', 'color' : '#666'},
    150 : {'text' : T('Lightly Polluted'),    'bgColor' : '#ffb753', 'color' : '#666'},
    200 : {'text' : T('Moderately Polluted'), 'bgColor' : '#fd4441', 'color' : '#666'},
    300 : {'text' : T('Heavily Polluted'),    'bgColor' : '#d19341', 'color' : '#666'},
    999 : {'text' : T('Severely Polluted'),   'bgColor' : '#7f1f25', 'color' : '#fff'},
}

SYSTEM_ACTIONS = {
   'VIEW': {'value': 'view', 'name': 'Permission_View', 'seq': 1},
   'CREATE': {'value': 'create', 'name': 'Permission_Create', 'seq': 2},
   'EDIT': {'value': 'edit', 'name': 'Permission_Edit', 'seq': 3},
   'DELETE': {'value': 'delete', 'name': 'Permission_Delete', 'seq': 4},
   'IMPORT': {'value': 'import', 'name': 'Permission_Import', 'seq': 5},
   'EXPORT': {'value': 'export', 'name': 'Permission_Export', 'seq': 6},
   'APPROVE': {'value': 'approve', 'name': 'Permission_Approve', 'seq': 7},
   'REJECT': {'value': 'reject', 'name': 'Permission_Reject', 'seq': 8},
   'ADJUST': {'value': 'adjust', 'name': 'Permission_Adjust', 'seq': 9},
   'PUBLIC': {'value': 'public', 'name': 'Permission_Public', 'seq': 10},
   'EXECUTE': {'value': 'execute', 'name': 'Permission_Execute', 'seq': 11},
   'SCHEDULE': {'value': 'schedule', 'name': 'Permission_Schedule', 'seq': 12},
}


import operator as op

WQI_INDICATOR_A     = ['BOD5', 'COD', 'N-NH4', 'P-PO4', 'DO']
WQI_INDICATOR_B     = ['TURBIDITY', 'TSS']
WQI_INDICATOR       = ['BOD5', 'COD', 'N-NH4', 'P-PO4', 'COLIFORM', 'TURBIDITY', 'TSS']
WQI_INDICATOR_ALL   = WQI_INDICATOR + ['DO', 'TEMP', 'PH']

WQI_BP = {
    'BOD5':      [4, 6, 15, 25, 50],   
    'COD':       [10, 15, 30, 50, 80],
    'N-NH4':     [0.1, 0.2, 0.5, 1, 5],
    'P-PO4':     [0.1, 0.2, 0.3, 0.5, 6],
    'TURBIDITY': [5, 20, 30, 70, 100],
    'TSS':       [20, 30, 50, 100, 100],
    'COLIFORM':  [2500, 5000, 7500, 10000, 10000],
}

OP_1 = {
    'BOD5':      [op.le, op.lt, op.lt, op.lt, op.ge],   
    'COD':       [op.le, op.lt, op.lt, op.lt, op.ge],
    'N-NH4':     [op.le, op.lt, op.lt, op.lt, op.ge],
    'P-PO4':     [op.le, op.lt, op.lt, op.lt, op.ge],
    'TURBIDITY': [op.le, op.lt, op.lt, op.lt, op.ge],
    'TSS':       [op.le, op.lt, op.lt, op.lt, op.gt],
    'COLIFORM':  [op.le, op.lt, op.lt, op.lt, op.gt],
}

QI = [100, 75, 50, 25, 1]

DO_BP = [20, 20, 50, 75, 88, 112, 125, 150, 200, 200]
DO_QI = [1, 25, 50, 75, 100, 100, 75, 50, 25, 1]
OP_2  = [op.le, op.lt, op.lt, op.lt, op.lt, op.le, op.lt, op.lt, op.lt, op.ge]

PH_BP = [5.5, 5.5, 6, 8.5, 9, 9]
PH_QI = [1, 50, 100, 100, 50, 1]
OP_3  = [op.le, op.lt, op.lt, op.le, op.lt, op.ge]
