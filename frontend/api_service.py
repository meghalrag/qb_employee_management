import requests
from config import API_URL
from utils import format_api_res
from flask import session

# API_URL = API_URL

def login_api(params:dict):
    headers = {
        'accept': 'application/json',
        'Content-Type': 'application/json',
    }
    response = requests.post(f'{API_URL}/api/login', headers=headers, json=params)
    return format_api_res(response)


def create_emp_api(params:dict):
    headers = {
        'accept': 'application/json',
        'Content-Type': 'application/json',
        'Authorization': f'Bearer {session.get("access_token")}'
    }
    response = requests.post(f'{API_URL}/api/user', headers=headers, json=params)
    return format_api_res(response)


def get_all_users_api(id=None, filters = {}):
    headers = {
        'accept': 'application/json',
        'Content-Type': 'application/json',
        'Authorization': f'Bearer {session.get("access_token")}'
    }
    if id:
        response = requests.get(f'{API_URL}/api/user/{id}', headers=headers)
    else:
        response = requests.get(f'{API_URL}/api/user', headers=headers, json=filters)
    return format_api_res(response)


def get_current_user_api():
    headers = {
        'accept': 'application/json',
        'Content-Type': 'application/json',
        'Authorization': f'Bearer {session.get("access_token")}'
    }
    response = requests.get(f'{API_URL}/api/user/me', headers=headers)
    return format_api_res(response)


def edit_employee_api(id, params:dict):
    headers = {
        'accept': 'application/json',
        'Content-Type': 'application/json',
        'Authorization': f'Bearer {session.get("access_token")}'
    }
    response = requests.put(f'{API_URL}/api/user/{id}', headers=headers, json=params)
    return format_api_res(response)


def delete_employee_api(id):
    headers = {
        'accept': 'application/json',
        'Content-Type': 'application/json',
        'Authorization': f'Bearer {session.get("access_token")}'
    }
    response = requests.delete(f'{API_URL}/api/user/{id}', headers=headers)
    return format_api_res(response)


def export_employee_api(id, type):
    headers = {
        'accept': 'application/json',
        'Content-Type': 'application/json',
        'Authorization': f'Bearer {session.get("access_token")}'
    }
    response = requests.get(f'{API_URL}/api/user/export/{id}/{type}', headers=headers)
    return format_api_res(response)


def logout_api():
    headers = {
        'accept': 'application/json',
        'Content-Type': 'application/json',
        'Authorization': f'Bearer {session.get("access_token")}'
    }
    response = requests.post(f'{API_URL}/api/logout', headers=headers)
    return format_api_res(response)


def get_all_roles():
    headers = {
        'accept': 'application/json',
        'Content-Type': 'application/json',
        'Authorization': f'Bearer {session.get("access_token")}'
    }
    response = requests.get(f'{API_URL}/api/roles', headers=headers)
    return format_api_res(response)