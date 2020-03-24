import config
from flask import session, redirect, url_for, g
from functools import wraps

# 登录验证
def login_required(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        if config.CMS_USER_ID in session:
            return func(*args, **kwargs)
        else:
            return redirect(url_for("cms.login"))
    return wrapper

# 权限验证
def permission_required(permission):
    def outter(func):
        @wraps(func)
        def inner(*args, **kwargs):
            if g.cms_user.has_permission(permission):
                return func(*args, **kwargs)
            else:
                return redirect(url_for("cms.index"))
        return inner
    return outter