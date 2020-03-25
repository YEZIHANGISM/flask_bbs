from flask import (
    Blueprint,
    views,
    render_template,
    make_response,
    request,
    redirect,
    url_for
)
from io import BytesIO
from utils.captcha import Captcha
from exts import db
from .forms import SignupForm
from utils import restful, safe_url
from .models import FrontUser
from utils import cache

bp = Blueprint("front", __name__)

@bp.route("/")
def index():
    return render_template("front/front_base.html")

@bp.route("/captcha/", endpoint="graph_captcha")
def graph_captcha():
    text, image = Captcha.gene_graph_captcha()
    cache.set(text.lower(), text.lower())
    out = BytesIO()
    image.save(out, 'png')
    out.seek(0)
    response = make_response(out.read())
    response.content_type = "image/png"
    return response

class SignupView(views.MethodView):
    """注册"""

    def get(self):
        # 获取该次请求的上一个url，用于注册完成后返回上一个访问的页面
        next = request.referrer
        if next and next != request.url and safe_url(next):
            return render_template("front/front_signup.html", next=next)
        else:
            return render_template("front/front_signup.html")

    def post(self):
        form = SignupForm(request.form)
        if form.validate():
            telephone = form.telephone.data
            username = form.username.data
            password = form.password.data
            user = FrontUser(telephone=telephone, username=username, password=password)
            db.session.add(user)
            db.session.commit()
            return restful.success()
        else:
            error = form.errors.popitem()[1][0]
            print(error)
            return restful.param_error(message=error)

bp.add_url_rule("/signup/", view_func=SignupView.as_view("signup"))