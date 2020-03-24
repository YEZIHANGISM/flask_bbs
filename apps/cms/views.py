from flask import (
    Blueprint,
    render_template,
    views,
    request,
    session,
    redirect,
    url_for,
    g
)
from flask_mail import Message
from .forms import LoginForm, SetPwdForm, VerifyEmailForm
from .models import CMSUser
from exts import db, mail
from .decorators import login_required
from utils import restful
from utils import send_email
from utils import cache
from threading import Thread
import config
import string
import random


bp = Blueprint("cms", __name__, url_prefix="/cms")


@bp.route("/", endpoint="home")
@login_required
def home():
    return render_template("cms/cms_base.html")

@bp.route("/logout/", endpoint="logout")
@login_required
def logout():
    del session[config.CMS_USER_ID]
    return redirect(url_for("cms.login"))

@bp.route("/index/", endpoint="index")
@login_required
def index():
    return render_template("cms/index.html")

@bp.route("/profile/", endpoint="profile", methods=["GET",])
@login_required
def profile():
    return render_template("cms/profile.html")

@bp.route("/email_captcha/", endpoint="email_capthca")
@login_required
def email_captcha():
    email = request.args.get("email")
    if not email:
        return restful.param_error(message="请传递参数")

    source = list(string.ascii_letters)
    source.extend([str(i) for i in range(10)])
    captcha = "".join(random.sample(source, 6))

    # 缓存验证码
    cache.set(email, captcha)

    msg = Message("flask测试验证码", recipients=[email])
    msg.body = 'captcha: %s'%captcha
    try:
        th = Thread(target=send_email.send_email_async, args=[msg])
        # mail.send(msg)
        th.start()
        th.join()
    except:
        return restful.server_error("服务器开小差了")
    return restful.success()


class SetEmailView(views.MethodView):
    """修改邮箱"""
    decorators = [login_required]

    def get(self):
        return render_template("cms/setemail.html")

    def post(self):
        form = VerifyEmailForm(request.form)
        if form.validate():
            email = form.email.data
            g.cms_user.email = email
            db.session.commit()
            return restful.success()
        else:
            return restful.param_error("验证失败")

class SetPwdView(views.MethodView):
    decorators = [login_required]

    def get(self, error=None, message=None):
        return render_template("cms/setpwd.html", error=error, message=message)

    def post(self):
        form = SetPwdForm(request.form)
        if form.validate():
            raw_password = form.raw_password.data
            password = form.password.data
            error = None
            message = None
            if not g.cms_user.check_password(raw_password):
                error = "原密码错误"
            elif raw_password == password:
                error = "不能使用原密码作为新密码"
            else:
                g.cms_user.password = password
                db.session.commit()
                message = "修改成功"

            return self.get(error=error, message=message)
        else:
            return self.get(error=form.errors)

class LoginView(views.MethodView):
    def get(self, error=None):
        return render_template("cms/login.html", error=error)

    def post(self):
        form = LoginForm(request.form)
        if form.validate():
            email = form.email.data
            password = form.password.data
            remember = form.remember.data
            user = CMSUser.query.filter_by(email=email).first()
            if user and user.check_password(password):
                session[config.CMS_USER_ID] = user.id
                if remember:
                    session.permanent = True

                return redirect(url_for("cms.home"))
            else:
                return self.get(error="邮箱或密码错误")
        else:
            error = form.errors.get("password")[0]
            return self.get(error=error)

bp.add_url_rule("/login/", view_func=LoginView.as_view("login"))
bp.add_url_rule("/setpwd/", view_func=SetPwdView.as_view("setpwd"))
bp.add_url_rule("/setemail/", view_func=SetEmailView.as_view("setemail"))