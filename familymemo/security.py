# -*- coding: utf-8 -*- 
# to control the access

USERS = {'alog':'alog',
          'viewer':'viewer'}
GROUPS = {'alog':['group:editors']}

def groupfinder(userid, request):
    if userid in USERS:
        return GROUPS.get(userid, [])