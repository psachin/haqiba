$('#suggestion').keyup(function(){
    var query;
    query = $(this).val();
    $.get('/emacshaqiba/suggest_code/', {suggestion: query}, function(data){
	$('#cats').html(data);
    });
});

