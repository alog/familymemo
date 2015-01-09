# -*- coding: utf-8 -*- 
<%inherit file="mainlayout.mako"/>

<h3>Please login</h3>
			
<form action="${url}" method="post">
  
  <input type="hidden" name="came_from" value="${came_from}"/>
  <b>Login</b> 
  <input type="text" name="login" value="${login}"/><br/><br/>
  <b>Password</b> 
  <input type="password" name="password" value="${password}"/><br/><br/>
  <input type="submit" name="button" value="Log In" class="button">
  <input type="submit" name="button" value="Cancel" class="button">
</form>
 
  