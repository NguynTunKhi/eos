# -*- coding: utf-8 -*-
###############################################################################
# Author : hungdx
# Date   : 2019 - 06 - 19
#
# Description : create API for mobile - Dehan
#
###############################################################################
from datetime import datetime, timedelta
from applications.eos.modules import const
from gluon.tools import prettydate
import json
from gluon.tools import AuthJWT
import datetime
import ast
import requests

myjwt = AuthJWT(auth, secret_key='secret@259',  expiration=60*60*24*365)

auth.settings.allow_basic_login = True


def call():
    session.forget()
    response.headers["Access-Control-Allow-Origin"] = '*'
    response.headers['Access-Control-Max-Age'] = 86400
    response.headers['Access-Control-Allow-Headers'] = '*'
    response.headers['Access-Control-Allow-Methods'] = '*'
    response.headers['Access-Control-Allow-Credentials'] = 'true'
    return service()


################################################################################
@service.json
def get_app_setting(*args, **kwargs):
    settings = db().select(db.app_settings.ALL).first()
    if settings:
        active = settings.active_mobile
        if active is True:
            return dict(success=True, data=settings)
        elif active is False:
            return dict(success=False, massage='Bản Mobile chưa được active')
        else:
            return dict(success=True, data=settings)

    return dict(success=True, data=settings)

##################################
def get_token_with():
    try:
        row = db(db.camera_tokens.id > 0).select(db.camera_tokens.ALL).first()
        if not row:
            return None
        url = row['url']
        last_time_access = row['last_time_access']
        last_time_refresh = row['last_time_refresh']
        access_token_expires = row['access_token_expires']
        refresh_token_expires = row['refresh_token_expires']
        access_token = row['access_token']
        refresh_token = row['refresh_token']
        username = row['username']

        if last_time_access and last_time_refresh:
            now = datetime.datetime.utcnow()
            if last_time_access + datetime.timedelta(seconds=access_token_expires - (60 * 60)) > now:
                return access_token
            else:
                if last_time_refresh + datetime.timedelta(seconds=refresh_token_expires - (60 * 15)) > now:
                    req = requests.get('{}/zm/api/host/login.json?token={}'.format(url, refresh_token), verify=False)
                    content = req.content
                    dic = ast.literal_eval(content)
                    db(db.camera_tokens.username == username).update(
                        last_time_access=now,
                        access_token_expires=dic['access_token_expires'],
                        access_token=dic['access_token']
                    )
                    return dic['access_token']
        try:
            username = row['username']
            password = row['password']
            req = requests.get('{}/zm/api/host/login.json?token={}'.format(url, refresh_token), verify=False)
            content = req.content
            dic = ast.literal_eval(content)
            if not dic['access_token']:
                return None
            now = datetime.datetime.utcnow()
            db(db.camera_tokens.username == username).update(
                last_time_access=now,
                last_time_refresh=now,
                access_token_expires=dic['access_token_expires'],
                refresh_token_expires=dic['refresh_token_expires'],
                access_token=dic['access_token'],
                refresh_token=dic['refresh_token']
            )
            return dic['access_token']
        except Exception as ex:
            return None
    except Exception as ex:
        return None

################################################################################
@service.json
def get_common_settings(*args, **kwargs):
    try:
        # aqi_colors
        aqi_colors = []
        for k in sorted(const.AQI_COLOR):
            name = ''
            if const.AQI_COLOR[k]['to']:
                name = '%s-%s (%s)' % (
                const.AQI_COLOR[k]['from'], const.AQI_COLOR[k]['to'], T(const.AQI_COLOR[k]['text']))
            else:
                name = '%s %s (%s)' % (T('Greater'), const.AQI_COLOR[k]['from'] - 1, T(const.AQI_COLOR[k]['text']))

            aqi_colors.append({
                'name': name,
                'from': const.AQI_COLOR[k]['from'],
                'to': const.AQI_COLOR[k]['to'] if const.AQI_COLOR[k]['to'] != None else 600,
                'color': const.AQI_COLOR[k]['bgColor'],
            })
            pass

        # wqi_colors
        wqi_colors = []
        for k in sorted(const.WQI_COLOR):
            name = ''
            if const.WQI_COLOR[k]['to']:
                name = '%s - %s (%s)' % (
                const.WQI_COLOR[k]['from'], const.WQI_COLOR[k]['to'], T(const.WQI_COLOR[k]['text']))
            else:
                name = '%s %s (%s)' % (T('Greater'), const.WQI_COLOR[k]['from'] - 1, T(const.WQI_COLOR[k]['text']))

            wqi_colors.append({
                'name': name,
                'from': const.WQI_COLOR[k]['from'],
                'to': const.WQI_COLOR[k]['to'] if const.WQI_COLOR[k]['to'] != None else 600,
                'color': const.WQI_COLOR[k]['bgColor'],
            })
            pass

        # status
        status = []
        status_good = ''
        for k in const.STATION_STATUS:
            if k in ['GOOD', 'TENDENCY', 'PREPARING']:
                if status_good:
                    status_good += ','
                status_good += str(const.STATION_STATUS[k]['value'])
                continue
            status.append({
                'value': const.STATION_STATUS[k]['value'],
                'name': T(const.STATION_STATUS[k]['name'])
            })
            pass
        status.append({
            'value': status_good,
            'name': T(const.STATION_STATUS['GOOD']['name'])
        })

        # STATION_TYPE
        station_type = []
        for k in const.STATION_TYPE:
            station_type.append({
                'value': const.STATION_TYPE[k]['value'],
                'name': T(const.STATION_TYPE[k]['name'])
            })
            pass

        # provinces
        provinces = []
        conditions = (db.provinces.id > 0)
        rows = db(conditions).select(db.provinces.id,
                                     db.provinces.province_name,
                                     orderby=db.provinces.province_name)
        for row in rows:
            provinces.append({
                'id': str(row.id),
                'name': row.province_name,
            })

        # areas
        areas = []
        conditions = (db.areas.id > 0)
        rows = db(conditions).select(db.areas.id,
                                     db.areas.area_code,
                                     db.areas.area_name,
                                     orderby=db.areas.area_name)
        for row in rows:
            areas.append({
                'id': str(row.id),
                'area_code': row.area_code,
                'area_name': row.area_name,
            })

        return dict(success=True, qi_colors=aqi_colors, aqi_colors=aqi_colors, wqi_colors=wqi_colors, status=status,
                    provinces=provinces, station_type=station_type, areas=areas)
    except Exception as ex:
        return dict(success=False, message=str(ex))


@service.json
def login(*args, **kwargs):
    token = myjwt.jwt_token_manager()
    json_object = json.loads(token)
    user = db.auth_user(auth.user_id)
    if user.is_active == 0:
        return dict(success=False, error_code=0, message='User hiện tại đã ngừng hoạt động.')
    is_admin = False
    if auth.has_membership('admin') or auth.has_membership(const.GROUP_MANAGER):
        is_admin = True

    login_user = db(db.login_user.user_id == auth.user_id).select()
    if login_user:
        curent_user = login_user.first()
        try:
            confirm_2fa = curent_user.confirm_2fa
        except:
            confirm_2fa = False

        if confirm_2fa is True:
            import smtplib
            from email.mime.text import MIMEText
            import datetime
            import random
            try:
                mail_token = random.randint(1000, 9999)  # sinh mail_token
                time_create_mail_token = datetime.datetime.now()

                db(db.login_user.user_id == auth.user_id).update(mail_token=mail_token,
                                                                  time_create_mail_token=time_create_mail_token,
                                                                  token=json_object['token'], pass_old=user.password, is_admin=is_admin)
                db.token_user.insert(user_id=auth.user_id, token=json_object['token'])
                db.commit()

                mail_server_config = db(db.mail_server.id > 0).select()
                if mail_server_config:
                    mail_server_config = mail_server_config.first()
                    SENDER_EMAIL = str(mail_server_config.sender_email)
                    MAIL_SERVER = str(mail_server_config.mail_server)
                    MAIL_SENDER_PASSWORD = str(mail_server_config.sender_email_password)
                    MAIL_SERVER_PORT = int(mail_server_config.mail_server_port)

                msg = MIMEText('Mã xác thực 2 lớp cho Envisoft của bạn là: ' + str(mail_token), 'html', 'UTF-8')
                msg['Subject'] = 'Xác thực 2 lớp cho Envisoft'
                msg["From"] = SENDER_EMAIL  # 'hd.envisoft@gmail.com'
                msg["To"] = user.email
                msg["Cc"] = ''

                server = smtplib.SMTP()

                mail_server = MAIL_SERVER  # 'smtp.gmail.com'

                mail_port = MAIL_SERVER_PORT  # 587

                server.connect(mail_server, mail_port)

                mail_user = SENDER_EMAIL  # 'hd.envisoft@gmail.com'
                mail_pwd = MAIL_SENDER_PASSWORD  # 'ttqtduan!$2019'

                server.starttls()  # Khoi tao ket noi TLS SMTP
                server.login(mail_user, mail_pwd)

                server.sendmail(msg["From"], msg["To"].split(','), msg.as_string())

                server.close()  # ket thuc
                return dict(success=True, message='Gửi mã xác thực đến mail thành công')
            except:
                return dict(success=False, message='Có lỗi trong quá trình gửi mã xác thực đến mail.')
        else:
            db(db.login_user.user_id == auth.user_id).update(token=json_object['token'], pass_old=user.password, is_admin=is_admin)
            db.token_user.insert(user_id=auth.user_id, token=json_object['token'])
            db.commit()
            return dict(success=True, token=json_object['token'])
    else:
        db.login_user.insert(user_id=auth.user_id, confirm_2fa=False, token=json_object['token'], is_admin=is_admin)
        db.token_user.insert(user_id=auth.user_id, token=json_object['token'])
        db.commit()

        return dict(success=True, token=json_object['token'])


def get_fcm_setting_by_user(user_id, send_type=0):
    conds = (db.fcm_user_setting.id > 0)
    conds &= (db.fcm_user_setting.send_type == send_type)
    conds &= (db.fcm_user_setting.user_id == user_id)
    user = db(conds).select(db.fcm_user_setting.is_send).first()
    if user is None:
        return True
    return user.is_send

