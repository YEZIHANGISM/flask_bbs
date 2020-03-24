$(function () {
    $('#gcaptcha').click(function (event) {
        var self = $(this);
        var src = self.attr('src');
        var newsrc = param.setParam(src, 'n', Math.random());
        self.attr('src', newsrc);
    });
});