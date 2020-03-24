from flask import (
    Blueprint,
    views,
    render_template,
    make_response,
)
from io import BytesIO
from utils.captcha import Captcha

bp = Blueprint("front", __name__)

@bp.route("/")
def index():
    return "front index"

@bp.route("/captcha/", endpoint="graph_captcha")
def graph_captcha():
    text, image = Captcha.gene_graph_captcha()
    out = BytesIO()
    image.save(out, 'png')
    out.seek(0)
    response = make_response(out.read())
    response.content_type = "image/png"
    return response

class SignupView(views.MethodView):
    """注册"""

    def get(self):
        return render_template("front/front_signup.html")

    def post(self):
        pass

bp.add_url_rule("/signup/", view_func=SignupView.as_view("signup"))