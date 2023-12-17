#!/usr/bin/env python
# coding: utf8
################################################################################
import os, ConfigParser, traceback, datetime
from gluon import current
from gluon.http import HTTP, redirect
from gluon.html import URL
from w2pex import util, mvc, bootstrap, val
from w2pex.mvc import ActionHandler
from w2pex.util import Decorator, RequiresLogin
from w2pex.val import Validation
from w2pex.bootstrap import BootstrapWidgets
from applications.eip.modules import common
from gluon.contrib.appconfig import AppConfig
myconf = AppConfig(reload = True)

       
################################################################################
class AppActionHandler(ActionHandler):
    def __init__(self):
        super(AppActionHandler, self).__init__()
        self.add_action_executing_handler(self._on_action_executing)
        self.add_action_executed_handler(self._on_action_executed)
        self.add_view_rendering_handler(self._on_view_rendering)
        self.add_view_rendered_handler(self._on_view_rendered)
        self.add_action_finished_handler(self._on_action_finished)
        self.add_exception_handler(self._on_exception)

    def _on_action_executing(self):
        if current.session.user:
            user = current.session.user
            request = current.request
            if user.last_visit:
                if user.last_visit + datetime.timedelta(days = 0, seconds = user.expiration) < request.utcnow:
                    current.session.user = None
                    redirect(URL('master', 'login'))
                if (request.utcnow - user.last_visit).seconds > (user.expiration / 10):
                    user.last_visit = request.utcnow
                    cookies_expiration = user.last_visit + datetime.timedelta(days = 0, seconds = user.expiration)
                    response = current.response
                    response.cookies[response.session_id_name]['expires'] = cookies_expiration.strftime('%a, %d-%b-%Y %H:%M:%S GMT')
            else:
                user.last_visit = request.utcnow

    def _on_action_executed(self):
        request = current.request
        current.logger.info('*' * 70)
        current.logger.info('On action executed: ' + request.controller + '/' + request.function)
        current.logger.info(current.db._lastsql)
        print ''

    def _on_view_rendering(self):
        request = current.request

    def _on_view_rendered(self):
        request = current.request

    def _on_action_finished(self):
        request = current.request

    def _on_exception(self, e):
        if isinstance(e, HTTP) and e.status == 303: return
        message = str(e) + '\n' + traceback.format_exc()
        # if current.config.log_lastsql:
        if myconf.get('log.log_lastsql'):
            if hasattr(current, 'db'):
                lastsql = current.db._lastsql
                # message = message + '\nLast SQL executed by the DAL: ' + '\n' + lastsql
                message = message + '\n'
        current.logger.error(message)

################################################################################
class AppDecorator(Decorator):
    def __init__(self):
        super(AppDecorator, self).__init__()
        self.set_check_login(lambda: current.session.user is not None)
        self.set_login_url(URL('master', 'login'))
        self.set_login_next(True)
        self.set_check_permission(lambda function_code: (current.session.user is not None) and \
                                                        (('admin' in current.session.user.roles) or \
                                                         (function_code in current.session.user.function_codes)))
        self.set_permission_url(URL('master', 'access_denied'))
        self.set_permission_next(True)

################################################################################
class AppUtil:
    _instance = None

    @classmethod
    def get_instance(cls):
        if cls._instance is None: cls._instance = cls()
        return cls._instance

    def __init__(self):
        # self._config = AppCfg()
        # self._logger = util.init_log(level = logging.ERROR)
        self._logger = util.init_log()
        self._action_handler = AppActionHandler()
        self._decorator = AppDecorator()
        self._validation = Validation()
        self._requires_login = RequiresLogin()
        self._bootstrap_widgets = BootstrapWidgets()
        self._requires_login = RequiresLogin()
        self._action_handler.add_action_executing_handler(self._requires_login.run)

    # def get_config(self):
        # return self._config

    def get_logger(self):
        return self._logger

    def get_action_handler(self):
        return self._action_handler

    def get_decorator(self):
        return self._decorator

    def get_validation(self):
        return self._validation

    def get_bootstrap_widgets(self):
        return self._bootstrap_widgets

    def controller_requires_login(self):
        self._requires_login.add(current.session.request.controller)

    def get_user_roles(self):
        roles = set()
        role_ids = set()
        db = current.db
        user_id = current.session.user.id
        memberships = db(db.auth_membership.user_id == user_id).select()
        
        group_dict = common.get_group_dict()
        
        for membership in memberships:
            roles.add(group_dict.get(str(membership.group_id)))
            role_ids.add(str(membership.group_id))

        return roles, role_ids