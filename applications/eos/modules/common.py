# -*- coding: utf-8 -*-

from gluon import current
import const


def get_station_types():
	arr = []
	try:
		if current is None or current.db is None:
			return arr
		db = current.db
		conditions = (db.station_types.id > 0)
		conditions &= (db.station_types.del_flag == False)
		ls = db(conditions).select(db.station_types.ALL, orderby=db.station_types.order)
		for row in ls:
			arr.append({'value': int(row.code), 'name': row.station_type, 'image': row.icon})
		return arr
	except Exception as ex:
		print ex.message
		return arr


################################################################################
# hungdx fix lost data  add return last_time
def get_lastest_files_dict_new():
	db = current.db

	rows = db(db.last_data_files.id > 0).select(
		db.last_data_files.filename,
		db.last_data_files.station_id,
		db.last_data_files.lasttime,
	)
	res = {}
	last_time = {}
	for item in rows:
		res[str(item.station_id)] = item.filename
		last_time[str(item.station_id)] = item.lasttime
	return res, last_time


################################################################################
# hungdx new functions start issue 30
def get_lastest_hour_calcu():
	db = current.db

	rows = db(db.data_hour_lastest.id > 0).select(
		db.data_hour_lastest.station_id,
		db.data_hour_lastest.last_time,
	)
	last_time_calc = {}
	for item in rows:
		last_time_calc[str(item.station_id)] = item.last_time
	return last_time_calc


################################################################################
def get_lastest_day_calcu():
	db = current.db

	rows = db(db.data_day_lastest.id > 0).select(
		db.data_day_lastest.station_id,
		db.data_day_lastest.last_time,
	)
	last_time_calc = {}
	for item in rows:
		last_time_calc[str(item.station_id)] = item.last_time
	return last_time_calc


################################################################################
def get_lastest_month_calcu():
	db = current.db

	rows = db(db.data_month_lastest.id > 0).select(
		db.data_month_lastest.station_id,
		db.data_month_lastest.last_time,
	)
	last_time_calc = {}
	for item in rows:
		last_time_calc[str(item.station_id)] = item.last_time
	return last_time_calc


# hungdx end issue 30
################################################################################
def get_lastest_files_dict():
	db = current.db

	rows = db(db.last_data_files.id > 0).select(
		db.last_data_files.filename,
		db.last_data_files.station_id,
	)
	res = {}
	for item in rows:
		res[str(item.station_id)] = item.filename
	return res


################################################################################
def get_usr_dict():
	db = current.db

	rows = db(db.auth_user.id > 0).select(db.auth_user.id, db.auth_user.fullname, db.auth_user.image)
	res_name = {}
	res_avatar = {}

	for item in rows:
		res_name[str(item.id)] = item.fullname
		res_avatar[str(item.id)] = item.image

	return res_name, res_avatar


################################################################################
def get_group_dict():
	db = current.db

	rows = db(db.auth_group.id > 0).select()
	res = {}
	for item in rows:
		res[str(item.id)] = item.role

	return res


################################################################################
def get_province_dict():
	db = current.db

	provinces = db(db.provinces.id > 0).select()
	res = {}
	for item in provinces:
		res[str(item.id)] = item.province_name

	return res


################################################################################
def get_province_have_station(station_type=None):
	db = current.db
	ret = dict()
	conds = db.stations.id > 0
	if station_type is not None:
		conds &= db.stations.station_type == station_type
	stations = db(conds).select(db.stations.province_id, distinct=True)
	province_ids = [station.province_id for station in stations]

	provinces = db(db.provinces.id.belongs(province_ids)).select()

	for row in provinces:
		ret[str(row.id)] = row.as_dict()
	return ret


###############################################################################
def get_province_have_station_for_envisoft(station_type=None):
	db = current.db
	ret = dict()
	conds = db.stations.id > 0
	if station_type is not None:
		conds &= db.stations.station_type == station_type
	session = current.session
	if session:
		if not 'admin' in session.auth.user_groups.values():
			list_station_manager = db(db.manager_stations.user_id == session.auth.user.user_id). \
				select(db.manager_stations.station_id)
			station_ids = [str(item.station_id) for item in list_station_manager]
			conds &= (db.stations.id.belongs(station_ids))
	stations = db(conds).select(db.stations.province_id, distinct=True)
	province_ids = [station.province_id for station in stations]

	provinces = db(db.provinces.id.belongs(province_ids)).select()

	for row in provinces:
		ret[str(row.id)] = row.as_dict()
	return ret


