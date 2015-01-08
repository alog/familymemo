# -*- coding: utf-8 -*- 
<%inherit file="layout.mako"/>

<h2>Add a new task</h2>


<form action="${request.route_url('new')}" method="post">
  <input type="text" maxlength="100" name="content">
  <input type="submit" name="button" value="ADD" class="button">
  <input type="submit" name="button" value="Cancel" class="button">
</form>