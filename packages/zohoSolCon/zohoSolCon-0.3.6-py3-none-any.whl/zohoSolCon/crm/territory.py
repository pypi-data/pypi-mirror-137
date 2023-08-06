import requests
import json


def make_header(token):
    return {
        "Authorization": f'Zoho-oauthtoken {token.access}'
    }

def get_territories(token):
    url = "https://www.zohoapis.com/crm/v2.1/settings/territories"
    headers = make_header(token)
    response = requests.get(url=url, headers=headers)

    if response.status_code == 401:
        token.generate()
        print("Auth")
        return get_territories(token)

    else:
        content = json.loads(response.content.decode('utf-8'))
        return token, content.get("territories")


def assign_territories(token, module, record_id, territory_id_list):
    url = f"https://www.zohoapis.com/crm/v2.1/{module}/actions/assign_territories"
    headers = make_header(token)
    request_body = {}

    data_object = {'id': record_id}
    territory_list = []
    for id in territory_id_list:
        territory_list.append({"id":id})

    data_object['Territories'] = territory_list
    record_list = [data_object]

    request_body['data'] = record_list

    data = json.dumps(request_body).encode('utf-8')

    response = requests.post(url=url, headers=headers, data=data)

    if response.status_code == 401:
        print("Auth")
        token.generate()
        return assign_territories(token, module, record_id, territory_id_list)

    else:
        content = json.loads(response.content.decode('utf-8'))
        return token, response.status_code, content



def remove_territories(token, module, record_id, territory_id_list):
    url = f"https://www.zohoapis.com/crm/v2.1/{module}/actions/remove_territories"
    headers = make_header(token)
    request_body = {}

    data_object = {'id': record_id}
    territory_list = []
    for id in territory_id_list:
        territory_list.append({"id":id})

    data_object['Territories'] = territory_list
    record_list = [data_object]

    request_body['data'] = record_list

    data = json.dumps(request_body).encode('utf-8')

    response = requests.post(url=url, headers=headers, data=data)

    if response.status_code == 401:
        print("Auth")
        token.generate()
        return remove_territories(token, module, record_id, territory_id_list)

    else:
        content = json.loads(response.content.decode('utf-8'))
        return token, response.status_code, content


def get_territories_assigned(token, module, record_id):
    url = f'https://www.zohoapis.com/crm/v2.1/{module}/{record_id}'
    headers = make_header(token)
    response = requests.get(url=url, headers=headers)

    if response.status_code == 401:
        print("Auth")
        token.generate()
        return get_territories_assigned(token, module, record_id)

    else:
        content = json.loads(response.content.decode('utf-8'))
        data = content.get("data")
        if data is not None:
            return token, data.get("Territories")
    
