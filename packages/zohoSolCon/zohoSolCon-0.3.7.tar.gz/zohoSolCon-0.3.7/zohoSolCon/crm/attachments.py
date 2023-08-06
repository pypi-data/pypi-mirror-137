import requests
import json
import os


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



def upload_attachment(token, module, record_id, file_name):
    url = f'https://www.zohoapis.com/crm/v2.1/{module}/{record_id}/Attachments'
    headers = make_header(token)

    with open(file_name, 'rb') as f:
        request_body = {'file': f}
        response = requests.post(url=url, files=request_body, headers=headers)

    if response.status_code == 401:
        token.generate()
        return upload_attachment(token, module, record_id, file_name)

    else:
        content = json.loads(response.content.decode('utf-8'))
        return token, response.status_code, content.get("data")



def download_attachment(token, module, record_id, attachment_id, destination_dir):
    url = f'https://www.zohoapis.com/crm/v2.1/{module}/{record_id}/Attachments/{attachment_id}'
    headers = make_header(token)

    response = requests.get(url=url, headers=headers)

    if response.status_code == 401:
        token.generate()
        return download_attachment(token, module, record_id, attachment_id, destination_dir)

    else:
        if "Content-Type" in response.headers:
            content_type = response.headers['Content-Type']

            if content_type == 'application/json':
                return token, response.json

            else:
                if "Content-Disposition" in response.headers:
                    file_name = ''
                    content_disposition = response.headers["Content-Disposition"]

                    if "'" in content_disposition:
                        start_index = content_disposition.rindex("'")
                        file_name = content_disposition[start_index + 1:]

                    elif '"' in content_disposition:
                        start_index = content_disposition.rindex('=')
                        file_name = content_disposition[start_index + 1:].replace('"', '')

                    destination_file = os.path.join(destination_dir, file_name)

                    with open(destination_file, 'wb') as f:
                        for chunk in response:
                            f.write(chunk)

                    return token, destination_file


def delete_attachment(token, module, record_id, attachment_id):
    url = f'https://www.zohoapis.com/crm/v2.1/{module}/{record_id}/Attachments/{attachment_id}'
    headers = make_header(token)

    response = requests.delete(url=url, headers=headers)

    if response.status_code == 401:
        token.generate()
        return delete_attachment(token, module, record_id, attachment_id)


    else:
        content = json.loads(response.content.decode('utf-8'))
        return token, content.get("data")



def delete_photo(token, module, record_id):
    url = f'https://www.zohoapis.com/crm/v2.1/{module}/{record_id}/photo'
    headers = make_header(token)

    response = requests.delete(url=url, headers=headers)

    if response.status_code == 401:
        token.generate()
        return delete_photo(token, module, record_id)

    else:
        content = json.loads(response.content.decode('utf-8'))
        return token, content.get("data")


def upload_photo(token, module, record_id, file_name):
    url = f'https://www.zohoapis.com/crm/v2.1/{module}/{record_id}/photo'
    headers = make_header(token)

    with open(file_name, 'rb') as f:
        request_body = {'file': f}
        response = requests.post(url=url, files=request_body, headers=headers)

    if response.status_code == 401:
        token.generate()
        return upload_photo(token, module, record_id, file_name)

    else:
        content = json.loads(response.content.decode('utf-8'))
        return token, response.status_code, content.get("data")


def download_photo(token, module, record_id, destination_dir):
    url = f'https://www.zohoapis.com/crm/v2.1/{module}/{record_id}/photo'
    headers = make_header(token)

    response = requests.get(url=url, headers=headers)

    if response.status_code == 401:
        token.generate()
        return download_photo(token, module, record_id, destination_dir)

    else:
        if "Content-Type" in response.headers:
            content_type = response.headers['Content-Type']

            if content_type == 'application/json':
                return token, response.json

            else:
                if "Content-Disposition" in response.headers:
                    file_name = ''
                    content_disposition = response.headers["Content-Disposition"]

                    if "'" in content_disposition:
                        start_index = content_disposition.rindex("'")
                        file_name = content_disposition[start_index + 1:]

                    elif '"' in content_disposition:
                        start_index = content_disposition.rindex('=')
                        file_name = content_disposition[start_index + 1:].replace('"', '')

                    destination_file = os.path.join(destination_dir, file_name)

                    with open(destination_file, 'wb') as f:
                        for chunk in response:
                            f.write(chunk)

                    return token, destination_file


    
    