################################################################################
def get_province_have_station_with_station_type(station_type=''):
	db = current.db
	ret = dict()
	c = db.stations.province_id.count()
	conds = db.stations.id > 0
	conds &= db.stations.station_type == station_type
	conds &= db.stations.is_public == True
	rows = db(conds).select(
		db.stations.province_id,
		c,
		groupby=db.stations.province_id
	)
	for row in rows:
		ret[row['stations']['province_id']] = row[c]
	return ret


################################################################################
'''
Get station_indicator by station_id or station_type
Return dict with format: {indicator_id: row.as_dict()}
'''


def get_station_indicator_by_station(station_id='', station_type=''):
	db = current.db
	try:
		si_dict = dict()
		conditions = (db.station_indicator.id > 0)
		conditions &= (db.station_indicator.status == const.SI_STATUS['IN_USE']['value'])
		if station_type:
			db.station_indicator.station_type == station_type
		if station_id:
			db.station_indicator.station_id == station_id
		rows = db(conditions).select(db.station_indicator.ALL)
		for row in rows:
			si_dict[str(row.indicator_id)] = row.as_dict()
		return si_dict
	except Exception as ex:
		return dict()


################################################################################
'''
Get station_indicator by station_id or station_type
Return dict with format: {indicator_id: row.as_dict()}
'''


def get_station_indicator_by_station_2(station_indicator_rows, station_id=''):
	db = current.db
	try:
		si_dict = dict()
		for row in station_indicator_rows:
			si_dict[str(row.indicator_id)] = row.as_dict()
		return si_dict
	except Exception as ex:
		return dict()


################################################################################
'''
# Get indicator by station_id
station_indicators_rows: ROWS of station_indicator
indicators_rows: ROWS of indicators
Return ROWS of indicators
'''


def get_indicators_by_station_id(station_indicators_rows, indicators_rows, station_id=''):
	try:
		rows = []
		old_station_id = str(station_id)
		indicator_ids = []
		for si_row in station_indicators_rows:
			new_station_id = str(si_row.station_id)
			if new_station_id == old_station_id:
				indicator_id = str(si_row.indicator_id)
				indicator_ids.append(indicator_id)

		for i_row in indicators_rows:
			new_indicator_id = str(i_row.id)
			if new_indicator_id in indicator_ids:
				rows.append(i_row)
		return rows
	except Exception as ex:
		return []


################################################################################
# Get all indicator for station
# Return ROWS indicators
def get_indicator_station_info():
	try:
		db = current.db
		# Get list indicator_id from mapping table
		conditions = (db.station_indicator.station_id > 0)
		conditions &= (db.station_indicator.status == const.SI_STATUS['IN_USE']['value'])
		# rows = db(conditions).select(db.station_indicator.indicator_id)
		rows = db(conditions).select(db.station_indicator.ALL)

		# Get list indicator_id used
		indicator_ids = []
		for row in rows:
			if row.indicator_id not in indicator_ids:
				indicator_ids.append(row.indicator_id)

		# Get indicator_dict {indicator_id : indicator_name}
		indicators = db(db.indicators.id.belongs(indicator_ids)).select(
			db.indicators.id,
			db.indicators.indicator
		)
		indicator_dict = {}
		for item in indicators:
			indicator_dict[str(item.id)] = item.indicator

		station_indicator_dict = {}
		for row in rows:
			if row.station_id not in station_indicator_dict:
				station_indicator_dict[row.station_id] = {}

			indicator = indicator_dict.get(row.indicator_id)
			station_indicator_dict[row.station_id][indicator] = {
				'id': str(row.id),
				'equipment_id': row.equipment_id,
				'equal0': row.equal0,
				'negative_value': row.negative_value,
				'out_of_range': row.out_of_range,
				'out_of_range_min': row.out_of_range_min,
				'out_of_range_max': row.out_of_range_max,
				'continous_equal': row.continous_equal,
				'continous_equal_value': row.continous_equal_value,
				'remove_with_indicator_check': row.remove_with_indicator_check,
				'remove_with_indicator': row.remove_with_indicator,
				'continous_times': row.continous_times,
				'mapping_name': row.mapping_name,
				'convert_rate': row.convert_rate,
			}

		exceed_dict = {}
		preparing_dict = {}
		tendency_dict = {}
		for item in rows:
			indicator = indicator_dict.get(item.indicator_id).upper()  # ten chi so

			if item.station_id in exceed_dict:
				exceed_dict[item.station_id][indicator] = item.exceed_value
				preparing_dict[item.station_id][indicator] = item.preparing_value
				tendency_dict[item.station_id][indicator] = item.tendency_value
			else:
				exceed_dict[item.station_id] = {indicator: item.exceed_value}
				preparing_dict[item.station_id] = {indicator: item.preparing_value}
				tendency_dict[item.station_id] = {indicator: item.tendency_value}

		return station_indicator_dict, indicators, exceed_dict, preparing_dict, tendency_dict
	except Exception as ex:
		return [], [], [], [], []


