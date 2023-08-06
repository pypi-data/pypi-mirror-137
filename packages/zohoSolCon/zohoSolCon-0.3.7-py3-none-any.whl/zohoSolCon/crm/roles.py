import requests
import json


def make_header(token):
    return {
        "Authorization": f"Zoho-oauthtoken {token.access}"
    }

def get_roles(token):
    url = 'https://www.zohoapis.com/crm/v2.1/settings/roles'
    headers = make_header(token)
    response = requests.get(url=url, headers=headers)

    if response.status_code == 401:
        token.generate()
        return get_roles(token)

    else:
        content = json.loads(response.content.decode('utf-8'))
        return token, content.get("roles")


def get_role(token, role_id):
    url = f'https://www.zohoapis.com/crm/v2.1/settings/roles/{role_id}'
    headers = make_header(token)
    
    response = requests.get(url=url, headers=headers)

    if response.status_code == 401:
        token.generate()
        return get_role(token, role_id)

    else:
        content = json.loads(response.content.decode('utf-8'))
        return token, content.get("roles")


def create_role(token, data_object):
    url = 'https://www.zohoapis.com/crm/v2.1/settings/roles'
    headers = make_header(token)
    request_body = dict()
    role_list = list()

    role_list.append(data_object)
    request_body['roles'] = role_list

    data = json.dumps(request_body).encode('utf-8')

    response = requests.post(url=url, headers=headers, data=data)

    if response.status_code == 401:
        token.generate()
        return create_role(token, data_object)

    else:
        content = json.loads(response.content.decode('utf-8'))
        return token, content
    

def delete_role(token, role_id, transfer_to):
    url = f'https://www.zohoapis.com/crm/v2.1/settings/roles/{role_id}'
    params = {'transfer_to_id': transfer_to}
    headers = make_header(token)

    response = requests.delete(url=url, headers=headers, params=params)

    if response.status_code == 401:
        token.generate()
        return delete_role(token, role_id, transfer_to)

    else:
        content = json.loads(response.content.decode('utf-8'))
        return token, content


    
