import requests
import json


def make_header(token):
    return {
        'Authorization': f'Zoho-oauthtoken {token.access}'
    }

def get_attachments(token, module, record_id, **kwargs):
    url = f'https://www.zohoapis.com/crm/v2.1/{module}/{record_id}/Attachments'
    headers = make_header(token)
    response = requests.get(url=url, headers=headers, params=kwargs)

    if response.status_code == 401:
        print("Auth")
        token.generate()
        return get_attachments(token, module, record_id, **kwargs)

    else:
        content = json.loads(response.content.decode('utf-8'))
        return token, content.get("data")



