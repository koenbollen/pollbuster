
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
			$(".pollinfo .ui-widget-content", html).hide();
			$(".pollinfo .ui-widget-header", html).click(function(){
				$(".pollinfo .ui-widget-content", html).toggle("blind");
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
						result.html( '<h1>Success!</h1> <p><object width="425" height="344"><param name="movie" value="http://www.youtube-nocookie.com/v/g4uxIo4t7xM&hl=en_US&fs=1&autoplay=1"></param><param name="allowFullScreen" value="true"></param><param name="allowscriptaccess" value="always"></param><embed src="http://www.youtube-nocookie.com/v/g4uxIo4t7xM&hl=en_US&fs=1&autoplay=1" type="application/x-shockwave-flash" allowscriptaccess="always" allowfullscreen="true" width="425" height="344"></embed></object></p>' );
					}, "json" );
					//...
				}
			}).button();
			result.html( html );
			result.show();

		}, "json" );
	}).button();

});
