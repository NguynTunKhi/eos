
# Current user
current_user = None
if session.auth:
    if session.auth.user:
        is_update_roles_to_session = False
        if not hasattr(session.auth.user, 'roles') or not hasattr(session.auth.user, 'role_ids'):
            is_update_roles_to_session = True
        else:
            if not session.auth.user.roles or not session.auth.user.role_ids:
                is_update_roles_to_session = True
        if is_update_roles_to_session:
            roles = set()
            role_ids = set()
            user_id = session.auth.user.id
            memberships = db(db.auth_membership.user_id == user_id).select()
            group_dict = common.get_group_dict()
            for membership in memberships:
                roles.add(group_dict.get(str(membership.group_id)))
                role_ids.add(str(membership.group_id))
            session.auth.user.roles = roles
            session.auth.user.role_ids = role_ids
        session.auth.user.user_id = str(session.auth.user.id)
        current_user = session.auth.user
