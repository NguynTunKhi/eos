'''
Using replicated databases :
'''
# def fail_safe_round_robin(*uris):
     # i = cache.ram('round-robin', lambda: 0, None)
     # uris = uris[i:]+uris[:i] # rotate the list of uris
     # cache.ram('round-robin', lambda: (i+1)%len(uris), 0)
     # return uris
     
# db = DAL(fail_safe_round_robin('mysql://...1','mysql://...2','mysql://...3'))

'''
It is also possible to connect to different databases depending on the requested action or controller. 
In a master-slave database configuration, some action performs only a read and some person both read/write.
The former can safely connect to a slave db server, while the latter should connect to a master
(where 1,2,3 are slaves and 3,4,5 are masters.)
'''
# if request.function in read_only_actions:
   # db = DAL(sample(['mysql://...1','mysql://...2','mysql://...3'], 3))
# elif request.action in read_only_actions:
   # db = DAL(shuffle(['mysql://...1','mysql://...2','mysql://...3']))
# else:
   # db = DAL(sample(['mysql://...3','mysql://...4','mysql://...5'], 3))

   
db = DAL(myconf.get('db.uri'), 
        pool_size = myconf.get('db.pool_size'), 
        check_reserved = None, 
        # check_reserved = ['all'], 
        decode_credentials = True,
        migrate_enabled = myconf.get('db.migrate'))
        
db2 = DAL(myconf.get('db2.uri'), 
        pool_size = myconf.get('db2.pool_size'))
        # check_reserved = None,
        # decode_credentials = True,
        # migrate_enabled = myconf.get('db2.migrate'))
        
# -------------------------------------------------------------------------
# configure auth policy
# -------------------------------------------------------------------------
import os        
# host names must be a list of allowed host names (glob syntax allowed)
from custom_auth import CustomAuth
auth = CustomAuth(db, host_names=myconf.get('host.names'))
# auth = Auth(db, host_names=myconf.get('host.names'))

auth.settings.extra_fields['auth_user'] = [
    Field('fullname', compute = lambda r: r['last_name'] + ' ' + r['first_name']),
    Field('address'),
    Field('city'),
    Field('phone'),
    Field('birthdate', 'date'),
    Field('is_supper_admin', 'boolean', default=False),
    Field('gender', 'integer', default = 0),
    Field('is_active', 'integer',default =1, label = T('LBL_STATUS')),
    Field('image', 'upload', uploadfolder = os.path.join(request.folder, 'uploads/user image'), default = ''),
    Field('created_by', 'string', default = str(session.auth.user.id) if session.auth and hasattr(session.auth, 'user') and session.auth.user else '',
          writable=False, readable=False, label=T('Created by')),
]
auth.settings.extra_fields['auth_group'] = [
    Field('manager', 'string'),
    Field('created_by', 'string', default = str(session.auth.user.id) if session.auth and hasattr(session.auth, 'user') and session.auth.user else '',
          writable=False, readable=False, label=T('Created by')),
]
auth.define_tables(username=True, signature=True)
db.auth_user._format = '%(fullname)s (%(username)s)'
db.auth_user.gender.requires = IS_IN_SET([0, 1], [T('male'), T('female')])
db.auth_user.is_active.requires = IS_IN_SET({1: T('Active'), 0: T('In-active')})
db.auth_user.is_supper_admin.requires = IS_IN_SET({True: T('Active'), False: T('In-active')})
db.auth_group.manager.requires = IS_NULL_OR(IS_IN_DB(db, db.auth_user.id, db.auth_user._format))


auth.settings.registration_requires_verification = False
auth.settings.registration_requires_approval = False
auth.settings.reset_password_requires_verification = True
auth.settings.update(login_url=URL('master', 'login'))
auth.settings.login_url=URL('master', 'login')
def after_login_succes(form):
    if auth.has_membership('admin'):
        conditions  = (db2.scheduler_task.task_name.contains('task_get_data'))
        conditions &= (db2.scheduler_task.status.belongs(['QUEUED', 'RUNNING']))
        count = db2(conditions).count()
        if not count:
            session.request_active_task_get_data = True
    pass
auth.settings.login_onaccept = lambda form:after_login_succes(form)
# auth.settings.login_onfail = redirect(URL('master', 'login'))
ACCESS_DENIES_URL =  URL('default', 'user', args = ['not_authorized'])

# auth.enable_record_versioning(db)