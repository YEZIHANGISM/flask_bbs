$(function () {
    $('#gcaptcha').click(function (event) {
        var self = $(this);
        var src = self.attr('src');
        var newsrc = param.setParam(src, 'n', Math.random());
        self.attr('src', newsrc);
    });
});

$(function () {
    $("#signup").click(function (event) {
        event.preventDefault();
        var csrftoken = $('input[name="csrf_token"]').val();

        var telephone_input = $("#telephone");
        var captcha_input = $("#captcha");
        var username_input = $("#username");
        var password_input = $("#password");
        var repeatpwd_input = $("#repeat_password");
        var graph_captcha_input = $("#graph_captcha");

        var telephone = telephone_input.val();
        var captcha = captcha_input.val();
        var username = username_input.val();
        var password = password_input.val();
        var repeat = repeatpwd_input.val();
        var graph_captcha = graph_captcha_input.val();

        console.log(password);
        console.log(repeat);

        $.ajax({
            'url': '/signup/',
            'type': 'post',
            'data': {
                'telephone': telephone,
                'captcha': captcha,
                'username': username,
                'password': password,
                'repeat_password': repeat,
                'graph_captcha': graph_captcha,
                'csrf_token': csrftoken
            },
            'success': function (data) {
                if (data["code"] == 200) {
                    var next = $("#next").text()
                    if (next) {
                        alert("注册成功");
                        window.location = next
                    } else {
                        alert("注册成功");
                        window.location = "/"
                    }
                } else {
                    alert(data["message"]);
                }
            },
            'fail': function (error) {
                alert("出错了");
            }
        })
    })
})