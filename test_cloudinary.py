import os
import django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'university_portal.settings')
django.setup()

from django.core.files.storage import default_storage
from django.core.files.base import ContentFile

print(f"Active storage: {default_storage.__class__.__name__}")

file = ContentFile(b"test content", name="test.txt")
url = default_storage.save("test_upload.txt", file)
print(f"Cloudinary URL: {url}")  # Should show cloudinary.com URL