function getCookie(name) {
    var r = document.cookie.match("\\b" + name + "=([^;]*)\\b");
    return r ? r[1] : undefined;
}

// TODO: 点击推出按钮时执行的函数
function logout() {
    
}

$(document).ready(function(){

    // TODO: 在页面加载完毕之后去加载个人信息
    $.get('/api/v1.0/user', function (resp) {
        if (resp.errno == '0') {
            // 获取信息成功
            // 设置用户的头像地址，用户名和手机号
            $('#user-avatar').attr('src', resp.data.avatar_url);
            $('#user-name').html(resp.data.username);
            $('#user-mobile').html(resp.data.mobile);
        }
        else {
            // 获取信息失败
            alert(resp.errmsg);
        }
    })

});
