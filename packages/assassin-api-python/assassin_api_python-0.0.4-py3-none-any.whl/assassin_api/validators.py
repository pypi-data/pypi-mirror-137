
import sys
from contextlib import contextmanager

from .exceptions import *


@contextmanager
def disable_exception_traceback():
    """
    All traceback information is suppressed and only the exception type and value are printed
    """

    default_value = getattr(sys, "tracebacklimit", 1000)  # `1000` is a Python's default value
    sys.tracebacklimit = 0
    yield
    sys.tracebacklimit = default_value



class AssetValidator:

    @staticmethod
    def validate(obj):
        # print('OBJECT:')
        # for k, v  in obj.items():
        #     print()
        #     print(f'{k}: {v}')

        if obj.get('type', None):
            if type(obj['type']) is not int:
                if obj['type'] is not None:
                    obj['type'] = obj['type']['id']
            

        if obj.get('category', None):
            if type(obj['category']) is not int:
                if obj['category'] is not None:
                    obj['category'] = obj['category']['id']

        if obj.get('subcategory', None):
            if type(obj['subcategory']) is not int:
                if obj['subcategory'] is not None:
                    obj['subcategory'] = obj['subcategory']['id']

        has_preview = False
        previews_extensions = [
            '.jpg', '.jpeg', '.png', '.bmp', '.gif',
            '.webp', '.svg', '.wav', '.mp3', '.flac',
            '.mp4', '.mov', '.avi', '.mkv', '.wmv',
            '.pdf', '.hdr', '.exr'
        ]
        images_extensions = [
            '.jpg', '.jpeg', '.png', '.bmp',
            '.gif','.webp', '.svg'
        ]
        for f in obj['files']:
            try:
                f = dict(f)
            except:
                pass
            
            if type(f) == dict:
                for i in images_extensions:
                    if f.get('file', None):
                        if i in f['file']:
                            has_preview = True
                            break
            else:
                for i in previews_extensions:
                    if i in f:
                        has_preview = True
                        break
            if has_preview == True:
                break

        if not has_preview:
            with disable_exception_traceback():
                raise ValidationError({'files': 'At least one image is required'})

        return obj


class CreateAssetTypeValidator:

    @staticmethod
    def validate(obj):
        name = obj.get('name', None)
        # image = obj.get('image', None)

        if not name or not len(name.strip()):
            with disable_exception_traceback():
                raise ValidationError('Please provide new asset type name.')

        # if not image:
        #     with disable_exception_traceback():
        #         raise ValidationError('Please provide new asset type image.')

        return obj