################################################################################
# Get all station_indicator
# Return ROWS station_indicator
# def get_station_indicator_value():
#     try:
#         db = current.db
#         # Get list indicator_id from mapping table
#         # conditions = (db.station_indicator.station_id > 0)
#         # conditions &= (db.station_indicator.indicator_id > 0)
#         conditions = (db.station_indicator.indicator_id > 0)
#         rows = db(conditions).select(db.station_indicator.ALL)
#         return rows
#     except Exception as ex:
#         return []

################################################################################
# Get color for indicator of Station
# si_dict: dict station_indicator {indicator_name: row.as_dict()}
# id: id of indicator
# value: value of indicator
def getColorByIndicator(si_dict, id, value):
	try:
		c = '#c9c9c9'
		if si_dict.has_key(id):
			data = si_dict[id]
			tendency = data['tendency_value']
			preparing = data['preparing_value']
			exceed = data['exceed_value']
			if value >= exceed:
				c = const.STATION_STATUS['EXCEED']['color']
			elif value >= preparing:
				c = const.STATION_STATUS['PREPARING']['color']
			elif value >= tendency:
				c = const.STATION_STATUS['TENDENCY']['color']
			else:
				c = const.STATION_STATUS['GOOD']['color']

		return c
	except Exception as ex:
		return '#c9c9c9'


################################################################################
# Get color for indicator of Station [QCVN]
# si_dict: dict station_indicator {indicator_name: row.as_dict()}
# id: id of indicator
# value: value of indicator
def getColorByIndicatorQcvn(si_dict, id, value):
	try:
		c = '#c9c9c9'
		if si_dict.has_key(id):
			data = si_dict[id]
			qcvn_detail_min_value = data['qcvn_detail_min_value']
			qcvn_detail_max_value = data['qcvn_detail_max_value']

			if qcvn_detail_min_value and qcvn_detail_max_value:
				# So sanh <= ... <=
				if (float(value) >= qcvn_detail_min_value) and (float(value) <= qcvn_detail_max_value):
					c = const.STATION_STATUS['GOOD']['color']
				else:
					c = const.STATION_STATUS['EXCEED']['color']
			else:
				if qcvn_detail_max_value:
					if float(value) <= qcvn_detail_max_value:
						c = const.STATION_STATUS['GOOD']['color']
					else:
						c = const.STATION_STATUS['EXCEED']['color']
				elif qcvn_detail_min_value:
					if float(value) >= qcvn_detail_min_value:
						c = const.STATION_STATUS['GOOD']['color']
					else:
						c = const.STATION_STATUS['EXCEED']['color']
				else:
					c = const.STATION_STATUS['GOOD']['color']
		return c
	except Exception as ex:
		return '#c9c9c9'


################################################################################

def getColorByIndicatorQcvn2(value, qcvn_detail_min_value, qcvn_detail_max_value):
	try:
		c = '#c9c9c9'
		if qcvn_detail_min_value and qcvn_detail_max_value:
			# So sanh <= ... <=
			if (float(value) >= qcvn_detail_min_value) and (float(value) <= qcvn_detail_max_value):
				c = const.STATION_STATUS['GOOD']['color']
			else:
				c = const.STATION_STATUS['EXCEED']['color']
		else:
			if qcvn_detail_max_value:
				if float(value) <= qcvn_detail_max_value:
					c = const.STATION_STATUS['GOOD']['color']
				else:
					c = const.STATION_STATUS['EXCEED']['color']
			elif qcvn_detail_min_value:
				if float(value) >= qcvn_detail_min_value:
					c = const.STATION_STATUS['GOOD']['color']
				else:
					c = const.STATION_STATUS['EXCEED']['color']
			else:
				c = const.STATION_STATUS['GOOD']['color']
		return c
	except Exception as ex:
		return '#c9c9c9'


