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
  'GOOD': {'value': 0, 'name': 'Good', 'color': '#1dce6c', 'icon': 'fa fa-circle'},  # fa fa-spinner fa-spin
  # 'TENDENCY': {'value': 1, 'name': 'Tendency', 'color': '#F1D748', 'icon': 'fa fa-circle'},
  'TENDENCY': {'value': 1, 'name': 'Good', 'color': '#1dce6c', 'icon': 'fa fa-circle'},
  # 'PREPARING': {'value': 2, 'name': 'Preparing', 'color': '#F08432', 'icon': 'fa fa-circle'},
  'PREPARING': {'value': 2, 'name': 'Good', 'color': '#1dce6c', 'icon': 'fa fa-circle'},
  'EXCEED': {'value': 3, 'name': 'Exceed', 'color': '#EA3223', 'icon': 'fa fa-circle'},
  'OFFLINE': {'value': 4, 'name': 'Offline', 'color': '#999999', 'icon': 'fa fa-stop'},
  'ADJUSTING': {'value': 5, 'name': 'Adjusting', 'color': 'purple', 'icon': 'fa fa-pause'},
  'ERROR': {'value': 6, 'name': 'Sensor error', 'color': '#ff7e00', 'icon': 'fa fa-times-circle-o'},
}

SI_STATUS = {  # Station indicator status
  'IN_USE': {'value': 1, 'name': 'In use'},
  'DELETED': {'value': 2, 'name': 'Deleted'},
  'ERROR': {'value': 3, 'name': 'Sensor error'},
}

SENSOR_STATUS = {  # Station indicator status
  'ADJUSTMENT': {'value': 1, 'name': 'Adjustment'},
  'ERROR': {'value': 2, 'name': 'Sensor error'},
}

ALARM_LEVEL = {
  'TENDENCY': {'value': 0, 'name': 'Tendency', 'color': '#F1D748', 'color2': '#FFFFFF',
               'icon': 'fa fa-circle text-info'},
  'PREPARING': {'value': 1, 'name': 'Preparing', 'color': '#EA3223', 'color2': '#FFFFFF',
                'icon': 'fa fa-circle text-info'},
  'EXCEED': {'value': 2, 'name': 'Exceed', 'color': '#EA3223', 'color2': '#FFFFFF',
             'icon': 'fa fa-arrow-up text-danger'},
}

ALARM_LOG_LEVEL = {
  'Immediate': {'value': 0, 'name': 'Immediate', 'color': '#EA3223', 'color2': '#FFFFFF',
                'icon': 'fa fa-arrow-down text-info'},
  'High': {'value': 1, 'name': 'High', 'color': '#F08432', 'color2': '#FFFFFF', 'icon': 'fa fa-arrow-up text-danger'},
  'Medium': {'value': 2, 'name': 'Medium', 'color': '#F1D748', 'color2': '#FFFFFF',
             'icon': 'fa fa-pause text-warning'},
  'Low': {'value': 3, 'name': 'Low', 'color': '#f7fbd7', 'color2': '#898989', 'icon': 'fa fa-pause text-warning'},
}

VIEW_BY = {
  'MINUTE': {'value': 1, 'name': 'by minute', 'table': 'data_min', 'order': 1},
  'HOUR': {'value': 2, 'name': 'by hour', 'table': 'data_hour', 'order': 2},
  'DAY': {'value': 3, 'name': 'by day', 'table': 'data_day', 'order': 4},
  'MONTH': {'value': 4, 'name': 'by month', 'table': 'data_mon', 'order': 5},
  'HOUR_8': {'value': 5, 'name': 'by hour', 'table': 'data_hour_8h', 'order': 3},
  'AQI_HOUR': {'value': 6, 'name': 'by month', 'table': 'aqi_data_hour', 'order': 6},
  'AQI_DAY': {'value': 7, 'name': 'by month', 'table': 'aqi_data_24h', 'order': 7},
  'WQI_HOUR': {'value': 8, 'name': 'by month', 'table': 'wqi_data_hour', 'order': 8},
}

VIEW_BY_ADJUST = {
  'MINUTE': {'value': 1, 'name': 'by minute', 'table': 'data_adjust'},
  'HOUR': {'value': 2, 'name': 'by hour', 'table': 'data_hour_adjust'},
  'DAY': {'value': 3, 'name': 'by day', 'table': 'data_day_adjust'},
  'MONTH': {'value': 4, 'name': 'by month', 'table': 'data_mon_adjust'},
  'HOUR_8': {'value': 5, 'name': 'by hour', 'table': 'data_hour_8h_adjust'},
  'AQI_HOUR': {'value': 6, 'name': 'by month', 'table': 'aqi_data_adjust_hour'},
  'AQI_DAY': {'value': 7, 'name': 'by month', 'table': 'aqi_data_adjust_24h'},
  'WQI_HOUR': {'value': 8, 'name': 'by month', 'table': 'wqi_data_adjust_hour'},
}

DATA_TYPE = {
  'YET_APPROVED': {'value': 1, 'name': 'Yet Approved'},
  'APPROVED': {'value': 2, 'name': 'Approved'},
  'ORIGINAL_DATA': {'value': 3, 'name': 'Original Data'},
}

DATA_TYPE_FILTER = {
  'APPROVED': {'value': 2, 'name': 'Approved'},
  'ORIGINAL_DATA': {'value': 3, 'name': 'Original Data'},
}

DATA_FILTER_BY = {
  'NEGATIVE': {'value': 1, 'name': 'Negative'},
  'IS_ZERO': {'value': 2, 'name': 'Is Zero'},
  'OUT_OF_RANGE': {'value': 3, 'name': 'Out of range'},
}

