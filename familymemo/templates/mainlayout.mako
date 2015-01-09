<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<title>FamilyMemo</title>
<link rel="stylesheet" href="/static/style.css">
<link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/3.3.1/css/bootstrap.min.css">
<link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/3.3.1/css/bootstrap-theme.min.css">

<script src="https://ajax.googleapis.com/ajax/libs/jquery/1.11.1/jquery.min.js"></script>
<script src="https://maxcdn.bootstrapcdn.com/bootstrap/3.3.1/js/bootstrap.min.js"></script>
<style type="text/css">
    body{
    	padding-top: 70px;
    }
</style>
</head>
<body>
<nav id="myNavbar" class="navbar navbar-default navbar-inverse navbar-fixed-top" role="navigation">
	<!-- Brand and toggle get grouped for better mobile display -->
	<div class="container">
		
		<!-- Collect the nav links, forms, and other content for toggling -->
		<div class="collapse navbar-collapse" id="navbarCollapse">
			<ul class="nav navbar-nav">
				<li class="active"> <a href="${request.route_url('list')}">Home</a></li>
				<li><a href="${request.route_url('list')}" target="_blank">About</a></li>
				<li><a href="${request.route_url('list')}" target="_blank">Contact</a></li>
                <li display=none> Not shown </li>
                <li>
                    % if logged_in :
                        <a   href="${request.application_url}/logout">[ ${logged_in}, Logout ]</a>
                    % else:
                        <a   href="${request.application_url}/login">[ Login ]</a>
                    % endif	
                    </li>
			</ul>
		</div>
	</div>
</nav>
<div class="container">
 
	<div class="row">
		<div class="col-sm-8">
            ${next.body()}
        </div>
		 
	</div>
    <hr>
	<div class="row">
		<div class="col-xs-4">
			<p><a href="${request.route_url('backup')}"  class="btn btn-success">Backup</a></p>
            <p>Backup your current memo to a file.</p>
		</div>
		<div class="col-xs-4">
			<p><a href="${request.route_url('restore')}"   class="btn btn-success">Restore</a></p>
			<p>Restore your memo from backup file.</p>
		</div>
 
	</div>
	<hr>
	<div class="row">
		<div class="col-xs-12">
			<footer>
				<p> 
                  % if request.session.peek_flash():
                  <div id="flash">
                    <% flash = request.session.pop_flash() %>
                    % for message in flash:
                    ${message}<br>
                    % endfor
                  </div>
                  % endif
                
                </p>
			</footer>
		</div>
	</div>
</div>
</body>
</html> 