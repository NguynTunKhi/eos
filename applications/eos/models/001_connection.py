'''
Using replicated databases :
'''
import const
from applications.eos.modules import common
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
import pymongo
import os
if False:
    from gluon import *
    request = current.request
    response = current.response
    session = current.session
    cache = current.cache
    T = current.T
client = pymongo.MongoClient(myconf.get('db.uri'))
mongo_db_name = os.getenv('ENV_MONGO_DB_NAME', 'eos')
pydb = client[mongo_db_name]
   
db = DAL(myconf.get('db.uri'), 
        pool_size = myconf.get('db.pool_size'), 
        check_reserved = None, 
        # check_reserved = ['all'], 
        decode_credentials = True,
        migrate_enabled = myconf.get('db.migrate'))
        
db2 = DAL(myconf.get('db2.uri'), 
        pool_size = myconf.get('db2.pool_size'))
        #check_reserved = None,
        #decode_credentials = True)
        #migrate_enabled = myconf.get('db2.migrate'))

from gluon import current
current.db = db
current.db2 = db2
# -------------------------------------------------------------------------
# configure auth policy
# -------------------------------------------------------------------------
import os
# host names must be a list of allowed host names (glob syntax allowed)
from custom_auth import CustomAuth
auth = CustomAuth(db, host_names=myconf.get('host.names'))
# auth = Auth(db, host_names=myconf.get('host.names'))

auth_user_type_values = []
for key, item in common.sort_dict_const_by_value(const.AUTH_USER_TYPE):
    auth_user_type_values.append(item['value'])

auth.settings.extra_fields['auth_user'] = [
  Field('fullname', compute=lambda r: r['last_name'] + ' ' + r['first_name']),
  Field('address'),
  Field('city'),
  Field('phone'),
  Field('birthdate', 'date'),
  Field('gender', 'integer', default=0),
  Field('type', 'integer', default=const.AUTH_USER_TYPE['GOVERNMENT']['value']),
  Field('is_active', 'integer', default=1, label=T('LBL_STATUS')),
  Field('is_supper_admin', 'boolean', default=False),
  Field('agent_id', 'string'),
  Field('image', 'upload', uploadfolder=os.path.join(request.folder, 'uploads/user image'), default=''),
  Field('created_by', 'string', default=str(session.auth.user.id) if session.auth and hasattr(session.auth,
                                                                                              'user') and session.auth.user else '',
        writable=False, readable=False, label=T('Created by')),
]
auth.settings.extra_fields['auth_group'] = [
  Field('manager', 'string'),
  Field('created_by', 'string', default=str(session.auth.user.id) if session.auth and hasattr(session.auth,
                                                                                              'user') and session.auth.user else '',
        writable=False, readable=False, label=T('Created by')),
]

auth.define_tables(username=True, signature=True)
db.auth_user._format = '%(fullname)s (%(username)s)'
db.auth_user.gender.requires = IS_IN_SET([0, 1], [T('male'), T('female')])
db.auth_user.is_active.requires = IS_IN_SET({1: T('Active'), 0: T('In-active')})
db.auth_user.type.requires = IS_IN_SET({const.AUTH_USER_TYPE_ENTERPRISE: T('AUTH_USER_TYPE_ENTERPRISE'), const.AUTH_USER_TYPE_GOVERNMENT: T('AUTH_USER_TYPE_GOVERNMENT')})

# User manager
conditions_auth_user = db.auth_user.id > 0
conditions_auth_user &= ~db.auth_user.username.belongs(['admin'])
if session.auth and hasattr(session.auth, 'user') and session.auth.user:
  if not (auth.has_membership('admin') or auth.has_membership('managers')):
    user_id = session.auth.user.id
    groups = db(db.auth_membership.user_id == user_id).select(db.auth_membership.group_id)
    if groups:
      group_ids = [str(r.group_id) for r in groups]
      user_rows = db(db.auth_membership.group_id.belongs(group_ids)).select(db.auth_membership.user_id)
      user_ids = [str(r.user_id) for r in user_rows]
      conditions_auth_user &= db.auth_user.id.belongs(user_ids)
      conditions_auth_user &= ~db.auth_user.id.belongs([user_id])
    else:
      conditions_auth_user &= db.auth_user.created_by == user_id

db.auth_group.manager.requires = IS_NULL_OR(IS_IN_DB(db(conditions_auth_user), db.auth_user.id, db.auth_user._format))


auth.settings.registration_requires_verification = False
auth.settings.registration_requires_approval = False
auth.settings.reset_password_requires_verification = True
auth.settings.update(login_url=URL('master', 'login'))
auth.settings.login_url=URL('master', 'login')

def after_login_succes(form):
    db2(db2.scheduler_task.id > 0).delete()
    # if auth.has_membership('admin'):
    #     # conditions  = (db2.scheduler_task.task_name.contains('task_get_data'))
    #     conditions = (db2.scheduler_task.status.belongs(['QUEUED', 'RUNNING']))
    #     count = db2(conditions).count()
    #     if not count:
    #         session.request_active_task_get_data = True
    # pass
auth.settings.login_onaccept = lambda form:after_login_succes(form)
# auth.settings.login_onfail = redirect(URL('master', 'login'))
ACCESS_DENIES_URL =  URL('default', 'user', args = ['not_authorized'])

# auth.enable_record_versioning(db)