# -*- coding: utf-8 -*- 
<%inherit file="mainlayout.mako"/>

<h2>Edit task</h2>
			
<form action="${request.route_url('update',id=task_id)}" method="post">
  <textarea  cols="100" rows="4" maxlength="200" name="task_content"  >${task_content}</textarea>
  
  <input type="submit" name="button" value="Update" class="button">
  <input type="submit" name="button" value="Cancel" class="button">
</form>


 