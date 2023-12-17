import os
import ConfigParser
import logging.handlers
from gluon import current
from gluon.html import URL
from gluon.http import redirect
from gluon.storage import Storage

#Configuration
class Configuration(object):
    
    def __init__(self, filename, default_values={}):
        self._config = ConfigParser.SafeConfigParser(default_values)
        self._config.read(filename)
        self._filename = filename

    def get(self, section, option):
        #return self._config[section][option] -> error: SafeConfigParser no has __getitem__
        return self._config.get(section, option) 

    def set(self, section, option, value):
        self._config.set(section, option, value)
        
    def save(self, section, option, value):
        self._config.set(section, option, value)
        self._config.write(open(self._filename, 'w'))
        
    def write():
        self._config.write(open(self._filename, 'w'))
        
    def get_int(self, section, option):
        return self._config.getint(section, option) 
        
    def get_float(self, section, option):
        return self._config.getfloat(section, option) 
        
    def get_boolean(self, section, option):
        return self._config.getboolean(section, option) 

# Logging        
def init_log(level = logging.DEBUG,
             formatter = '%(asctime)s %(levelname)s %(filename)s:%(funcName)s:%(lineno)d: %(message)s',
             fileName = 'log/app.log',
             maxBytes = 1024 * 1024 * 10,
             backupCount = 1024):

    request = current.request
    logger = logging.getLogger(request.application)
    
    # Check if logger had initialized. 
    # If yes return logger else initialize it and set 'init_log' = True
    if hasattr(logger, 'init_log'):
        return logger

    # GAE or rolling-file logging handler
    if request.env.web2py_runtime_gae:
        handler = logging.getLogger().handlers[0]
    else:
        # Add handle log to file
        handler = logging.handlers.RotatingFileHandler(os.path.join(request.folder, fileName),
                                                     maxBytes = maxBytes,
                                                     backupCount = backupCount)
        logger.addHandler(handler)
        
        # Todo : Add handle log to console
        #handler = logging.handlers.StreamHandler(sys.stdout)
        #logger.addHandler(logging.StreamHandler(sys.stdout))

    handler.setLevel(level)
    handler.setFormatter(logging.Formatter(formatter))

    logger.setLevel(level)
    logger.init_log = True
    return logger

# Generic decorator
class Decorator(object):
    
    def __init__(self, 
        check_login = None, login_url = None, login_next = None,
        check_permission = None, permission_url = None, permission_next = None):
        self._check_login = check_login
        self._login_url = login_url
        self._login_next = login_next
        self._check_permission = check_permission
        self._permission_url = permission_url
        self._permission_next = permission_next
        
    def set_check_login(self, check_login):
        self._check_login = check_login
        
    def set_login_url(self, login_url):
        self._login_url = login_url
        
    def set_login_next(self, login_next):
        self._login_next = login_next
        
    def set_check_permission(self, check_permission):
        self._check_permission = check_permission
        
    def set_permission_url(self, permission_url):
        self._permission_url = permission_url
        
    def set_permission_next(self, permission_next):
        self._permission_next = permission_next
        
    def requires(self, condition, otherwise = None):
        
        def wrapper(old_func):
            if condition['args'] == ['delete_any_table']:
                permission = '%s|delete' %(current.request.args[2])
                condition['args'] = [permission]
                condition['name'] = 'requires permission: ' + permission
            
            def new_func(*a, **b):
                if condition.value:
                    flag = condition.value
                elif condition.func:
                    if condition.args and condition.kwargs:
                        flag = condition.func(*(condition.args), **(condition.kwargs))
                    elif condition.args:
                        flag = condition.func(*(condition.args))
                    elif condition.kwargs:
                        flag = condition.func(**(condition.kwargs))
                    else:
                        flag = condition.func()
                else:
                    flag = True
                if (not flag) and otherwise and otherwise.func:
                    if otherwise.args and otherwise.kwargs:
                        otherwise.func(*(otherwise.args), **(otherwise.kwargs))
                    elif otherwise.args:
                        otherwise.func(*(otherwise.args))
                    elif otherwise.kwargs:
                        otherwise.func(**(otherwise.kwargs))
                    else:
                        otherwise.func()
                return old_func(*a, **b)
                
            new_func.__doc__ = old_func.__doc__
            new_func.__name__ = old_func.__name__
            new_func.__dict__.update(old_func.__dict__)
            return new_func

        return wrapper

    def requires_login(self):
        
        def _otherwise():
            if self._login_next:
                if isinstance(self._login_next, bool):
                    request = current.request
                    controller = request.controller
                    function = request.function
                    current.session.login_nexturl = URL(controller, function, args = request.args, vars = request.vars)
                else:
                    current.session.login_nexturl = self._login_next
            if self._login_url:
                redirect(self._login_url)                
            
        condition = Storage(func = self._check_login, name='requires login')
        otherwise = Storage(func = _otherwise)
        return self.requires(condition, otherwise)

    def requires_permission(self, permission = None):
        
        def _otherwise():
            if self._permission_next:
                if isinstance(self._permission_next, bool):
                    request = current.request
                    controller = request.controller
                    function = request.function
                    current.session.permission_nexturl = URL(controller, function, args = request.args, vars = request.vars)
                else:
                    current.session.permission_nexturl = self._permission_next
            if self._permission_url:
                redirect(self._permission_url)                
        
        condition = Storage(func = self._check_permission, args = [permission], name='requires permission: ' + permission)
        otherwise = Storage(func = _otherwise)
        return self.requires(condition, otherwise)
        
class RequiresLogin(object):
    
    def __init__(self, check_login = None, login_url = None, login_next = None):
        self._controllers = set()
        self._check_login = check_login
        self._login_url = login_url
        self._login_next = login_next
        
    def set_check_login(self, check_login):
        self._check_login = check_login
        
    def set_login_url(self, login_url):
        self._login_url = login_url
        
    def set_login_next(self, login_next):
        self._login_next = login_next
        
    def set(self, controllers):
        if controllers:
            self._controllers = controllers
        
    def get(self):
        return self._controllers
        
    def add(self, controller):
        if controller and len(controller) > 0:
            if controller not in self._controllers:
                self._controllers.add(controller)

    def run(self):
        request = current.request
        controller = request.controller
        function = request.function
        if controller not in self._controllers: return
        if (self._check_login() if callable(self._check_login) else self._check_login): return
        if self._login_next:
            if isinstance(self._login_next, bool):
                current.session.login_nexturl = URL(controller, function, args = request.args, vars = request.vars)
            else:
                current.session.login_nexturl = self._login_next
        if self._login_url:
            redirect(self._login_url)

# Create global variables
# Example: global_dict = cache.ram('my_thread_safe_object', lambda: ThreadSafe(), ThreadSafe.forever) 
#          global_dict.key1 = 4
#          print global_dict.key1
class ThreadSafe(dict): 
    forever = 10**10
    
    def __init__(self): 
         import thread 
         self['lock'] = thread.allocate_lock()
         
    def __setattr__(self,key,value): 
         self['lock'].acquire() 
         self[key] = value 
         self['lock'].release()
         
    def __getattr__(self,key): 
         self['lock'].acquire() 
         value = self[key] 
         self['lock'].release() 
         return value 
