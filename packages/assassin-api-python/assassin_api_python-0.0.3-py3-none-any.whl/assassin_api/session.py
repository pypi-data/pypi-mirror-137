from .api import UserRequest
from .exceptions import Error, InvalidQueryError
from .queries import (
    UserQuery, AssetTypeQuery, AssetCategoryQuery, AssetSubcategoryQuery, CollectionQuery, AuthorQuery, ProjectQuery,
    TagQuery, AssetQuery
)
from .mapping_models import (
    UserModel, AssetTypeModel, AssetCategoryModel, AssetSubcategoryModel, CollectionModel, ProjectModel,
    AuthorModel, TagModel, AssetModel
)


class Session(object):
    server = None
    user = None
    password = None
    token = None
    session_objects = []

    query_model_mapping = {
        'user': UserModel,
        'type': AssetTypeModel,
        'category': AssetCategoryModel,
        'subcategory': AssetSubcategoryModel,
        'collection': CollectionModel,
        'author': AuthorModel,
        'project': ProjectModel,
        'tag': TagModel,
        'asset': AssetModel
    }

    query_object_mapping = {
        'user': UserQuery,
        'type': AssetTypeQuery,
        'category': AssetCategoryQuery,
        'subcategory': AssetSubcategoryQuery,
        'collection': CollectionQuery,
        'author': AuthorQuery,
        'project': ProjectQuery,
        'tag': TagQuery,
        'asset': AssetQuery
    }

    def __init__(self, server, user, password):
        self.server = server
        self.host = self.server
        self.user = user
        self.password = password

    def connect(self):
        try:
            login = UserRequest(session=self).user_login(email=self.user, password=self.password)
            self.token = login.json()['access']
            return True
        except Error as e:
            raise e

    def create(self, obj_string):
        obj = None

        model = self.query_model_mapping.get(obj_string.lower().strip())
        if model is None:
            raise InvalidQueryError()

        obj = model({}, session=self)

        if obj is None:
            raise InvalidQueryError()
        obj.is_new = True
        self.session_objects.append(obj)
        return obj

    def query_object(self, query_model, query_parts):
        if len(query_parts) < 2:
            raise InvalidQueryError()
        if len(query_parts) == 2:
            return query_model
        if query_parts[2].lower().strip() == 'where':
            if len(query_parts) == 3:
                raise InvalidQueryError()
            if query_parts[3].lower().strip() == 'id':
                try:
                    id = int(query_parts[5])
                except TypeError:
                    raise InvalidQueryError()

                data_detail = query_model.detail(id)

                exists = False
                for o in self.session_objects:
                    # print()
                    # print(o.__class__.__name__, o['id'])
                    # print(data_detail.__class__.__name__, data_detail['id'])
                    # print()
                    # print(o.__class__ == data_detail.__class__ and o['id'] == data_detail['id'])

                    if o.__class__ == data_detail.__class__ and o['id'] == data_detail['id']:
                        self.session_objects[self.session_objects.index(o)] = data_detail
                        exists = True
                        break
                if not exists:
                    self.session_objects.append(data_detail)
                
                return query_model.base_model(data_detail, self)
            else:
                try:
                    query_string = ' '.join(query_parts[3:])
                    params = query_string.split('and')
                    param_dict = {}
                    for param in params:
                        if ' is ' in param:
                            param_parts = param.split(' is ')
                            param_dict[param_parts[0].strip().lower()] = param_parts[1].strip().lower()
                        if ' like ' in param:
                            param_parts = param.split(' like ')
                            param_dict[param_parts[0].strip().lower()] = param_parts[1].strip().lower()

                    query_model.set_query_params(param_dict)
                    return query_model
                except IndexError:
                    raise InvalidQueryError()
        else:
            raise InvalidQueryError()

    def query(self, request_str: str):
        # print('self:', self.__dict__)
        # print('request_str:', request_str)
        query_parts = request_str.split(' ')
        if len(query_parts) < 2 or query_parts[0].lower() != 'select':
            raise InvalidQueryError()

        query_model = self.query_object_mapping.get(query_parts[1].lower().strip())
        if query_model is None:
            raise InvalidQueryError()

        object = self.query_object(query_model(self), query_parts)
        # print('OBJECT:', object.__dict__)
        return object

    def commit(self):
        # print()
        # print('SESSION OBJECTS:')
        # for i, obj in enumerate(self.session_objects, start=1):
        #     print(f'{i}.')
        #     print('Class:', type(obj))
        #     print('Object:', obj.__dict__)
        #     print('Data:', obj)

        for obj in self.session_objects:
            obj = obj.commit()

        self.session_objects = list(filter(lambda o: not o.is_deleted, self.session_objects))

        # print()
        # print()
        # print('SESSION OBJECTS AFTER COMMIT:')
        # for i, obj in enumerate(self.session_objects, start=1):
        #     print(f'{i}.')
        #     print('Class:', type(obj))
        #     print('Object:', obj.__dict__)
        #     print('Data:', obj)