<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Strict//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-strict.dtd">
<html xmlns="http://www.w3.org/1999/xhtml">
	<head>
		<title>Pollbuster - 305 Use Proxy</title>
		<link rel="stylesheet" type="text/css" media="screen" href="static/custom-theme/jquery-ui-1.8.2.custom.css" />
		<link rel="stylesheet" type="text/css" media="screen" href="static/pollbuster.css" />
		<script language="JavaScript" src="http://ajax.googleapis.com/ajax/libs/jquery/1.4.2/jquery.min.js"></script>
		<script language="JavaScript" src="http://ajax.googleapis.com/ajax/libs/jqueryui/1.8.2/jquery-ui.min.js"></script>
		<script language="JavaScript" src="static/pollbuster.js"></script>
	</head>
	<body>
		<div id="trace"></div>
		<div id="error" style="display: none"></div>
		<div id="nsfw"><h1>NSFW</h1></div>

		<h1>Pollbuster</h1>

		<div id="selector">
			<form name="selector" action="#">
				<input type="text" name="url" value="" />
				<a href="#">fetch poll</a>
			</form>
		</div>

		<div id="content">
            <div id="result" style="display:none"></div>
            <div id="explain">[TODO: Explain Pollbuster here...]</div>
		</div>

	</body>
</html>
