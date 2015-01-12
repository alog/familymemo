# -*- coding: utf-8 -*- 
from pyramid.response import (Response , FileResponse)
from pyramid.view import view_config
from pyramid.httpexceptions import HTTPFound
from sqlalchemy.exc import DBAPIError
import datetime
import os
from tempfile import NamedTemporaryFile

from .models import (
    DBSession,
    Task,
    )

from pyramid.view import (
    view_config,
    forbidden_view_config,
    )

from pyramid.security import (
    remember,
    forget,
    )

from .security import USERS


'''
暂时保留
@view_config(route_name='home', renderer='templates/mytemplate.pt')
def my_view(request):
    try:
        one = DBSession.query(Task).filter(Task.name == 'one').first()
    except DBAPIError:
        return Response(conn_err_msg, content_type='text/plain', status_int=500)
    return {'one': one, 'project': 'familymemo'}
'''

# views
@view_config(route_name='list', renderer='list.mako', permission='view')
def list_view(request):
    #return Response('Hello')  #保留此语句，用于测试--直接返回简单语句
       
    #rs = request.db.execute("select id, content from tasks where status = 0")
    #rs = DBSession.query(Task.id, Task.content).filter(Task.status==0).all()
        #返回的result是tuple, 将其转换成dictionary，这个dictionary会被传入list.mako模板
    rs=Task.all_active_task();    
    tasks=[dict(id=task.id,content=task.brief_content()) for task in rs]
    return dict(tasks=tasks, logged_in = request.authenticated_userid )

@view_config(route_name='new', renderer='new.mako', permission='edit')
def new_view(request):
    #return Response('Update view is called')
    if (request.POST.get('button') == 'Cancel'):
        return HTTPFound(location=request.route_url('list'))

    if (request.POST.get('button') == 'ADD'):
        if request.POST.get('content'):
            '''
            request.db.execute(
                'insert into tasks (content, status) values (?, ?)',
                [request.POST['content'], 0])
            #避免SQL注入漏洞，注意要使用问号生成SQL声明语句
            '''
            new_task = Task(content=request.POST['content'], owner=request.authenticated_userid,status=0)
            DBSession.add(new_task)
            
            request.session.flash('New task was successfully added!')
            return HTTPFound(location=request.route_url('list'))
        else:
            #如果输入的内容为空，则显示提示，要求再次输入，
            request.session.flash('Please enter the content for the task!')
    return dict(logged_in = request.authenticated_userid )
    
@view_config(route_name='update', renderer='update.mako', permission='edit')
def update_view(request):
    #用户update一个任务，
    task_id = int(request.matchdict['id'])
    current_task=DBSession.query(Task).filter(Task.id==task_id).one()				   
    if request.method == 'POST':
        if (request.POST.get('button') == 'Update'):
            # Updaed button is clicked.  Save the content.
            current_task.content=request.POST.get('task_content')
            request.session.flash('New task was successfully updated!')
        return HTTPFound(location=request.route_url('list'))
    else:
		# request.matchdict['id'] it's string 
		#必须提供一个dict 给mako template！！！
        return dict( task_id = request.matchdict['id'],
                     task_content=current_task.content,
                     logged_in = request.authenticated_userid )


@view_config(route_name='close', permission='edit')
def close_view(request):
    #
    #用户关闭一个任务，显示一个成功信息，然后重定向回到list_view页面
    task_id = int(request.matchdict['id'])
    '''request.db.execute("update tasks set status = ? where id = ?",
                       (1, task_id))
    request.db.commit()
    '''
    current_task=DBSession.query(Task).filter(Task.id==task_id).one()
    current_task.status=1
    request.session.flash('Task was successfully closed!')
    return HTTPFound(location=request.route_url('list') )

@view_config(route_name='login', renderer='login.mako')
@forbidden_view_config(renderer='login.mako')
def login(request):
    login_url = request.route_url('login')
    referrer = request.url
    if referrer == login_url:
        referrer = '/' # never use the login form itself as came_from
    came_from = request.params.get('came_from', referrer)
    message = 'Please login in, or press Cancel to return.'
    login = ''
    password = ''
    if 'button' in request.params:
        if ( request.POST.get('button') == "Log In"):
            login = request.params['login']
            password = request.params['password']
            # no user database function yet, just pass it.
            if USERS.get(login) == 'admin':
                #登录成功
                headers = remember(request, login)
                return HTTPFound(location = came_from, headers = headers)
            else:
                message = 'Failed login, please try again or press Cancel to return.'
                
        else:
            #取消登录
            return HTTPFound(location=request.route_url('list'))
    request.session.flash(message)
    return dict(
        message = message,
        url = request.application_url + '/login',
        came_from = came_from,
        login = login,
        password = password,
        )

@view_config(route_name='logout')
def logout(request):
    headers = forget(request)
    return HTTPFound(location = request.route_url('list'),
                     headers = headers)

@view_config(route_name='backup',permission='edit')
def backup(request):

    # 理想的做法是 在内存中生成内容，直接提供下载，避免生成中间文件
    # 尝试使用StringIO 可是不成功
    # 这里使用NamedTemporaryFile()生成的中间文件， 事后自动删除。
    #  
    #  
    rs=Task.all()  
    name_suggested='task_'+datetime.datetime.now().strftime("%b%d%H%M")+'.json'
    tf = NamedTemporaryFile(prefix='abc'  , suffix='.gb', delete=True)
    print(os.path.abspath(tf.name))
    print('--------------------------')
    for task in rs:
            line=str(task.row2dict()) + '\n'
            tf.write( bytes( line, 'UTF-8'))
    tf.seek(0)
    response = Response(content_type='text/plain')
    response.app_iter = tf
    response.headers['Content-Disposition'] = ("attachment; filename=%s" %name_suggested)
    return response   
    
@view_config(route_name='restore',permission='edit'  )
def restore(request):
    rs=Task.all()  
    name_suggested='task_'+datetime.datetime.now().strftime("%b%d%H%M")+'.json'
    tf = NamedTemporaryFile(prefix='abc'  , suffix='.gb', delete=True)
    print(os.path.abspath(tf.name))
    print('--------------------------')
    for task in rs:
            line=str(task.row2dict()) + '\n'
            tf.write( bytes( line, 'UTF-8'))
    tf.seek(0)
    response = Response(content_type='text/plain')
    response.app_iter = tf
    response.headers['Content-Disposition'] = ("attachment; filename=%s" %name_suggested)
    return response
'''                     
@view_config(route_name='restore',permission='edit')
def restore(request):
    request.session.flash('restore executed') 
    return HTTPFound(location = request.route_url('list'))
'''



conn_err_msg = """\
Pyramid is having a problem using your SQL database.  The problem
might be caused by one of the following things:

1.  You may need to run the "initialize_familymemo_db" script
    to initialize your database tables.  Check your virtual
    environment's "bin" directory for this script and try to run it.

2.  Your database server may not be running.  Check that the
    database server referred to by the "sqlalchemy.url" setting in
    your "development.ini" file is running.

After you fix the problem, please restart the Pyramid application to
try it again.
"""
