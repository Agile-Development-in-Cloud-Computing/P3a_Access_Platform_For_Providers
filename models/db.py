# -*- coding: utf-8 -*-

# -------------------------------------------------------------------------
# AppConfig configuration made easy. Look inside private/appconfig.ini
# Auth is for authenticaiton and access control
# -------------------------------------------------------------------------
from gluon.contrib.appconfig import AppConfig
from gluon.tools import Auth
import datetime
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
import sys
sys.path.append('/modules')

# Now you can import your module
from acl import Access

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

if db(db.masteragreementtype).count()==0:
    db.masteragreementtype.insert(Name='Master Agreement 001', ValidFrom=datetime.date.today(),
                                  ValidUntil=datetime.date.today()+ datetime.timedelta(days=7), DailyRateIndicator=True,
                                  Deadline= datetime.date(year=2023, month=1, day=22), TeamDeadLine=datetime.date(year=2023, month=1, day=18),
                                  WorksContractDeadline=datetime.date(year=2023, month=1, day=17))
    db.masteragreementtype.insert(Name='Master Agreement 002', ValidFrom=datetime.date.today(),
                                  ValidUntil=datetime.date.today() + datetime.timedelta(days=7),
                                  DailyRateIndicator=True,
                                  Deadline=datetime.date(year=2023, month=1, day=22),
                                  TeamDeadLine=datetime.date(year=2023, month=1, day=18),
                                  WorksContractDeadline=datetime.date(year=2023, month=1, day=17))
    db.masteragreementtype.insert(Name='Master Agreement 003', ValidFrom=datetime.date.today(),
                                  ValidUntil=datetime.date.today() + datetime.timedelta(days=7),
                                  DailyRateIndicator=False,
                                  Deadline=datetime.date(year=2023, month=1, day=22),
                                  TeamDeadLine=datetime.date(year=2023, month=1, day=18),
                                  WorksContractDeadline=datetime.date(year=2023, month=1, day=17))
    db.masteragreementtype.insert(Name='Master Agreement 004', ValidFrom=datetime.date.today(),
                                  ValidUntil=datetime.date.today() + datetime.timedelta(days=7),
                                  DailyRateIndicator=True,
                                  Deadline=datetime.date(year=2023, month=1, day=22),
                                  TeamDeadLine=datetime.date(year=2023, month=1, day=18),
                                  WorksContractDeadline=datetime.date(year=2023, month=1, day=17))


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
    Field('RegistrationDate', 'datetime', default=datetime.datetime.now()),
    Field('ma_id', 'reference master_aggr'),
    Field('LastLoginDate', 'datetime'),
    Field('IsActive', 'boolean', default=True)
)

def get_user_role():
    user = db(db.p_user.Email == session.username).select().first()
    if user:
        return user.Role
    else:
        return 'BasicUser'

