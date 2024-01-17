import json
from collections import defaultdict
import requests
from dataclasses import dataclass

@dataclass
class Role:
    providerName:str
    domainId:int
    domainName:str
    roleName: str
    experienceLevel:str
    technologiesCatalog:str
    mastAggr:str

@dataclass
class Service:
    serviceId:int
    projectInfo:str
    startDate:str
    endDate: str
    workLocation:str
    domain:str
    role:str
    skill:str
    technology:str
    experience:str
    onsiteDaysPerWeek:str
    remoteDaysPerWeek:str

class BuildAPI:
    @staticmethod
    def buildApiDict():
        json_data = get_2a_provider_data()
        print('json_data', json_data, type(json_data))
        role_dict = {}
        for provider_data in json_data:
            provider_name = provider_data['providerName']

            for domain_data in provider_data['domains']:
                domain_id = domain_data['id']
                domain_name = domain_data['domainName']

                for role_data in domain_data['roles']:
                    role_name = role_data['roleName']
                    role_key = (provider_name, domain_id, role_name)

                    # Create Role object
                    role_object = Role(
                        providerName=provider_name,
                        domainId=domain_id,
                        domainName=domain_name,
                        roleName=role_name,
                        experienceLevel=role_data['experienceLevel'],
                        technologiesCatalog=role_data['technologiesCatalog'],
                        mastAggr=provider_data['masterAgreementTypeId']
                    )

                    # Add to the dictionary
                    role_dict[role_key] = role_object
        return role_dict

    @staticmethod
    def buildServiceAgreementDict():
        json_data = get_4a_services()
        services = {}
        for service in json_data:
            service_obj = Service(serviceId=service['serviceId'], projectInfo=service['projectInfo'],
                                                    startDate=service['startDate'], endDate=service['endDate'],
                                                    workLocation=service['workLocation'], domain=service['domain'],
                                                    role=service['role'], skill=service['skill'], technology=service['technology'],
                                                    experience=service['experience'], onsiteDaysPerWeek=service['onsiteDaysPerWeek'],
                                                    remoteDaysPerWeek=service['remoteDaysPerWeek'])
            services[service['serviceId']]= service_obj
        return services


def get_2a_provider_data():
    provider_api = "http://ec2-16-171-169-38.eu-north-1.compute.amazonaws.com:5000/api/providers"
    try:
        response = requests.get(provider_api)
        response.raise_for_status()  # Raise an exception for bad responses
        data = response.json()  # Assuming the API returns JSON data
        return data
    except requests.exceptions.RequestException as e:
        return dict(response=f"Error fetching data: {e}")


def get_2a_ma_data():
    ma_api = "http://ec2-16-171-169-38.eu-north-1.compute.amazonaws.com:5000/api/mastertype/all"
    try:
        response = requests.get(ma_api)
        response.raise_for_status()  # Raise an exception for bad responses
        data = response.json()  # Assuming the API returns JSON data
        return data
    except requests.exceptions.RequestException as e:
        return dict(response=f"Error fetching data: {e}")




def get_4a_services():
    sm_api = "http://ec2-54-145-132-89.compute-1.amazonaws.com:9198/api/v1/serviceManagement"
    try:
        response = requests.get(sm_api)
        response.raise_for_status()  # Raise an exception for bad responses
        data = response.json()  # Assuming the API returns JSON data
        return data
    except requests.exceptions.RequestException as e:
        return dict(response=f"Error fetching data: {e}")
