import requests
import json


def make_header(token):
    return {
        "Authorization": f"Zoho-oauthtoken {token.access}"
    }


def get_org_details(token):
    url = "https://www.zohoapis.com/crm/v2.1/org"

    headers = make_header(token)
    response = requests.get(url=url, headers=headers)

    if response.status_code == 401:
        token.generate()
        return get_org_details(token)

    else:
        content = json.loads(response.content.decode('utf-8'))
        org = content.get("org")
        return token, org


def upload_org_photo(token, file_name):
    url = 'https://www.zohoapis.com/crm/v2.1/org/photo'
    headers = make_header(token)

    with open(file_name, 'rb') as file:
        request_body = {'file': file}
        response = requests.post(url=url, files=request_body, headers=headers)

    if response.status_code == 401:
        token.generate()
        return upload_org_photo(token, file_name)

    else:
        content = json.loads(response.content.decode('utf-8'))
        return token, content
