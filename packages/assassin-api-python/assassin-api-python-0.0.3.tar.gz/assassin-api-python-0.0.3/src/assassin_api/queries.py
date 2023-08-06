from .api import (
    UserRequest, ApiRequest, AssetTypeRequest, AssetCategoryRequest, AssetSubcategoryRequest,
    CollectionRequest, ProjectRequest, AuthorsRequest, TagRequest, AssetRequest
)
from .exceptions import Error
from .mapping_models import (
    BaseModel, UserModel, AssetTypeModel, AssetCategoryModel, AssetSubcategoryModel, CollectionModel,
    AuthorModel, ProjectModel, TagModel, AssetModel
)


class BaseQuery(object):

    session = None
    request_model = ApiRequest
    base_model = BaseModel

    _query_params = {}

    def __init__(self, session):
        self.session = session

    def set_query_params(self, params):
        self._query_params = params

    def all(self):
        try:
            objs_to_return = []
            objs = self.request_model(self.session).get_objects_list(self._query_params).json()

            for obj in objs:
                # obj = self.detail(obj['id'])
                obj = self.base_model(obj, session=self.session)
                objs_to_return.append(obj)
                self.session.session_objects.append(obj)
            
            # print()
            # print('objs_to_return:', objs_to_return)
            return objs_to_return
        except Error as a:
            raise a

    def first(self):
        try:
            self._query_params['first'] = True
            obj = self.request_model(self.session).get_objects_list(self._query_params).json()[0]
            obj = self.detail(obj['id'])

            return obj
        except Error as a:
            return a
        except IndexError:
            return {}

    def one(self):
        try:
            self._query_params['one'] = True
            obj = self.request_model(self.session).get_objects_list(self._query_params).json()[0]
            obj = self.detail(obj['id'])
                        
            return obj
        except Error as a:
            return a
        except IndexError:
            return {}

    def last(self):
        try:
            self._query_params['last'] = True
            obj = self.request_model(self.session).get_objects_list(self._query_params).json()[0]
            obj = self.detail(obj['id'])

            return obj
        except Error as a:
            raise a
        except IndexError:
            return {}

    def detail(self, id):
        try:
            obj = self.request_model(self.session).get_object_detail(id).json()
            obj = self.base_model(obj, session=self.session)
            
            exists = False
            for o in self.session.session_objects:
                if o.__class__ == obj.__class__ and o['id'] == obj['id']:
                    self.session.session_objects[self.session.session_objects.index(o)] = obj
                    exists = True
                    break
            if not exists:
                self.session.session_objects.append(obj)
            
            return obj
        
        except Error as a:
            raise a
        except IndexError:
            return {}

    def __str__(self):
        return 'Please provide one of query methods: .first(), .one(), .last(), .all()'


class UserQuery(BaseQuery):
    request_model = UserRequest
    base_model = UserModel


class AssetTypeQuery(BaseQuery):
    request_model = AssetTypeRequest
    base_model = AssetTypeModel


class AssetCategoryQuery(BaseQuery):
    request_model = AssetCategoryRequest
    base_model = AssetCategoryModel


class AssetSubcategoryQuery(BaseQuery):
    request_model = AssetSubcategoryRequest
    base_model = AssetSubcategoryModel


class CollectionQuery(BaseQuery):
    request_model = CollectionRequest
    base_model = CollectionModel


class AuthorQuery(BaseQuery):
    request_model = AuthorsRequest
    base_model = AuthorModel

    def one(self):
        raise NotImplementedError()

    def detail(self, id):
        raise NotImplementedError()

    def first(self):
        raise NotImplementedError()

    def last(self):
        raise NotImplementedError()


class ProjectQuery(BaseQuery):
    request_model = ProjectRequest
    base_model = ProjectModel

    def one(self):
        raise NotImplementedError()

    def detail(self, id):
        raise NotImplementedError()

    def first(self):
        raise NotImplementedError()

    def last(self):
        raise NotImplementedError()


class TagQuery(BaseQuery):
    request_model = TagRequest
    base_model = TagModel

    def one(self):
        raise NotImplementedError()

    def detail(self, id):
        raise NotImplementedError()

    def first(self):
        raise NotImplementedError()

    def last(self):
        raise NotImplementedError()


class AssetQuery(BaseQuery):
    request_model = AssetRequest
    base_model = AssetModel
