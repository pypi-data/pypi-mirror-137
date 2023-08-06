import uuid

from assassin_api.validators import AssetValidator
from .exceptions import Error, InvalidQueryError
from .api import (
    UserRequest, ApiRequest, AssetTypeRequest, AssetCategoryRequest, AssetSubcategoryRequest,
    CollectionRequest, AuthorsRequest, ProjectRequest, TagRequest, AssetRequest, AssetFileRequest
)


class BaseModel(dict):
    request_model = ApiRequest
    session = None
    is_new = False
    is_deleted = False
    file_fields = []
    custom_fields = None
    updated_fields = None

    def __init__(self, obj, session):
        self.session = session
        self.custom_fields = set()
        self.updated_fields = set()
        super(BaseModel, self).__init__(obj)
        

    def __setitem__(self, key, value):
        # print('SET ITEM:', self.__class__.__name__, self.__dict__,' <- (', key, ',', value, ')')
        # if self.is_deleted:
        #     raise Error('Was deleted')

        if self.__dict__.get(key) != value:
            self.updated_fields.add(key)
            super(BaseModel, self).__setitem__(key, value)

    def create_object(self):
        try:
            obj = self.request_model(self.session).create_object(self, self.file_fields).json()
            for key, value in obj.items():
                self[key] = value
            
            self.updated_fields.clear()
            self.custom_fields.clear()

            return self['id']
        except Error as a:
            raise a

    def update_object(self, id, data):

        # print()
        # print('UPDATE OBJECT DATA:', data)
        try:
            obj = self.request_model(self.session).update_object(id, data, self.file_fields).json()
            for key, value in obj.items():
                self[key] = value

            self.updated_fields.clear()
            self.custom_fields.clear()

            return self
        except Error as a:
            raise a

    def delete_object(self, id):
        try:
            self.request_model(self.session).delete_object(id)
            # input()
            # self.session.sesion_objects = list(filter(lambda x: x.get('id')!=id, self.session.sesion_objects))
            # print('SESSION OBJECTS:')
            # for object in self.session.session_objects:
            #     print(object['id'])
            # for object in self.session.session_objects:
            #     try:
            #         object = object.request_model(self.session).get_object_detail(object['id'])
            #         print('GOT OBJECT:')
            #     except Exception as e:
            #         print('ERROR GETTING OBJECT:', object, repr(e))
            #         try:
            #             print('DELETING OBJECT:', object)
            #             object.delete()
            #         except Exception as e:
            #             print('ERROR DELETING OBJECT:', object, repr(e))
            #             pass

        except Error as a:
            pass

    def delete(self):
        self.is_deleted = True

    def commit(self):
        updated_fields = {}
        id = self.get('id')
        if self.is_deleted and not self.is_new:
            self.delete_object(id)
            return None

        if self.is_new:
            self.create_object()
            self.is_new = False
            return self['id']

        # print()
        # print('self.updated_fields:', self.updated_fields)
        # print()
        # print('self.custom_fields:', self.custom_fields)
        # print()
        # print('self.updated_fields.difference(self.custom_fields):', self.updated_fields.difference(self.custom_fields))


        for field in self.updated_fields.difference(self.custom_fields):
            updated_fields[field] = self[field]

        if len(updated_fields.keys()) > 0:
            self.update_object(id, updated_fields)

        self.updated_fields.clear()
        # print('self.updated_fields.clear():', self.updated_fields.clear())

        return self['id']

    # def __getattribute__(self, name):
    #     def is_attribute_implemented():
    #         try:
    #             return super(BaseModel, self).__getattribute__(name)
    #         except AttributeError:
    #             return f'Method or attribute <{name}> not implemented for your query'
    #     return is_attribute_implemented