################################################################################

def getColorByIsExceed(is_exceed):
	try:
		color = '#c9c9c9'
		if is_exceed:
			if is_exceed:
				color = const.STATION_STATUS['EXCEED']['color']
			else:
				color = const.STATION_STATUS['GOOD']['color']
		else:
			color = const.STATION_STATUS['GOOD']['color']
		return color
	except Exception as ex:
		return '#c9c9c9'


################################################################################
# Get latest data for station
# Return json data
def get_data_lastest_by_station(station_id):
	try:
		db = current.db
		conditions = (db.data_lastest.station_id == station_id)
		if station_id == "":
			conditions = (db.data_lastest.station_id > 0)
		record = db(conditions).select(db.data_lastest.data).first()
		if record:
			return record.data
		return dict()
	except Exception as ex:
		return dict()


################################################################################
''' Get latest data for station
    Return json data, format {station_id :
                                {indicator : value, ...}
                             }
'''


def get_all_data_lastest():
	data_lastest_dict = {}
	try:
		db = current.db
		conditions = (db.data_lastest.station_id > 0)
		rows = db(conditions).select(db.data_lastest.station_id, db.data_lastest.data)

		for item in rows:
			data_dict = {}
			for indicator in item.data:
				data_dict[indicator] = item.data[indicator]
			data_lastest_dict[item.station_id] = data_dict

		return data_lastest_dict
	except Exception as ex:
		return data_lastest_dict


################################################################################
# Get latest data for station
# Return json data
def get_data_lastest_by_station_id(data_lastest_rows, station_id):
	try:
		for row in data_lastest_rows:
			if row.station_id == station_id:
				return row.data
		return dict()
	except Exception as ex:
		return dict()


################################################################################
# Get latest data for station
# Return json data_status
def get_data_status_by_station_id(data_lastest_rows, station_id):
	try:
		for row in data_lastest_rows:
			if row.station_id == station_id:
				return row.data_status
		return dict()
	except Exception as ex:
		return dict()


################################################################################
# Get station info
# Return json data
def get_all_station_ftp_info():
	try:
		db = current.db
		field = [
			db.stations.id,
			db.stations.station_code,
			db.stations.data_server,
			db.stations.data_server_port,
			db.stations.data_folder,
			db.stations.username,
			db.stations.pwd,
			db.stations.file_mapping,
			db.stations.scan_failed,
			db.stations.retry,
		]
		conditions = (db.stations.id > 0)
		conditions &= (db.stations.station_code != None)
		conditions &= (db.stations.data_server != None)
		conditions &= (db.stations.data_folder != None)
		rows = db(conditions).select(*field)

		res_ip = {}
		res_data_folder = {}
		res_username = {}
		res_pwd = {}
		res_port = {}
		res_file_mapping = {}
		res_file_mapping2 = {}
		res_scan_failed = {}
		res_retry = {}

		for item in rows:
			res_ip[item.station_code] = item.data_server
			res_data_folder[item.station_code] = item.data_folder
			res_username[item.station_code] = item.username
			res_pwd[item.station_code] = item.pwd
			res_port[item.station_code] = item.data_server_port
			res_scan_failed[item.station_code] = item.scan_failed
			res_retry[item.station_code] = item.retry
			res_file_mapping2[item.station_code] = item.retry
			if item.file_mapping:
				res_file_mapping[item.file_mapping] = str(item.id)

		return res_ip, res_data_folder, res_username, res_pwd, res_port, res_file_mapping, res_scan_failed, res_retry, res_file_mapping2
	except Exception as ex:
		return dict()


################################################################################
def get_indicator_dict():
	db = current.db

	rows = db(db.indicators.id > 0).select()
	res = {}
	for item in rows:
		res[str(item.id)] = item.indicator

	return res

def where_is_exceed(added_columns , qcvn_dict):
	exceed_data = []
	for indicator in added_columns:
		name_decode = indicator.encode('utf-8')
		qcvn_min = qcvn_dict[name_decode]['qcvn_detail_min_value'] if qcvn_dict.has_key(
			name_decode) else None
		qcvn_max = qcvn_dict[name_decode]['qcvn_detail_max_value'] if qcvn_dict.has_key(
			name_decode) else None
		qcvn_query = dict()
		if qcvn_max is not None:
			qcvn_query["$gt"] = qcvn_max
		if qcvn_min is not None:
			qcvn_query["$lt"] = qcvn_min
		if qcvn_min is not None or qcvn_max is not None:
			exceed_data.append({"data." + indicator: qcvn_query})
	return exceed_data

