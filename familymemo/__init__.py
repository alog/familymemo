# -*- coding: utf-8 -*- 
from pyramid.config import Configurator
from sqlalchemy import engine_from_config
from pyramid.session import UnencryptedCookieSessionFactoryConfig
from pyramid.authentication import AuthTktAuthenticationPolicy
from pyramid.authorization import ACLAuthorizationPolicy
from familymemo.security import groupfinder     # import the groupfinder function

#从models.py文件中引入
from .models import (   
    DBSession,
    Base,
    )


def main(global_config, **settings):
    """ This function returns a Pyramid WSGI application.
    """
    print("__init__.py is executed...")
    
    engine = engine_from_config(settings, 'sqlalchemy.')   #ini文件里指定了数据库文件位置
    DBSession.configure(bind=engine)
    Base.metadata.bind = engine
    # session factory
    session_factory = UnencryptedCookieSessionFactoryConfig('itsaseekreet')
    authn_policy = AuthTktAuthenticationPolicy('sosecret', callback=groupfinder, hashalg='sha512')
    authz_policy = ACLAuthorizationPolicy()

    config = Configurator(settings=settings,
                          root_factory='familymemo.models.RootFactory',
                          session_factory=session_factory)
    # ini文件里的各项参数设定以字典值的形式传入 config
    # 如果需要在View里访问Configurator, 则访问request.registry.settings即可
    
    config.set_authentication_policy(authn_policy)
    config.set_authorization_policy(authz_policy)

    config.include('pyramid_chameleon')
    config.include('pyramid_mako')  # 加入对mako支持
    config.add_static_view('static', 'static', cache_max_age=3600)
    config.add_route('list', '/')
    config.add_route('new', '/new')
    config.add_route('close', '/close/{id}')
    config.add_route('update', '/update/{id}')
    config.add_route('login', '/login')
    config.add_route('logout', '/logout')
    config.add_route('backup', '/backup')
    config.add_route('restore', '/restore')
    config.scan()
    return config.make_wsgi_app()
