(function($){
  $(function(){

    $('.sidenav').sidenav();
    $('select').formSelect();
    $('.collapsible').collapsible();
    $('.datepicker').datepicker({format:'yyyy-mm-dd'});
	$('.tabs').tabs();

    //for the answer vote
    $(".vote").click(function(){
    	var a_tag = $(this)
    	var csrf = $("input[name='csrfmiddlewaretoken']").val();
    	var url_path = $("input[name='url_path']").val();
    	var answer_id = $(this).attr("answer-id");
    	var vote_type = $(this).attr("vote-type");

    	$.ajax({
    		url: url_path + '/vote',
    		data: {
    			'csrfmiddlewaretoken': csrf,
    			'answer_id': answer_id,
    			'vote_type': vote_type,
    		},
    		cache: false,
    		type: "post",
    		success: function(data){
    			$('.vote').removeClass('green-text');
    			$('.vote').removeClass('red-text');

    			if (vote_type == 'U'){
    				$(a_tag).addClass('green-text');
    			} else {
    				$(a_tag).addClass('red-text')
    			}
    			$('#answerVotes' + answer_id).text(data);
    		}
    	});
    	return false;
    });


  }); // end of document ready
})(jQuery); // end of jQuery name space

//Slider
const slider = document.querySelector('.slider');
M.Slider.init(slider, {
	indicators: false,
	height: 500,
	interval: 6000
});

//questionsPart
const accordion = document.getElementsByClassName('contentBx');
for(i=0; i<accordion.length; i++){
	accordion[i].addEventListener('click', function(){
		this.classList.toggle('active')
	})
}