import json
from collections import defaultdict
import requests

response.headers['Access-Control-Allow-Origin'] = '*'

provider_api = "http://ec2-16-171-169-38.eu-north-1.compute.amazonaws.com:5000/api/providers"

def get_g3a_data():
    main_dict = defaultdict()
    rows = db(db.p_user.Role).select()
    user_list = [{'username':row.Username, 'first_name':row.first_name, 'last_name':row.last_name,
                  'email':row.Email, 'role':row.Role, 'master_aggr_id':row.ma_id} for row in rows]

    json_data = json.dumps(user_list)
    return json_data

def get_2a_provider_data():
    try:
        response = requests.get(provider_api)
        response.raise_for_status()  # Raise an exception for bad responses
        data = response.json()  # Assuming the API returns JSON data
        return dict(data=data)
    except requests.exceptions.RequestException as e:
        return dict(response=f"Error fetching data: {e}")