if db(db.p_user).count()==0:
    db.p_user.insert(Username='fkhan', first_name='Faiz', last_name='Khan', Password='faiz@123',
                     Email='faiz.khan@stud.fra-uas.de', Role='SuperAdmin')
    db.p_user.insert(Username='apatil', first_name='Ankush', last_name='Patil', Password='ankush@123',
                     Email='ankush.patil@stud.fra-uas.de', Role='SuperAdmin')
    db.p_user.insert(Username='ssingari', first_name='Sahith', last_name='Singari', Password='sahith@123',
                     Email='sahith.singari@stud.fra-uas.de', Role='SuperAdmin')
    db.p_user.insert(Username='sbiru', first_name='Shiva', last_name='Biru', Password='shiva@123',
                     Email='shiva.biru@stud.fra-uas.de', Role='SuperAdmin')
    db.p_user.insert(Username='agadiraju', first_name='Anil', last_name='Gadiraju', Password='anil@123',
                     Email='anil.gadiraju@stud.fra-uas.de', Role='SuperAdmin')
    db.p_user.insert(Username='jdoe', first_name='John', last_name='Doe', Password='Password1',
                     Email='johndoe@example.com', Role='Admin')
    db.p_user.insert(Username='jsmith', first_name='Jane', last_name='Smith', Password='Password2',
                     Email='janesmith@example.com', Role='BasicUser')
    db.p_user.insert(Username='djohnson', first_name='David', last_name='Johnson', Password='Password3',
                     Email='davidjohnson@example.com', Role='BasicUser')
    db.p_user.insert(Username='swilliams', first_name='Sarah', last_name='Williams', Password='Password4',
                     Email='sarahwilliams@example.com', Role='Admin')
    db.p_user.insert(Username='mbrown', first_name='Michael', last_name='Brown', Password='Password5',
                     Email='michaelbrown@example.com', Role='BasicUser')
    db.p_user.insert(Username='ejones', first_name='Emily', last_name='Jones', Password='Password6',
                     Email='emilyjones@example.com', Role='Admin')
    db.p_user.insert(Username='cgarcia', first_name='Christopher', last_name='Garcia', Password='Password7',
                     Email='christophergarcia@example.com', Role='BasicUser')
    db.p_user.insert(Username='amartinez', first_name='Amanda', last_name='Martinez', Password='Password8',
                     Email='amandamartinez@example.com', Role='BasicUser')
    db.p_user.insert(Username='jrodriguez', first_name='James', last_name='Rodriguez', Password='Password9',
                     Email='jamesrodriguez@example.com', Role='Admin')
    db.p_user.insert(Username='slee', first_name='Sophia', last_name='Lee', Password='Password10',
                     Email='sophialee@example.com', Role='BasicUser')
    db.p_user.insert(Username='mlopez', first_name='Matthew', last_name='Lopez', Password='Password11',
                     Email='matthewlopez@example.com', Role='Admin')
    db.p_user.insert(Username='ohernandez', first_name='Olivia', last_name='Hernandez', Password='Password12',
                     Email='oliviahernandez@example.com', Role='BasicUser')
    db.p_user.insert(Username='dscott', first_name='Daniel', last_name='Scott', Password='Password13',
                     Email='danielscott@example.com', Role='BasicUser')
    db.p_user.insert(Username='imiller', first_name='Isabella', last_name='Miller', Password='Password14',
                     Email='isabellamiller@example.com', Role='Admin')
    db.p_user.insert(Username='wgonzalez', first_name='William', last_name='Gonzalez', Password='Password15',
                     Email='williamgonzalez@example.com', Role='BasicUser')
    db.p_user.insert(Username='cperez', first_name='Chloe', last_name='Perez', Password='Password16',
                     Email='chloeperez@example.com', Role='Admin')
    db.p_user.insert(Username='awilson', first_name='Alexander', last_name='Wilson', Password='Password17',
                     Email='alexanderwilson@example.com', Role='BasicUser')
    db.p_user.insert(Username='eanderson', first_name='Ella', last_name='Anderson', Password='Password18',
                     Email='ellaanderson@example.com', Role='BasicUser')
    db.p_user.insert(Username='btaylor', first_name='Benjamin', last_name='Taylor', Password='Password19',
                     Email='benjamintaylor@example.com', Role='Admin')
    db.p_user.insert(Username='amartinez', first_name='Ava', last_name='Martinez', Password='Password20',
                     Email='avamartinez@example.com', Role='BasicUser')
    db.p_user.insert(Username='lkim', first_name='Liam', last_name='Kim', Password='Password21',
                     Email='liamkim@example.com', Role='Admin')
    db.p_user.insert(Username='mnguyen', first_name='Mia', last_name='Nguyen', Password='Password22',
                     Email='muanguyen@example.com', Role='BasicUser')
    db.p_user.insert(Username='eking', first_name='Ethan', last_name='King', Password='Password23',
                     Email='ethanking@example.com', Role='BasicUser')
    db.p_user.insert(Username='ghall', first_name='Grace', last_name='Hall', Password='Password24',
                     Email='gracehall@example.com', Role='Admin')
    db.p_user.insert(Username='lwright', first_name='Lucas', last_name='Wright', Password='Password25',
                     Email='lucaswright@example.com', Role='BasicUser')

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