@service.json
@myjwt.allows_jwt()
def send_token_fcm(*args, **kwargs):
    try:
        token = request.env.get('HTTP_AUTHORIZATION').split(" ")[1]
        condition_token = (db.token_user.token == token)
        user_token = db(condition_token).select()
        if not user_token:
            return dict(success=False, error_code=1, message='Token đã hết hạn.')

        user = db.auth_user(auth.user_id)
        if user.is_active == 0:
            return dict(success=False, error_code=0, message='User hiện tại đã ngừng hoạt động.')

        token_fcm = request.vars.token_fcm
        device_type = request.vars.device_type
        device_name = request.vars.device_name
        device_version = request.vars.device_version
        device_id = request.vars.device_id

        # check trong ban token_fcm_user neu co token_fcm roi thi update ko thi insert
        condition_token_fcm = (db.token_fcm_user.token_fcm == token_fcm)
        user_fcm = db(condition_token_fcm).select()
        is_send = get_fcm_setting_by_user(auth.user_id)
        user_id = auth.user_id
        if user_fcm:
            db(db.token_fcm_user.token_fcm == token_fcm).update(
                user_id=user_id, token_fcm=token_fcm, device_version=device_version,
                device_id=device_id, device_name=device_name,
            )
            db.commit()
            return dict(success=True, message='Lưu token của FCM thành công.', is_send=is_send, user_id=str(user_id))
        else:
            db.token_fcm_user.insert(
                user_id=user_id, token_fcm=token_fcm, device_type=device_type,
                device_name=device_name, device_version=device_version,
                device_id=device_id
             )

            db.fcm_user_setting.update_or_insert(db.fcm_user_setting.user_id == user_id, user_id=user_id,
                                                     is_send=is_send)
            return dict(success=True, message='Lưu token của FCM thành công.', is_send=is_send, user_id=str(user_id))
    except:
        return dict(success=False, message='Có lỗi xảy ra khi lưu token của FCM.')


@service.json
@myjwt.allows_jwt()
def logout(*args, **kwargs):
    try:
        token = request.env.get('HTTP_AUTHORIZATION').split(" ")[1]
        condition_token = (db.token_user.token == token)
        user_token = db(condition_token).select()
        if not user_token:
            return dict(success=False, error_code=1, message='Token đã hết hạn.')

        user = db.auth_user(auth.user_id)
        if user.is_active == 0:
            return dict(success=False, error_code=0, message='User hiện tại đã ngừng hoạt động.')


        token_fcm = request.vars.token_fcm
        # check trong ban token_fcm_user neu co token_fcm roi thi xoa di
        condition_token_fcm = (db.token_fcm_user.token_fcm == token_fcm)
        db(condition_token_fcm).delete()
        condition_token_delete = (db.token_user.token == token)
        db(condition_token_delete).delete()
        db.commit()
        return dict(success=True, message='Xóa token thành công.')
    except:
        return dict(success=False, message='Có lỗi xảy ra khi xóa token.')


@service.json
def get_token_with_code(*args, **kwargs):
    username = request.vars.username
    mail_token = request.vars.mail_token
    conditons = (db.auth_user.id > 0)
    conditons &= (db.auth_user.username == username)
    list_user = db(conditons).select()
    if list_user:
        user = list_user.first()
        if user.is_active == 0:
            return dict(success=False, error_code=0, message='User hiện tại đã ngừng hoạt động.')

        conditons_login = (db.login_user.user_id == user.id)
        conditons_login &= (db.login_user.mail_token == mail_token)

        list_login = db(conditons_login).select()
        if list_login:
            user_login = list_login.first()

            if datetime.datetime.now() < user_login.time_create_mail_token + timedelta(minutes=5):
                return dict(success=True, token=user_login.token)
            else:
                return dict(success=False, message='Mã xác thực đã hết hạn.')
        else:
            return dict(success=False, message='Có lỗi xảy ra khi lấy token. Vui lòng kiểm tra lại.')
    else:
        return dict(success=False, message='Có lỗi xảy ra khi lấy token. Vui lòng kiểm tra lại.')


@service.json
def send_code_to_mail_forget_pass(*args, **kwargs):
    import smtplib, ssl
    from email.mime.text import MIMEText
    import datetime
    import random

    email_send = request.vars.email

    conditons = (db.auth_user.id > 0)
    conditons &= (db.auth_user.email == email_send)

    list_user = db(conditons).select()
    if list_user:
        user = list_user.first()
        if user.is_active == 0:
            return dict(success=False, error_code=0, message='User hiện tại đã ngừng hoạt động.')
        try:
            mail_code = random.randint(1000, 9999)  # sinh mail_token
            time_create_mail_code = datetime.datetime.now()

            db(db.login_user.user_id == user.id).update(mail_code=mail_code,
                                                              time_create_mail_code=time_create_mail_code)
            db.commit()

            mail_server_config = db(db.mail_server.id > 0).select()
            if mail_server_config:
                mail_server_config = mail_server_config.first()
                SENDER_EMAIL = str(mail_server_config.sender_email)
                MAIL_SERVER = str(mail_server_config.mail_server)
                MAIL_SENDER_PASSWORD = str(mail_server_config.sender_email_password)
                MAIL_SERVER_PORT = int(mail_server_config.mail_server_port)

            msg = MIMEText('Bạn hoặc ai đó vừa gửi yêu cầu xác thực quên mật khẩu của Envisoft. Mã xác thực: ' + str(mail_code), 'html', 'UTF-8')
            msg['Subject'] = 'Mã xác thực quên mật khẩu'
            msg["From"] = SENDER_EMAIL  # 'hd.envisoft@gmail.com'
            msg["To"] = user.email
            msg["Cc"] = ''

            server = smtplib.SMTP()

            mail_server = MAIL_SERVER  # 'smtp.gmail.com'

            mail_port = MAIL_SERVER_PORT  # 587

            server.connect(mail_server, mail_port)

            mail_user = SENDER_EMAIL  # 'hd.envisoft@gmail.com'
            mail_pwd = MAIL_SENDER_PASSWORD  # 'ttqtduan!$2019'

            server.starttls()  # Khoi tao ket noi TLS SMTP
            server.login(mail_user, mail_pwd)

            server.sendmail(msg["From"], msg["To"].split(','), msg.as_string())

            server.close()  # ket thuc
            return dict(success=True, message='Đã gửi mã xác thực quên mật khẩu tới mail đăng ký vui lòng kiểm tra.')
        except:
            return dict(success=False, message='Có lỗi trong quá trình gửi mail. Vui lòng kiểm tra lại.')
    else:
        return dict(success=False, message='Có lỗi trong quá trình gửi mã xác thực quên mật khẩu. Vui lòng kiểm tra lại.')

@service.json
def check_code_forget_pass(*args, **kwargs):
    code = request.vars.code
    mail = request.vars.mail

    condition_user = (db.auth_user.email == mail)
    users = db(condition_user).select()
    if users:
        user = users.first()

        if user.is_active == 0:
            return dict(success=False, error_code=0, message='User hiện tại đã ngừng hoạt động.')

        condition_login = (db.login_user.user_id == user.id)
        condition_login &= (db.login_user.mail_code == code)
        login_user = db(condition_login).select()
        if login_user:
            login_user = login_user.first()
            if datetime.datetime.now() < login_user.time_create_mail_code + timedelta(minutes=5):
                return dict(success=True, message='Xác nhận mã quên mật khẩu thành công.', token=login_user.token)
            else:
                return dict(success=False, message='Mã xác thực đã hết hạn.')
        else:
            return dict(success=False, message='Có lỗi xảy ra vui lòng kiểm tra lại.')
    else:
        return dict(success=False, message='Có lỗi xảy ra vui lòng kiểm tra lại.')


@service.json
def set_password(*args, **kwargs):
    try:
        token = request.env.get('HTTP_AUTHORIZATION').split(" ")[1]
        condition_token = (db.login_user.token == token)
        token_users = db(condition_token).select()
        if token_users:
            login_user = token_users.first()
            condition_user = (db.auth_user.id == login_user.user_id)
            users = db(condition_user).select()
            if users:
                user = users.first()
                if user.is_active == 0:
                    return dict(success=False, error_code=0, message='User hiện tại đã ngừng hoạt động.')

                user.password = CRYPT(digest_alg='sha512', salt=True)(request.vars.password)[0]
                db(db.auth_user.id == user.id).update(password=user.password)
                db(db.token_user.user_id == user.id).delete()
                db.commit()
                return dict(success=True, message='Cập nhật mật khẩu thành công.')
            else:
                return dict(success=False, message='Cập nhật mật khẩu không thành công.')
        else:
            return dict(success=False, message='Cập nhật mật khẩu không thành công.')

    except:
        return dict(success=False, message='Cập nhật mật khẩu không thành công.')


@service.json
@myjwt.allows_jwt()
def change_password(*args, **kwargs):
    try:
        token = request.env.get('HTTP_AUTHORIZATION').split(" ")[1]
        condition_token = (db.token_user.token == token)
        user = db(condition_token).select()
        if not user:
            return dict(success=False, error_code=1, message='Token đã hết hạn.')

        user = db.auth_user(auth.user_id)
        if user.is_active == 0:
            return dict(success=False,error_code=0, message='User hiện tại đã ngừng hoạt động.')

        old_password = request.vars.old_password
        new_password = request.vars.new_password
        print request.post_vars
        if CRYPT(digest_alg='sha512', salt=True)(old_password)[0] == user.password:
            if user:
                user.password = CRYPT(digest_alg='sha512', salt=True)(new_password)[0]

                db(db.auth_user.id == user.id).update(password=user.password)
                db.commit()

                token = myjwt.jwt_token_manager()
                json_object = json.loads(token)
                token_value = json_object['token']

                db(db.login_user.user_id == auth.user_id).update(token=token_value)
                db(db.token_user.user_id == user.id).delete()
                db.commit()
                db.token_user.insert(user_id=auth.user_id, token=token_value)
                db.commit()

                return dict(success=True, token=token_value, message='Thay đổi mật khẩu thành công.')
            else:
                return dict(success=False, message='Có lỗi xảy ra khi thay đổi mật khẩu.')
        else:
            return dict(success=False, message='Mật khẩu cũ không chính xác. Vui lòng thử lại.')
    except:
        return dict(success=False, message='Có lỗi xảy ra khi thay đổi mật khẩu.')


