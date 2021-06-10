var $messages = $('.messages-content'),
    d, h, m,
    i = 0;

$(window).load(function() {
    $messages.mCustomScrollbar();
    setTimeout(function() {
        fakeMessage();
    }, 100);
});

function updateScrollbar() {
    $messages.mCustomScrollbar("update").mCustomScrollbar('scrollTo', 'bottom', {
        scrollInertia: 10,
        timeout: 0
    });
}

function setDate() {
    d = new Date()
    if (m != d.getMinutes()) {
        m = d.getMinutes();
        $('<div class="timestamp">' + d.getHours() + ':' + m + '</div>').appendTo($('.message:last'));
    }
}

function insertMessage() {
    //获取message的值
    msg = $('.message-input').val();
    if ($.trim(msg) == '') {
        return false;
    }
    //将message传到后台
    $.ajax({
        url: "/send_message",
        type: "GET",
        data: {
            message: msg
        },
        success: function(data) {
            // alert(data)
            console.log("传到前端的数据的类型：" + typeof(data.message));
            $('<div class="message message-personal">' + data + '</div>').appendTo($('.mCSB_container')).addClass('new');
            console.log("传到前端的数据：" + data);
            console.log("传到前端的数据的类型：");
            //将后端数据显示在前端
            $.getJSON("/change_to_json", function(data) {
                //$("#recv_content").val(data.message) 

                //setDate();
                // setTimeout(function() {
                //     fakeMessage();
                // }, 1000 + (Math.random() * 20) * 100);
                $('<div class="message loading new">' + data + '<figure class="avatar"><img src="../static/image/chatbot.png" /></figure><span></span></div>').appendTo($('.mCSB_container'));
                console.log("传到前端的数据：" + data);
                //$('.message-input').val(null);
                updateScrollbar();

            })
        },
        error: function() {
            alert("接收失败")
        }
    })


}
//点击发送
$('.message-submit').click(function() {
    insertMessage();

});

$(window).on('keydown', function(e) {
    if (e.which == 13) {
        insertMessage();
        return false;
    }
})

var Fake = [
    'Hi Welcome back to our Chatbot, we are ',
]

function fakeMessage() {
    if ($('.message-input').val() != '') {
        return false;
    }
    $('<div class="message loading new"><figure class="avatar"><img src="../static/image/chatbot.png" /></figure><span></span></div>').appendTo($('.mCSB_container'));
    updateScrollbar();

    setTimeout(function() {
        $('.message.loading').remove();
        $('<div class="message new"><figure class="avatar"><img src="../static/image/chatbot.png" /></figure>' + Fake[i] + '</div>').appendTo($('.mCSB_container')).addClass('new');
        setDate();
        updateScrollbar();
        i++;
    }, 1000 + (Math.random() * 20) * 100);

}