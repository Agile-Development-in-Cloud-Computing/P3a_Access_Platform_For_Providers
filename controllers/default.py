# -*- coding: utf-8 -*-
from collections import defaultdict
# -------------------------------------------------------------------------
# This is a sample controller
# this file is released under public domain and you can use without limitations
# -------------------------------------------------------------------------
import datetime
import sys
from dataclasses import dataclass
sys.path.append('/modules')

# Now you can import your module
from acl import Access
from api_builder import get_2a_provider_data, get_2a_ma_data, BuildAPI
from helper import Helper



access=Access(db, session)
Access.buildAccessCache(db)


helper=Helper(db, session)

all_service_requests = BuildAPI.buildServiceAgreementDict()
agreements = BuildAPI.buildMADict()


# ---- example index page ----
def index():
    if session.username:
        redirect(URL('ma_details'))
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
            if access.isBasicUser():
                redirect(URL('employee_dashboard'))
            redirect(URL('user_dashboard'))  # Redirect to dashboard after successful login
        response.flash = 'Invalid credentials'

    return dict(form=form)


def logout():
    session.username=None
    redirect(URL('login'))

def employee_dashboard():
    emp = db(db.p_user.Email==session.username).select().first()
    name=emp.first_name+' '+emp.last_name
    emp_details = db(db.employee.name==name).select().first()
    emp_offers= db(db.service_request_offer.employee==emp_details.id).select()
    offers =[all_service_requests[r.serviceId] for r in emp_offers]
    return dict(emp_details=emp_details, offers=offers, helper=helper)

def employee_accept_offer():
    is_accepted_str = request.vars['isAccepted'].lower()
    offer_id = request.vars['offerId']

    is_accepted = is_accepted_str == 'true'
    db.employee_accept.insert(offerId=offer_id, isAccepted=is_accepted)
    redirect(URL('employee_dashboard'))