@service.json
@myjwt.allows_jwt()
def get_user_info(*args, **kwargs):
    try:
        token = request.env.get('HTTP_AUTHORIZATION').split(" ")[1]
        condition_token = (db.token_user.token == token)
        user = db(condition_token).select()
        if not user:
            return dict(success=False, error_code=1, message='Token đã hết hạn.')

        user = db.auth_user(auth.user_id)
        if user.is_active == 0:
            return dict(success=False, error_code=0, message='User hiện tại đã ngừng hoạt động.')

        is_send = get_fcm_setting_by_user(auth.user_id)
        if user:
            user_info = dict()
            user_info['first_name'] = user.first_name
            user_info['last_name'] = user.last_name
            user_info['gender'] = user.gender
            user_info['birthdate'] = user.birthdate
            user_info['email'] = user.email
            user_info['phone'] = user.phone
            user_info['address'] = user.address
            user_info['image'] = user.image
            user_info['id'] = str(user.id)
            user_info['is_send'] = is_send
            user_login = db(db.login_user.user_id == auth.user_id).select()
            if user_login:
                user_info['confirm_2fa'] = user_login[0].confirm_2fa
            else:
                user_info['confirm_2fa'] = False

            roles = set()
            role_ids = set()
            permision = set()

            memberships = db(db.auth_membership.user_id == auth.user_id).select()
            group_dict = common.get_group_dict()

            for membership in memberships:
                roles.add(group_dict.get(str(membership.group_id)))
                role_ids.add(str(membership.group_id))

                permisions = db(db.auth_permission.group_id == membership.group_id).select(db.auth_permission.name,
                                                                                           db.auth_permission.table_name)
                for per in permisions:
                    if per.name == 'view':
                        permision.add(str(per.table_name))

            return dict(success=True, data=user_info, permision_view=permision)
        else:
            return dict(success=False, message='Lấy thông tin user lỗi.')
    except:
        return dict(success=False, message='Lấy thông tin user lỗi.')


@service.json
@myjwt.allows_jwt()
def update_user_info(*args, **kwargs):
    token = request.env.get('HTTP_AUTHORIZATION').split(" ")[1]
    condition_token = (db.token_user.token == token)
    user_token = db(condition_token).select()
    if not user_token:
        return dict(success=False, error_code=1, message='Token đã hết hạn.')

    user = db.auth_user(auth.user_id)
    if user.is_active == 0:
        return dict(success=False, error_code=0, message='User hiện tại đã ngừng hoạt động.')

    if user:
        try:
            confirm_2fa = request.vars.confirm_2fa
            first_name = request.vars.first_name
            last_name = request.vars.last_name
            phone = request.vars.phone

            db(db.auth_user.id == auth.user_id).update(first_name=first_name, last_name=last_name, phone=phone)
            db(db.login_user.user_id == auth.user_id).update(confirm_2fa=confirm_2fa)
            db.commit()
            return dict(success=True, message='Cập nhật thông tin user thành công')
        except:
            return dict(success=False, message='Cập nhật thông tin user không thành công')
    else:
        return dict(success=False, message='Cập nhật thông tin user không thành công')


@service.json
@myjwt.allows_jwt()
def update_user_image(*args, **kwargs):

    token = request.env.get('HTTP_AUTHORIZATION').split(" ")[1]
    condition_token = (db.token_user.token == token)
    user_token = db(condition_token).select()
    if not user_token:
        return dict(success=False, error_code=1, message='Token đã hết hạn.')

    user = db.auth_user(auth.user_id)
    if user.is_active == 0:
        return dict(success=False, error_code=0, message='User hiện tại đã ngừng hoạt động.')

    if user:
        try:
            db(db.auth_user.id == auth.user_id).update(image=request.vars['image'])
            db.commit()
            return dict(success=True, message='Cập nhật thông tin user thành công')
        except:
            return dict(success=False, message='Cập nhật thông tin user không thành công')
    else:
        return dict(success=False, message='Cập nhật thông tin user không thành công')


################################################################################
@service.json
@myjwt.allows_jwt()
def send_mail(*args, **kwargs):
    token = request.env.get('HTTP_AUTHORIZATION').split(" ")[1]
    condition_token = (db.token_user.token == token)
    user_token = db(condition_token).select()
    if not user_token:
        return dict(success=False, error_code=1, message='Token đã hết hạn.')

    user = db.auth_user(auth.user_id)
    if user.is_active == 0:
        return dict(success=False, error_code=0, message='User hiện tại đã ngừng hoạt động.')

    if user:
        mail = request.vars.mail
        subject = request.vars.subject
        content = request.vars.content
        try:
            import smtplib, ssl
            from email.mime.text import MIMEText
            import datetime
            import random
            mail_server_config = db(db.mail_server.id > 0).select()
            if mail_server_config:
                mail_server_config = mail_server_config.first()
                SENDER_EMAIL = str(mail_server_config.sender_email)
                MAIL_SERVER = str(mail_server_config.mail_server)
                MAIL_SENDER_PASSWORD = str(mail_server_config.sender_email_password)
                MAIL_SERVER_PORT = int(mail_server_config.mail_server_port)

            msg = MIMEText(content, 'html', 'UTF-8')
            msg['Subject'] = str(subject)
            msg["From"] = SENDER_EMAIL  # 'hd.envisoft@gmail.com'
            msg["To"] = mail
            msg["Cc"] = ''

            server = smtplib.SMTP()

            mail_server = MAIL_SERVER  # 'smtp.gmail.com'

            mail_port = MAIL_SERVER_PORT  # 587

            server.connect(mail_server, mail_port)

            mail_user = SENDER_EMAIL  # 'hd.envisoft@gmail.com'
            mail_pwd = MAIL_SENDER_PASSWORD  # 'ttqtduan!$2019'

            server.starttls()  # Khoi tao ket noi TLS SMTP
            server.login(mail_user, mail_pwd)

            server.sendmail(msg["From"], msg["To"].split(','), msg.as_string())

            server.close()  # ket thuc
            return dict(success=True, message='Gửi mail thành công.')
        except:
            return dict(success=False, message='Có lỗi trong quá trình gửi mail. Vui lòng kiểm tra lại.')


################################################################################
@service.json
@myjwt.allows_jwt()
def get_stations(*args, **kwargs):
    token = request.env.get('HTTP_AUTHORIZATION').split(" ")[1]
    condition_token = (db.token_user.token == token)
    user_token = db(condition_token).select()
    if not user_token:
        return dict(success=False, error_code=1, message='Token đã hết hạn.')

    user = db.auth_user(auth.user_id)
    if user.is_active == 0:
        return dict(success=False, error_code=0, message='User hiện tại đã ngừng hoạt động.')
    # if check_update_pass(user.id):
    #     return dict(success=False, error_code=1, message='Token đã hết hạn.')

    try:
        station_type = request.vars.station_type
        status = request.vars.status
        province_id = request.vars.province_id

        stations = []
        conditions = (db.stations.id > 0)
        if province_id:
            conditions &= (db.stations.province_id == province_id)

        if station_type:
            conditions &= (db.stations.station_type == station_type)

        if status:
            status = status.split(',')
            conditions &= (db.stations.status.belongs(status))

        current_user = db.auth_user(auth.user_id)
        if current_user:
            if not (auth.has_membership('admin') or auth.has_membership(const.GROUP_MANAGER)):
                list_station_manager = db(db.manager_stations.user_id == current_user.id).select(
                    db.manager_stations.station_id)
                station_ids = [str(item.station_id) for item in list_station_manager]
                conditions &= (db.stations.id.belongs(station_ids))

        rows = db(conditions).select(db.stations.ALL, orderby=db.stations.order_no)
        access_token = None

        for row in rows:
            color = '#333333'
            status = ''
            icon = ''

            for k in const.STATION_STATUS:
                if const.STATION_STATUS[k]['value'] == row.status:
                    color = const.STATION_STATUS[k]['color']
                    # status = T(const.STATION_STATUS[k]['name'])
                    icon = T(const.STATION_STATUS[k]['icon'])

            data_lastest = db(db.data_lastest.station_id == row.id).select(db.data_lastest.data_status)
            if data_lastest:
                data_lastest = data_lastest.first()
            for data_row in data_lastest:
                temp_object = {}
                data = data_lastest['data_status']
                for key in data:
                    try:
                        data_indicator = float(data[key]['value'])
                        if math.isnan(data_indicator):
                            data_indicator = None
                            data_lastest['data_status'][key]['value'] = data_indicator
                    except:
                        data_lastest['data_status'][key]['value'] = None
            camera_list = []
            if access_token is None:
                access_token = get_token_with()
            camera_rows = db(db.camera_links.station_id == row.id).select(db.camera_links.description, db.camera_links.camera_source,
                                                                          db.camera_links.camera_source_zm)
            for c_row in camera_rows:
                c_row['camera_source'] = 'zm_{}'.format(c_row['camera_source_zm'])
                camera_list.append(c_row)
            list_indicator = []
            list_station_indicator = []
            list_indicator_station_byorder = []
            conditions_indicator = (db.station_indicator.station_id == row.id)
            conditions_indicator &= (db.station_indicator.status == 1)
            list_indicator_station = db(conditions_indicator).select(db.station_indicator.indicator_id, db.station_indicator.unit,
                                                                     db.station_indicator.exceed_value, db.station_indicator.qcvn_detail_max_value,
                                                                     db.station_indicator.qcvn_detail_min_value, db.station_indicator.preparing_value,
                                                                     db.station_indicator.tendency_value, db.station_indicator.mapping_name)
            lstMeasuring = db(db.indicators.order_no > 1).select(orderby=db.indicators.order_no)
            if lstMeasuring:
                whereQuery = None
                for item in lstMeasuring:
                    whereQuery = conditions_indicator
                    whereQuery &= (db.station_indicator.indicator_id == item.id)
                    mea = db(whereQuery).select(db.station_indicator.indicator_id, db.station_indicator.unit,
                                                                     db.station_indicator.exceed_value, db.station_indicator.qcvn_detail_max_value,
                                                                     db.station_indicator.qcvn_detail_min_value, db.station_indicator.preparing_value,
                                                                     db.station_indicator.tendency_value, db.station_indicator.mapping_name)
                    for a in mea:
                        list_indicator_station_byorder.append(a)
                    whereQuery = None

            if list_indicator_station_byorder:
                list_station_indicator = list_indicator_station_byorder
            else:
                list_station_indicator = list_indicator_station

            if list_station_indicator:
                for indication in list_station_indicator:
                    indicator = db(db.indicators.id == indication.indicator_id).select(db.indicators.indicator)
                    list_indicator.append({
                        'indicator_name': indicator[0].indicator,
                        'mapping_name': indication.mapping_name,
                        'indicator_id': indication.indicator_id,
                        'unit': indication.unit,
                        'exceed_value': indication.exceed_value,
                        'qcvn_detail_max_value': indication.qcvn_detail_max_value,
                        'qcvn_detail_min_value': indication.qcvn_detail_min_value,
                        'preparing_value': indication.preparing_value,
                        'tendency_value': indication.tendency_value,
                        # 'order_no': indication.order_no if indication.order_no  else 0,
                    })
            tmp_obj = {
                'id': str(row.id),
                'station_name': row.station_name,
                'province_id': row.province_id,
                'station_type': row.station_type,
                'longitude': row.longitude,
                'latitude': row.latitude,
                'status': row.status,
                'color': color,
                'icon': icon,
                'address': row.address,
                'data_lastest': data_lastest,
                'camera_list': camera_list,
                'list_indicator': list_indicator,
            }
            if len(camera_list) > 0:
                tmp_obj['camera_token'] = [{'access_token': access_token}]
            stations.append(tmp_obj)
        return dict(success=True, total=len(stations), stations=stations)
    except Exception as ex:
        return dict(success=False, message=str(ex))


