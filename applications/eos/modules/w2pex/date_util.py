from datetime import datetime, date
# from dateutil import tz

# local_zone = tz.tzlocal()
# utc_zone = tz.tzutc()

#convert: 'YYYY-mm-dd' to datetime.date(YYYY, mm, dd)
def string_to_date(str_date, format='%Y-%m-%d'):
    try:
        type_date = datetime.strptime(str_date, format)
        result = type_date.date()
    except:
        result = date.today()
        
    return result

def string_to_datetime(str_date, format='%Y-%m-%d'):
    try:
        result = datetime.strptime(str_date, format)
    except:
        result = datetime.now()
        
    return result
    
# #Convert UTC time zone to local time zone
# def to_local_time(utc_time):
    # # Tell the datetime object that it's in UTC time zone since 
    # # datetime objects are 'naive' by default
    # utc_time = utc_time.replace(tzinfo = utc_zone)

    # return utc_time.astimezone(local_zone) #convert time zone

# #Convert local time zone to UTC time zone
# def to_utc_time(local_time):
    # # Tell the datetime object that it's in local time zone since 
    # # datetime objects are 'naive' by default
    # local_time = local_time.replace(tzinfo = local_zone)

    # return local_time.astimezone(utc_zone) #convert time zone

def get_first_day_last_month(current_date):
    day = 1
    month = current_date.month
    year = current_date.year
    if (current_date.month == 1):
        month = 12
        year -= 1
    else:
        month -= 1
    return date(year, month, day)

def get_first_day_next_month(current_date):
    day = 1
    month = current_date.month
    year = current_date.year
    if (current_date.month == 12):
        month = 1
        year += 1
    else:
        month += 1
    return date(year, month, day)
    
def get_first_day_current_month(current_date):
    day = 1
    month = current_date.month
    year = current_date.year
    return date(year, month, day)

def get_first_day_current_quarter(current_date):
    quarter = get_quarter(current_date)
    day = 1
    month = 3 * quarter - 2
    year = current_date.year
    return date(year, month, day)

def get_first_day_last_quarter(current_date):
    quarter = get_quarter(current_date)
    day = 1
    month = 3 * quarter
    year = current_date.year
    return date(year, month, day)
def get_first_day_next_quarter (current_date):
    quarter = get_quarter(current_date)
    day = 1
    month = 3 * (quarter + 1)
    year = current_date.year
    if quarter == 4:
        month = 1
        year += 1
    return date(year, month, day)
def get_quarter(current_date):
    return (int(current_date.month) - 1) / 3 + 1


def get_first_day_current_year(current_date):
    day = 1
    month = 1
    year = current_date.year
    return date(year, month, day)

def get_first_day_last_year(current_date):
    day = 1
    month = 12
    year = current_date.year
    return date(year, month, day)
def get_first_day_next_year (current_date):
    quarter = get_quarter(current_date)
    day = 1
    month = 1
    year = current_date.year + 1
    return date(year, month, day)
def pretty_date(time=False):
    """
    Get a datetime object or a int() Epoch timestamp and return a
    pretty string like 'an hour ago', 'Yesterday', '3 months ago',
    'just now', etc
    """
    from datetime import datetime
    now = datetime.now()
    if type(time) is int:
        diff = now - datetime.fromtimestamp(time)
    elif isinstance(time,datetime):
        diff = now - time
    elif not time:
        diff = now - now
    second_diff = diff.seconds
    day_diff = diff.days

    if day_diff < 0:
        return ''

    if day_diff == 0:
        if second_diff < 10:
            return "just now"
        if second_diff < 60:
            return str(second_diff) + " seconds ago"
        if second_diff < 120:
            return "a minute ago"
        if second_diff < 3600:
            return str(second_diff / 60) + " minutes ago"
        if second_diff < 7200:
            return "an hour ago"
        if second_diff < 86400:
            return str(second_diff / 3600) + " hours ago"
    if day_diff == 1:
        return "Yesterday"
    if day_diff < 7:
        return str(day_diff) + " days ago"
    if day_diff < 31:
        return str(day_diff / 7) + " weeks ago"
    if day_diff < 365:
        return str(day_diff / 30) + " months ago"
    return str(day_diff / 365) + " years ago"