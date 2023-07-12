

$(document).ready(function () {
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
        me.text("60s");
        var countdownTimer = setInterval(function () {
            var timeReg = new RegExp(/[0-9]+/)
            var currentTime = parseInt(me.text().match(timeReg));
            currentTime -= 1;
            if (0 == currentTime) {
                me.text("获取验证码");
                clearInterval(countdownTimer);
            } else {
                me.text(currentTime + 's');
            }
        }, 1000);
    })

})