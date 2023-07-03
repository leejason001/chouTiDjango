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
        var imageElement = $(this)
        imageElement.attr("src",imageElement.attr("src")+"?")
    })
})