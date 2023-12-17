import requests
from applications.eos.modules.appbase import myconf

def check_mqtt_status(vars, record):
    try:
        if record:
            if not vars.mqtt_usr == record.mqtt_usr or not vars.mqtt_pwd == record.mqtt_pwd:
                rs = post_mqtt_api('api/v4/auth_username', {'username': vars.mqtt_usr, 'password': vars.mqtt_pwd})
        data = get_mqtt_api('api/v4/clients/' + vars['mqtt_client_id'])
        if data.has_key('data') and len(data['data']) > 0:
            return data['data'][0]['connected']
    except:
        pass
    return False

def post_mqtt_api(path, params):
    try:
        url = '%s/%s' % (myconf.get('mqtt.url', ''), path)
        res = requests.post(url, json=params, headers={'Authorization': myconf.get('mqtt.auth_token', '')}, timeout=3)
        rs = dict(success=False)
        if res.status_code == 200:
            rs['success'] = True
            try:
                data = res.json()
                rs['data'] = data['data']
            except:
                pass
        return rs
    except Exception as e:
        return dict(success=False, message=e.message)


def get_mqtt_api(path):
    try:
        url = '%s/%s' % (myconf.get('mqtt.url', ''), path)
        res = requests.get(url, headers={'Authorization': myconf.get('mqtt.auth_token', '')}, timeout=3)

        rs = dict(success=False)
        if res.status_code == 200:
            rs['success'] = True
            try:
                data = res.json()
                rs['data'] = data['data']
            except:
                pass
        return rs

    except Exception as e:
        return dict(success=False, message=e.message)

def get_send_file_name(station, province, agents, data_send_list):
    send_file_name = ""
    if data_send_list:
        send_file_name = data_send_list[0].file_name
    else:
        send_file_name += province.province_code + '_' if province else '_'
        send_file_name += agents.agent_code + '_' if agents else ''
        send_file_name += station.station_code

    return send_file_name

def get_send_data_status(data_send_list):
    if data_send_list:
        data_send = data_send_list[0]
        if data_send.status == 0:
            current_send_name = 'In-active'
        elif data_send.status == 1:
            current_send_name = 'Active'
        return {'value': data_send.status, 'name': current_send_name}
    return dict()