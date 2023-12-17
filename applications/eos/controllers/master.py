# -*- coding: utf-8 -*-
###############################################################################
# Author : 
# Date   : 
# 
# Description : 
# 
###############################################################################


def login():
    PUBLIC_KEY = '6LeIyaIUAAAAAG2E1rZ6j43wE7pFS8ZFJHzSrEOf'
    PRIVATE_KEY = '6LeIyaIUAAAAAH9WLA5_LkbgfuMyGchFstQj6qua'
    HOST = ['cem.gov.vn', 'envisoft.gov.vn', 'gov.vn']
    TOKEN_PUBLIC = '0RJITA9ewVBPYVdggzWi5YNvmH4nPfy'

    on_captcha = False
    url2 = request.env.http_host

    username = request.vars['username']
    password = request.vars['password']
    token = request.vars['token']

    if username and password and token and token == TOKEN_PUBLIC:
        login_status = auth.login_bare(username, password)
        if login_status:
            data = db(db.manager_owner_information.id > 0).select().first()
            session.ownerName = unicode(data.name, "utf-8")
            session.ownerDivision = unicode(data.division, "utf-8")
            return redirect(URL('dashboard', 'index'))

    for item in HOST:
        if item == url2.split(':')[0]:
            on_captcha = True
        if item == ".".join(url2.split(':')[0].split('.')[1:4]):
            on_captcha = True
    if on_captcha:
        from gluon.tools import Recaptcha2
        auth.settings.captcha = Recaptcha2(request, PUBLIC_KEY, PRIVATE_KEY,
                                           error_message=T('Vui lòng nhập lại captcha'), label=T('Xác thực:'),
                                           options={'hl': 'vi'})
    data = db(db.manager_owner_information.id > 0).select().first()
    session.ownerName = unicode(data.name, "utf-8")
    session.ownerDivision = unicode(data.division, "utf-8")
    session.perThousand = data.perThousand
    session.decimal = data.decimal
    frm = auth.login()
    frm.custom.widget.username['_placeholder'] = T('Enter username')
    frm.custom.widget.username['_tabindex'] = 1
    frm.custom.widget.username['_autofocus'] = True
    frm.custom.widget.password['_placeholder'] = T('Enter password')
    frm.custom.widget.password['_tabindex'] = 2
    return dict(form=frm)

    if current_user:  # Already logged-in
        redirect(URL('dashboard', 'index'))
    else:
        form = FORM(Recaptcha2())
        if form.process().accepted:
            user = db(db.auth_user.username == request.vars.username).select().first()

            if user:
                # Login succeeded
                if CRYPT(digest_alg='sha512', salt=True)(request.vars.password)[0] == user.password:
                    if user.is_active:
                        current_user = user
                        if request.vars.remember:
                            user.expiration = int(myconf.get('misc.session_long_expiration'))
                        else:
                            user.expiration = int(myconf.get('misc.session_default_expiration'))
                        user.roles, user.role_ids = app.get_user_roles()
                        user.last_visit = request.utcnow
                        # user.function_codes = get_function_codes()
                        # user.menu_codes = get_menu_codes()
                        # user.menu_html = get_menu_html()
                        user.id = str(user.id)

                        if 'admin' in user.roles:
                            conditions = (db2.scheduler_task.task_name.contains('task_get_data'))
                            conditions &= (db2.scheduler_task.status.belongs(['QUEUED', 'RUNNING']))
                            conditions &= (db2.scheduler_task.next_run_time >= request.now)
                            count = db2(conditions).count()
                            if not count:
                                session.request_active_task_get_data = True

                        # if session.login_nexturl:
                        # redirect(session.login_nexturl)

                        redirect(URL('dashboard', 'index'))
                    else:
                        val.add_to_validation_summary(T('This account has been locked!'))
                        return dict(form=form)
                else:
                    val.add_to_validation_summary(T('Username or password incorrect!'))
                    return dict(form=form)
            else:
                val.add_to_validation_summary(T('Username or password incorrect!'))
                return dict(form=form)
        elif form.errors:
            val.add_to_validation_summary(T('Username or password incorrect!'));
            return dict(form=form)
        else:
            if not session.login_nexturl:  # The login page is the first page
                session.login_nexturl = URL('dashboard', 'index')
            return dict(form=form)


################################################################################

def loggedout():
    session.auth = None

    redirect(URL('master', 'login'))
    return dict()


################################################################################
def registration_succeeded():
    return dict()


################################################################################
def access_denied():
    return dict()


################################################################################
# @decor.requires_login()
def change_password():
    form = auth.change_password()
    form.custom.widget.old_password['_placeholder'] = T('PLH_ENTER_PASSWORD')
    form.custom.widget.old_password['_tabindex'] = 1
    form.custom.widget.old_password['_autofocus'] = True
    form.custom.widget.new_password['_placeholder'] = T('Enter new password')
    form.custom.widget.new_password['_tabindex'] = 2
    form.custom.widget.new_password2['_placeholder'] = T('Retype password')
    form.custom.widget.new_password2['_tabindex'] = 3
    return dict(form=form)

    form = SQLFORM.factory(
        Field('old_password', requires=[IS_LENGTH(minsize=1, maxsize=64)]),
        Field('password', requires=[IS_LENGTH(minsize=1, maxsize=64)]),
        Field('password_again', requires=[IS_LENGTH(minsize=1, maxsize=64),
                                          IS_EQUAL_TO(request.vars.password,
                                                      error_message=T('MSG_ERR_UNMATCHED_PASSWORD'))]))
    if form.process().accepted:
        user = current_user
        if CRYPT(digest_alg='sha512', salt=True)(request.vars.old_password)[0] == user.password:
            user.password = CRYPT(digest_alg='sha512', salt=True)(request.vars.password)[0]
            # db.usr[user.id] = dict(password = user.password)
            db.auth_user[user.id] = dict(password=user.password)
            redirect(URL('home', 'change_password_succeeded'))
        else:
            val.add_to_form_errors(form, 'old_password', T('MSG_ERR_INVALID_PASSWORD_2'))
            return dict(form=form)
    elif form.errors:
        return dict(form=form)
    else:
        return dict(form=form)


################################################################################
def change_password_succeeded():
    return dict()


################################################################################
def reset_password():
    form = SQLFORM.factory(
        Field('username', requires=[IS_LENGTH(minsize=1, maxsize=64),
                                    IS_IN_DB(db, 'auth_user.username', error_message=T('MSG_ERR_INVALID_PASSWORD'))]),
        Field('password', requires=[IS_LENGTH(minsize=1, maxsize=64)]),
        Field('password_again', requires=[IS_LENGTH(minsize=1, maxsize=64),
                                          IS_EQUAL_TO(request.vars.password,
                                                      error_message=T('MSG_ERR_UNMATCHED_PASSWORD'))]))
    if form.process().accepted:
        user = db(db.auth_user.username == request.vars.username).select().first()
        if user:
            user.update_record(password=CRYPT(key=auth.settings.hmac_key)(request.vars.password)[0],
                               reset_password_key='')
        redirect(URL('master', 'reset_password_succeeded'))
    elif form.errors:
        return dict(form=form)
    else:
        return dict(form=form)


################################################################################
def reset_password_succeeded():
    return dict()


################################################################################
def information_credential():
    if session.ownerDivision is None:
        data = db(db.manager_owner_information.id > 0).select().first()
        session.ownerName = unicode(data.name, "utf-8")
        session.ownerDivision = unicode(data.division, "utf-8")
        session.logo = None
        if data.logo:
            session.logo = '/eos/default/download/{}'.format(data.logo)
    return dict()

