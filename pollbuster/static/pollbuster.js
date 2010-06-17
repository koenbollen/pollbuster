
function showerror( msg )
{
	$("#error").html( "Error, "+msg ).show("pulsate").delay(5000).fadeOut(1000);
}

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
		var result = $("#result")
		result.hide();
		$.post( "poll.extract", form.serialize(), function(json){
			if( json.status != "ok" )
			{
				showerror( "failed to fetch poll: " + json.errstr );
				return;
			}
			if( json.result.type == "multiple" )
			{
				showerror( "detected multiple polls ("+json.result.count+"), not yet supported." );
				return;
			}

			html = $(json.result.html);
			$("tbody", html).hide();
			$("caption", html).click(function(){
				$("tbody", html).toggle();
			});
			$("a.submit", html).click(function(){
				val = $("input:checked", html).val();
				if( typeof val == "undefined" )
				{
					showerror( "no poll choice selected!" );
				}
				else
				{
					$.post( "poll.submit", "choice="+val, function(json){
						if( json == null || json.status != "ok" )
						{
							var errstr;
							if( json == null )
							{
								errstr = "unknown error";
							}
							else
							{
								errstr = json.errstr;
							}
							showerror( "failed to submit job: " + errstr );
							return;
						}
						result.html( "Success! [TODO: more specific message here]" );
					}, "json" );
					//...
				}
			}).button();
			result.html( html );
			result.show();

		}, "json" );
	});

});
