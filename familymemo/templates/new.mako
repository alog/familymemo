# -*- coding: utf-8 -*- 
<%inherit file="mainlayout.mako"/>

<h2>Add a new task</h2>


<form action="${request.route_url('new')}" method="post">
  
  <textarea  cols="100" rows="4" maxlength="200" name="content" > </textarea>
  
  <input type="submit" name="button" value="ADD" class="button">
  <input type="submit" name="button" value="Cancel" class="button">
</form>