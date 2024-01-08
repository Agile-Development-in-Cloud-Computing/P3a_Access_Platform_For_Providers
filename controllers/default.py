# -*- coding: utf-8 -*-
from collections import defaultdict
# -------------------------------------------------------------------------
# This is a sample controller
# this file is released under public domain and you can use without limitations
# -------------------------------------------------------------------------
import datetime
import sys
sys.path.append('/modules')

# Now you can import your module
from acl import Access




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
    userid = request.vars.userid
    user_record=None
    if userid:
        user_record = db(db.p_user.id==userid).select().first()
    if not access.is_superAdmin():
        roles_array = ['Admin', 'BasicUser']
        user_rows = db(db.p_user.Role!='SuperAdmin').select()
    else:
        roles_array = ['SuperAdmin', 'Admin', 'BasicUser']
        user_rows = db(db.p_user).select()
    fields = [db.p_user.Username, db.p_user.first_name, db.p_user.last_name, db.p_user.Email, db.p_user.Role, db.p_user.RegistrationDate, db.p_user.ma_id, db.p_user.LastLoginDate]
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
        Field('Username', 'string', requires=IS_NOT_EMPTY()),
        Field('first_name', 'string', requires=IS_NOT_EMPTY()),
        Field('last_name', 'string'),
        Field('Email', 'string', requires=IS_NOT_EMPTY()),
        Field('ma_id', requires=IS_IN_SET([])),
        Field('Role', requires=IS_IN_SET(roles_array)),
        Field('Password', 'password', requires=IS_NOT_EMPTY()),
        record=user_record
    )
    if form.process().accepted:
        if user_record:
            user_record.update_record(**form.vars)
            response.flash = 'Record Updated'
        else:
            db.p_user.insert(**form.vars)
            response.flash = 'New Record Created'
        redirect(URL('user_dashboard'))

    return dict(form=form, grid=grid, super_admin_count=super_admin_count, admin_count=admin_count,
                basic_user_count=basic_user_count, access=access, user_rows=user_rows)

def edit_user():
    userid = request.vars.userid
    user_record = None
    if userid:
        user_record = db(db.p_user.id == userid).select().first()
    if not access.is_superAdmin():
        roles_array = ['Admin', 'BasicUser']
    else:
        roles_array = ['SuperAdmin', 'Admin', 'BasicUser']
    form = SQLFORM.factory(
        Field('Username', 'string', requires=IS_NOT_EMPTY()),
        Field('first_name', 'string', requires=IS_NOT_EMPTY()),
        Field('last_name', 'string'),
        Field('Email', 'string', requires=IS_NOT_EMPTY()),
        Field('ma_id', requires=IS_IN_SET([])),
        Field('Role', requires=IS_IN_SET(roles_array)),
        Field('Password', 'password', requires=IS_NOT_EMPTY()),
        record=user_record
    )
    if form.process().accepted:
        if user_record:
            user_record.update_record(**form.vars)
            response.flash = 'Record Updated'
        else:
            db.p_user.insert(**form.vars)
            response.flash = 'New Record Created'
        redirect(URL('user_dashboard'))

    return dict(form=form)

def delete_user():
    userid = request.vars.userid
    db(db.p_user.id==userid).delete()
    redirect(URL('user_dashboard'))

def domain():
    ma_rows = db(db.masteragreementtype).select()
    return dict(ma_rows=ma_rows)


def positions():
    return dict()

def providerpage():
    response.view='default/provider_layout.html'
    return dict()

def Forgot_Password():
    return dict()
