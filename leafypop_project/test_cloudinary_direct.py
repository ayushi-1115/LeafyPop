import os
import cloudinary
import cloudinary.uploader
from dotenv import load_dotenv

# Load env
load_dotenv()

# Config
cloudinary.config(
    cloud_name="dxrz29nkw",
    api_key="568446338943447",
    api_secret="63vrzkJ51F-teHHHUjPPvJNPItA",
    secure=True
)

def test_upload():
    print("Testing direct Cloudinary upload...")
    test_file = "store/static/store/images/education_real.jpeg"
    
    if not os.path.exists(test_file):
        print(f"Error: {test_file} not found")
        return

    try:
        response = cloudinary.uploader.upload(test_file, folder="test/")
        print("Upload Success!")
        print(f"URL: {response.get('secure_url')}")
    except Exception as e:
        print(f"Upload Failed: {str(e)}")

if __name__ == "__main__":
    test_upload()