################################################################################

@service.json
@myjwt.allows_jwt()
def get_stations_info(*args, **kwargs):
    token = request.env.get('HTTP_AUTHORIZATION').split(" ")[1]
    condition_token = (db.token_user.token == token)
    user_token = db(condition_token).select()
    if not user_token:
        return dict(success=False, error_code=1, message='Token đã hết hạn.')

    user = db.auth_user(auth.user_id)
    if user.is_active == 0:
        return dict(success=False, error_code=0, message='User hiện tại đã ngừng hoạt động.')

    try:
        station_type = request.vars.station_type
        status = request.vars.status
        province_id = request.vars.province_id

        stations = []
        conditions = (db.stations.id > 0)
        if province_id:
            conditions &= (db.stations.province_id == province_id)

        if station_type:
            conditions &= (db.stations.station_type == station_type)

        if status:
            status = status.split(',')
            conditions &= (db.stations.status.belongs(status))

        current_user = db.auth_user(auth.user_id)
        if current_user:
            if not (auth.has_membership('admin') or auth.has_membership(const.GROUP_MANAGER)):
                list_station_manager = db(db.manager_stations.user_id == current_user.id).select(
                    db.manager_stations.station_id)
                station_ids = [str(item.station_id) for item in list_station_manager]
                conditions &= (db.stations.id.belongs(station_ids))

        rows = db(conditions).select(db.stations.ALL, orderby=db.stations.order_no)


        for row in rows:
            color = '#333333'
            status = ''
            icon = ''

            for k in const.STATION_STATUS:
                if const.STATION_STATUS[k]['value'] == row.status:
                    color = const.STATION_STATUS[k]['color']
                    # status = T(const.STATION_STATUS[k]['name'])
                    icon = T(const.STATION_STATUS[k]['icon'])

            stations.append({
                'id': str(row.id),
                'station_name': row.station_name,
                'province_id': row.province_id,
                'station_type': row.station_type,
                'status': row.status,
                'color': color,
                'address': row.address
            })
        return dict(success=True, total=len(stations), stations=stations)
    except Exception as ex:
        return dict(success=False, message=str(ex))


################################################################################

@service.json
@myjwt.allows_jwt()
def get_stations_qi(*args, **kwargs):
    token = request.env.get('HTTP_AUTHORIZATION').split(" ")[1]
    condition_token = (db.token_user.token == token)
    user_token = db(condition_token).select()
    if not user_token:
        return dict(success=False, error_code=1, message='Token đã hết hạn.')

    user = db.auth_user(auth.user_id)
    if user.is_active == 0:
        return dict(success=False, error_code=0, message='User hiện tại đã ngừng hoạt động.')

    try:
        type_qi = int(request.vars.type_qi)
        province_id = request.vars.province_id

        stations = []
        conditions = (db.stations.id > 0)
        if province_id:
            conditions &= (db.stations.province_id == province_id)

        conditions &= (db.stations.is_qi == True)

        if type_qi == 0:
            conditions &= (db.stations.station_type.belongs([const.STATION_TYPE['STACK_EMISSION']['value'],
                                                             const.STATION_TYPE['AMBIENT_AIR']['value']]))
        elif type_qi == 1:
            conditions &= (db.stations.station_type.belongs([const.STATION_TYPE['WASTE_WATER']['value'],
                                                             const.STATION_TYPE['SURFACE_WATER']['value'],
                                                             const.STATION_TYPE['UNDERGROUND_WATER']['value']]))

        rows = db(conditions).select(db.stations.ALL, orderby=db.stations.station_name)

        dt_format = '%Y-%m-%d %H:%M:%S'

        for row in rows:
            color = '#333333'
            status = ''
            icon = ''

            for k in const.STATION_STATUS:
                if const.STATION_STATUS[k]['value'] == row.status:
                    color = const.STATION_STATUS[k]['color']
                    status = T(const.STATION_STATUS[k]['name'])
                    icon = T(const.STATION_STATUS[k]['icon'])

            qi_detail_info = {}
            if row.station_type in [const.STATION_TYPE['WASTE_WATER']['value'],
                                    const.STATION_TYPE['SURFACE_WATER']['value'],
                                    const.STATION_TYPE['UNDERGROUND_WATER']['value']]:
                colors = const.WQI_COLOR
            else:
                colors = const.AQI_COLOR
            for key in sorted(colors):
                if row.qi_adjust <= key:
                    qi_detail_info = colors[key]
                    break
            if qi_detail_info.has_key('description'):
                qi_detail_info['description'] = str(T(qi_detail_info['description']))
            if qi_detail_info.has_key('text'):
                qi_detail_info['text'] = str(T(qi_detail_info['text']))
            if not row.qi_adjust:
                qi_detail_info = {}

            list_indicator = []
            conditions_indicator = (db.station_indicator.station_id == row.id)
            conditions_indicator &= (db.station_indicator.status == 1)
            conditions_indicator &= (db.station_indicator.is_calc_qi == True)
            list_indicator_station = db(conditions_indicator).select(db.station_indicator.indicator_id)

            if list_indicator_station:
                for indication in list_indicator_station:
                    indicator = db(db.indicators.id == indication.indicator_id).select(db.indicators.indicator)
                    list_indicator.append(indicator[0].indicator)

                stations.append({
                    'id': str(row.id),
                    'station_name': row.station_name,
                    'longitude': row.longitude,
                    'latitude': row.latitude,
                    'status': row.status,
                    'color': color,
                    'icon': icon,
                    'address': row.address,
                    'station_type':row.station_type,
                    'list_indicator_cal': list_indicator,
                    'qi_detail_info': qi_detail_info,
                    'qi_adjust': row.qi_adjust,
                    'qi_adjust_time': row.qi_adjsut_time.strftime(dt_format) if row.qi_adjsut_time else None,
                })
        return dict(success=True, total=len(stations), stations=stations)
    except Exception as ex:
        return dict(success=False, message=str(ex))


