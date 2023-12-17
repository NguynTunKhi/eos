# -*- coding: utf-8 -*-

JS_LANGUAGES = '''
{
    "JS_MSG_SAVE_SUCCESS": "Data saved successfully!",
    "JS_MSG_CONFIRM_SAVE": "Do you want to save?",
    "JS_MSG_DATA_LOGGER": "DataLogger ID not configured. Do you want to configure?",
    "JS_MSG_CONFIRM_DELETE": "Do you want to delete?",
    "JS_MSG_CONFIRM_ISSUE_COMMAND": "Do you want to execute sampling order?",
    "JS_MSG_CONFIRM_SET_SCHEDULE_COMMAND": "Do you want to set a sampling plan?",
    "MSG_CONFIRM_RUN_TASK": "Do you want to start the batch to run automatically?",
    "JS_MSG_CONFIRM_UPDATE" : "Parameter already exists. Would you like to update?",
    "JS_DT_SEARCH": "Searc",
    "JS_DT_DISPLAY": "Display ",
    "JS_DT_NO_RECORD": "No data! ",
    "LBL_PLEASE_WAIT": "Processing ..",
    "LBL_OK": "OK",
    "LBL_NOTIFICATION": "Notification",
    "LBL_ALERT": "Warning",
    "LBL_ERROR": "Error",
    "LBL_CANCEL": "Cancel",
    "LBL_CONFIRM_ACTION": " ",
    "LBL_HAVE_NOT_SELECTED_RECORD_YET": "No data selected!",
    "LBL_ONLY_SELECT_ONE_RECORD": "Just select the data stream!",
    "JS_DT_IN": "Total ",
    "JS_DT_FIRST": "|<",
    "JS_DT_PREVIOUS": "<<",
    "JS_DT_NEXT": ">>",
    "JS_DT_LAST": ">|",
    "JS_MSG_UPLOAD_SUCCESSFULLY": "Upload successful!",
    "JS_MSG_GENERATED_SUCCESSFULLY": "File export success!",
    "JS_MSG_THIS_FILE_EXISTED_OVERWRITE": "File already exists. Do you want to overwrite?",
    "MSG_PASSWORD_AGAIN_IS_NOT_MATCHED": "Password incorrect",
    "MSG_ONLY_INPUT_IMAGE_FOR_THIS_FIELD": "Please enter the image file for the 'Avatar' field!",
    "LBL_INPUT_VALID_IP_ADDRESS": "Enter a valid URL!",
    "LBL_INPUT_GREATER_THAN_TWO": "Input Number >= 2",
    "LBL_INPUT_INTEGER": "Please enter an integer!",
    "LBL_INPUT_INTEGER_MAX": "Note that the upper limit must be less than the standard value or the middle value (in the case of lower value)!",
    "LBL_INPUT_IP": "Wrong format IP Address",
    "LBL_SELECT_THIS_FIELD": "Please select this school!",
    "LBL_USERNAME_IS_INVALID": "Username is not valid!",
    "MSG_SELECT_RECORD_TO_DELETE": "Please select a record to delete!",
    "MSG_SELECT_ATLEAST_ONE_RECORD": "Please select at least one record!",
    "MSG_BIRTHDATE_MUST_BE_GREATER_THAN_NOW": "Date of birth should not be greater than the current date!",
    "JS_MSG_INVALID_FILE_JAR": "File format is not .jar!",
    "JS_DATA": "Data",
    "JS_FIELD_NAME": "Name",
    "Please select a station first!": "Please select a station!",
    "Please select both year and month/quarter!": "Please select both year and month/quarter!",
    "LBL_INPUT_MANDATORY_FIELD": "Please enter this field!",
    "LBL_CBB_DATALOGGER_TYPE": "You have not selected Datalogger type!",
    "LBL_INPUT_USERNAME_FIELD": "Username is malformed (instant, no spaces)",
    "LBL_INPUT_DIGIT_VALUE" : "Please enter this field a numeric value!",
    "LBL_INPUT_RANGE" : "Please enter a value in the range {0} - {1}",
    "LBL_INPUT_EMAIL_FIELD" : "Email invalidate",
    "LBL_INPUT_PHONE_FIELD" : "Phone invalidate",
    "ERR_Tendecy_Preparing_Exceed" : "Lower measurement value <Middle measurement value <Non-normality value",
    "ERR_Day_Search" : "The start date is greater than the end date",
    "ERR_Day_Input" : "The entered date is incorrect",
    "ERR_Day_Input_To_Date" : "The entered end date is incorrect",
    "ERR_Day_Input_From_Date" : "The input start date is incorrect",
    "ERR_Day_Input_From_Date_1_YEAR" : "Start date is more than 1 year from the end date",
    "ERR_Day_Input_From_Date_1_MONTH" : "Start date is more than 1 month from the end date",
    "ERR_Excel_Export_1_Month" : "Cannot export excel file for more than 1 month",
    "ERR_Day_Input_From_Date_14_DAYS" : "Start date is more than 14 days from the end date",
    "ERR_Day_Blank" : "No date entered",
    "ERR_Day_Input_Blank" : "No start date entered",
    "ERR_Day_Input_To_Date_Max_Exceed" : "The end date cannot be too current",
    "View more": "View more",
    "Indicators": "Indicator",
    "Show labels": "Label display",
    "Warning Levels": "Alert level",
    "Unit": "Unit",
    "Value": "Value",
    "Parameter": "Indicator",
    "Status:": "Status",
    "Latitude:": "Latitude",
    "Longitude": "Longitude",
    "Address:": "Address:",
    "Province:": "Province:",
    "Station Code:": "Station Code:",
    "Layer Switcher": "Switch background layer",
    "Are you sure to approve?": "Are you sure to approve?",
    "Are you sure to remove?": "Are you sure to remove?",
    "FORBIDDEN": "Not enough permissions to access!",
    "Index": "Index",
    "click for more information": "Click to see more",
    "Air Quanlity Index": "AQI",
    "Water Quanlity Index": "WQI",
    "AQI Indicators": "AQI Indicators",
    "WQI Indicators": "WQI Indicators",
    "MSG_CONFIRM_RUN_TASK": "Are you sure running?",
    "Number of Stations": "Number of Stations",
    "No data": "No data",
    "JS_MSG_txtQcvnMin_less_txtQcvnMax": "The max limit value must be greater than the min limit value",
    "MSG_STATION_NOT_CONFIG_QCVN": "The station has not configured QCVN.",
    "MSG_NO_DATA_SEARCH": "No data available for the time period:",
    "MSG_NO_DATA_EXPORT": "Not enough data to export data",
    "LBL_SUCSESS_CONNECT": "Connection successful!",
    "FTP_SUCSESS_CONNECT": "FTP connection and configuration reading successful!",
    "FTP_FAIL_CONNECT": "FTP connection and configuration reading failed!",
    "LBL_FAIL_CONNECT": "Connection failed!",
    "LBL_FAIL_CONNECT_FTP": "Unable to connect to the FTP server. Please check back!",
    "LBL_IN_PUT_ALL": "Please enter the required fields!",
    "Schedule set successful":"Schedule successful",
    "JS_MSG_ERROR_COMMAND_ID_REQUIRED" : "No order selected",
    "JS_MSG_ERROR_START_TIME_REQUIRED" : "No execution start time selected",
    "JS_MSG_ERROR_END_TIME_REQUIRED" : "No end time for order execution",
    "JS_MSG_ERROR_START_DATE_REQUIRED" : "No command scheduling period selected",
    "JS_MSG_ERROR_END_DATE_REQUIRED" : "No command time period selected",
    "JS_MSG_ERROR_WEEKLY_REQUIRED" : "No repeat schedule selected yet",
    "JS_MSG_ERROR_MONTHLY_REQUIRED" : "No repeat schedule selected yet",
    "JS_MSG_ERROR_TIME_STARTEND_REQUIRED" : "Start time is greater than end time",
    "JS_MSG_ERROR_DATE_STARTEND_REQUIRED" : "Start time is greater than end time",
    "Please select a province!" : "Please select a province!",
    "Please select a province or an area!" : "Please select a province or an area!",
    "Please select a station type!" : "Please select an environmental component!",
    "Please select a station type or an area!" : "Please select a station type or an area!",
    "Please select a station type or province!" : "Please select an environmental component or a province!",
    "Please select time!" : "Please select time!",
    "alert_cant_delete": "Can't Delete Because It's Using!",
    "alert_delete_success": "Delete Success!",
    "sure_to_delete":"Are you sure to delete?"
}
'''