ADJUSTMENT_TYPE = {
  'EXECUTE': {'value': 1, 'name': 'Execute_adjustment'},
  'REJECT_ADJUSTMENT': {'value': 0, 'name': 'Reject_adjustments'},
}

ADJUSTMENT_STATUS = {
  'DRAFT': {'value': 0, 'name': 'Draft'},
  'WAIT_FOR_APPROVE': {'value': 2, 'name': 'Wait for approve'},
  'REJECTED': {'value': 3, 'name': 'Rejected'},
  'ACCEPTED': {'value': 4, 'name': 'Accepted'},
  'CANCELLED': {'value': 5, 'name': 'Cancelled'},
}

T = current.T
AQI_COLOR = {
  # 50  :       {'from': 0,   'to': 50,   'text' : 'Index - Good',    'bgColor' : '#008000', 'color' : '#ffffff', 'description': 'effect_to_the_health_50'},
  # 100 :       {'from': 51,  'to': 100,  'text' : 'Index - Medium',  'bgColor' : '#ffff00', 'color' : '#333333', 'description': 'effect_to_the_health_100'},
  # 200 :       {'from': 101, 'to': 200,  'text' : 'Index - Low',     'bgColor' : '#099099', 'color' : '#efa216', 'description': 'effect_to_the_health_200'},
  # 300 :       {'from': 201, 'to': 300,  'text' : 'Index - Bad',     'bgColor' : '#ff0000', 'color' : '#ffffff', 'description': 'effect_to_the_health_300'},
  # 999999999 : {'from': 301, 'to': None, 'text' : 'Index - Serious', 'bgColor' : '#800080', 'color' : '#ffffff', 'description': 'effect_to_the_health_other'},
  # update 2019-02-20
  50: {'from': 0, 'to': 50, 'text': 'Index - Good', 'bgColor': '#00e400', 'color': '#ffffff',
       'description': 'effect_to_the_health_50'},
  100: {'from': 51, 'to': 100, 'text': 'Index - Medium', 'bgColor': '#ffff00', 'color': '#333333',
        'description': 'effect_to_the_health_100'},
  150: {'from': 101, 'to': 150, 'text': 'Index - Low', 'bgColor': '#ff7e00', 'color': '#000000',
        'description': 'effect_to_the_health_200'},
  300: {'from': 151, 'to': 300, 'text': 'Index - Bad', 'bgColor': '#ff0000', 'color': '#ffffff',
        'description': 'effect_to_the_health_300'},
  500: {'from': 301, 'to': 500, 'text': 'Index - Serious', 'bgColor': '#8f3f97', 'color': '#ffffff',
        'description': 'effect_to_the_health_500'},
  999999999: {'from': 501, 'to': None, 'text': 'Index - VerySerious', 'bgColor': '#7e0019', 'color': '#ffffff',
              'description': 'effect_to_the_health_other'},

}
WQI_COLOR = {
  # 25  :   {'from': 0,  'to': 25,  'text' : 'Index - Serious',    'bgColor' : '#ff0000', 'color' : '#333333', 'description': 'water_effect_to_the_health_25'},
  # 50 :    {'from': 26, 'to': 50,  'text' : 'Index - Bad',  'bgColor' : '#ff9933', 'color' : '#333333', 'description': 'water_effect_to_the_health_50'},
  # 75 :    {'from': 51, 'to': 75,  'text' : 'Index - Low',     'bgColor' : '#ffff00', 'color' : '#333333', 'description': 'water_effect_to_the_health_75'},
  # 90 :    {'from': 76, 'to': 90,  'text' : 'Index - Medium',     'bgColor' : '#00b0f0', 'color' : '#333333', 'description': 'water_effect_to_the_health_90'},
  # 100 :   {'from': 91, 'to': 100, 'text' : 'Index - Good', 'bgColor' : '#0070c0', 'color' : '#333333', 'description': 'water_effect_to_the_health_100'},
  10: {'from': 0, 'to': 10, 'text': 'Index - VerySerious', 'bgColor': '#7e0019', 'color': '#ffffff',
       'description': 'water_effect_to_the_health_25'},
  25: {'from': 11, 'to': 25, 'text': 'Index - Serious', 'bgColor': '#ff0000', 'color': '#ffffff',
       'description': 'water_effect_to_the_health_25'},
  50: {'from': 26, 'to': 50, 'text': 'Index - Bad', 'bgColor': '#ff7e00', 'color': '#333333',
       'description': 'water_effect_to_the_health_50'},
  75: {'from': 51, 'to': 75, 'text': 'Index - Low', 'bgColor': '#ffff00', 'color': '#333333',
       'description': 'water_effect_to_the_health_75'},
  90: {'from': 76, 'to': 90, 'text': 'Index - Medium', 'bgColor': '#00e400', 'color': '#333333',
       'description': 'water_effect_to_the_health_90'},
  100: {'from': 91, 'to': 100, 'text': 'Index - Good', 'bgColor': '#3333ff', 'color': '#ffffff',
        'description': 'water_effect_to_the_health_100'},
}

