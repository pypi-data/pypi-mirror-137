import requests
import json


def make_header(token):
    return {
        "Authorization": f'Zoho-oauthtoken {token.access}'
    }


def get_related_records(token, module, record_id, related_list, **kwargs):
    url = f"https://www.zohoapis.com/crm/v2.1/{module}/{record_id}/{related_list}"

    headers = make_header(token)
    
    response = requests.get(url=url, headers=headers, params=kwargs)

    if response.status_code == 401:
        token.generate()
        print("Auth")
        return get_related_records(token, module, record_id, related_list, **kwargs)

    else:
        content = json.loads(response.content.decode('utf-8'))
        data = content.get("data")
        return token, data


def update_related_record(token, module, record_id, related_list, related_id, data_object):
    url = f'https://www.zohoapis.com/crm/v2.1/{module}/{record_id}/{related_list}'
    headers = make_header(token)
    
    data_object['id'] = related_id
    request_body = {}
    record_list = [data_object]

    request_body['data'] = record_list
    data = json.dumps(request_body).encode('utf-8')
    
    response = requests.put(url=url, headers=headers,data=data)

    if response.status_code == 401:
        print("Auth")
        token.generate()
        return update_related_record(token, module, record_id, related_list, related_id, data_object)

    else:
        content = json.loads(response.content.decode('utf-8'))
        return token, response.status_code, content