################################################################################
@service.json
@myjwt.allows_jwt()
def get_data_station(*args, **kwargs):
    # import sys
    # reload(sys)
    # sys.setdefaultencoding('utf8')

    token = request.env.get('HTTP_AUTHORIZATION').split(" ")[1]
    condition_token = (db.token_user.token == token)
    user_token = db(condition_token).select()
    if not user_token:
        return dict(success=False, error_code=1, message='Token đã hết hạn.')

    user = db.auth_user(auth.user_id)
    if user.is_active == 0:
        return dict(success=False, error_code=0, message='User hiện tại đã ngừng hoạt động.')


    try:
        station_id = request.vars.station_id
        indicators = request.vars.indicators
        type_data = int(request.vars.type_data)
        from_date = request.vars.from_date
        to_date = request.vars.to_date
        is_exceed = request.vars.is_exceed
        type_sum = int(request.vars.type_sum)
        page = int(request.vars.page)
        start = int(300*page)
        indicator_array = str(indicators).split(',')

        from_date = datetime.datetime.strptime(from_date, '%Y-%m-%d %H:%M:%S')
        to_date = datetime.datetime.strptime(to_date, '%Y-%m-%d %H:%M:%S')

        data_return = dict()
        count = 0

        if type_data == 0:    # du lieu nguyen goc
            if type_sum == 0:   # data_min
                conditons_min = (db.data_min.station_id == station_id)
                conditons_min &= (db.data_min.get_time >= from_date)
                conditons_min &= (db.data_min.get_time <= to_date)
                data_return = db(conditons_min).select(db.data_min.get_time, db.data_min.data, db.data_min.data_status,
                                                                              orderby=~db.data_min.get_time,
                                                                              limitby=(start, 301))
                count = db(conditons_min).count()

            elif type_sum == 1:   # data_hour
                conditons_1h = (db.data_hour.station_id == station_id)
                conditons_1h &= (db.data_hour.get_time >= from_date)
                conditons_1h &= (db.data_hour.get_time <= to_date)
                data_return = db(conditons_1h).select(db.data_hour.get_time, db.data_hour.data,
                                                                              orderby=~db.data_hour.get_time,
                                                                              limitby=(start, 301))
                count = db(conditons_1h).count()
            elif type_sum == 2:    # data_8h
                conditons_8h = (db.data_hour_8h.station_id == station_id)
                conditons_8h &= (db.data_hour_8h.get_time >= from_date)
                conditons_8h &= (db.data_hour_8h.get_time <= to_date)
                data_return = db(conditons_8h).select(db.data_hour_8h.get_time, db.data_hour_8h.data,
                                                                              orderby=~db.data_hour_8h.get_time,
                                                                              limitby=(start, 301))
                count = db(conditons_8h).count()
            elif type_sum == 3:    # data_day
                conditons_day = (db.data_day.station_id == station_id)
                conditons_day &= (db.data_day.get_time >= from_date)
                conditons_day &= (db.data_day.get_time <= to_date)
                data_return = db(conditons_day).select(db.data_day.get_time, db.data_day.data,
                                                                              orderby=~db.data_day.get_time,
                                                                              limitby=(start, 301))
                count = db(conditons_day).count()
            elif type_sum == 4:     #data_month
                conditons_mon = (db.data_mon.station_id == station_id)
                conditons_mon &= (db.data_mon.get_time >= from_date)
                conditons_mon &= (db.data_mon.get_time <= to_date)
                data_return = db(conditons_mon).select(db.data_mon.get_time, db.data_mon.data,
                                                                              orderby=~db.data_mon.get_time,
                                                                              limitby=(start, 301))
                count = db(conditons_mon).count()
            else:
                conditons_min = (db.data_min.station_id == station_id)
                conditons_min &= (db.data_min.get_time >= from_date)
                conditons_min &= (db.data_min.get_time <= to_date)
                data_return = db(conditons_min).select(db.data_min.get_time, db.data_min.data,
                                                       orderby=~db.data_min.get_time,
                                                       limitby=(start, 301))
                count = db(conditons_min).count()
        else:
            if type_sum == 0:  # data_adjust
                conditons_adjust = (db.data_adjust.station_id == station_id)
                conditons_adjust &= (db.data_adjust.get_time >= from_date)
                conditons_adjust &= (db.data_adjust.get_time <= to_date)
                data_return = db(conditons_adjust).select(db.data_adjust.get_time, db.data_adjust.data,
                                                       orderby=~db.data_adjust.get_time,
                                                       limitby=(start, 301))
                count = db(conditons_adjust).count()
            elif type_sum == 1:  # data_hour
                conditons_1h = (db.data_hour_adjust.station_id == station_id)
                conditons_1h &= (db.data_hour_adjust.get_time >= from_date)
                conditons_1h &= (db.data_hour_adjust.get_time <= to_date)
                data_return = db(conditons_1h).select(db.data_hour_adjust.get_time, db.data_hour_adjust.data,
                                                      orderby=~db.data_hour_adjust.get_time,
                                                      limitby=(start, 301))
                count = db(conditons_1h).count()
            elif type_sum == 2:  # data_8h
                conditons_8h = (db.data_hour_8h_adjust.station_id == station_id)
                conditons_8h &= (db.data_hour_8h_adjust.get_time >= from_date)
                conditons_8h &= (db.data_hour_8h_adjust.get_time <= to_date)
                data_return = db(conditons_8h).select(db.data_hour_8h_adjust.get_time, db.data_hour_8h_adjust.data,
                                                      orderby=~db.data_hour_8h_adjust.get_time,
                                                      limitby=(start, 301))
                count = db(conditons_8h).count()
            elif type_sum == 3:  # data_day
                conditons_day = (db.data_day_adjust.station_id == station_id)
                conditons_day &= (db.data_day_adjust.get_time >= from_date)
                conditons_day &= (db.data_day_adjust.get_time <= to_date)
                data_return = db(conditons_day).select(db.data_day_adjust.get_time, db.data_day_adjust.data,
                                                       orderby=~db.data_day_adjust.get_time,
                                                       limitby=(start, 301))
                count = db(conditons_day).count()
            elif type_sum == 4:  # data_month
                conditons_mon = (db.data_mon_adjust.station_id == station_id)
                conditons_mon &= (db.data_mon_adjust.get_time >= from_date)
                conditons_mon &= (db.data_mon_adjust.get_time <= to_date)
                data_return = db(conditons_mon).select(db.data_mon_adjust.get_time, db.data_mon_adjust.data,
                                                       orderby=~db.data_mon_adjust.get_time,
                                                       limitby=(start, 301))
                count = db(conditons_mon).count()
            else:
                conditons_adjust = (db.data_adjust.station_id == station_id)
                conditons_adjust &= (db.data_adjust.get_time >= from_date)
                conditons_adjust &= (db.data_adjust.get_time <= to_date)
                data_return = db(conditons_adjust).select(db.data_adjust.get_time, db.data_adjust.data,
                                                          orderby=~db.data_adjust.get_time,
                                                          limitby=(start, 301))
                count = db(conditons_adjust).count()
        count_in_page = 0

        if data_return:
            for row in data_return:
                data = row.data
                data_new = dict()
                if is_exceed == 'true' and type_data == 0 and type_sum == 0:
                    data_status = row.data_status
                    data_status_new = dict()
                for indicator in indicator_array:
                    data_new[indicator] = None
                    if is_exceed == 'true' and type_data == 0 and type_sum == 0:
                        data_status_new[indicator] = None
                        if data_status:
                            if data_status.has_key(indicator.decode('utf-8')):
                                if data_status[indicator.decode('utf-8')]['is_exceed'] is True:
                                    data_status_new[indicator] = data_status[indicator.decode('utf-8')]['value']
                    else:
                        if data.has_key(indicator.decode('utf-8')):
                             data_new[indicator] = float(data[indicator.decode('utf-8')])

                if is_exceed == 'true' and type_data == 0 and type_sum == 0:
                    row.data = data_status_new
                else:
                    row.data = data_new
                if type_data == 0 and type_sum == 0:
                    del row.data_status

            count_in_page = len(data_return)

        page_info = dict()
        page_info['current_page'] = page
        page_info['count_all_item'] = count
        page_info['count_in_page_current'] = count_in_page
        page_info['item_per_page'] = 300

        return dict(success=True, data_return=data_return, page_info=page_info)
    except Exception as ex:
        return dict(success=False, message=str(ex))


################################################################################
@service.json
@myjwt.allows_jwt()
def get_data_qi_station(*args, **kwargs):

    token = request.env.get('HTTP_AUTHORIZATION').split(" ")[1]
    condition_token = (db.token_user.token == token)
    user_token = db(condition_token).select()
    if not user_token:
        return dict(success=False, error_code=1, message='Token đã hết hạn.')

    user = db.auth_user(auth.user_id)
    if user.is_active == 0:
        return dict(success=False, error_code=0, message='User hiện tại đã ngừng hoạt động.')


    try:
        station_id = request.vars.station_id
        type_qi = int(request.vars.type_qi)     # co 2 loai la AQI, WQI (0 la AQI, 1 la WQI) chi lay data adjust
        from_date = request.vars.from_date
        to_date = request.vars.to_date
        type_time = int(request.vars.type_time)       # co 2 loai la NGAY va GIO (0 - la GIO, 1 la NGAY)
        page = int(request.vars.page)
        start = int(300*page)

        from_date = datetime.datetime.strptime(from_date, '%Y-%m-%d %H:%M:%S')
        to_date = datetime.datetime.strptime(to_date, '%Y-%m-%d %H:%M:%S')

        data_return = dict()
        count = 0
        count_in_page = 0

        if type_qi == 0:    # du lieu aqi
            if type_time == 0:   # aqi adjust hour
                conditons_aqi_hour = (db.aqi_data_adjust_hour.station_id == station_id)
                conditons_aqi_hour &= (db.aqi_data_adjust_hour.get_time >= from_date)
                conditons_aqi_hour &= (db.aqi_data_adjust_hour.get_time <= to_date)
                data_return = db(conditons_aqi_hour).select(db.aqi_data_adjust_hour.get_time, db.aqi_data_adjust_hour.data,
                                                                              orderby=~db.aqi_data_adjust_hour.get_time,
                                                                              limitby=(start, 301))
                count = db(conditons_aqi_hour).count()

            elif type_time == 1:   # aqi adjust day
                conditons_aqi_day = (db.aqi_data_adjust_24h.station_id == station_id)
                conditons_aqi_day &= (db.aqi_data_adjust_24h.get_time >= from_date)
                conditons_aqi_day &= (db.aqi_data_adjust_24h.get_time <= to_date)
                data_return = db(conditons_aqi_day).select(db.aqi_data_adjust_24h.get_time, db.aqi_data_adjust_24h.data_24h,
                                                                              orderby=~db.aqi_data_adjust_24h.get_time,
                                                                              limitby=(start, 301))
                count = db(conditons_aqi_day).count()
            else:
                conditons_aqi_hour = (db.aqi_data_adjust_hour.station_id == station_id)
                conditons_aqi_hour &= (db.aqi_data_adjust_hour.get_time >= from_date)
                conditons_aqi_hour &= (db.aqi_data_adjust_hour.get_time <= to_date)
                data_return = db(conditons_aqi_hour).select(db.aqi_data_adjust_hour.get_time,
                                                            db.aqi_data_adjust_hour.data,
                                                            orderby=~db.aqi_data_adjust_hour.get_time,
                                                            limitby=(start, 301))
                count = db(conditons_aqi_hour).count()
        else:
            if type_time == 0:  # data_wqi adjust hour
                conditons_wqi_hour = (db.wqi_data_adjust_hour.station_id == station_id)
                conditons_wqi_hour &= (db.wqi_data_adjust_hour.get_time >= from_date)
                conditons_wqi_hour &= (db.wqi_data_adjust_hour.get_time <= to_date)
                data_return = db(conditons_wqi_hour).select(db.wqi_data_adjust_hour.get_time, db.wqi_data_adjust_hour.data,
                                                            orderby=~db.wqi_data_adjust_hour.get_time,
                                                            limitby=(start, 301))
                count = db(conditons_wqi_hour).count()
            else:
                conditons_wqi_hour = (db.wqi_data_adjust_hour.station_id == station_id)
                conditons_wqi_hour &= (db.wqi_data_adjust_hour.get_time >= from_date)
                conditons_wqi_hour &= (db.wqi_data_adjust_hour.get_time <= to_date)
                data_return = db(conditons_wqi_hour).select(db.wqi_data_adjust_hour.get_time,
                                                            db.wqi_data_adjust_hour.data,
                                                            orderby=~db.wqi_data_adjust_hour.get_time,
                                                            limitby=(start, 301))
                count = db(conditons_wqi_hour).count()

        if data_return:
            count_in_page = len(data_return)
        page_info = dict()
        page_info['current_page'] = page
        page_info['count_all_item'] = count
        page_info['count_in_page_current'] = count_in_page
        page_info['item_per_page'] = 300

        return dict(success=True, data_return=data_return, page_info=page_info)
    except Exception as ex:
        return dict(success=False, message=str(ex))