AQI_COLOR_TCMT = {
  50: {'text': T('Excellent'), 'bgColor': '#00b9e7', 'color': '#666'},
  100: {'text': T('Good'), 'bgColor': '#ffec60', 'color': '#666'},
  150: {'text': T('Lightly Polluted'), 'bgColor': '#ffb753', 'color': '#666'},
  200: {'text': T('Moderately Polluted'), 'bgColor': '#fd4441', 'color': '#666'},
  300: {'text': T('Heavily Polluted'), 'bgColor': '#d19341', 'color': '#666'},
  500: {'text': T('Very Heavily Polluted'), 'bgColor': '#d19341', 'color': '#666'},
  999: {'text': T('Severely Polluted'), 'bgColor': '#7f1f25', 'color': '#fff'},
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

RULES = {

  'VIEW': {'value': 'view', 'name': 'Permission_View', 'seq': 1},
  'CREATE': {'value': 'create', 'name': 'Permission_Create', 'seq': 2},
  'EDIT': {'value': 'edit', 'name': 'Permission_Edit', 'seq': 3},
  'DELETE': {'value': 'delete', 'name': 'Permission_Delete', 'seq': 4},
}

RULES_ACTION = {
  'DASHBOARD': {
    'VIEW': {'value': 'view', 'name': 'Permission_View', 'seq': 1}
  },
  'MAP': {
    'VIEW': {'value': 'view', 'name': 'Permission_View', 'seq': 1}
  },
  'REALTIME': {
    'VIEW': {'value': 'view', 'name': 'Permission_View', 'seq': 1}
  },
  'REPORT': {
    'COMMON': {
      'VIEW': {'value': 'view', 'name': 'Permission_View', 'seq': 1}
    },
  },
  'QI': {
    'COMMON': {
      'VIEW': {'value': 'view', 'name': 'Permission_View', 'seq': 1}
    },
    'AQI': {
      'VIEW': {'value': 'view', 'name': 'Permission_View', 'seq': 1}
    },
    'WQI': {
      'VIEW': {'value': 'view', 'name': 'Permission_View', 'seq': 1}
    },
  },
  'CAMERA': {
    'COMMON': {
      'VIEW': {'value': 'view', 'name': 'Permission_View', 'seq': 1}
    }
  },
  'ALARM_LOG': {
    'COMMON': {
      'VIEW': {'value': 'view', 'name': 'Permission_View', 'seq': 1}
    },
    'HISTORY_DISCONNECT': {
      'VIEW': {'value': 'view', 'name': 'Permission_View', 'seq': 1}
    }
  },
  'QA_QC': {
    'COMMON': {
      'VIEW': {'value': 'view', 'name': 'Permission_View', 'seq': 1}
    }
  },
  'NOTIFICATION': {
    'COMMON': {
      'VIEW': {'value': 'view', 'name': 'Permission_View', 'seq': 1}
    }
  },
  'ADJUST_COMPANY': {
    'COMMON': {
      'VIEW': {'value': 'view', 'name': 'Permission_View', 'seq': 1}
    },
    'ADJUTS_LIST': {
      'VIEW': {'value': 'view', 'name': 'Permission_View', 'seq': 1},
      'CREATE': {'value': 'create', 'name': 'Permission_Create', 'seq': 2},
      'EDIT': {'value': 'edit', 'name': 'Permission_Edit', 'seq': 3},
      'DELETE': {'value': 'delete', 'name': 'Permission_Delete', 'seq': 4}
    },
    'ADJUTS_CALENDAR': {
      'VIEW': {'value': 'view', 'name': 'Permission_View', 'seq': 1},
      'CREATE': {'value': 'create', 'name': 'Permission_Create', 'seq': 2}
    }
  },
  'ADJUST_MANAGER': {
    'COMMON': {
      'VIEW': {'value': 'view', 'name': 'Permission_View', 'seq': 1}
    },
    'ADJUTS_LIST': {
      'VIEW': {'value': 'view', 'name': 'Permission_View', 'seq': 1},
      'CREATE': {'value': 'create', 'name': 'Permission_Create', 'seq': 2},
      'EDIT': {'value': 'edit', 'name': 'Permission_Edit', 'seq': 3},
      'DELETE': {'value': 'delete', 'name': 'Permission_Delete', 'seq': 4}
    },
    'ADJUTS_CALENDAR': {
      'VIEW': {'value': 'view', 'name': 'Permission_View', 'seq': 1},
      'CREATE': {'value': 'create', 'name': 'Permission_Create', 'seq': 2}
    }
  },
  'COMMAND': {
    'COMMON': {
      'VIEW': {'value': 'view', 'name': 'Permission_View', 'seq': 1}
    },
    'EXECUTE_COMMAND': {
      'VIEW': {'value': 'view', 'name': 'Permission_View', 'seq': 1},
      'CREATE': {'value': 'create', 'name': 'Permission_Create', 'seq': 2},
      'EDIT': {'value': 'edit', 'name': 'Permission_Edit', 'seq': 3},
      'DELETE': {'value': 'delete', 'name': 'Permission_Delete', 'seq': 4}
    },
    'COMMNAND_SCHEDULE': {
      'VIEW': {'value': 'view', 'name': 'Permission_View', 'seq': 1},
      'CREATE': {'value': 'create', 'name': 'Permission_Create', 'seq': 2},
      'DELETE': {'value': 'delete', 'name': 'Permission_Delete', 'seq': 3}
    },
    'COMMNAND_HISTORY': {
      'VIEW': {'value': 'view', 'name': 'Permission_View', 'seq': 1},
      'CREATE': {'value': 'create', 'name': 'Permission_Create', 'seq': 2}
    },
    'COMMNAND_RESULTS': {
      'VIEW': {'value': 'view', 'name': 'Permission_View', 'seq': 1}
    },
  },
  'STATIONS': {
    'COMMON': {
      'VIEW': {'value': 'view', 'name': 'Permission_View', 'seq': 1}
    }
  },
  'ADMIN': {
    'COMMON': {
      'VIEW': {'value': 'view', 'name': 'Permission_View', 'seq': 1}
    },
    'RESETPASSWORD': {
      'VIEW': {'value': 'view', 'name': 'Permission_View', 'seq': 1},
      'EDIT': {'value': 'edit', 'name': 'Permission_Edit', 'seq': 2}
    },
    'GROUP': {
      'VIEW': {'value': 'view', 'name': 'Permission_View', 'seq': 1},
      'CREATE': {'value': 'create', 'name': 'Permission_Create', 'seq': 2},
      'EDIT': {'value': 'edit', 'name': 'Permission_Edit', 'seq': 3},
      'DELETE': {'value': 'delete', 'name': 'Permission_Delete', 'seq': 4}
    },
    'USERS': {
      'VIEW': {'value': 'view', 'name': 'Permission_View', 'seq': 1},
      'CREATE': {'value': 'create', 'name': 'Permission_Create', 'seq': 2},
      'EDIT': {'value': 'edit', 'name': 'Permission_Edit', 'seq': 3},
      'DELETE': {'value': 'delete', 'name': 'Permission_Delete', 'seq': 4}
    },
    'TASK': {
      'VIEW': {'value': 'view', 'name': 'Permission_View', 'seq': 1},
      'CREATE': {'value': 'create', 'name': 'Permission_Create', 'seq': 2}
    }
  },
  'VIEW_LOG': {
    'COMMON': {
      'VIEW': {'value': 'view', 'name': 'Permission_View', 'seq': 1}
    },
    'ORIGIN': {
      'VIEW': {'value': 'view', 'name': 'Permission_View', 'seq': 1}
    },
    '1_H': {
      'VIEW': {'value': 'view', 'name': 'Permission_View', 'seq': 1}
    },
    '8_H': {
      'VIEW': {'value': 'view', 'name': 'Permission_View', 'seq': 1}
    },
    'DAY': {
      'VIEW': {'value': 'view', 'name': 'Permission_View', 'seq': 1}
    },
    'MONTH': {
      'VIEW': {'value': 'view', 'name': 'Permission_View', 'seq': 1}
    },
    'AQI_H': {
      'VIEW': {'value': 'view', 'name': 'Permission_View', 'seq': 1}
    },
    'AQI_D': {
      'VIEW': {'value': 'view', 'name': 'Permission_View', 'seq': 1}
    },
    'WQI_H': {
      'VIEW': {'value': 'view', 'name': 'Permission_View', 'seq': 1}
    },
  },
  'SETTING': {
    'COMMON': {
      'VIEW': {'value': 'view', 'name': 'Permission_View', 'seq': 1}
    },
    'STATION': {
      'VIEW': {'value': 'view', 'name': 'Permission_View', 'seq': 1},
      'CREATE': {'value': 'create', 'name': 'Permission_Create', 'seq': 2},
      'EDIT': {'value': 'edit', 'name': 'Permission_Edit', 'seq': 3},
      'DELETE': {'value': 'delete', 'name': 'Permission_Delete', 'seq': 4},
      'EXPORT': {'value': 'export', 'name': 'Permission_Export', 'seq': 5}
      # 'CHECK_MAPPING_INDICATOR' : {'value': '', 'name': '', 'seq': 6},
      # 'CHECK_CONNECT_FTP': {'value': '', 'name': '', 'seq': 7}
    },
    'MANAGE_HISTORY': {
      'VIEW': {'value': 'view', 'name': 'Permission_View', 'seq': 1}
    },
    'QCVN': {
      'VIEW': {'value': 'view', 'name': 'Permission_View', 'seq': 1},
      'CREATE': {'value': 'create', 'name': 'Permission_Create', 'seq': 2},
      'EDIT': {'value': 'edit', 'name': 'Permission_Edit', 'seq': 3},
      'DELETE': {'value': 'delete', 'name': 'Permission_Delete', 'seq': 4}
    },
    'PUBLIC': {
      'VIEW': {'value': 'view', 'name': 'Permission_View', 'seq': 1},
      'EDIT': {'value': 'edit', 'name': 'Permission_Edit', 'seq': 2}
    },
    'SETTING_AQI': {
      'VIEW': {'value': 'view', 'name': 'Permission_View', 'seq': 1},
      'EDIT': {'value': 'edit', 'name': 'Permission_Edit', 'seq': 2}
    },
    'SETTING_WQI': {
      'VIEW': {'value': 'view', 'name': 'Permission_View', 'seq': 1},
      'EDIT': {'value': 'edit', 'name': 'Permission_Edit', 'seq': 2}
    },
    'DATALOGGER': {
      'VIEW': {'value': 'view', 'name': 'Permission_View', 'seq': 1},
      'CREATE': {'value': 'create', 'name': 'Permission_Create', 'seq': 2},
      'EDIT': {'value': 'edit', 'name': 'Permission_Edit', 'seq': 3},
      'DELETE': {'value': 'delete', 'name': 'Permission_Delete', 'seq': 4}
    },
    'EQUIPMENTS': {
      'VIEW': {'value': 'view', 'name': 'Permission_View', 'seq': 1},
      'CREATE': {'value': 'create', 'name': 'Permission_Create', 'seq': 2},
      'EDIT': {'value': 'edit', 'name': 'Permission_Edit', 'seq': 3},
      'DELETE': {'value': 'delete', 'name': 'Permission_Delete', 'seq': 4}
    },
    'INDICATOR': {
      'VIEW': {'value': 'view', 'name': 'Permission_View', 'seq': 1},
      'CREATE': {'value': 'create', 'name': 'Permission_Create', 'seq': 2},
      'EDIT': {'value': 'edit', 'name': 'Permission_Edit', 'seq': 3},
      'DELETE': {'value': 'delete', 'name': 'Permission_Delete', 'seq': 4}
    },
    'STATION_TYPE': {
      'VIEW': {'value': 'view', 'name': 'Permission_View', 'seq': 1},
      'CREATE': {'value': 'create', 'name': 'Permission_Create', 'seq': 2},
      'EDIT': {'value': 'edit', 'name': 'Permission_Edit', 'seq': 3},
      'DELETE': {'value': 'delete', 'name': 'Permission_Delete', 'seq': 4}
    },
    'AREAS': {
      'VIEW': {'value': 'view', 'name': 'Permission_View', 'seq': 1},
      'CREATE': {'value': 'create', 'name': 'Permission_Create', 'seq': 2},
      'EDIT': {'value': 'edit', 'name': 'Permission_Edit', 'seq': 3},
      'DELETE': {'value': 'delete', 'name': 'Permission_Delete', 'seq': 4}
    },
    'PROVINCE': {
      'VIEW': {'value': 'view', 'name': 'Permission_View', 'seq': 1},
      'CREATE': {'value': 'create', 'name': 'Permission_Create', 'seq': 2},
      'EDIT': {'value': 'edit', 'name': 'Permission_Edit', 'seq': 3},
      'DELETE': {'value': 'delete', 'name': 'Permission_Delete', 'seq': 4}
    },
    'AGENTS': {
      'VIEW': {'value': 'view', 'name': 'Permission_View', 'seq': 1},
      'CREATE': {'value': 'create', 'name': 'Permission_Create', 'seq': 2},
      'EDIT': {'value': 'edit', 'name': 'Permission_Edit', 'seq': 3},
      'DELETE': {'value': 'delete', 'name': 'Permission_Delete', 'seq': 4}
    },
    'OWNER_INFOMATION': {
      'VIEW': {'value': 'view', 'name': 'Permission_View', 'seq': 1},
      'EDIT': {'value': 'edit', 'name': 'Permission_Edit', 'seq': 2}
    },
    'MAIL_SERVER': {
      'VIEW': {'value': 'view', 'name': 'Permission_View', 'seq': 1},
      'EDIT': {'value': 'edit', 'name': 'Permission_Edit', 'seq': 2}
    },
    'FAQ': {
      'VIEW': {'value': 'view', 'name': 'Permission_View', 'seq': 1},
      'EDIT': {'value': 'edit', 'name': 'Permission_Edit', 'seq': 2}
    }
  }
}

FUNC_NAMES = {
  'view_log': "Historical data",
  "ftp_send_receive": "Send/receive FTP",
  "data_adjust_company": "Station adjustment company",
  "master_agent": "Master agents",
  "master_qcvn": "Master qcvns",
  "master_equipment": "Master equipments",
  "master_station": "Master stations",
  "master_indicator": "Master indicators",
  "master_station_type": "Master station types",
  "master_area": "Master areas",
  "master_province": "Master provinces",
  "admin_reset_pwd": "Reset user's password",
  "admin_grant_privilege": "Grant privileges",
  "admin_group": "Admin groups",
  "admin_user": "Admin users",
  "admin_func": "System functions",
  "admin_batch": "Manage batch background",
  "command_log": "Command log",
  "settings": "Settings",
  "ftp_transfer": "File transfer",
  "commands_schedule": "Make command schedules",
  "command_results": "Manage command results",
  "commands": "Manage commands",
  "adjust_schedule": "Manage adjustment schedules",
  "data": "Manage data",
  "data_adjust": "Data adjust",
  "data_alarm": "Data alarm",
  "station_off_log": "View station disconnect logs",
  "alarm_log": "Alarm logs",
  "wqi": "WQI",
  "notifications": "Notifications",
  "aqi": "AQI",
  "camera": "Camera",
  "realtime": "Realtime",
  "map": "Station map",
  "dashboard": "Dashboard",

}

SYS_PERMISSION = {
  "dashboard": {'name': 'Dashboard', 'rules': RULES_ACTION['DASHBOARD'], 'seq': 1},
  "map": {'name': 'Station map', 'rules': RULES_ACTION['MAP'], 'seq': 2},
  "realtime": {'name': 'Realtime', 'rules': RULES_ACTION['REALTIME'], 'seq': 3},
  'view_log': {'name': 'Historical data', 'rules': RULES_ACTION['VIEW_LOG']['ORIGIN'], 'seq': 4},
  "data_adjust_company": {'name': 'Station adjustment company', 'rules': RULES_ACTION['ADJUST_COMPANY']['COMMON'],
                          'seq': 6},
  "master_agent": {'name': 'Master agents', 'rules': RULES_ACTION['SETTING']['AGENTS'], 'seq': 7},
  "master_qcvn": {'name': 'Master qcvns', 'rules': RULES_ACTION['SETTING']['QCVN'], 'seq': 8},
  "master_equipment": {'name': 'Master equipments', 'rules': RULES_ACTION['SETTING']['EQUIPMENTS'], 'seq': 9},
  "master_station": {'name': 'Master stations', 'rules': RULES_ACTION['SETTING']['STATION'], 'seq': 10},
  "master_indicator": {'name': 'Master indicators', 'rules': RULES_ACTION['SETTING']['INDICATOR'], 'seq': 11},
  "master_station_type": {'name': 'Master station types', 'rules': RULES_ACTION['SETTING']['STATION_TYPE'], 'seq': 12},
  "master_area": {'name': 'Master areas', 'rules': RULES_ACTION['SETTING']['AREAS'], 'seq': 13},
  "master_province": {'name': 'master_province', 'rules': RULES_ACTION['SETTING']['PROVINCE'], 'seq': 14},
  "admin_reset_pwd": {'name': 'Reset user password', 'rules': RULES_ACTION['ADMIN']['RESETPASSWORD'], 'seq': 15},
  "admin_grant_privilege": {'name': 'Grant privileges', 'rules': RULES_ACTION['ADMIN']['COMMON'], 'seq': 16},
  "admin_group": {'name': 'Admin groups', 'rules': RULES_ACTION['ADMIN']['COMMON'], 'seq': 17},
  "admin_user": {'name': 'Admin users', 'rules': RULES_ACTION['ADMIN']['USERS'], 'seq': 18},
  "admin_func": {'name': 'System functions', 'rules': RULES_ACTION['ADMIN']['COMMON'], 'seq': 19},
  "admin_batch": {'name': 'Manage batch background', 'rules': RULES_ACTION['ADMIN']['TASK'], 'seq': 20},
  "command_log": {'name': 'Command log', 'rules': RULES_ACTION['COMMAND']['COMMNAND_HISTORY'], 'seq': 21},
  "settings": {'name': 'Settings', 'rules': RULES_ACTION['SETTING']['COMMON'], 'seq': 22},
  "commands_schedule": {'name': 'Make command schedules', 'rules': RULES_ACTION['COMMAND']['COMMNAND_SCHEDULE'],
                        'seq': 24},
  "command_results": {'name': 'Manage command results', 'rules': RULES_ACTION['COMMAND']['COMMNAND_RESULTS'],
                      'seq': 25},
  "commands": {'name': 'Manage commands', 'rules': RULES_ACTION['COMMAND']['COMMON'], 'seq': 26},
  "adjust_schedule": {'name': 'Manage adjustment schedules', 'rules': RULES_ACTION['ADJUST_MANAGER']['ADJUTS_LIST'],
                      'seq': 27},
  "data": {'name': 'Manage data', 'rules': RULES_ACTION['VIEW_LOG']['COMMON'], 'seq': 28},
  "data_adjust": {'name': 'Data adjust', 'rules': RULES_ACTION['ADJUST_MANAGER']['COMMON'], 'seq': 29},
  "data_alarm": {'name': 'Data alarm', 'rules': RULES_ACTION['ALARM_LOG']['COMMON'], 'seq': 30},
  "station_off_log": {'name': 'View station disconnect logs', 'rules': RULES_ACTION['ALARM_LOG']['HISTORY_DISCONNECT'],
                      'seq': 31},
  "alarm_log": {'name': 'Alarm logs', 'rules': RULES_ACTION['ALARM_LOG']['COMMON'], 'seq': 32},
  "notifications": {'name': 'Notifications', 'rules': RULES_ACTION['NOTIFICATION']['COMMON'], 'seq': 33},
  "wqi": {'name': 'WQI', 'rules': RULES_ACTION['QI']['WQI'], 'seq': 34},
  "aqi": {'name': 'AQI', 'rules': RULES_ACTION['QI']['AQI'], 'seq': 35},
  "camera": {'name': 'Camera', 'rules': RULES_ACTION['CAMERA']['COMMON'], 'seq': 36},
  "report": {'name': 'Report', 'rules': RULES_ACTION['REPORT']['COMMON'], 'seq': 37}
}

SYS_PERMISSION_NEW = {
  # TrangChu
  "dashboard": {'name': 'Dashboards', 'rules': RULES_ACTION['DASHBOARD'], 'seq': 1},
  # BanDo
  "map": {'name': 'Station map', 'rules': RULES_ACTION['MAP'], 'seq': 2},
  # TheoDoiOnLine
  "realtime": {'name': 'Realtime monitor', 'rules': RULES_ACTION['REALTIME'], 'seq': 3},
  # TraCuuDulieu
  "view_log": {'name': 'Historical data', 'rules': RULES_ACTION['VIEW_LOG']['ORIGIN'], 'seq': 4},
  # BaoCao
  "view_report": {'name': 'Report', 'rules': RULES_ACTION['REPORT']['COMMON'], 'seq': 5},
  # AQI-WQI
  "qi": {'name': 'WQI / AQI', 'rules': RULES_ACTION['QI']['COMMON'], 'seq': 6},
  # AQI
  "aqi": {'name': 'AQI', 'rules': RULES_ACTION['QI']['AQI'], 'seq': 7},
  # WQI
  "wqi": {'name': 'WQI', 'rules': RULES_ACTION['QI']['WQI'], 'seq': 8},
  # Camera
  "camera": {'name': 'Camera', 'rules': RULES_ACTION['CAMERA']['COMMON'], 'seq': 9},
  # NhatKyCanhBao
  "alarm_log": {'name': 'Alarm logs', 'rules': RULES_ACTION['ALARM_LOG']['COMMON'], 'seq': 10},
  # KiemDuyetDuLieu
  "qa_qc": {'name': 'QA/QC data', 'rules': RULES_ACTION['QA_QC']['COMMON'], 'seq': 11},
  # QuanLyHieuChuan
  "adjust_manager": {'name': 'Station adjustment', 'rules': RULES_ACTION['ADJUST_MANAGER']['COMMON'], 'seq': 12},
  # HieuChuanDoanhNghiep
  "adjust_company": {'name': 'Station adjustment company', 'rules': RULES_ACTION['ADJUST_COMPANY']['COMMON'],
                     'seq': 13},
  # DieuKhienLayMau
  "commands": {'name': 'Command get data', 'rules': RULES_ACTION['COMMAND']['COMMON'], 'seq': 14},
  # DieuKhienLayMau:
  "control": {'name': 'Execute Command', 'rules': RULES_ACTION['COMMAND']['EXECUTE_COMMAND'], 'seq': 15},
  # LapLichLayMau
  "command_schedule": {'name': 'Command schedule', 'rules': RULES_ACTION['COMMAND']['COMMNAND_SCHEDULE'], 'seq': 16},
  # LichSuLayMau
  "command_history": {'name': 'Historical commands', 'rules': RULES_ACTION['COMMAND']['COMMNAND_HISTORY'], 'seq': 17},
  # KetQuaLayMau
  "command_result": {'name': 'Command results', 'rules': RULES_ACTION['COMMAND']['COMMNAND_RESULTS'], 'seq': 18},
  # QuanLyTram(ThongKeTheoTungLoaiTram)
  "manager_station_type": {'name': 'Stations', 'rules': RULES_ACTION['STATIONS']['COMMON'], 'seq': 19},
  # PhanQuyen(quantriAdmin)
  "admin": {'name': 'Administrator', 'rules': RULES_ACTION['ADMIN']['COMMON'], 'seq': 20},
  # DichVuChayNgam
  "tasks": {'name': 'Schedule batch', 'rules': RULES_ACTION['ADMIN']['TASK'], 'seq': 21},
  # DanhSachNguoiDung
  "users": {'name': 'User list', 'rules': RULES_ACTION['ADMIN']['USERS'], 'seq': 22},
  # DanhSachNhomQuyen
  "groups": {'name': 'Group list', 'rules': RULES_ACTION['ADMIN']['GROUP'], 'seq': 23},
  # ResetPassword
  "reset_password": {'name': 'Reset password', 'rules': RULES_ACTION['ADMIN']['RESETPASSWORD'], 'seq': 24},
  # CaiDat(QuanLyCacModule)
  "settings": {'name': 'Master data', 'rules': RULES_ACTION['SETTING']['COMMON'], 'seq': 25},
  # QuanLyTram
  "stations": {'name': 'Stations', 'rules': RULES_ACTION['SETTING']['STATION'], 'seq': 26},
  # QuanLyLichSuThayDoiCacThongTin
  "manage_stations_history": {'name': 'manage_stations_history', 'rules': RULES_ACTION['SETTING']['MANAGE_HISTORY'],
                              'seq': 27},
  # QCVN
  "qcvn": {'name': 'QCVN', 'rules': RULES_ACTION['SETTING']['QCVN'], 'seq': 28},
  # CongBoThongTin
  "public": {'name': 'Public indicators', 'rules': RULES_ACTION['SETTING']['PUBLIC'], 'seq': 29},
  # CongThucTinhAQI
  "setting_aqi": {'name': 'Setting AQI', 'rules': RULES_ACTION['SETTING']['SETTING_AQI'], 'seq': 30},
  # CongThucTinhWQI
  "setting_wqi": {'name': 'Setting WQI', 'rules': RULES_ACTION['SETTING']['SETTING_WQI'], 'seq': 31},
  # QuanLyCacDatalogger
  "datalogger": {'name': 'LBL_Datalogger', 'rules': RULES_ACTION['SETTING']['DATALOGGER'], 'seq': 32},
  # QuanLyCacThietBi
  "equipments": {'name': 'Equipments', 'rules': RULES_ACTION['SETTING']['EQUIPMENTS'], 'seq': 33},
  # QuanLyCacThongSo
  "indicators": {'name': 'Indicators', 'rules': RULES_ACTION['SETTING']['INDICATOR'], 'seq': 34},
  # QuanLyThanhPhanMoiTruong
  "station_types": {'name': 'Station types', 'rules': RULES_ACTION['SETTING']['STATION_TYPE'], 'seq': 35},
  # QuanLyNhomTram
  "areas": {'name': 'Areas', 'rules': RULES_ACTION['SETTING']['AREAS'], 'seq': 36},
  # QuanLyDonViQuanLy
  "provinces": {'name': 'Provinces', 'rules': RULES_ACTION['SETTING']['PROVINCE'], 'seq': 37},
  # CoQuanQuanLy
  "agents": {'name': 'Management agents', 'rules': RULES_ACTION['SETTING']['AGENTS'], 'seq': 38},
  # ThongTinChuQuan
  "owner_information": {'name': 'Owner Information', 'rules': RULES_ACTION['SETTING']['OWNER_INFOMATION'], 'seq': 39},
  # CauHinhEmail
  "mail_server": {'name': 'Mail Server', 'rules': RULES_ACTION['SETTING']['MAIL_SERVER'], 'seq': 40},
  # QuanLyFAQ
  "faq": {'name': 'FAQ', 'rules': RULES_ACTION['SETTING']['FAQ'], 'seq': 41}
}


import operator as op

# pH, As, Cd, Pb, Cr6+, Cu, Zn, Hg nhom I
# DO, BOD5, COD, TOC, N-NH4,  NO3, TN, P-PO4, TP nhom II
# TURBIDITY, TSS nhom III
# Coliform nhom IV
# WQI can co nhom II, min 3 nhom, moi nhom it nhat 1 thong so (can nhom II vs tong nhom >=3)

WQI_GR_1 = ['PH', 'AS', 'CD', 'PB', 'CR6+', 'CU', 'ZN', 'HG']
WQI_GR_2 = ['DO', 'BOD', 'COD', 'TOC', 'N-NH4', 'NO3', 'TN', 'P-PO4', 'TP']
WQI_GR_3 = ['TURBIDITY', 'TSS']
WQI_GR_4 = ['COLIFORM']
WQI_ALL = WQI_GR_1 + WQI_GR_2 + WQI_GR_3 + WQI_GR_4
WQI_INDICATOR = ['BOD', 'COD', 'TOC', 'N-NH4', 'NO3', 'TN', 'P-PO4', 'TP', 'AS', 'CD', 'PB', 'CR6+', 'CU', 'ZN', 'HG',
                 'TURBIDITY', 'TSS', 'COLIFORM']
WQI_INDICATOR_I = ['pH', 'AS', 'Cd', 'Pb', 'Cr6+', 'Cu', 'Zn', 'Hg']
WQI_INDICATOR_II = ['DO', 'BOD', 'COD', 'TOC', 'N-NH4', 'NO3', 'TN', 'P-PO4', 'TP']
WQI_INDICATOR_III = ['TURBIDITY', 'TSS']
WQI_INDICATOR_IV = ['Coliform']

# <= VS >=
WQI_INDICATOR_SAME_1 = ['BOD', 'COD', 'TOC', 'TN', 'P-PO4', 'TP', 'CR6+', 'CU', 'ZN', 'TURBIDITY']
# <= VS >
WQI_INDICATOR_SAME_2 = ['NO3', 'TSS', 'COLIFORM', 'AS']
# < VS >=
WQI_INDICATOR_SAME_3 = ['N-NH4', 'CD', 'PB', 'HG']

WQI_BP = {
  'BOD': [4, 6, 15, 25, 50],
  'COD': [10, 15, 30, 50, 150],
  'TOC': [4, 6, 15, 25, 50],
  'N-NH4': [0.3, 0.3, 0.6, 0.9, 5],
  'NO3': [2, 5, 10, 15, 15],
  'TN': [3, 6, 12, 18, 40],
  'P-PO4': [0.1, 0.2, 0.3, 0.5, 4],
  'TP': [0.2, 0.4, 0.6, 2, 6],
  'TSS': [20, 30, 50, 100, 100],
  'TURBIDITY': [5, 20, 30, 70, 100],
  'COLIFORM': [2500, 5000, 7500, 10000, 10000],
  'AS': [0.01, 0.02, 0.05, 0.1, 0.1],
  'CD': [0.005, 0.005, 0.008, 0.01, 0.1],
  'PB': [0.02, 0.02, 0.04, 0.05, 0.5],
  'CR6+': [0.01, 0.02, 0.04, 0.05, 0.1],
  'CU': [0.1, 0.2, 0.5, 1.0, 2],
  'ZN': [0.5, 1.0, 1.5, 2.0, 3],
  'HG': [0.001, 0.001, 0.0015, 0.002, 0.01],
}

OP_1 = {
  'BOD': [op.le, op.lt, op.lt, op.lt, op.ge],
  'COD': [op.le, op.lt, op.lt, op.lt, op.ge],
  'TOC': [op.le, op.lt, op.lt, op.lt, op.ge],
  'N-NH4': [op.lt, op.le, op.lt, op.lt, op.ge],
  'NO3': [op.le, op.lt, op.lt, op.lt, op.gt],
  'TN': [op.le, op.lt, op.lt, op.lt, op.ge],
  'P-PO4': [op.le, op.lt, op.lt, op.lt, op.ge],
  'TP': [op.le, op.lt, op.lt, op.lt, op.ge],
  'TSS': [op.le, op.lt, op.lt, op.le, op.gt],
  'TURBIDITY': [op.le, op.lt, op.lt, op.lt, op.ge],
  'COLIFORM': [op.le, op.lt, op.lt, op.le, op.gt],
  'AS': [op.le, op.lt, op.lt, op.le, op.gt],
  'CD': [op.lt, op.le, op.lt, op.lt, op.ge],
  'PB': [op.lt, op.le, op.lt, op.lt, op.ge],
  'CR6+': [op.le, op.lt, op.lt, op.lt, op.ge],
  'CU': [op.le, op.lt, op.lt, op.lt, op.ge],
  'ZN': [op.le, op.lt, op.lt, op.lt, op.ge],
  'HG': [op.lt, op.le, op.lt, op.lt, op.ge],
}

QI = [100, 75, 50, 25, 10]
DO_BP = [20, 20, 50, 75, 88, 112, 125, 150, 200, 200]
DO_QI = [1, 25, 50, 75, 100, 100, 75, 50, 25, 1]
OP_2 = [op.le, op.lt, op.lt, op.lt, op.lt, op.lt, op.lt, op.lt, op.lt, op.ge]

PH_BP = [5.5, 5.5, 6, 8.5, 9, 9]
PH_QI = [10, 50, 100, 100, 50, 10]
OP_3 = [op.lt, op.lt, op.lt, op.lt, op.lt, op.gt]

EXPRESSION_QCVN_INDICATOR = {
  'EXPRESSION_1': {'value': 2, 'text': T('qcvn_indecator>=min')},
  'EXPRESSION_2': {'value': 1, 'text': T('qcvn_indecator<=max')},
  'EXPRESSION_3': {'value': 3, 'text': T('min<=qcvn_indecator<=max')},
  # 'EXPRESSION_4': {'value': 4, 'text': T('min<qcvn_indecator<=max')},
  # 'EXPRESSION_5': {'value': 5, 'text': T('min<=qcvn_indecator<max')},
}

AQI_INDICATOR_SETTING = ['SO2', 'CO', 'NO2', 'O3', 'PM-2-5', 'PM-10']
HAVE_FACTOR_QCVN = {
  'NO': {'value': 2, 'text': T('Not_Apply')},
  'YES': {'value': 1, 'text': T('Apply')},
}

DAYS_OF_WEEK = {
  'MONDAY': {'value': 0, 'text': T('Mon')},
  'TUESDAY': {'value': 1, 'text': T('Tue')},
  'WEDNESDAY': {'value': 2, 'text': T('Wed')},
  'THURSDAY': {'value': 3, 'text': T('Thu')},
  'FRIDAY': {'value': 4, 'text': T('Fri')},
  'SATURDAY': {'value': 5, 'text': T('Sat')},
  'SUNDAY': {'value': 6, 'text': T('Sun')},
}

FREQUENCY = {
  'DAILY': {'value': 'daily', 'text': T('Every day')},
  'WEEKLY': {'value': 'weekly', 'text': T('Every week')},
  'MONTHLY': {'value': 'monthly', 'text': T('Every month')},
}
