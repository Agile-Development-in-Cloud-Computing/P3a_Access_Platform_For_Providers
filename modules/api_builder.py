import json
from collections import defaultdict
import requests




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