class UserModel(BaseModel):
    request_model = UserRequest
    old_user_groups = []

    def __setitem__(self, key, value):
        if self.is_deleted:
            raise Error('Was deleted')

        if key == 'groups':
            self.old_user_groups.extend(self['groups'])
            self.custom_fields.add(key)
        
        if key == 'password':
            self.custom_fields.add(key)

        super(UserModel, self).__setitem__(key, value)

    def add_user_to_groups(self, id, groups):
        try:
            result = UserRequest(self.session).add_user_to_groups(id, groups).json()
            return result
        except Error as a:
            raise a

    def remove_user_from_groups(self, id, groups):
        try:
            result = UserRequest(self.session).remove_user_from_groups(id, groups).json()
            return result
        except Error as a:
            raise a

    def change_password(self, id, password):
        try:
            result = self.request_model(self.session).change_password(id, password).json()
            return result
        except Error as a:
            raise a

    def commit(self):
        id = super(UserModel, self).commit()

        if id is None:
            return

        updated_fields = self.custom_fields

        if 'groups' in updated_fields:
            try:
                self.remove_user_from_groups(id, self.old_user_groups)
                self.add_user_to_groups(id, self['groups'])
            except Error:
                pass
        if 'password' in updated_fields:
            try:
                self.change_password(id, self['password'])
            except Error:
                pass
        self.custom_fields.clear()


class AssetTypeModelMixin(BaseModel):

    def change_order(self, id, order):
        try:
            result = self.request_model(self.session).change_order(id, order).json()
            return result
        except Error as a:
            raise a

    def __setitem__(self, key, value):
        if self.is_deleted:
            # print()
            # print()
            # print(self)
            # print()
            # print()
            # print(self.__dict__)
            # print()
            # print()
            raise Error('Instance was deleted earlier')

        if key in ('order', ):
            self.custom_fields.add(key)

        super(AssetTypeModelMixin, self).__setitem__(key, value)


class AssetSubcategoryModel(AssetTypeModelMixin):
    request_model = AssetSubcategoryRequest

    def commit(self):

        if type(self['category']) is not int:
            self['category'] = int(self['category']['id'])

        id = super(AssetSubcategoryModel, self).commit()

        if id is None:
            return

        updated_fields = self.custom_fields

        if 'order' in updated_fields:
            try:
                self.change_order(id, self['order'])
            except Error:
                pass

        self.custom_fields.clear()


class AssetCategoryModel(AssetTypeModelMixin):
    request_model = AssetCategoryRequest

    def commit(self):

        if type(self['type']) is not int:
            self['type'] = int(self['type']['id'])

        id = super(AssetCategoryModel, self).commit()

        if id is None:
            return

        updated_fields = self.custom_fields

        if 'order' in updated_fields:
            try:
                self.change_order(id, self['order'])
            except Error:
                pass

        self.custom_fields.clear()


class AssetTypeModel(AssetTypeModelMixin):
    file_fields = ['image']
    request_model = AssetTypeRequest

    def __setitem__(self, key, value):
        if self.is_deleted:
            raise Error('Was deleted')

        if key in ('available_asset_fields', 'available_file_types', 'order'):
            self.custom_fields.add(key)

        super(AssetTypeModel, self).__setitem__(key, value)

    def create_object(self):
        try:
            # print('SELF:', self)
            # print('SELF DICT:', self.__dict__)
            obj = self.request_model(self.session).create_object(self, self.file_fields).json()
            # print('AssetTypeModel create_object:', obj)
            for key, value in obj.items():
                if key in ('available_asset_fields', 'available_file_types') and obj[key] == ['{', '}']:
                    obj[key] = []
                self[key] = obj[key]

            self.updated_fields.clear()
            self.custom_fields.clear()

            return self['id']
        except Error as a:
            raise a

    def update_object(self, id, data):
        try:
            obj = self.request_model(self.session).update_object(id, data, self.file_fields).json()
            for key, value in obj.items():
                if key in ('available_asset_fields', 'available_file_types') and obj[key] == ['{', '}']:
                    obj[key] = []
                self[key] = obj[key]

            self.updated_fields.clear()
            self.custom_fields.clear()

            return obj
        except Error as a:
            raise a

    def update_attributes(self, id, available_asset_fields, available_file_types):
        try:
            result = self.request_model(self.session).update_attributes(
                id, available_asset_fields, available_file_types
            ).json()
            return result
        except Error as a:
            raise a

    def commit(self):
        id = super(AssetTypeModel, self).commit()

        if id is None:
            return

        updated_fields = self.custom_fields

        if 'order' in updated_fields:
            try:
                self.change_order(id, self['order'])
            except Error:
                pass

        if 'available_asset_fields' in updated_fields or 'available_file_types' in updated_fields:
            try:
                self.update_attributes(id, self['available_asset_fields'], self['available_file_types'])
            except Error:
                pass

        self.custom_fields.clear()