################################################################################
def get_qcvn_kind_dict():
	db = current.db

	rows = db(db.qcvn_kind.id > 0).select()
	res = {}
	for item in rows:
		res[str(item.id)] = item.qcvn_kind

	return res


################################################################################
def get_station_dict():
	db = current.db
	field = [
		db.stations.id,
		db.stations.station_code,
		db.stations.station_name,
		db.stations.station_type,
		db.stations.status,
		db.stations.area_ids,
	]

	stations = db(db.stations.id > 0).select(*field)
	res_name = {}
	res_type = {}
	res_status = {}
	res_code = {}
	res_area = {}

	for item in stations:
		res_name[str(item.id)] = item.station_name
		res_type[str(item.id)] = item.station_type
		res_status[str(item.id)] = item.status
		res_area[str(item.id)] = item.area_ids
		res_code[item.station_code] = str(item.id)

	return res_name, res_type, res_status, res_code, res_area


################################################################################
'''
    Description : Lay dict() cac tram voi nguong qua han cua tung chi so
    Return      : dict(station_id : dict(indicator : exceed value))
'''


# def get_station_indicator_thresdhold_dict():
# db = current.db
# logger = current.logger

# fields = [  db.station_indicator.station_id,
# db.station_indicator.indicator_id,
# db.station_indicator.exceed_value]

# rows = db(db.station_indicator.id > 0).select(*fields)


# indicator_dict = get_indicator_dict()
# res = {}
# for item in rows:
# indicator = indicator_dict.get(item.indicator_id).upper()   # ten chi so

# if item.station_id in res:
# res[item.station_id][indicator] = item.exceed_value
# else:
# res[item.station_id] = {indicator : item.exceed_value}

# return res

################################################################################
def get_area_by_station_dict():
	'''
	Return : dict(key  : station_id,
				  value: all areas which station belonged (separated by comma))
	'''
	db = current.db
	field = [
		db.areas.id,
		db.areas.area_name,
	]

	records = db(db.areas.id > 0).select(*field)
	res_name = {}

	for item in records:
		if item.id not in res_name:
			res_name[str(item.id)] = item.area_name
		else:
			res_name[str(item.id)] = '%s, %s' % (res_name[str(item.id)], item.area_name)

	return res_name


################################################################################
def get_area_by_station_id_dict():
	'''
	Return : dict(key  : station_id,
				  value: all areas which station belonged (separated by comma))
	'''
	db = current.db
	field = [
		db.areas.id,
		db.areas.area_name,
	]

	records = db(db.areas.id > 0).select(*field)
	res_name = {}

	for item in records:
		if item.id not in res_name:
			res_name[str(item.id)] = item.area_name
		else:
			res_name[str(item.id)] = '%s, %s' % (res_name[str(item.id)], item.area_name)

	return res_name

def get_career_by_station_dict():
	'''
	Return : dict(key  : station_id,
				  value: all careers which station belonged (separated by comma))
	'''
	db = current.db
	field = [
		db.manager_careers.id,
		db.manager_careers.career_name,
	]

	records = db(db.manager_careers.id > 0).select(*field)
	res_name = {}

	for item in records:
		if item.id not in res_name:
			res_name[str(item.id)] = item.career_name
		else:
			res_name[str(item.id)] = '%s, %s' % (res_name[str(item.id)], item.career_name)

	return res_name

def get_agents_by_station_dict():
	'''
	Return : dict(key  : station_id,
				  value: all agents which station belonged (separated by comma))
	'''
	db = current.db
	field = [
		db.agents.id,
		db.agents.agent_name,
	]

	records = db(db.agents.id > 0).select(*field)
	res_name = {}

	for item in records:
		if item.id not in res_name:
			res_name[str(item.id)] = item.agent_name
		else:
			res_name[str(item.id)] = '%s, %s' % (res_name[str(item.id)], item.agent_name)

	return res_name


