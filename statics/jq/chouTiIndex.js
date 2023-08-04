function getValidatorCodeCountdown(currentHtmlElement) {
    currentHtmlElement.text("60s");
    var countdownTimer = setInterval(function () {
        var timeReg = new RegExp(/[0-9]+/)
        var currentTime = parseInt(currentHtmlElement.text().match(timeReg));
        currentTime -= 1;
        if (0 == currentTime) {
            currentHtmlElement.text("获取验证码");
            clearInterval(countdownTimer);
        } else {
            currentHtmlElement.text(currentTime + 's');
        }
    }, 1000);
}

function createCommentDomTree(ret, parentNode) {
    if (ret.length > 0) {
        $.each(ret, function (index, comment) {
            var node = $("<div></div>")
            node.append($("<span>"+comment["content"]+"</span>"))
            parentNode.append(node)
            createCommentDomTree(comment["children"], node)
        })
    }
}

$(document).ready(function () {
    var csrftoken = $.cookie('csrftoken');
    function csrfSafeMethod(method) {
        // these HTTP methods do not require CSRF protection
        return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
    }
    $.ajaxSetup({
        beforeSend: function(xhr, settings) {
            if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
                xhr.setRequestHeader("X-CSRFToken", csrftoken);
            }
        }
    });

    $(".tabContentItemPage").width($(".chouTiContent-middlePart").width() -$(".tabContentItem img").width())
    $(".chouTiContentHead-middlePart li").click(function () {
        me = $(this)
        $(".chouTiContent-middlePart .tabContent").each(function (index, currentDom) {
            if (!$(currentDom).hasClass("hideTabContent")) {
                $(currentDom).addClass("hideTabContent")
            }
            if ($(currentDom).hasClass(me.attr("id"))) {
                $(currentDom).removeClass("hideTabContent")
            }
        })

    })
    $(".register_title .closeButton").click(function () {
        $(this).parents(".maskBackground").addClass("css_hide")
    })
    $(".identityContainer").click(function () {
        $(".register_title .closeButton").parents(".maskBackground").removeClass("css_hide")
    })

    $(".login_content img.showValidate").click(function(){
        var imageElement = $(this);
        imageElement.attr("src",imageElement.attr("src")+"?")
    })

    $("#getValidateCode").click(function(){
        var me =$(this);
        if(/[0-9]/g.test(me.text()) == true) {
            alert("倒计时还未结束");
            return;
        }
        if(/^[a-zA-Z0-9_-]+@([a-zA-Z0-9_-]+)(\.[a-zA-Z0-9_-]+)+/g.test(me.prev(".validateEmail").val()) == false) {
            alert("邮箱格式错误");
        } else {
            $.ajax({
                url:"submitValidateEmail",
                type: "post",
                data: {"validateEmail": me.prev(".validateEmail").val()},
                dataType: "JSON",
                success:function (data, textStatus, xhr) {
                    if(false == data.status) {
                        $("#getValidateCode").siblings(".validateEmailError").text(data.summary)
                    }
                }
            })
            getValidatorCodeCountdown(me);
        }
    })

    $(".operateImageCommon.liked").click(function () {
        var likedElement = $(this)
        $.ajax({
            url: /newLikedClick/,
            type: "post",
            data: {"new_id": likedElement.parents(".newItem").attr("new_id")},
            success:function (data) {
                if(data != 0) {
                    likedElement.siblings(".likedTxt").text(data)
                }
                else {
                    likedElement.siblings(".likedTxt").text("")
                }
            }
        })
    })

    $(".operateImageCommon.comments").click(function () {
        var commentImage = $(this)
        $.ajax({
            url:"/getComments/",
            type:"GET",
            data:{"new_id":commentImage.parents(".newItem").attr("new_id")},
            dataType:"JSON",
            success:function (arg) {
                var commentArea = $(document.createElement("div"))
                commentArea.append($("<div><textarea></textarea><button>评论</button></div>"))
                commentImage.parents(".operateBox").append(commentArea)
                createCommentDomTree(arg, commentArea)
            }
        })
    })

})