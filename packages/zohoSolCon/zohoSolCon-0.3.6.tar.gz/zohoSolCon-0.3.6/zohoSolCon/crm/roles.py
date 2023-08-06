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