################################################################################
def get_stations_belong_current_user():
	'''
	Return : list(station_ids)
	'''
	db = current.db
	session = current.session
	station_ids = db(db.station_role.role_id.belongs(session.user.role_ids)).select(db.station_role.station_id)
	station_ids = [item.station_id for item in station_ids]

	return station_ids


################################################################################
def format_passed_time(seconds=0):
	if not seconds: return ''

	T = current.T
	if seconds >= 86400:  # Ngay
		return '%d %s %d %s' % (seconds / 86400, T('day'), (seconds % 86400) / 3600, T('hour'))
	elif seconds >= 3600:  # Gio
		return '%d %s %d %s' % (seconds / 3600, T('hour'), (seconds % 3600) / 60, T('minute'))
	elif seconds >= 60:  # Phut
		return '%d %s %d %s' % (seconds / 60, T('minute'), seconds % 60, T('second'))
	else:
		return '%d %s' % (seconds, T('second'))


################################################################################
def send_mail(mail_to='', mail_cc='', subject='Subject', message='Content'):
	try:
		myconf = current.myconf
		import smtplib
		from email.mime.text import MIMEText

		msg = MIMEText(message, 'html', 'UTF-8')
		msg['Subject'] = subject
		msg["From"] = myconf.get('smtp.sender')
		msg["To"] = mail_to
		msg["Cc"] = mail_cc

		server = smtplib.SMTP()
		mail_server = myconf.get('smtp.server')
		mail_port = myconf.get('smtp.port')
		server.connect(mail_server, mail_port)
		mail_user = myconf.get('smtp.login')
		mail_pwd = myconf.get('smtp.pwd')
		server.starttls()
		server.login(mail_user, mail_pwd)
		server.sendmail(msg["From"], msg["To"].split(','), msg.as_string())
		return True
	except Exception as ex:
		current.logger.error('Send email error')
		current.logger.error(str(ex))
		return False


################################################################################
def send_mail_alarm(mail_to, mail_cc, subject, message):
	try:
		# myconf = current.myconf

		# import smtplib
		import smtplib, ssl
		from email.mime.text import MIMEText
		# from email.mime.multipart import MIMEMultipart

		db = current.db
		session = current.session
		mail_server_config = db(db.mail_server.id > 0).select()
		if mail_server_config:
			mail_server_config = mail_server_config.first()
			SENDER_EMAIL = str(mail_server_config.sender_email)
			MAIL_SERVER = str(mail_server_config.mail_server)
			MAIL_SENDER_PASSWORD = str(mail_server_config.sender_email_password)
			MAIL_SERVER_PORT = int(mail_server_config.mail_server_port)

		msg = MIMEText(message, 'html', 'UTF-8')
		msg['Subject'] = subject
		msg["From"] = SENDER_EMAIL  # 'hd.envisoft@gmail.com'
		msg["To"] = mail_to
		msg["Cc"] = mail_cc

		server = smtplib.SMTP()

		mail_server = MAIL_SERVER  # 'smtp.gmail.com'

		mail_port = MAIL_SERVER_PORT  # 587

		server.connect(mail_server, mail_port)

		mail_user = SENDER_EMAIL  # 'hd.envisoft@gmail.com'
		mail_pwd = MAIL_SENDER_PASSWORD  # 'ttqtduan!$2019'

		server.starttls()  # Khoi tao ket noi TLS SMTP
		server.login(mail_user, mail_pwd)  # Dang nhap user, pass

		# https://realpython.com/python-send-email/
		# Create secure connection with server and send email
		# context = ssl.create_default_context()
		# with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context) as server:
		#     server.login(sender_email, password)
		#     server.sendmail(
		#         sender_email, receiver_email, message.as_string()
		#     )

		server.sendmail(msg["From"], msg["To"].split(','), msg.as_string())

		server.close()  # ket thuc

		# self.station_logger.debug("send_mail: send ok")

		return True
	except Exception as ex:
		# traceback.print_exc()
		# self.station_logger.error('send_mail --> Exception = %s', ex.message)
		current.logger.error('Send email error')
		current.logger.error(str(ex))
		return False


