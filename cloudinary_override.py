from django.core.files.storage import get_storage_class
from django.conf import settings

def get_cloudinary_storage():
    """Forcefully returns Cloudinary storage with correct config"""
    cloudinary_storage = get_storage_class('cloudinary_storage.storage.MediaCloudinaryStorage')
    return cloudinary_storage(
        cloud_name=settings.CLOUDINARY_STORAGE['CLOUD_NAME'],
        api_key=settings.CLOUDINARY_STORAGE['API_KEY'],
        api_secret=settings.CLOUDINARY_STORAGE['API_SECRET']
    )

default_storage = get_cloudinary_storage()