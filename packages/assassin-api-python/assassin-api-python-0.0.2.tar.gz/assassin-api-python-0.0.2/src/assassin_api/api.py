from uuid import uuid4
import requests
from requests.api import head

from assassin_api.validators import CreateAssetTypeValidator
from .decorators import api_exceptions_handler
from .exceptions import *


class ApiRequest(object):
    session = None
    URL = None

    def __init__(self, session):
        self.session = session
        self.token = session.token
        self.host = session.host

    def _add_auth_header(self, headers):
        if self.token is not None:
            headers['Authorization'] = f'Bearer {self.token}'

    def _send_request(self, method, url, headers={}, data={}, files=None, json=True):
        self._add_auth_header(headers)

        

        
        # print()
        # print()
        # print('-'*40)
        # print(method.upper(), url)
        # print()
        # print('REQUEST DATA:')

        if json == True:
            headers['Content-Type'] = 'application/json'
            import json
            data = json.dumps(data)
        elif headers.get('Content-Type', None):
            del headers['Content-Type']
        

        # print(data)
        # print('HEADERS:')
        # print(headers)
        # print()
        response = requests.request(method=method, url=url, headers=headers, data=data, files=files)
        
        # print()
        # print('RESPONSE JSON:')
        # print(response.json())
        # # for k,v in response.json().items():
        # #     print(f'{k}: {v}')
        # print()
        
        # print('FILES:')
        # if response.json().get('asset_files', None):
            # for i in response.json()['asset_files']:
            #     print(i)
            #     print()
        return response

    def get_files(self, data, file_fields):
        files = {}
        for field in file_fields:
            if field in data.keys():
                try:
                    files[field] = open(data[field], 'rb')
                except Exception:
                    raise ValueError(f"Could not open file {data[field]}")
        return None if files == {} else files

    @api_exceptions_handler
    def get_objects_list(self, params: dict = {}):
        params_list = []
        for k, v in params.items():
            params_list.append(f'{k}={v}')
        if len(params_list) > 0:
            params_str = f'?{"&".join(params_list)}'
        else:
            params_str = ""
        return self._send_request('get', f'{self.host}{self.URL}{params_str}')

    @api_exceptions_handler
    def get_object_detail(self, id):
        response = self._send_request('get', f'{self.host}{self.URL}{id}/')
        # self.session.session_objects.append(response)
        return response

    @api_exceptions_handler
    def create_object(self, data, file_fields=[]):
        # print()
        # print('API REQUEST create object data:', data)
        # print()
        files = self.get_files(data, file_fields)
        import json
        return self._send_request('post', f'{self.host}{self.URL}', data=data, files=files)

    @api_exceptions_handler
    def update_object(self, id, data, file_fields=[]):
        files = self.get_files(data, file_fields)
        return self._send_request('patch', f'{self.host}{self.URL}{id}/', data=data, files=files)

    @api_exceptions_handler
    def delete_object(self, id):
        return self._send_request('delete', f'{self.host}{self.URL}{id}')


class UserRequest(ApiRequest):
    URL = '/api/v1/users/'

    @api_exceptions_handler
    def user_login(self, email, password):
        return self._send_request(
            'post', f'{self.host}{self.URL}token/',
            data={'email': email, 'password': password}
        )

    @api_exceptions_handler
    def add_user_to_groups(self, id, groups):
        data = {'groups': groups}
        return self._send_request(
            'put', f'{self.host}{self.URL}{id}/add-user-to-groups',
            data=data
        )

    @api_exceptions_handler
    def remove_user_from_groups(self, id, groups):
        data = {'groups': groups}
        return self._send_request(
            'put', f'{self.host}{self.URL}{id}/remove-user-from-groups',
            data=data
        )

    @api_exceptions_handler
    def change_password(self, id, password):
        data = {'password': password}
        return self._send_request(
            'put', f'{self.host}{self.URL}{id}/change-password',
            data=data
        )


class AssetTypeTreeRequestMixin(ApiRequest):

    @api_exceptions_handler
    def change_order(self, id, order):
        data = {'position': order}
        return self._send_request(
            'put', f'{self.host}{self.URL}{id}/change-order',
            data=data
        )


class AssetTypeRequest(AssetTypeTreeRequestMixin):
    URL = '/api/v1/asset-types/'

    @api_exceptions_handler
    def create_object(self, data, file_fields=[]):
        validator = CreateAssetTypeValidator
        data = validator.validate(data)


        files = self.get_files(data, file_fields)
        # print('files:', files)

        # data['image'] = files['image']

        return self._send_request('post', f'{self.host}{self.URL}', data=data, files=files, json=False)

    @api_exceptions_handler
    def update_attributes(self, id, available_asset_fields, available_file_types):
        data = {
            'available_asset_fields': available_asset_fields,
            'available_file_types': available_file_types
        }
        return self._send_request(
            'put', f'{self.host}{self.URL}{id}/attributes/',
            data=data
        )


class AssetCategoryRequest(AssetTypeTreeRequestMixin):
    URL = '/api/v1/asset-categories/'


class AssetSubcategoryRequest(AssetTypeTreeRequestMixin):
    URL = '/api/v1/asset-subcategories/'


class CollectionRequest(ApiRequest):
    URL = '/api/v1/asset-collections/'


class ProjectRequest(ApiRequest):
    URL = '/api/v1/projects/'

    def get_object_detail(self, id):
        raise NotImplementedError()

    def create_object(self, data, file_fields=[]):
        raise NotImplementedError()

    def update_object(self, id, data, file_fields=[]):
        raise NotImplementedError()

    def delete_object(self, id):
        return NotImplementedError()


class AuthorsRequest(ApiRequest):
    URL = '/api/v1/authors/'

    def get_object_detail(self, id):
        raise NotImplementedError()

    def create_object(self, data, file_fields=[]):
        raise NotImplementedError()

    def update_object(self, id, data, file_fields=[]):
        raise NotImplementedError()

    def delete_object(self, id):
        return NotImplementedError()


class TagRequest(ApiRequest):
    URL = '/api/v1/asset-tags/'

    def get_object_detail(self, id):
        raise NotImplementedError()

    def update_object(self, id, data, file_fields=[]):
        raise NotImplementedError()

    def delete_object(self, id):
        return NotImplementedError()


class AssetRequest(ApiRequest):
    URL = '/api/v1/assets/'
    
    @api_exceptions_handler
    def get_objects_list(self, params):
        params['no_page'] = True
        return super(AssetRequest, self).get_objects_list(params)

    @api_exceptions_handler
    def set_rating(self, id, rating):
        data = {'rating': rating}
        return self._send_request(
            'post', f'{self.host}{self.URL}{id}/set-asset-rating/',
            data=data
        )


class AssetFileRequest(ApiRequest):
    URL = '/api/v1/assets/upload-file'

    def get_object_detail(self, id):
        raise NotImplementedError()

    def create_object(self, data, file_fields=[]):
        raise NotImplementedError()

    def update_object(self, id, data, file_fields=[]):
        raise NotImplementedError()

    def delete_object(self, id):
        return NotImplementedError()

    @api_exceptions_handler
    def upload_file(self, data, file_fields):
        # print('API upload_file:', self, data, file_fields)
        # files = self.get_files(data, file_fields)
        # raise ValueError('ERR')
        try:
            with open(data['filepath'], 'rb') as file:
                # print('OK')
                return self._send_request('post', f'{self.host}{self.URL}/?X-Progress-ID={data["file_id"]}', data=data, files={'file':file}, json=False)
        except:
            # print('EX')
            print(f"File not found: {data['file_path']}")
            sys.exit()
        