################################################################################
def send_mail2(mail_to='', mail_cc='', subject='Subject', message='Content'):
	try:
		import smtplib  # Sử dụng module smtp của Python
		from email.mime.text import MIMEText

		# Khai báo username và pass
		username = 'c0909i1240'
		password = 'chinguyen12345'
		# Tạo đối tượng làm việc với smtp của gmail
		server = smtplib.SMTP('smtp.gmail.com:587')  # Tạo một kết nối đến SMTP của gmail
		server.starttls()  # Khởi tạo kết nối TLS SMTP
		server.login(username, password)  # Đăng nhập user, pass

		msg = MIMEText(message, 'html', 'UTF-8')
		msg['Subject'] = subject
		msg["To"] = mail_to
		msg["Cc"] = mail_cc
		server.sendmail(msg["From"], msg["To"].split(','),
						msg.as_string())  # Gửi email từ hocbaomat@gmail.com đến maivanthang@gmail.com

		server.close()  # Kết thúc
	except Exception as ex:
		current.logger.error('Send email error')
		current.logger.error(str(ex))
		return False


################################################################################
def convert_to_unsigned(text):
	import re
	import sys
	patterns = {
		'[àáảãạăắằẵặẳâầấậẫẩ]': 'a',
		'[đ]': 'd',
		'[èéẻẽẹêềếểễệ]': 'e',
		'[ìíỉĩị]': 'i',
		'[òóỏõọôồốổỗộơờớởỡợ]': 'o',
		'[ùúủũụưừứửữự]': 'u',
		'[ỳýỷỹỵ]': 'y'
	}
	output = text
	for regex, replace in patterns.items():
		output = re.sub(regex, replace, output)
		# deal with upper case
		output = re.sub(regex.upper(), replace.upper(), output)
	return output


################################################################################
def display_list_integer(resource, numbers):
	try:
		ret = ''
		for number in numbers:
			name = resource.get(str(number))
			if name:
				if ret: ret += ', '
				ret += name
		return ret
	except Exception as ex:
		return numbers


################################################################################
def get_info_from_const(data, value):
	try:
		ret = []
		for key, item in data.iteritems():
			if item['value'] == value:
				return item
		return ret
	except Exception as ex:
		return []


################################################################################
# Format of item in dict: 'KEY1': {'value': 0, 'name': 'name1', 'seq': 1}
def sort_dict_const_by_value(dict_const):
	key_field = 'value'
	ret = dict_const.items()
	total = len(ret)
	if total > 0:
		item = ret[0][1]
		if item.has_key('seq'):
			key_field = 'seq'
	for i in range(0, total - 1):
		for j in range(i + 1, total):
			if ret[j][1][key_field] < ret[i][1][key_field]:
				temp = ret[j]
				ret[j] = ret[i]
				ret[i] = temp
	return ret


################################################################################
def sort_tuple(ret):
	def sr(s):
		return s[1]['seq']

	ret.sort(key=sr)
	return ret


################################################################################
# Format of item in dict: 'KEY1': {'value': 0, 'name': 'name1', 'seq': 1, 'order': 1}
def sort_dict_const_by_order(dict_const):
	key_field = 'order'
	ret = dict_const.items()
	total = len(ret)
	if total > 0:
		item = ret[0][1]
		if item.has_key('seq'):
			key_field = 'seq'
	for i in range(0, total - 1):
		for j in range(i + 1, total):
			if ret[j][1][key_field] < ret[i][1][key_field]:
				temp = ret[j]
				ret[j] = ret[i]
				ret[i] = temp
	return ret


################################################################################
def get_const_by_value(dict_const, value):
	ret = []
	for k in dict_const:
		if str(dict_const[k]['value']) == str(value):
			return dict_const[k]
	return ret


def get_station_status_by(dic, status, fielName):
	k = str(status)
	if dic.has_key(k):
		return dic.get(k)[fielName]
	return None


def convert_data(data):
	try:
		value = "{:,.2f}".format(data)
		session = current.session
		perThousand = session.perThousand
		decimal = session.decimal
		if decimal == ',':
			arr = value.split(".")
			first = arr[0]
			f = first.replace(decimal, perThousand)
			if str(arr[1]) == '00':
				val = str(f)
			else:
				val = str(f) + decimal + str(arr[1])
		else:
			arr = value.split(".")
			if str(arr[1]) == '00':
				val = arr[0]
		return val
	except Exception as ex:
		return value


def get_public_time_air():
	from datetime import datetime, timedelta
	try:
		time_public = 3
		data = db(db.eip_config.name == 'eip_config').select(db.eip_config.time_public).first()
		if data:
			time_public = data['time_public']
	except Exception as ex:
		pass
	return datetime.now() - timedelta(hours=time_public)