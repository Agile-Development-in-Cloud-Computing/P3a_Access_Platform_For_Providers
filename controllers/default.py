# -*- coding: utf-8 -*-
from collections import defaultdict
# -------------------------------------------------------------------------
# This is a sample controller
# this file is released under public domain and you can use without limitations
# -------------------------------------------------------------------------
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

access=Access(db, session)
Access.buildAccessCache(db)
# ---- example index page ----
def index():
    redirect(URL('WelCome'))


def test_view():
    values = request.vars
    myText = 'Hello Project 3, Access Platform for providers'
    form = SQLFORM(db.university)
    if form.process().accepted:
        response.flash = 'Your form was submitted successfully'
    else:
        response.flash = 'there is an error'

    form_2 = SQLFORM.factory(
        Field('name', 'string', required=IS_NOT_EMPTY()),
        Field('ranking', 'integer')
    )
    if form_2.process().accepted:
        db.university.insert(name=form_2.vars.name, ranking=form_2.vars.ranking)
    new_value = values.para
    return dict(myText=myText, form_2=form_2, new_value=new_value)


def edit_provider_credentials():
    credential_form = SQLFORM.factory(
        Field('provider_name', 'string'),
        Field('email', 'string'),
        Field('password', 'string'),
        Field('re_enter_password', 'string'),
        Field('role', 'string'), submit_button='Sign up'
    )

    return dict(credential_form=credential_form)


def provider_admin():
    total_users = 8
    providers = 3
    admin = 4
    roles = 3

    return dict(total_users=total_users, providers=providers, admin=admin, roles=roles)

def Team():

    return dict()

def About():
    return dict()

def team():
    response.view = 'default/Base_FrameWork.html'
    return dict()


def WelCome():
    return dict()

def login():
    # Your login logic goes here
    form = SQLFORM.factory(
        Field('Email', 'string', requires=IS_NOT_EMPTY()),
        Field('password', 'password', requires=IS_NOT_EMPTY())
    )

    if form.process().accepted:
        # Example: Check credentials against a database
        user = db(db.p_user.Email == form.vars.Email).select().first()
        if user and user.Password == form.vars.password:
            session.username = user.Email  # Use 'Email' instead of 'Username'
            user.update_record(LastLoginDate=datetime.datetime.now())
            redirect(URL('user_dashboard'))  # Redirect to dashboard after successful login
        response.flash = 'Invalid credentials'

    return dict(form=form)


def logout():
    session.username=None
    redirect(URL('WelCome'))

def user_dashboard():
    fields = [db.p_user.Username, db.p_user.first_name, db.p_user.last_name, db.p_user.Email, db.p_user.Role,
              db.p_user.RegistrationDate, db.p_user.ma_id, db.p_user.LastLoginDate]
    if access.is_superAdmin():
        grid = SQLFORM.grid(db.p_user, user_signature=False, fields=fields)
    elif access.isAdmin():
        grid = SQLFORM.grid((db.p_user.Role=='Admin') | (db.p_user.Role=='BasicUser'), user_signature=False, fields=fields)
    else:
        redirect(URL('domain'))
    super_admin_count = db(db.p_user.Role=='SuperAdmin').count()
    admin_count = db(db.p_user.Role=='Admin').count()
    basic_user_count = db(db.p_user.Role=='BasicUser').count()
    form = SQLFORM.factory(
        Field('first_name', 'string'),
        Field('last_name', 'string'),
        Field('email', 'string'),
        Field('master_agreement', requires=IS_IN_SET([])),
        Field('role', requires=IS_IN_SET(['admin', 'basic_user'])),
        Field('password', 'string'),
        Field('confirm_password', 'string')
    )

    return dict(form=form, grid=grid, super_admin_count=super_admin_count, admin_count=admin_count,
                basic_user_count=basic_user_count, access=access)

def domain():
    return dict()


def positions():
    return dict()

def providerpage():
    response.view='default/provider_layout.html'
    return dict()

def Forgot_Password():
    return dict()