################################################################################
@service.json
@myjwt.allows_jwt()
def get_list_notification(*args, **kwargs):

    token = request.env.get('HTTP_AUTHORIZATION').split(" ")[1]
    condition_token = (db.token_user.token == token)
    user_token = db(condition_token).select()
    if not user_token:
        return dict(success=False, error_code=1, message='Token đã hết hạn.')

    user = db.auth_user(auth.user_id)
    if user.is_active == 0:
        return dict(success=False, error_code=0, message='User hiện tại đã ngừng hoạt động.')

    try:
        alarm_type = request.vars.alarm_type      # co 3 loai canh bao: 0 - mat ket noi, 1- ket noi lai, 2 - vuot nguong
        station_ids = request.vars.station_ids
        from_date = request.vars.from_date
        to_date = request.vars.to_date
        page = int(request.vars.page)
        start = int(300*page)

        data_return = dict()
        count = 0
        count_in_page = 0

        conditions_notification = (db.notification_app.id > 0)
        conditions_notification &= (db.notification_app.user_id == user.id)
        if alarm_type:
            alarm_types = [int(t) for t in alarm_type.split(',')]
            conditions_notification &= (db.notification_app.alarm_type.belongs(alarm_types))

        if station_ids:
            station_ids = station_ids.split(',')
            conditions_notification &= (db.notification_app.station_id.belongs(station_ids))

        if from_date:
            from_date = datetime.datetime.strptime(from_date, '%Y-%m-%d %H:%M:%S')
            conditions_notification &= (db.notification_app.get_time >= from_date)
        if to_date:
            to_date = datetime.datetime.strptime(to_date, '%Y-%m-%d %H:%M:%S')
            conditions_notification &= (db.notification_app.get_time <= to_date)

        data_return = db(conditions_notification).select(orderby=~db.notification_app.get_time, limitby=(start, 301))
        count = db(conditions_notification).count()
        notifications = []
        if data_return:
            for row in data_return:
                station = db(db.stations.id == row.station_id).select(db.stations.station_name).first()
                notifications.append({
                    'id': str(row.id),
                    'user_id': row.user_id,
                    'station_id': row.station_id,
                    'station_name': station.station_name,
                    'get_time': row.get_time,
                    'content': row.content,
                    'alarm_type': row.alarm_type,
                    'data': row.data,
                    'time_sent': row.time_sent,
                    'is_open': row.is_open,
                })

        page_info = dict()
        page_info['current_page'] = page
        page_info['count_all_item'] = count
        page_info['count_in_page_current'] = count_in_page
        page_info['item_per_page'] = 300

        return dict(success=True, data_return=notifications, page_info=page_info)
    except Exception as ex:
        return dict(success=False, message=str(ex))


################################################################################
@service.json
@myjwt.allows_jwt()
def update_user_notification(*args, **kwargs):

    token = request.env.get('HTTP_AUTHORIZATION').split(" ")[1]
    condition_token = (db.token_user.token == token)
    user_token = db(condition_token).select()
    if not user_token:
        return dict(success=False, error_code=1, message='Token đã hết hạn.')

    user = db.auth_user(auth.user_id)
    if user.is_active == 0:
        return dict(success=False, error_code=0, message='User hiện tại đã ngừng hoạt động.')


    if user:
        try:
            id_notification = request.vars.id_notification
            is_open = request.vars.is_open

            db(db.notification_app.id == id_notification).update(is_open=is_open)
            db.commit()
            return dict(success=True, message='Cập nhật trạng thái notification thành công')
        except:
            return dict(success=False, message='Cập nhật trạng thái notification không thành công')
    else:
        return dict(success=False, message='Cập nhật trạng thái notification không thành công')


################################################################################
@service.json
@myjwt.allows_jwt()
def get_station_type(*args, **kwargs):

    token = request.env.get('HTTP_AUTHORIZATION').split(" ")[1]
    condition_token = (db.token_user.token == token)
    user_token = db(condition_token).select()
    if not user_token:
        return dict(success=False, error_code=1, message='Token đã hết hạn.')

    user = db.auth_user(auth.user_id)
    if user.is_active == 0:
        return dict(success=False, error_code=0, message='User hiện tại đã ngừng hoạt động.')


    province_id = request.vars.province_id

    # Select stations to fill in dropdown box
    fields = [
        db.stations.id,
        db.stations.station_name,
        db.stations.station_type,
        db.stations.status,
    ]

    conditions = (db.stations.id > 0)
    if province_id:
        conditions &= (db.stations.province_id == province_id)

    current_user = db.auth_user(auth.user_id)
    if current_user:
        if not (auth.has_membership('admin') or auth.has_membership(const.GROUP_MANAGER)):
            list_station_manager = db(db.manager_stations.user_id == current_user.id).select(
                db.manager_stations.station_id)
            station_ids = [str(item.station_id) for item in list_station_manager]
            conditions &= (db.stations.id.belongs(station_ids))

    stations = db(conditions).select(*fields)

    station_type_online = dict()
    for st in const.STATION_TYPE:
        if not station_type_online.has_key(st):
            station_type_online[st] = dict()
            station_type_online[st]['value'] = const.STATION_TYPE[st]['value']
            station_type_online[st]['name'] = const.STATION_TYPE[st]['name']
            station_type_online[st]['name_vn'] = T(const.STATION_TYPE[st]['name'])
            station_type_online[st]['image'] = const.STATION_TYPE[st]['image']
            station_type_online[st]['online'] = 0
            station_type_online[st]['exceed'] = 0
            station_type_online[st]['total'] = 0
            station_type_online[st]['offline'] = 0
            station_type_online[st]['adjust'] = 0
            station_type_online[st]['error'] = 0

    total_online, total_adjust, total_offline, total_error, total_exceed = 0, 0, 0, 0, 0

    for station in stations:
        for st in station_type_online:
            if station.station_type == station_type_online[st]['value']:
                if station.status == const.STATION_STATUS['ADJUSTING']['value']:
                    station_type_online[st]['adjust'] += 1
                    total_adjust += 1
                elif station.status == const.STATION_STATUS['OFFLINE']['value']:
                    station_type_online[st]['offline'] += 1
                    total_offline += 1
                elif station.status == const.STATION_STATUS['ERROR']['value']:
                    station_type_online[st]['error'] += 1
                    total_error += 1
                elif station.status == const.STATION_STATUS['EXCEED']['value']:
                    station_type_online[st]['exceed'] += 1
                    total_exceed += 1
                else:
                    station_type_online[st]['online'] += 1
                    total_online += 1

                station_type_online[st]['total'] += 1
                break
    station_type = []
    for st in station_type_online:
        station_type.append(station_type_online[st])
    time_count = datetime.datetime.now()
    return dict(success=True, time_count=time_count, station_type=station_type, total_error=total_error,
                total_station=len(stations), total_online=total_online, total_offline=total_offline,
                total_adjust=total_adjust, total_exceed=total_exceed)


################################################################################

@service.json
@myjwt.allows_jwt()
def get_station_distribution_by_province(*args, **kwargs):

    token = request.env.get('HTTP_AUTHORIZATION').split(" ")[1]
    condition_token = (db.token_user.token == token)
    user_token = db(condition_token).select()
    if not user_token:
        return dict(success=False, error_code=1, message='Token đã hết hạn.')

    user = db.auth_user(auth.user_id)
    if user.is_active == 0:
        return dict(success=False, error_code=0, message='User hiện tại đã ngừng hoạt động.')

    try:
        province_id = request.vars.province_id

        data = dict()
        data['categories'] = []
        data['series'] = [{
            'name': T('Good'),
            'color': const.STATION_STATUS['GOOD']['color'],
            'data': [],
        }
            , {
                'name': T('Exceed'),
                'color': const.STATION_STATUS['EXCEED']['color'],
                'data': [],
            }
            , {
                'name': T('Offline'),
                'color': const.STATION_STATUS['OFFLINE']['color'],
                'data': [],
            }
            , {
                'name': T('Adjusting'),
                'color': const.STATION_STATUS['ADJUSTING']['color'],
                'data': [],
            }
            , {
                'name': T('Sensor error'),
                'color': const.STATION_STATUS['ERROR']['color'],
                'data': [],
            }]

        data['title'] = T('Stations distributed by Province')
        data['subtitle'] = ''
        if province_id:
            rows = db(db.provinces.id == province_id).select(db.provinces.id, db.provinces.province_name,
                                                  orderby=db.provinces.order_no)
        else:
            rows = db(db.provinces.id > 0).select(db.provinces.id, db.provinces.province_name,
                                                  orderby=db.provinces.order_no)
        provinces = dict()
        for row in rows:
            provinces[str(row.id)] = row.province_name

        conditions = (db.stations.id > 0)
        # hungdx phan quyen quan ly trạm theo user issue 44
        if user:
            if not (auth.has_membership('admin') or auth.has_membership(const.GROUP_MANAGER)):
                list_station_manager = db(db.manager_stations.user_id == user.id).select(
                    db.manager_stations.station_id)
                station_ids = [str(item.station_id) for item in list_station_manager]
                conditions &= (db.stations.id.belongs(station_ids))

        conditions &= (db.stations.province_id != None)

        rows = db(conditions).select(db.stations.province_id, db.stations.status, limitby=(0, 100))
        categories = dict()
        if not rows:
            data['subtitle'] = T('No data found!')
        for row in rows:
            province_id = str(row.province_id)
            if provinces.has_key(province_id):
                if not categories.has_key(province_id):
                    categories[province_id] = {
                        'name': provinces[province_id],
                        'qty': 0,
                        'qty_good': 0,
                        'qty_exceed': 0,
                        'qty_offline': 0,
                        'qty_adjust': 0,
                        'qty_error': 0
                    }
                categories[province_id]['qty'] += 1
                if row.status == const.STATION_STATUS['EXCEED']['value']:
                    categories[province_id]['qty_exceed'] += 1
                    pass
                elif row.status == const.STATION_STATUS['GOOD']['value'] or \
                        row.status == const.STATION_STATUS['TENDENCY']['value'] or \
                        row.status == const.STATION_STATUS['PREPARING']['value']:
                    categories[province_id]['qty_good'] += 1
                elif row.status == const.STATION_STATUS['OFFLINE']['value']:
                    categories[province_id]['qty_offline'] += 1
                elif row.status == const.STATION_STATUS['ADJUSTING']['value']:
                    categories[province_id]['qty_adjust'] += 1
                elif row.status == const.STATION_STATUS['ERROR']['value']:
                    categories[province_id]['qty_error'] += 1

        for item in categories:
            data['categories'].append(categories[item]['name'])
            data['series'][0]['data'].append(categories[item]['qty_good'])
            data['series'][1]['data'].append(categories[item]['qty_exceed'])
            data['series'][2]['data'].append(categories[item]['qty_offline'])
            data['series'][3]['data'].append(categories[item]['qty_adjust'])
            data['series'][4]['data'].append(categories[item]['qty_error'])

        return dict(success=True, data=data)
    except Exception as ex:
        return dict(success=False, msg=str(ex))


################################################################################

