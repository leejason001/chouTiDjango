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
function createCommentTreeNodeContent(content) {
    return $("<span>"+content+"</span><span class='commentReply'>回复</span>")
}

function createCommentDomTree(ret, parentNode) {
    if (ret.length > 0) {
        $.each(ret, function (index, comment) {
            var node = $("<div class='commentNode' comment_id="+comment["id"]+"></div>")
            node.append(createCommentTreeNodeContent(comment["content"]))
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

    $(".chouTiContentHead .publish").click(function () {
        console.log("cccccccccc")
    })

    $("#imageInput").on("change", function (e) {
        $(this).parent("form").submit()
    })
    $("#imageInput").siblings("iframe").on("load", function () {
        iframe = $(this)
        console.log(JSON.parse(iframe.contents().find("body").text())["imagePath"])
        var imagePath = JSON.parse(iframe.contents().find("body").text())["imagePath"]
        var image = document.createElement("img")
        image.src = imagePath
        iframe.after($(image))
        $("#upload_aNewToDataBase").children("input[name=portraitPath]").val(imagePath)
    })

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

    $(".operateBox").on("click", ".commentReply", function () {
        var me = $(this)
        if (me.siblings(".replyCommentArea").length > 0) {
            me.siblings(".replyCommentArea").remove()
        } else if(0 == me.siblings(".replyCommentArea").length) {
            me.after("<div class='replyCommentArea'><textarea class='replyCommentInput'></textarea><button class='submitReply'>回复</button></div>")
            me.siblings(".replyCommentArea").children(".submitReply").on("click", function () {
                replyCommentInput = $(this).siblings("textarea.replyCommentInput")
                if (replyCommentInput.val()!="") {
                    $.ajax({
                        url:"/submitCommentReply/",
                        type:"POST",
                        data:{"content": replyCommentInput.val(), "new_id":replyCommentInput.parents(".newItem").attr("new_id"), "parentComment_id": replyCommentInput.parents(".commentNode").attr("comment_id")},
                        success: function(arg){
                            if (arg != "failed") {
                                var commentNode = $("<div class='commentNode' comment_id="+arg+"></div>")
                                commentNode.append(createCommentTreeNodeContent(replyCommentInput.val()))
                                fatherAppend_commentNode = replyCommentInput.parent()
                                while(!fatherAppend_commentNode.hasClass("commentNode")) {
                                    fatherAppend_commentNode = fatherAppend_commentNode.parent()
                                }
                                fatherAppend_commentNode.append(commentNode)
                                replyCommentInput.parents(".replyCommentArea").remove()
                            }
                        }
                    })
                }
            })
        }
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
        var commentArea  = commentImage.parent().siblings(".commentArea")
        if (commentArea.length > 0) {
            commentArea.remove()
        } else if(0 == commentArea.length) {
            var new_id = commentImage.parents(".newItem").attr("new_id")
            $.ajax({
                url:"/getComments/",
                type:"GET",
                data:{"new_id":new_id},
                dataType:"JSON",
                success:function (arg) {
                    var commentArea = $(document.createElement("div"))
                    commentArea.addClass("commentArea")
                    commentImage.parents(".operateBox").append(commentArea)
                    createCommentDomTree(arg, commentArea)

                    commentArea.append($("<div class='itemCommentArea'><textarea class='itemCommentInput'></textarea><button class='submitComment'>评论</button></div>"))

                    var itemCommentInput = $("textarea.itemCommentInput")
                    itemCommentInput.siblings(".submitComment").on("click", function () {
                        $.ajax({
                            url: "/submitNewComment/",
                            type: "POST",
                            data:{"new_id":new_id, "commentContent": itemCommentInput.val()},
                            success:function (arg) {
                                if (arg != "failed") {
                                    var commentNode = $("<div class='commentNode' comment_id="+arg+"></div>")
                                    commentNode.append(createCommentTreeNodeContent(itemCommentInput.val()))
                                    commentArea.children(".itemCommentArea").before(commentNode)

                                    itemCommentInput.val("")
                                } else {
                                    alert("新增评论失败")
                                }
                            }
                        })
                    })
                }
            })
        }
    })

})