import requests 
import json


def make_header(token):
    return {
        "Authorization": f"Zoho-oauthtoken {token.access}"
    }


def get_record(token, module, record_id):
    url = f"https://www.zohoapis.com/crm/v2.1/{module}/{record_id}"
    headers = make_header(token)
    response = requests.get(url=url, headers=headers)
    if response.status_code == 401:
        print("Authentication issue")
        token.generate()
        return get_record(token, module, record_id)

    else:
        json_content = json.loads(response.content.decode('utf-8'))
        data = json_content['data'][0]
        return token, data


def update_record(token, module, record_id, data_object):
    url = f"https://www.zohoapis.com/crm/v2.1/{module}"
    headers = make_header(token)
    
    data_object["id"] = record_id

    request_body = dict()
    record_list = list()

    record_list.append(data_object)
    request_body['data'] = record_list

    data = json.dumps(request_body).encode('utf-8')
    response = requests.put(url=url, headers=headers, data=data)

    if response.status_code == 401:
        print("Auth issue")
        token.generate()
        return update_record(token, module, record_id, data_object)

    else:
        return token, response.status_code, json.loads(response.content.decode('utf-8'))


def convert_lead(token, record_id, **kwargs):
    data_object = kwargs
    request_body = dict()
    record_list = list()

    record_list.append(data_object)
    request_body['data'] = record_list

    data = json.dumps(request_body).encode('utf-8')

    response = requests.post(url=url, headers=headers, data=data)

    if response.status_code == 401:
        token.generate()
        return convert_lead(token, record_id, **kwargs)

    else:
        content = json.loads(response.content.decode('utf-8'))
        return token, content.get("data")

def create_record(token, module, data_object):
    url = f"https://www.zohoapis.com/crm/v2.1/{module}"
    headers = make_header(token)
    
    request_body = {}
    record_list = [data_object]
    request_body['data'] = record_list

    data = json.dumps(request_body).encode('utf-8')

    response = requests.post(url=url, headers=headers, data=data)

    if response.status_code == 401:
        print("Auth")
        token.generate()
        return create_record(token, module, data_object)

    else:
        return token, response.status_code, json.loads(response.content.decode('utf-8'))


def get_records(token, module, **kwargs):
    url = f"https://www.zohoapis.com/crm/v2.1/{module}"
    headers = make_header(token)
    response = requests.get(url=url, headers=headers, params=kwargs)

    if response.status_code == 401:
        print("Auth")
        token.generate()
        return get_records(token, module, **kwargs)

    else:
        content = json.loads(response.content.decode('utf-8'))
        records = content.get('data')

        return token, records


def get_deleted_records(token, module, record_type, **kwargs):
    url = f'https://www.zohoapis.com/crm/v2.1/{module}/deleted?type={record_type}'
    headers = make_header(token)

    response = requests.get(url=url, headers=headers, params=kwargs)

    if response.status_code == 401:
        token.generate()
        return get_deleted_records(token, module, record_type, **kwargs)

    else:
        content = json.loads(response.content.decode('utf-8'))
        return token, content.get('data')


def record_count(token, module, criteria=None, **kwargs):
    url = f'https://www.zohoapis.com/crm/v2.1/{module}/actions/count'
    headers = make_header(token)

    params = kwargs
    if criteria is not None:
        params['criteria': criteria]

    response = requests.get(url=url, headers=headers, params=params)

    if response.status_code == 401:
        token.generate()
        return record_count(token, module, criteria=criteria, **kwargs)

    else:
        content = json.loads(response.content.decode('utf-8'))
        return token, content.get("count")

def search_records(token, module, criteria, **kwargs):
    url = f"https://www.zohoapis.com/crm/v2.1/{module}/search"
    headers = make_header(token)
    
    parameters = {"criteria":criteria}

    parameters.update(kwargs)

    response = requests.get(url=url, headers=headers, params=parameters)

    if response.status_code == 401:
        print("Auth")
        token.generate()
        return search_records(token, module, criteria, **kwargs)

    elif response.status_code >= 300:
        raise Exception("Error in response {}".format(response.status_code))

    else:
        content = json.loads(response.content.decode('utf-8'))
        records = content.get('data')
        page_info = content.get("info")
        return token, records, page_info


def mass_action(token, module, callback, **kwargs):
    empty = False
    url = f"https://www.zohoapis.com/crm/v2.1/{module}"
    headers = make_header(token)
    
    page = 1
    iterated = 0
    parameters = kwargs
    while not empty:
        parameters['page'] = str(page)
        parameters['per_page'] = "200"
        response = requests.get(url=url, headers=headers, params=parameters)
        if response.status_code == 401:
            token.generate()
            headers = make_header(token)
            continue
        content = json.loads(response.content.decode('utf-8'))
        data = content.get("data")

        if len(data) == 0:
            print("Done")
            empty = True

        for record in data:
            token, callback_response = callback(token, module, record)
            print(callback_response)
            iterated += 1
            print(f"{iterated} Records iterated")

        page += 1
        if len(data) < 200:
            empty = True

    return token, f"{iterated} Records iterated."



