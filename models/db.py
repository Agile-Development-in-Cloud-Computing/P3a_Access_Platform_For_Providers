# -*- coding: utf-8 -*-

# -------------------------------------------------------------------------
# AppConfig configuration made easy. Look inside private/appconfig.ini
# Auth is for authenticaiton and access control
# -------------------------------------------------------------------------
from gluon.contrib.appconfig import AppConfig
from gluon.tools import Auth
from datetime import datetime
# -------------------------------------------------------------------------
# This scaffolding model makes your app work on Google App Engine too
# File is released under public domain and you can use without limitations
# -------------------------------------------------------------------------

if request.global_settings.web2py_version < "2.15.5":
    raise HTTP(500, "Requires web2py 2.15.5 or newer")

# -------------------------------------------------------------------------
# if SSL/HTTPS is properly configured and you want all HTTP requests to
# be redirected to HTTPS, uncomment the line below:
# -------------------------------------------------------------------------
# request.requires_https()

# -------------------------------------------------------------------------
# once in production, remove reload=True to gain full speed
# -------------------------------------------------------------------------
configuration = AppConfig(reload=True)

if not request.env.web2py_runtime_gae:
    # ---------------------------------------------------------------------
    # if NOT running on Google App Engine use SQLite or other DB
    # ---------------------------------------------------------------------
    db = DAL(configuration.get('db.uri'),
             pool_size=configuration.get('db.pool_size'),
             migrate_enabled=configuration.get('db.migrate'),
             check_reserved=['all'])
else:
    # ---------------------------------------------------------------------
    # connect to Google BigTable (optional 'google:datastore://namespace')
    # ---------------------------------------------------------------------
    db = DAL('google:datastore+ndb')
    # ---------------------------------------------------------------------
    # store sessions and tickets there
    # ---------------------------------------------------------------------
    session.connect(request, response, db=db)
    # ---------------------------------------------------------------------
    # or store session in Memcache, Redis, etc.
    # from gluon.contrib.memdb import MEMDB
    # from google.appengine.api.memcache import Client
    # session.connect(request, response, db = MEMDB(Client()))
    # ---------------------------------------------------------------------

# -------------------------------------------------------------------------
# by default give a view/generic.extension to all actions from localhost
# none otherwise. a pattern can be 'controller/function.extension'
# -------------------------------------------------------------------------
response.generic_patterns = [] 
if request.is_local and not configuration.get('app.production'):
    response.generic_patterns.append('*')

# -------------------------------------------------------------------------
# choose a style for forms
# -------------------------------------------------------------------------
response.formstyle = 'bootstrap4_inline'
response.form_label_separator = ''

# -------------------------------------------------------------------------
# (optional) optimize handling of static files
# -------------------------------------------------------------------------
# response.optimize_css = 'concat,minify,inline'
# response.optimize_js = 'concat,minify,inline'

# -------------------------------------------------------------------------
# (optional) static assets folder versioning
# -------------------------------------------------------------------------
# response.static_version = '0.0.0'

# -------------------------------------------------------------------------
# Here is sample code if you need for
# - email capabilities
# - authentication (registration, login, logout, ... )
# - authorization (role based authorization)
# - services (xml, csv, json, xmlrpc, jsonrpc, amf, rss)
# - old style crud actions
# (more options discussed in gluon/tools.py)
# -------------------------------------------------------------------------
#
db.define_table(
    'master_aggr',
    Field('ma_id', 'string'),
    Field('provider_name')
)
# host names must be a list of allowed host names (glob syntax allowed)
auth = Auth(db, host_names=configuration.get('host.names'))

# -------------------------------------------------------------------------
# create all tables needed by auth, maybe add a list of extra fields
# -------------------------------------------------------------------------
auth.settings.extra_fields['auth_user'] = [
    Field('Role', requires=IS_IN_SET(['SuperAdmin', 'Admin', 'BasicUser'])),
    Field('ma_id', 'reference master_aggr'),
]
auth.define_tables(username=True, signature=False)

# -------------------------------------------------------------------------
# configure email
# -------------------------------------------------------------------------
mail = auth.settings.mailer
mail.settings.server = 'logging' if request.is_local else configuration.get('smtp.server')
mail.settings.sender = configuration.get('smtp.sender')
mail.settings.login = configuration.get('smtp.login')
mail.settings.tls = configuration.get('smtp.tls') or False
mail.settings.ssl = configuration.get('smtp.ssl') or False

# -------------------------------------------------------------------------
# configure auth policy
# -------------------------------------------------------------------------
auth.settings.registration_requires_verification = False
auth.settings.registration_requires_approval = False
auth.settings.reset_password_requires_verification = True

# -------------------------------------------------------------------------  
# read more at http://dev.w3.org/html5/markup/meta.name.html               
# -------------------------------------------------------------------------
response.meta.author = configuration.get('app.author')
response.meta.description = configuration.get('app.description')
response.meta.keywords = configuration.get('app.keywords')
response.meta.generator = configuration.get('app.generator')
response.show_toolbar = configuration.get('app.toolbar')

# -------------------------------------------------------------------------
# your http://google.com/analytics id                                      
# -------------------------------------------------------------------------
response.google_analytics_id = configuration.get('google.analytics_id')

# -------------------------------------------------------------------------
# maybe use the scheduler
# -------------------------------------------------------------------------
if configuration.get('scheduler.enabled'):
    from gluon.scheduler import Scheduler
    scheduler = Scheduler(db, heartbeat=configuration.get('scheduler.heartbeat'))

