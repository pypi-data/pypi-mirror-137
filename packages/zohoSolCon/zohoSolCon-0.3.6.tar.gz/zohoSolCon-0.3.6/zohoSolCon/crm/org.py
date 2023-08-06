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