@service.json
@myjwt.allows_jwt()
def get_station_data_by_province(*args, **kwargs):

    token = request.env.get('HTTP_AUTHORIZATION').split(" ")[1]
    condition_token = (db.token_user.token == token)
    user_token = db(condition_token).select()
    if not user_token:
        return dict(success=False, error_code=1, message='Token đã hết hạn.')

    user = db.auth_user(auth.user_id)
    if user.is_active == 0:
        return dict(success=False, error_code=0, message='User hiện tại đã ngừng hoạt động.')

    try:
        from w2pex import date_util
        from datetime import datetime, date

        province_id = request.vars.province_id

        conditions = (db.stations.id > 0)
        if province_id:
            conditions &= (db.stations.province_id == province_id)

        if user:
            if not (auth.has_membership('admin') or auth.has_membership(const.GROUP_MANAGER)):
                list_station_manager = db(db.manager_stations.user_id == user.id).select(
                    db.manager_stations.station_id)
                station_ids = [str(item.station_id) for item in list_station_manager]
                conditions &= (db.stations.id.belongs(station_ids))

        ids = db(conditions).select(db.stations.id)
        station_ids = [str(item.id) for item in ids]

        first_date_in_this_month = date_util.get_first_day_current_month(date.today())
        first_date_in_this_month = datetime.combine(first_date_in_this_month, datetime.min.time())
        first_date_in_last_month = date_util.get_first_day_last_month(date.today())
        first_date_in_last_month = datetime.combine(first_date_in_last_month, datetime.min.time())
        first_date_in_next_month = date_util.get_first_day_next_month(date.today())
        first_date_in_next_month = datetime.combine(first_date_in_next_month, datetime.min.time())

        t1 = 0
        t2 = 0
        n_this_month = 0
        n_last_month = 0
        # alarm_level
        if True:
            alarm_level_this_month = dict()
            alarm_level_last_month = dict()
            for item in const.STATION_STATUS:
                alarm_level_this_month[item] = dict()
                alarm_level_this_month[item]['value'] = const.STATION_STATUS[item]['value']
                alarm_level_this_month[item]['name'] = str(T(const.STATION_STATUS[item]['name']))
                alarm_level_this_month[item]['color'] = const.STATION_STATUS[item]['color']
                alarm_level_this_month[item]['icon'] = const.STATION_STATUS[item]['icon']
                alarm_level_this_month[item]['qty'] = 0
                alarm_level_this_month[item]['percent'] = 0

                alarm_level_last_month[item] = dict()
                alarm_level_last_month[item]['value'] = const.STATION_STATUS[item]['value']
                alarm_level_last_month[item]['name'] = str(T(const.STATION_STATUS[item]['name']))
                alarm_level_last_month[item]['color'] = const.STATION_STATUS[item]['color']
                alarm_level_last_month[item]['icon'] = const.STATION_STATUS[item]['icon']
                alarm_level_last_month[item]['qty'] = 0
                alarm_level_last_month[item]['percent'] = 0
        # station_type
        if True:
            station_type_this_month = dict()
            station_type_last_month = dict()
            for item in const.STATION_TYPE:
                station_type_this_month[item] = dict()
                station_type_this_month[item]['value'] = const.STATION_TYPE[item]['value']
                station_type_this_month[item]['name'] = str(T(const.STATION_TYPE[item]['name']))
                station_type_this_month[item]['qty'] = 0

                station_type_last_month[item] = dict()
                station_type_last_month[item]['value'] = const.STATION_TYPE[item]['value']
                station_type_last_month[item]['name'] = str(T(const.STATION_TYPE[item]['name']))
                station_type_last_month[item]['qty'] = 0

        alarm_level_this_month.pop('PREPARING')
        alarm_level_last_month.pop('PREPARING')
        alarm_level_this_month.pop('TENDENCY')
        alarm_level_last_month.pop('TENDENCY')

        stations = db(db.stations.id.belongs(station_ids)).select()
        ## tinh lượng datamin phải nhận trong tháng này
        conditions = (db.data_min_month_collect.station_id.belongs(station_ids))
        conditions &= (db.data_min_month_collect.date_month >= first_date_in_this_month)
        conditions &= (db.data_min_month_collect.date_month < first_date_in_next_month)
        data_min_month_this_month = db(conditions).select(db.data_min_month_collect.station_id,
                                                          db.data_min_month_collect.actual_datamin)

        data_min_month_this_month_dict = dict()
        for item in data_min_month_this_month:
            data_min_month_this_month_dict[item.station_id] = item
        expected_this_month = 0.0
        # số ngày trong tháng
        # days_this_month = (
        #         first_date_in_this_month.replace(month=first_date_in_this_month.month % 12 + 1, day=1) - timedelta(
        #     days=1)).day
        days_this_month = datetime.now().day - 1
        days_this_month += 1.0 / 24.0 * datetime.now().hour
        for row in stations:
            # tần suất nhận dữ liệu
            freq = row['frequency_receiving_data']
            # freq = 5
            indicator_number = db(db.station_indicator.station_id == row.id).count(db.station_indicator.indicator_id)
            if not indicator_number:
                indicator_number = 0
            if (not freq) or (freq == 0):
                freq = 5
            expected_this_month_each = (indicator_number * days_this_month * 24 * 60 / freq)
            if data_min_month_this_month_dict.has_key(str(row.id)):
                actual_this_month = data_min_month_this_month_dict[str(row.id)].actual_datamin

                if actual_this_month:
                    if expected_this_month_each < actual_this_month:
                        expected_this_month_each = actual_this_month
            expected_this_month += expected_this_month_each
        # Count number records of data_min in this month
        n_qty_this_month = 0
        n_qty_last_month = 0

        if data_min_month_this_month:

            # conditions = (db.data_min_month_collect.station_id.belongs(station_ids))
            # conditions &= (db.data_min_month_collect.date_month >= first_date_in_this_month)
            # conditions &= (db.data_min_month_collect.date_month < first_date_in_next_month)
            data = db(conditions).select(
                db.data_min_month_collect.actual_datamin.sum().with_alias('actual_datamin'),
                db.data_min_month_collect.qty_good.sum().with_alias('qty_good'),
                db.data_min_month_collect.qty_exceed.sum().with_alias('qty_exceed'),
                db.data_min_month_collect.qty_adjusting.sum().with_alias('qty_adjusting'),
                db.data_min_month_collect.qty_error.sum().with_alias('qty_error'),
            ).first()
            n_this_month = data['actual_datamin'] if data['actual_datamin'] else 0
            t1 = n_this_month
            n_qty_this_month = data['actual_datamin'] if data['actual_datamin'] else 0
            # Tinh theo %
            if expected_this_month and expected_this_month > 0:
                n_this_month = round(100 * data['actual_datamin'] / expected_this_month, 2) if data[
                    'actual_datamin'] else 0
            else:
                n_this_month = 0
            # n_this_month = "{:,}".format(n_this_month)
            alarm_level_this_month['GOOD']['qty'] = moneyfmt(data['qty_good'])
            alarm_level_this_month['GOOD']['percent'] = round(
                100.0 * data['qty_good'] / expected_this_month if expected_this_month > 0 and data['qty_good'] else 0,
                2)

            alarm_level_this_month['EXCEED']['qty'] = moneyfmt(data['qty_exceed'])
            alarm_level_this_month['EXCEED']['percent'] = round(
                100.0 * data['qty_exceed'] / expected_this_month if expected_this_month > 0 and data[
                    'qty_exceed'] else 0,
                2)

            alarm_level_this_month['ADJUSTING']['qty'] = moneyfmt(data['qty_adjusting'])
            alarm_level_this_month['ADJUSTING']['percent'] = round(
                100.0 * data['qty_adjusting'] / expected_this_month if expected_this_month > 0 and data[
                    'qty_adjusting'] else 0,
                2)
            alarm_level_this_month['ERROR']['qty'] = moneyfmt(data['qty_error'])
            alarm_level_this_month['ERROR']['percent'] = round(
                100.0 * data['qty_error'] / expected_this_month if expected_this_month > 0 and data['qty_error'] else 0,
                2)

            offline_count = expected_this_month - data['qty_good'] - data['qty_exceed'] - data['qty_adjusting'] - data[
                'qty_error']
            alarm_level_this_month['OFFLINE']['qty'] = moneyfmt(offline_count)
            alarm_level_this_month['OFFLINE']['percent'] = round(
                100.0 * offline_count / expected_this_month if expected_this_month > 0 and offline_count else 0,
                2)

        conditions = (db.data_min_month_collect.station_id.belongs(station_ids))
        conditions &= (db.data_min_month_collect.date_month >= first_date_in_last_month)
        conditions &= (db.data_min_month_collect.date_month < first_date_in_this_month)
        data_min_month_last_month = db(conditions).select(db.data_min_month_collect.station_id,
                                                          db.data_min_month_collect.actual_datamin)
        data_min_month_last_month_dict = dict()
        for item in data_min_month_last_month:
            data_min_month_last_month_dict[item.station_id] = item
        expected_last_month = 0.0
        # số ngày trong tháng
        days_last_month = (
                first_date_in_last_month.replace(month=first_date_in_last_month.month % 12 + 1, day=1) - timedelta(
            days=1)).day
        for row in stations:
            # tần suất nhận dữ liệu
            freq = row['frequency_receiving_data']
            # freq = 5
            indicator_number = db(db.station_indicator.station_id == row.id).count(db.station_indicator.indicator_id)
            if not indicator_number:
                indicator_number = 0
            if (not freq) or (freq == 0):
                freq = 5
            expected_last_month_each = (indicator_number * days_last_month * 24 * 60 / freq)
            # Trường hợp data nhận được nhiều hơn dự kiến (expected)
            if data_min_month_last_month_dict.has_key(str(row.id)):
                actual_last_month = data_min_month_last_month_dict[str(row.id)].actual_datamin
                if actual_last_month:
                    if expected_last_month_each < actual_last_month:
                        expected_last_month_each = actual_last_month
                expected_last_month += expected_last_month_each

        # Count number records of data_min in last month
        if data_min_month_last_month:
            # conditions = (db.data_min_month_collect.station_id.belongs(station_ids))
            # conditions &= (db.data_min_month_collect.date_month >= first_date_in_last_month)
            # conditions &= (db.data_min_month_collect.date_month < first_date_in_this_month)
            data = db(conditions).select(
                db.data_min_month_collect.actual_datamin.sum().with_alias('actual_datamin'),
                db.data_min_month_collect.qty_good.sum().with_alias('qty_good'),
                db.data_min_month_collect.qty_exceed.sum().with_alias('qty_exceed'),
                db.data_min_month_collect.qty_adjusting.sum().with_alias('qty_adjusting'),
                db.data_min_month_collect.qty_error.sum().with_alias('qty_error'),
            ).first()
            n_last_month = data['actual_datamin'] if data['actual_datamin'] else 0
            t2 = n_last_month
            n_qty_last_month = data['actual_datamin'] if data['actual_datamin'] else 0
            if expected_last_month and expected_last_month > 0:
                n_last_month = round(100 * data['actual_datamin'] / expected_last_month, 2) if data[
                    'actual_datamin'] else 0
            else:
                n_last_month = 0

            # alarm_level_last_month['TENDENCY']['qty'] = data['qty_good']
            # alarm_level_last_month['TENDENCY']['percent'] = round(
            #     100.0 * data['qty_good'] / data['actual_datamin'] if data['actual_datamin'] and data['qty_good'] else 0, 2)
            # alarm_level_last_month['TENDENCY']['name'] = T('Good')
            # alarm_level_last_month['EXCEED']['qty'] = data['qty_exceed']
            # alarm_level_last_month['EXCEED']['percent'] = round(
            #     100.0 * data['qty_exceed'] / data['actual_datamin'] if data['actual_datamin'] and data['qty_exceed'] else 0, 2)
            alarm_level_last_month['GOOD']['qty'] = moneyfmt(data['qty_good'])
            alarm_level_last_month['GOOD']['percent'] = round(
                100.0 * data['qty_good'] / expected_last_month if expected_last_month > 0 and data['qty_good'] else 0,
                2)

            alarm_level_last_month['EXCEED']['qty'] = moneyfmt(data['qty_exceed'])
            alarm_level_last_month['EXCEED']['percent'] = round(
                100.0 * data['qty_exceed'] / expected_last_month if expected_last_month > 0 and data[
                    'qty_exceed'] else 0,
                2)

            alarm_level_last_month['ADJUSTING']['qty'] = moneyfmt(data['qty_adjusting'])
            alarm_level_last_month['ADJUSTING']['percent'] = round(
                100.0 * data['qty_adjusting'] / expected_last_month if expected_last_month > 0 and data[
                    'qty_adjusting'] else 0,
                2)
            alarm_level_last_month['ERROR']['qty'] = moneyfmt(data['qty_error'])
            alarm_level_last_month['ERROR']['percent'] = round(
                100.0 * data['qty_error'] / expected_last_month if expected_last_month > 0 and data['qty_error'] else 0,
                2)

            offline_count = expected_last_month - data['qty_good'] - data['qty_exceed'] - data['qty_adjusting'] - data[
                'qty_error']
            alarm_level_last_month['OFFLINE']['qty'] = moneyfmt(offline_count)
            alarm_level_last_month['OFFLINE']['percent'] = round(
                100.0 * offline_count / expected_last_month if expected_last_month > 0 and offline_count else 0,
                2)
        # So sanh gtri collect tong cong
        collect_icon = 'fa fa-arrow-up text-info'
        if t1 < t2:
            collect_icon = 'fa fa-arrow-down text-info'
        elif t1 == t2:
            collect_icon = 'fa fa-pause text-warning'

        # So sanh gtri 3 nguong thang nay va thang truoc de display Icon len/xuong cho dung
        for item in alarm_level_last_month:
            if alarm_level_this_month[item]['percent'] > alarm_level_last_month[item]['percent']:
                alarm_level_this_month[item]['icon'] = 'fa fa-arrow-up text-danger'
            if alarm_level_this_month[item]['percent'] < alarm_level_last_month[item]['percent']:
                alarm_level_this_month[item]['icon'] = 'fa fa-arrow-down text-info'
            else:
                alarm_level_this_month[item]['icon'] = 'fa fa-pause text-warning'

        # Count number records of station_off_log in this month
        if True:
            conditions = (db.data_min_month_collect.station_id.belongs(station_ids))
            conditions &= (db.data_min_month_collect.date_month >= first_date_in_this_month)
            conditions &= (db.data_min_month_collect.date_month < first_date_in_next_month)
            conditions &= (db.data_min_month_collect.number_off_log > 0)
            rows = db(conditions).select(
                db.data_min_month_collect.id,
                db.data_min_month_collect.station_type,
                db.data_min_month_collect.number_off_log
            )
            n2_this_month = 0
            for row in rows:
                n2_this_month += row.number_off_log
                for item in station_type_this_month:
                    if row.station_type == station_type_this_month[item]['value']:
                        station_type_this_month[item]['qty'] += row.number_off_log
                        break
            for item in station_type_this_month:
                if station_type_this_month[item]['qty']:
                    station_type_this_month[item]['qty'] = moneyfmt(station_type_this_month[item]['qty'])
            t1 = n2_this_month
            n2_this_month = "{:,}".format(n2_this_month)

        # Count number records of station_off_log in last month
        if True:
            conditions = (db.data_min_month_collect.station_id.belongs(station_ids))
            conditions &= (db.data_min_month_collect.date_month >= first_date_in_last_month)
            conditions &= (db.data_min_month_collect.date_month < first_date_in_this_month)
            conditions &= (db.data_min_month_collect.number_off_log > 0)
            rows = db(conditions).select(
                db.data_min_month_collect.id,
                db.data_min_month_collect.station_type,
                db.data_min_month_collect.number_off_log
            )
            n2_last_month = 0
            for row in rows:
                n2_last_month += row.number_off_log
                for item in station_type_last_month:
                    if row.station_type == station_type_last_month[item]['value']:
                        station_type_last_month[item]['qty'] += row.number_off_log
                        break
            for item in station_type_last_month:
                if station_type_last_month[item]['qty']:
                    station_type_last_month[item]['qty'] = moneyfmt(station_type_last_month[item]['qty'])
            t2 = n2_last_month
            n2_last_month = "{:,}".format(n2_last_month)

        # So sanh gtri offline cua station
        offline_icon = 'fa fa-arrow-up text-danger'
        if t1 < t2:
            collect_icon = 'fa fa-arrow-down text-info'
        elif t1 == t2:
            collect_icon = 'fa fa-pause text-warning'

        return dict(success=True, n_this_month=n_this_month, n_last_month=n_last_month, collect_icon=collect_icon,
                    offline_icon=offline_icon,
                    alarm_level_this_month=alarm_level_this_month, alarm_level_last_month=alarm_level_last_month,
                    n2_this_month=n2_this_month, n2_last_month=n2_last_month,
                    station_type_this_month=station_type_this_month, station_type_last_month=station_type_last_month,
                    n_qty_this_month=moneyfmt(n_qty_this_month), expected_this_month=moneyfmt(expected_this_month),
                    n_qty_last_month=moneyfmt(n_qty_last_month), expected_last_month=moneyfmt(expected_last_month),
                    )
    except Exception as ex:
        return dict(success=False, msg=str(ex))


