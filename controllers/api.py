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

def agreement_offers_old():
    rows = db(db.masteragreementtype).select()
    data_list = [
        {'masterAgreementTypeId': row.masterAgreementTypeId,
         'masterAgreementTypeName': row.masterAgreementTypeName,
         'validFrom': str(row.validFrom),
         'validUntil': str(row.validUntil),
         'dailyrateIndicator': row.dailyrateIndicator,
         'deadline': str(row.deadline),
         'teamdeadline': str(row.teamdeadline),
         'workscontractdeadline': str(row.workscontractdeadline),
         'domains': [],
         'provider': row.provider,
         'quotePrice': row.quotePrice,
         'isAccepted': row.isAccepted} for row in rows]
    json_data = json.dumps(data_list)
    return json_data


def agreement_offers():
    """GET API FOR 2a"""

    # Group by roleName, masterAgreementTypeName, and domainId
    grouped_rows = db(db.role_offer).select(
        db.role_offer.id,
        db.role_offer.roleName,
        db.role_offer.experienceLevel,
        db.role_offer.technologiesCatalog,
        db.role_offer.domainId,
        db.role_offer.domainName,
        db.role_offer.offer_cycle,
        db.role_offer.masterAgreementTypeId,
        db.role_offer.masterAgreementTypeName,
        db.role_offer.provider,
        db.role_offer.quotePrice,
        db.role_offer.isAccepted,
        groupby=(
            db.role_offer.roleName,
            db.role_offer.masterAgreementTypeName,
            db.role_offer.domainId,
            db.role_offer.provider,
        ),
        orderby=db.role_offer.roleName,
    )

    # Create a new dictionary to store the aggregated data
    aggregated_data = {}

    # Iterate through the grouped rows and aggregate provider and quotePrice
    for row in grouped_rows:
        key = (
            row.roleName,
            row.masterAgreementTypeName,
            row.domainId,
        )

        if key not in aggregated_data:
            aggregated_data[key] = {
                'roleName': row.roleName,
                'experienceLevel': row.experienceLevel,
                'technologiesCatalog': row.technologiesCatalog,
                'domainId': row.domainId,
                'domainName': row.domainName,
                'masterAgreementTypeId': row.masterAgreementTypeId,
                'masterAgreementTypeName': row.masterAgreementTypeName,
                'provider': [],
            }

        aggregated_data[key]['provider'].append({
            'offerId': row.id,
            'name': row.provider,
            'quotePrice': row.quotePrice,
            'isAccepted': row.isAccepted,
            'cycle': row.offer_cycle
        })


    # Convert the aggregated data to a list
    final_aggregated_data = list(aggregated_data.values())

    # Convert the aggregated data to JSON
    json_data = json.dumps(final_aggregated_data, indent=4)

    return json_data

def post_ma_offer_response():
    """POST API FROM 2a"""
    is_accepted = bool(request.vars['isAccepted'])
    offer_id = request.vars['offerId']

    record = db(db.role_offer.id == offer_id).select().first()
    record.update_record(isAccepted=is_accepted)
    print(f'isAccepted: {is_accepted}, offerId: {offer_id}')

    # Return a JSON response
    return response.json({'status': 'success', 'message': 'Response Posted successfully'})



def service_offers():
    """GET API FOR 4a"""
    rows = db(db.service_request_offer).select()

    data_list = [{'offerId':row.id, 'serviceId':row.serviceId, 'masterAgreementTypeName':row.masterAgreementTypeName,'employee':{'employeeName':row.employee.name, 'employeeRole':row.employee.role, 'employeeExp':row.employee.experience},
                  'price':row.price, 'isAccepted':row.isAccepted} for row in rows]

    json_data = json.dumps(data_list)
    return json_data

# default.py


def post_service_offer_response():
    """POST API FROM 4a"""
    is_accepted = bool(request.vars['isAccepted'])
    offer_id = request.vars['offerId']

    # Your logic here, e.g., save data to the database
    record = db(db.service_request_offer.id==offer_id).select().first()
    record.update_record(isAccepted=is_accepted)
    # For demonstration purposes, let's just print the values
    print(f'isAccepted: {is_accepted}, offerId: {offer_id}')

    # Return a JSON response
    return response.json({'status': 'success', 'message': 'Response Posted successfully'})




















