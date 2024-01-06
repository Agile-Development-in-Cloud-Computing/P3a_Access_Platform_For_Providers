from collections import defaultdict

class Access:
    def __init__(self, db, session):
        self.db=db
        self.session=session
    _cache = {}
    def buildAccessCache(self, db):
        for row in db(db.p_user.Role=='SuperAdmin'):
            Access._cache[('superAdmin',)]=row.Email
        for row in db(db.p_user.Role=='Admin'):
            Access._cache[('admin',)]=row.Email
        for row in db(db.p_user.Role=='BasicUser'):
            Access._cache[('basicUser',)]=row.Email
        print(Access._cache)
