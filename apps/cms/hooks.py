from flask import session
from flask import g
from .views import bp
from .models import CMSUser
import config


@bp.before_request
def before_request():
    if config.CMS_USER_ID in session:
        id = session.get(config.CMS_USER_ID)
        user = CMSUser.query.filter_by(id=id).first()
        if user:
            g.cms_user = user