################################################################################
def moneyfmt(value, places=0, curr='', sep=',', dp='.', pos='', neg='(', trailneg=''):
    # """Convert Decimal to a money formatted string.
    #
    # places:  required number of places after the decimal point
    # curr:    optional currency symbol before the sign (may be blank)
    # sep:     optional grouping separator (comma, period, space, or blank)
    # dp:      decimal point indicator (comma or period)
    #          only specify as blank when places is zero
    # pos:     optional sign for positive numbers: '+', space or blank
    # neg:     optional sign for negative numbers: '-', '(', space or blank
    # trailneg:optional trailing minus indicator:  '-', ')', space or blank
    #
    # >>> d = Decimal('-1234567.8901')
    # >>> moneyfmt(d, curr='$')
    # '-$1,234,567.89'
    # >>> moneyfmt(d, places=0, sep='.', dp='', neg='', trailneg='-')
    # '1.234.568-'
    # >>> moneyfmt(d, curr='$', neg='(', trailneg=')')
    # '($1,234,567.89)'
    # >>> moneyfmt(Decimal(123456789), sep=' ')
    # '123 456 789.00'
    # >>> moneyfmt(Decimal('-0.02'), neg='<', trailneg='>')
    # '<0.02>'
    #
    # """
    from decimal import Decimal
    q = Decimal(10) ** -places      # 2 places --> '0.01'
    sign, digits, exp = Decimal(value).quantize(q).as_tuple()
    result = []
    digits = map(str, digits)
    build, next = result.append, digits.pop

    if places == 0:
        dp = ''

    if sign:
        build(trailneg)
    for i in range(places):
        build(next() if digits else '0')

    build(dp)
    if not digits:
        build('0')

    i = 0
    while digits:
        build(next())
        i += 1
        if i == 3 and digits:
            i = 0
            build(sep)
    build(curr)
    build(neg if sign else pos)
    return ''.join(reversed(result))


################################################################################
def check_update_pass(user_id):
    update_pass = False
    user = db.auth_user(user_id)
    condition_login = (db.login_user.user_id == user_id)
    user_login = db(condition_login).select()

    if user_login:
        user_login = user_login.first()
        if user.password == user_login.pass_old:
            update_pass = False
        else:
            db(db.token_user.user_id == user_id).delete()
            db.commit()
            update_pass = True

    return update_pass

@service.json
@myjwt.allows_jwt()
def update_receive_notify(*args, **kwargs):
    try:
        token = request.env.get('HTTP_AUTHORIZATION').split(" ")[1]
        condition_token = (db.token_user.token == token)
        user_token = db(condition_token).select()
        is_send = request.vars.is_send
        if not user_token:
            return dict(success=False, error_code=1, message='Token đã hết hạn.')

        user = db.auth_user(auth.user_id)
        if user.is_active == 0:
            return dict(success=False, error_code=0, message='User hiện tại đã ngừng hoạt động.')


        db.fcm_user_setting.update_or_insert(db.fcm_user_setting.user_id == auth.user_id, user_id=auth.user_id, is_send=is_send)
        return dict(success=True, user_id=str(auth.user_id))
    except Exception as ex:
        return dict(success=False, message=ex.message)


@service.json
def signup(*args, **kwargs):
    try:
        data = kwargs
        data['created_on'] = datetime.datetime.utcnow()
        data["is_active"] = 1

        user = db(db.auth_user.username == data['username']).select()
        if user:
            return dict(success=False, message='{} exists!'.format(data['username']))
        user = db(db.auth_user.email == data['email']).select()
        if user:
            return dict(success=False, message='{} exists!'.format(data['email']))
        password = CRYPT(digest_alg='sha512', salt=True)(data['password'])[0]
        data['password'] = password
        user = db.auth_user.insert(**data)
        return dict(success=True, message='Sign Up Success')
    except:
        return dict(success=False, message='Account creation failed!!')

# db.auth_user.insert(**dict(frm.vars))

################################################################################