def user_dashboard():
    if access.isBasicUser():
        redirect(URL('employee_dashboard'))
    userid = request.vars.userid
    try:
        logged_in_user = db(db.p_user.Email==session.username).select().first()
    except:
        raise Exception('No such user exists')
    user_record=None
    providers = []
    for p in get_2a_provider_data():
        providers.append(p["providerName"])
    if userid:
        user_record = db(db.p_user.id==userid).select().first()
    if not access.is_superAdmin():
        user_provider = logged_in_user.provider
        roles_array = ['Admin', 'BasicUser']
        user_rows = db((db.p_user.Role!='SuperAdmin') & (db.p_user.provider==user_provider)).select()
        admin_count = db((db.p_user.Role == 'Admin') & (db.p_user.provider==user_provider)).count()
        basic_user_count = db((db.p_user.Role == 'BasicUser') & (db.p_user.provider==user_provider)).count()
    else:
        roles_array = ['SuperAdmin', 'Admin']
        user_rows = db(db.p_user).select()
        admin_count = db(db.p_user.Role == 'Admin').count()
        basic_user_count = db(db.p_user.Role == 'BasicUser').count()
    fields = [db.p_user.Username, db.p_user.first_name, db.p_user.last_name, db.p_user.Email, db.p_user.Role, db.p_user.RegistrationDate, db.p_user.provider, db.p_user.LastLoginDate]
    if access.is_superAdmin():
        grid = SQLFORM.grid(db.p_user, user_signature=False, fields=fields)
    elif access.isAdmin():
        grid = SQLFORM.grid((db.p_user.Role=='Admin') | (db.p_user.Role=='BasicUser'), user_signature=False, fields=fields)
    else:
        redirect(URL('domain'))
    super_admin_count = db(db.p_user.Role=='SuperAdmin').count()
    form = SQLFORM.factory(
        Field('Username', 'string', requires=IS_NOT_EMPTY()),
        Field('first_name', 'string', requires=IS_NOT_EMPTY()),
        Field('last_name', 'string'),
        Field('Email', 'string', requires=IS_NOT_EMPTY()),
        Field('provider', requires=IS_IN_SET(providers)),
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

    providers = []
    for p in get_2a_provider_data():
        providers.append(p["providerName"])
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
        Field('provider', requires=IS_IN_SET(providers)),
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



def ma_details():
    if access.isBasicUser():
        redirect(URL('employee_dashboard'))
    ma_data = BuildAPI.buildMAStatic()
    provider_data = get_2a_provider_data()
    ma_rows = []
    providers=[]
    domains = []
    logged_in_provider = _get_provider()
    # data for super admin first
    ma_count = len(ma_data)

    provider_count = len(provider_data)
    open_ma = db(db.masteragreementtype.validUntil>datetime.date.today()).count()
    closed_ma = db(db.masteragreementtype.validUntil< datetime.date.today()).count()
    submitted_ma = db(db.masteragreementtype.provider == logged_in_provider).count()
    return dict(ma_rows=ma_data, provider_count=provider_count, open_ma=open_ma, closed_ma=closed_ma, ma_count=ma_count,
                access=access, submitted_ma=submitted_ma, helper=helper, provider=logged_in_provider)


def master_agreement():
    ma_key = request.vars['ma_key']
    ma_dict = BuildAPI.buildMAStatic()
    master_aggr = ma_dict[ma_key]
    provider = _get_provider()


    return dict(master_aggr=master_aggr, provider=provider)

def domains():
    if access.isBasicUser():
        redirect(URL('employee_dashboard'))
    provider_name = _get_provider()
    ma_data = agreements
    ma_key = request.vars['key']

    rejected_offers = db((db.role_offer.isAccepted==False) & (db.role_offer.provider==provider_name)).count()
    accepted_offers = db((db.role_offer.isAccepted==True) & (db.role_offer.provider==provider_name)).count()
    submitted_offers = db(db.role_offer.provider==provider_name).count()
    # Count of unique providers

    if ma_key:
        ma_data = {key: value for key, value in ma_data.items() if key[0] == ma_key}
        rejected_offers = db((db.role_offer.isAccepted == False) & (db.role_offer.provider == provider_name) & (db.role_offer.masterAgreementTypeName==ma_key)).count()
        accepted_offers = db((db.role_offer.isAccepted == True) & (db.role_offer.provider == provider_name) & (db.role_offer.masterAgreementTypeName==ma_key)).count()
        submitted_offers = db((db.role_offer.masterAgreementTypeName==ma_key) & (db.role_offer.provider==provider_name)).count()
    ma_s = [key[0] for key in ma_data.keys()]
    ma_count = len(set(ma_s))
    return dict(  provider=provider_name, helper=helper, pr_data=ma_data, ma_count=ma_count, rejected_offers=rejected_offers,
                  submitted_offers=submitted_offers, accepted_offers=accepted_offers)

def submit_price():
    domainId = int(request.vars['domainId'])
    role_name = request.vars['role_name']
    provider = _get_provider()
    price = int(request.vars['price'])
    masterAgreementTypeName = request.vars['masterAgreement']
    key = (masterAgreementTypeName, domainId, role_name)
    role_info = agreements[key]

    db.role_offer.insert(roleName=role_name, experienceLevel=role_info.experienceLevel, technologiesCatalog=role_info.technologiesCatalog,
                         domainId=domainId, domainName= role_info.domainName, masterAgreementTypeId=role_info.masterAgreementTypeId,
                         masterAgreementTypeName=masterAgreementTypeName, provider=provider,
                         quotePrice=price)

    redirect(URL('domains'))
    return dict()


def service_requests():
    if access.isBasicUser():
        redirect(URL('employee_dashboard'))
    provider=_get_provider()
    all_sr = all_service_requests
    return dict(all_sr=all_sr, helper=helper,provider=provider)



def view_service_request():
    provider = _get_provider()
    serviceId = int(request.vars['serviceId'])
    serviceInfo = all_service_requests[serviceId]

    current_offers = db(db.service_request_offer.serviceId==serviceId).select()

    form = SQLFORM.factory(
        Field('price', 'integer'),
        Field('employee', 'reference employee',
              requires=IS_IN_DB(db, 'employee.id',
                                '%(provider)s | %(name)s | %(role)s | %(experience)s years')),
        Field('suggestion', 'string')
    )
    # Assuming you have a db object defined

    if form.process().accepted:
        db.service_request_offer.insert(serviceId= serviceInfo.serviceId, employee=form.vars.employee, price=form.vars.price, masterAgreementTypeName=serviceInfo.masterAgreementTypeName, isAccepted=None,
                                        suggestion=form.vars.suggestion)
        redirect(URL('view_service_request', vars=dict(serviceId=serviceId)))

    return dict(serviceInfo=serviceInfo, form=form, current_offers=current_offers, provider=provider)

def negotiate():
    offerId = request.vars['offerId']
    row = db(db.service_request_offer.id==offerId).select().first()

    form=SQLFORM.factory(
        Field('price'),
        record=row, showid=False
    )
    if form.process().accepted:
        row.update_record(price=form.vars.price, isAccepted=None)
    return dict(row=row, form=form)

def positions():
    return dict()

def providerpage():
    response.view='default/provider_layout.html'
    return dict()

def Forgot_Password():
    return dict()

def Contact():
    return dict()

def Register():
    return dict()



def _get_provider():
    try:
        logged_in_user = db(db.p_user.Email == session.username).select().first()
        provider_name = logged_in_user.provider
        if provider_name is not None:
            return provider_name
        else:
            return 'FRAUAS'
    except:
        raise Exception('No such user exists')

def _did_provider_submit(ma_key, provider):
    try:
        row = db((db.masteragreementtype.masterAgreementTypeName == ma_key) & (db.masteragreementtype.provider == provider)).select().first()
        if row:
                if row.provider == provider:
                    return True
                else:
                    return False
    except:
        raise Exception('The MA offer for this provider does not exist')