class CollectionModel(BaseModel):
    request_model = CollectionRequest


class AuthorModel(BaseModel):
    request_model = AuthorsRequest

    def create_object(self):
        raise NotImplementedError()

    def update_object(self, id, data):
        raise NotImplementedError()

    def delete_object(self, id):
        raise NotImplementedError()

    def delete(self):
        raise NotImplementedError()


class ProjectModel(BaseModel):
    request_model = ProjectRequest

    def create_object(self):
        raise NotImplementedError()

    def update_object(self, id, data):
        raise NotImplementedError()

    def delete_object(self, id):
        raise NotImplementedError()

    def delete(self):
        raise NotImplementedError()


class TagModel(BaseModel):
    request_model = TagRequest

    def update_object(self, id, data):
        raise NotImplementedError()

    def delete_object(self, id):
        raise NotImplementedError()

    def delete(self):
        raise NotImplementedError()


class AssetModel(BaseModel):
    request_model = AssetRequest

    def __setitem__(self, key, value):
        if key == 'rating':
            self.custom_fields.add(key)

        super(AssetModel, self).__setitem__(key, value)

    def set_rating(self, id, rating):
        try:
            result = self.request_model(self.session).set_rating(id, rating).json()
            return result
        except Error as a:
            raise a

    def upload_files(self):
        asset_files_field = 'files'
        current_asset_files = self.get(asset_files_field, [])
        current_asset_files_ids = []

        if len(current_asset_files):
            current_asset_files_ids = [f['file_id'] for f in current_asset_files if type(f) == dict] 
        
        new_asset_files = []
        files_and_previews_ids = []

        for file in current_asset_files:
            if type(file) is dict:
                files_and_previews_ids.append(file['file_id'])

            else:
                file = {'file_id':str(uuid.uuid4()), 'filepath':file}
                file = AssetFile(file, self.session)
                    
                try:
                    new_file_and_previews_ids = file.upload_file()['files_ids']
                    new_asset_files += new_file_and_previews_ids
                    files_and_previews_ids += new_file_and_previews_ids
                except Exception as e:
                    pass

        if files_and_previews_ids == current_asset_files_ids:
            return None

        return list(set(files_and_previews_ids))

    def commit(self):
        # print()
        # print()
        # print()
        # print('ASSET BEFORE VALIDATION:')
        # print(self)
        # print()
        
        validator = AssetValidator
        validator.validate(self)


        # print()
        # print()
        # print()
        # print('ASSET AFTER VALIDATION:')
        # print(self)
        # print()


        if not self.is_deleted:
            file_ids = self.upload_files()

            self['files'] = file_ids

            if file_ids is None:
                if 'files' in self.updated_fields:
                    self.updated_fields.remove('files')
            else:
                self.updated_fields.add('files')

            id = super(AssetModel, self).commit()

            updated_fields = self.custom_fields

            if 'rating' in updated_fields:
                try:
                    self.set_rating(id, self['rating'])
                except Error:
                    pass
            self.custom_fields.clear()

            try:
                updated_asset = AssetRequest(self.session).get_object_detail(id).json()
                for k, v in updated_asset.items():
                    self[k] = v

                self.custom_fields.clear()
                self.updated_fields.clear()
            except Error:
                pass


class AssetFile(BaseModel):
    request_model = AssetFileRequest
    file_fields = ['file']

    def create_object(self):
        raise NotImplementedError()

    def update_object(self, id, data):
        raise NotImplementedError()

    # def delete_object(self, id):
    #     raise NotImplementedError()

    def delete(self):
        raise NotImplementedError()

    def upload_file(self):
        try:
            result = self.request_model(self.session).upload_file(
                self, self.file_fields
            ).json()
            return result
        except Exception as e:
            raise e
