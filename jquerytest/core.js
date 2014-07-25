$(document).ready(function() {	
	// 문서의 로딩이 끝나면, 이라는 뜻입니다. 잊지 않으셨죠?
    // 이곳에 코드를 작성하시면 됩니다.

    $('#shadow').mouseenter(function(){
		$(this).fadeOut('slow');
	});
	$('#car').mouseleave(function(){
		$('#shadow').fadeTo('slow',0.25);
	});
	
	


	$('#button_right').click(function(){
		$('#car').animate({right:"-=25px"},'slow');
	});
	$('#button_left').click(function(){
		$('#car').animate({right:"+=25px"},'slow');
	});
	$('#button_up').click(function(){
		$('#car').animate({bottom:"+=25px"},'slow');
	});
	$('#button_botton').click(function(){
		$('#car').animate({bottom:"-=25px"},'slow');
	});


    $(document).keydown(function(key) {
        switch(parseInt(key.which,10)) {
			// 왼쪽 방향키
			case 37:
				$('#car').animate({right: "+=25px"}, 'fast');
				break;
			// 위쪽 방향키
			case 38:
				$('#car').animate({bottom: "+=25px"}, 'fast');
				// 코드를 입력하세요.
				break;
			// 오른쪽 방향키
			case 39:
				$('#car').animate({right: "-=25px"}, 'fast');
				// 코드를 입력하세요.
				break;
			// 아래 방향키
			case 40:
				$('#car').animate({bottom: "-=25px"}, 'fast');
				// 코드를 입력하세요.
				break;
		}
	});
	
});