
$(document).ready(function() {

	if( document.cookie.indexOf( "nsfw" ) != -1 )
	{
		$("#nsfw").hide();
	}
	else
	{
		$("#nsfw").click(function(e) {
			$("#nsfw").fadeOut( "slow" );
			document.cookie = "nsfw=1";
		});
	}

	$("#selector a").click(function(e){
		var form = $("#selector form");
		var error = $("#selector .error")
		error.hide();
		$.post( "poll.extract", form.serialize(), function(json){
			if( json.status != "ok" )
			{
				error.html( "Failed to fetch: " + json.errstr ).show();
				return;
			}
			error.hide();
			alert( json.data );
		}, "json");
	});

});
