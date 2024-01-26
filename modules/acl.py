from collections import defaultdict

class Access:
    def __init__(self, db, session):
        self.db=db
        self.session=session
    _superadmins = set()
    _admins = set()
    _basicUsers = set()

    @staticmethod
    def buildAccessCache(db):
        for row in db(db.p_user.Role=='SuperAdmin').select():
            Access._superadmins.add(row.Email)
        for row in db(db.p_user.Role=='Admin').select():
            Access._admins.add(row.Email)
        for row in db(db.p_user.Role=='BasicUser').select():
            Access._basicUsers.add(row.Email)
    def is_superAdmin(self):
        return self.session.username in Access._superadmins
    def isAdmin(self):
        return self.session.username in Access._admins

    def isBasicUser(self):
        return self.session.username in Access._basicUsers
