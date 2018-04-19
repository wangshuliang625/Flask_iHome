function showSuccessMsg() {
    $('.popup_con').fadeIn('fast', function() {
        setTimeout(function(){
            $('.popup_con').fadeOut('fast',function(){}); 
        },1000) 
    });
}

function getCookie(name) {
    var r = document.cookie.match("\\b" + name + "=([^;]*)\\b");
    return r ? r[1] : undefined;
}

$(document).ready(function () {
    // TODO: 在页面加载完毕向后端查询用户的信息
    $.get('/api/v1.0/user', function (resp) {
        if (resp.errno == '0') {
            // 获取个人信息成功
            // 设置用户的个人头像
            $('#user-avatar').attr('src', resp.data.avatar_url);

            // 设置用户的个人的用户名
            $('#user-name').val(resp.data.username);
        }
        else {
            // 失败
            alert(resp.errmsg);
        }
    })

    // TODO: 管理上传用户头像表单的行为
    $('#form-avatar').submit(function (e) {
        // 阻止表单默认提交行为
        e.preventDefault();

        // 请求上传用户的头像
        // 模拟表单的提交操作
        $(this).ajaxSubmit({
            'url': '/api/v1.0/user/avatar',
            'type': 'post',
            'headers': {
                'X-CSRFToken': getCookie('csrf_token')
            },
            'success': function (resp) {
                if (resp.errno == '0') {
                    // 上传头像成功
                    // 设置用户的头像的img标签的src属性
                    $('#user-avatar').attr('src', resp.data.avatar_url);
                }
                else {
                    // 上传头像失败
                    alert(resp.errmsg);
                }
            }
        })
    })

    // TODO: 管理用户名修改的逻辑

})

