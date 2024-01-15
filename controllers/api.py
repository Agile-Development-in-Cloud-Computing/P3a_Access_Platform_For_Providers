import json
from collections import defaultdict
import requests

sys.path.append('/modules')

from api_builder import BuildAPI
from helper import Helper

helper=Helper(db, session)

response.headers['Access-Control-Allow-Origin'] = '*'
provider_dict = BuildAPI.buildApiDict()

def get_g3a_data():
    main_dict = defaultdict()
    rows = db(db.p_user).select()
    user_list = [{'username':row.Username, 'first_name':row.first_name, 'last_name':row.last_name,
                  'email':row.Email, 'role':row.Role, 'provider':row.provider} for row in rows]

    json_data = json.dumps(user_list)
    return json_data

def get_3a_offers():
    rows = db(db.offer.status=='Submitted').select()
    data_list = [{'providerName':row.provider, 'domainId':row.domain_id, 'roleName':row.role, 'price':row.price} for row in rows]
    json_data = json.dumps(data_list)
    return json_data



