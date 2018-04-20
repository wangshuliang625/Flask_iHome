function getCookie(name) {
    var r = document.cookie.match("\\b" + name + "=([^;]*)\\b");
    return r ? r[1] : undefined;
}

$(document).ready(function(){
    // $('.popup_con').fadeIn('fast');
    // $('.popup_con').fadeOut('fast');

    // TODO: 在页面加载完毕之后获取区域信息
    $.get("/api/v1.0/areas", function (resp) {
        if (resp.errno == "0") {
            // 加载城区信息成功
            // 遍历设置所有城区的信息
            var areas = resp.data;

            for (var i=0; i<areas.length; i++) {
                var area = areas[i];
                $("#area-id").append('<option value="' + area.aid + '">' + area.aname + '</option>')
            }
        }
        else {
            // 出错
            alert(resp.errmsg);
        }
    })

    // TODO: 处理房屋基本信息提交的表单数据

    // TODO: 处理图片表单的数据

})