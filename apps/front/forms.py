from wtforms import Form
from wtforms import StringField
from wtforms.validators import Regexp, Length, EqualTo, ValidationError
from utils import cache

class SignupForm(Form):
    telephone = StringField(validators=[Regexp(r'1[3578]\d{9}', message="手机号码格式不正确")])
    captcha = StringField(validators=[Regexp(r"\d{4}", message="验证码错误")])
    username = StringField(validators=[Regexp(r"^[a-zA-Z][a-zA-Z0-9]{4,21}$", message="用户名不规范。")])
    password = StringField(validators=[Length(6,12, message="密码格式不正确")])
    repeat_password = StringField(validators=[EqualTo("password", message="两次输入的密码不一致")])
    graph_captcha = StringField(validators=[Regexp(r"\w{4}", message="图形验证码错误")])

    def validate_captcha(self, field):
        captcha = field.data
        telephone = self.telephone
        # captcha_cache = cache.get(telephone)
        captcha_cache = "1234"
        print(captcha_cache)
        if not captcha_cache or captcha_cache != captcha:
            raise ValidationError(message="手机验证码错误")

    def validate_graph_captcha(self, field):
        graph_captcha = field.data
        graph_captcha_cache = cache.get(graph_captcha.lower())

        if not graph_captcha_cache:
            raise ValidationError(message="图形验证码错误")