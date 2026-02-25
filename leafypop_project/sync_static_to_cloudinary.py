import os
import django
from pathlib import Path

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'leafypop_project.settings')

# Load .env
from dotenv import load_dotenv
load_dotenv(os.path.join(os.path.dirname(__file__), '.env'))

django.setup()

import cloudinary
import cloudinary.uploader

# Configure Cloudinary
cloudinary_url = os.environ.get('CLOUDINARY_URL')
if cloudinary_url:
    cloudinary.config(cloudinary_url=cloudinary_url)
    print("Cloudinary configured.")

STATIC_IMAGES_DIR = Path(__file__).resolve().parent / 'store' / 'static' / 'store' / 'images'

files_to_upload = [
    'leafy_pop.png',
    'mascot.png',
    'education_real.jpeg',
    'companyname_D.png'
]

urls = {}

print("\n== Uploading Static Assets to Cloudinary ==")
for filename in files_to_upload:
    local_path = STATIC_IMAGES_DIR / filename
    if local_path.exists():
        print(f"  Uploading {filename}...")
        result = cloudinary.uploader.upload(
            str(local_path),
            public_id=filename.split('.')[0],
            folder='static_assets',
            overwrite=True
        )
        urls[filename] = result['secure_url']
        print(f"  [OK] -> {result['secure_url']}")
    else:
        print(f"  [ERROR] File not found: {local_path}")

print("\n== URLs to use in index.html ==")
for filename, url in urls.items():
    print(f"{filename}: {url}")
