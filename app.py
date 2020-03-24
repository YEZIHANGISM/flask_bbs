from flask import Flask
from apps.cms.views import bp as cms_bp
from apps.common.views import bp as common_bp
from apps.front.views import bp as front_bp
import config
from exts import db, mail
from flask_wtf import CSRFProtect
# from utils.cache import redis_client

def create_app():
    app = Flask(__name__)
    app.config.from_object(config)

    app.register_blueprint(cms_bp)
    app.register_blueprint(common_bp)
    app.register_blueprint(front_bp)

    db.init_app(app)
    mail.init_app(app)
    # redis_client.init_app(app)

    CSRFProtect(app)
    return app

if __name__ == '__main__':
    app = create_app()
    app.run()