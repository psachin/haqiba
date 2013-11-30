$('#suggestion').keyup(function(){
    var query;
    query = $(this).val();
    $.get('/emacshaqiba/suggest/', {suggestion: query}, function(data){
	$('#cats').html(data);
    });
});

