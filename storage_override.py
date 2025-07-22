from cloudinary_storage.storage import MediaCloudinaryStorage
from django.conf import settings

class ForceCloudinaryStorage(MediaCloudinaryStorage):
    def __init__(self):
        super().__init__(
            cloud_name=settings.CLOUDINARY_STORAGE['CLOUD_NAME'],
            api_key=settings.CLOUDINARY_STORAGE['API_KEY'],
            api_secret=settings.CLOUDINARY_STORAGE['API_SECRET']
        )

default_storage = ForceCloudinaryStorage()