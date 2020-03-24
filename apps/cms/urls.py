from apps.cms import views
from .views import bp

bp.add_url_rule("/login/", view_func=views.LoginView.as_view("login"))
bp.add_url_rule("/index/", view_func=views.IndexView.as_view("index"))