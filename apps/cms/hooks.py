from flask import session
from flask import g
from .views import bp
from .models import CMSUser
from apps.cms.models import CMSPermission
import config


@bp.before_request
def before_request():
    if config.CMS_USER_ID in session:
        id = session.get(config.CMS_USER_ID)
        user = CMSUser.query.filter_by(id=id).first()
        if user:
            g.cms_user = user

@bp.context_processor
def cms_context_pocessor():
    return {'CMSPermission':CMSPermission}