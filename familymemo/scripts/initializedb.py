# -*- coding: utf-8 -*- 
#
#   要初始化数据库， 删除数据库文件，
#   然后在目录C:\pyramidtut\familymemo 运行
#   %VENV%\Scripts\initialize_familymemo_db development.ini
import os
import sys
import transaction

from sqlalchemy import engine_from_config

from pyramid.paster import (
    get_appsettings,
    setup_logging,
    )

from pyramid.scripts.common import parse_vars

from ..models import (
    DBSession,
    Task,
    User,
    Base,
    )


def usage(argv):
    cmd = os.path.basename(argv[0])
    print('usage: %s <config_uri> [var=value]\n'
          '(example: "%s development.ini")' % (cmd, cmd))
    sys.exit(1)


def main(argv=sys.argv):
    if len(argv) < 2:
        usage(argv)
    config_uri = argv[1]
    options = parse_vars(argv[2:])
    setup_logging(config_uri)
    settings = get_appsettings(config_uri, options=options)
    engine = engine_from_config(settings, 'sqlalchemy.')
    DBSession.configure(bind=engine)
    Base.metadata.create_all(engine)
    with transaction.manager:
        model = User(login_name=u'demo', nickname=u'demo user',password=u'demo')
        DBSession.add(model)
        model = User(login_name=u'admin', nickname=u'app-developer',password=u'manager')
        DBSession.add(model)
    with transaction.manager:
        model = Task(content='Demo entry 1', owner=u'demo',status=0)
        DBSession.add(model)
