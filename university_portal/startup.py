import os
from pathlib import Path
from dotenv import load_dotenv

def verify_env():
    """Force-load and verify environment variables"""
    env_path = Path(__file__).parent.parent / '.env'
    load_dotenv(env_path, override=True)
    
    required = [
        'CLOUDINARY_CLOUD_NAME',
        'CLOUDINARY_API_KEY',
        'CLOUDINARY_API_SECRET'
    ]
    
    missing = [var for var in required if not os.environ.get(var)]
    if missing:
        raise EnvironmentError(f"Missing ENV vars: {', '.join(missing)}")

verify_env()