# -------------------------------------------------------------------------
# Define your tables below (or better in another model file) for example
#
# >>> db.define_table('mytable', Field('myfield', 'string'))
#
# Fields can be 'string','text','password','integer','double','boolean'
#       'date','time','datetime','blob','upload', 'reference TABLENAME'
# There is an implicit 'id integer autoincrement' field
# Consult manual for more options, validators, etc.
#
# More API examples for controllers:
#
# >>> db.mytable.insert(myfield='value')
# >>> rows = db(db.mytable.myfield == 'value').select(db.mytable.ALL)
# >>> for row in rows: print row.id, row.myfield
# -------------------------------------------------------------------------

# -------------------------------------------------------------------------
# after defining tables, uncomment below to enable auditing
# -------------------------------------------------------------------------
# auth.enable_record_versioning(db)
db.define_table('university',
                Field('name', 'string', required=IS_NOT_EMPTY()),
                Field('ranking', 'integer'))

# Define web2py models

# contract table
db.define_table(
    'contract',
    Field('UserOfferID', 'integer', 'reference useroffer'),
    Field('ContractDate', 'datetime'),
    Field('Status', 'string', length=50)
)

# evaluation table
db.define_table(
    'evaluation',
    Field('UserID', 'integer', 'reference p_user'),
    Field('ProviderID', 'integer', 'reference provider'),
    Field('ServiceRequestID', 'integer', 'reference servicerequest'),
    Field('Rating', 'integer'),
    Field('Comments', 'text')
)

# masteragreementtype table
db.define_table(
    'masteragreementtype',
    Field('Name', 'string', length=255),
    Field('ValidFrom', 'date'),
    Field('ValidUntil', 'date'),
    Field('DailyRateIndicator', 'boolean'),
    Field('Deadline', 'date'),
    Field('TeamDeadline', 'date'),
    Field('WorksContractDeadline', 'date'),
    Field('GroupID', 'integer', 'reference pgroup')
)

# negotiation table
db.define_table(
    'negotiation',
    Field('UserOfferID', 'integer', 'reference useroffer'),
    Field('ProposedPrice', 'decimal(10,2)'),
    Field('NegotiatedPrice', 'decimal(10,2)'),
    Field('Status', 'string', length=50)
)

# offer table
db.define_table(
    'offer',
    Field('ProviderID', 'integer', 'reference provider'),
    Field('AgreementTypeID', 'integer', 'reference masteragreementtype'),
    Field('OfferDate', 'datetime'),
    Field('Status', 'string', length=50)
)

# pgroup table
db.define_table(
    'pgroup',
    Field('Name', 'string', length=255),
    Field('Description', 'text')
)

# provider table
db.define_table(
    'provider',
    Field('Name', 'string', length=255),
    Field('Address', 'string', length=255),
    Field('ExistenceSince', 'date'),
    Field('ValidFrom', 'date'),
    Field('ValidUntil', 'date')
)

# requestcycle table
db.define_table(
    'requestcycle',
    Field('ServiceRequestID', 'integer', 'reference servicerequest'),
    Field('CycleNumber', 'integer'),
    Field('Status', 'string', length=50)
)

# servicerequest table
db.define_table(
    'servicerequest',
    Field('UserID', 'integer', 'reference p_user'),
    Field('RequestType', 'string', length=50),
    Field('SkillLevels', 'string', length=255),
    Field('ExpertiseLevel', 'string', length=255),
    Field('Role', 'string', length=50),
    Field('Status', 'string', length=50)
)

# user table
db.define_table(
    'p_user',
    Field('Username', 'string', length=255, requires=IS_NOT_EMPTY()),
    Field('first_name', 'string', length=255, requires=IS_NOT_EMPTY()),
    Field('last_name', 'string', length=255),
    Field('Password', 'password', requires=IS_NOT_EMPTY()),
    Field('Email', 'string', length=255, requires=IS_NOT_EMPTY()),
    Field('Role', requires=IS_IN_SET(['SuperAdmin', 'Admin', 'BasicUser'])),
    Field('RegistrationDate', 'datetime', default=datetime.now()),
    Field('ma_id', 'reference master_aggr'),
    Field('LastLoginDate', 'datetime'),
    Field('IsActive', 'boolean', default=True)
)

if db(db.p_user).count()==0:
    db.p_user.insert(Username='fkhan', first_name='Faiz', last_name='Khan', password='faiz@123',
                     Email='faiz.khan@stud.fra-uas.de', Role='SuperAdmin')
    db.p_user.insert(Username='apatil', first_name='Ankush', last_name='Patil', password='ankush@123',
                     Email='ankush.patil@stud.fra-uas.de', Role='SuperAdmin')
    db.p_user.insert(Username='ssingari', first_name='Sahith', last_name='Singari', password='sahith@123',
                     Email='sahith.singari@stud.fra-uas.de', Role='SuperAdmin')
    db.p_user.insert(Username='sbiru', first_name='Shiva', last_name='Biru', password='shiva@123',
                     Email='shiva.biru@stud.fra-uas.de', Role='SuperAdmin')
    db.p_user.insert(Username='agadiraju', first_name='Anil', last_name='Gadiraju', password='anil@123',
                     Email='anil.gadiraju@stud.fra-uas.de', Role='SuperAdmin')

# useroffer table
db.define_table(
    'useroffer',
    Field('UserID', 'integer', 'reference p_user'),
    Field('OfferID', 'integer', 'reference offer'),
    Field('IsChosen', 'boolean'),
    Field('IsAccepted', 'boolean')
)

# userprofile table
db.define_table(
    'userprofile',
    Field('UserID', 'integer', 'reference p_user'),
    Field('ServiceRequestID', 'integer', 'reference  '),
    Field('ProfileData', 'text')
)
