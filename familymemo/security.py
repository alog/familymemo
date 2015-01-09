# -*- coding: utf-8 -*- 
# to control the access

USERS = {'demo':'demo',
          'admin':'admin'}
GROUPS = {'admin':['group:editors']}

def groupfinder(userid, request):
    if userid in USERS:
        return GROUPS.get(userid, [])