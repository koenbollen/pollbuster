<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Strict//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-strict.dtd">
<html xmlns="http://www.w3.org/1999/xhtml">
    <head>
        <title>Pollbuster - 305 Use Proxy</title>
        <link rel="stylesheet" type="text/css" media="screen" href="stylesheets/pollbuster.css" />
        <script language="JavaScript" src="http://code.jquery.com/jquery-1.4.2.min.js"></script>
	<script language="JavaScript">

$(document).ready(function() {
	if( document.cookie.indexOf( "nsfw" ) != -1 )
	{
		$("#nsfw").hide();
	}
	$("#nsfw").click(function(e) {
  		$("#nsfw").fadeOut( "slow" );
		document.cookie = "nsfw=1";
	});
});

	</script>
    </head>
    <body>
	<div id="nsfw"><h1>NSFW</h1></div>
	
	<h1>Pollbuster</h1>
	
	<div id="content">{content}</div>
	
    </body>
</html>
