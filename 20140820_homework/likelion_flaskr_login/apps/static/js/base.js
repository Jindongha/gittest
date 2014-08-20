$(document).ready(function () {
	$('.llFlaskrArticleForm #content').summernote();

    $('.llFlaskrArticleForm').submit(function () {
        setTimeout(function () {
            $('#content').val($('.llFlaskrArticleForm #content').code());
        }, 50);
    });
});

$('.llArticleDetail').on( "click", ".panel-body .btn-warning", function () {
        var cur_item = $(this);
        $.ajax({
            url: "/article/detail_like",
            dataType:'JSON',
            data: {
                id : cur_item.children().last().val()
            },
            success: function() {
                var cur_value = cur_item.children().last().prev().text();
                cur_item.children().last().prev().text(parseInt(cur_value) + 1);
            },
            error: function(request,status,error){
                alert("code:"+request.status+"\n"+"error:"+error);
            }
        });
    });
$('.llCommentList').on( "click", ".well-sm .btn-warning", function () {
        var cur_item = $(this);
        $.ajax({
            url: "/article/comment_like",

            dataType:'JSON',
            data: {
                id : cur_item.children().last().val()
            },
            success: function() {
                var cur_value = cur_item.children().last().prev().text();
                cur_item.children().last().prev().text(parseInt(cur_value) + 1);
            },
            error: function(request,status,error){
                alert("code:"+request.status+"\n"+"error:"+error);
            }
        });
    });

$('.llArticleList').on( "click", ".well .btn-warning", function () {
        var cur_item = $(this);
        $.ajax({
            url: "/article/detail_like",

            dataType:'JSON',
            data: {
                id : cur_item.children().last().val()
            },
            success: function() {
                var cur_value = cur_item.children().last().prev().text();
                cur_item.children().last().prev().text(parseInt(cur_value) + 1);
            },
            error: function(request,status,error){
                alert("code:"+request.status+"\n"+"error:"+error);
            }
        });
    });