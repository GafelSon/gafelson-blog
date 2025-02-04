import os
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables
env_path = (
    Path(__file__).resolve().parent.parent.parent
    / f'.env.{os.getenv("DJANGO_ENV", "development")}'
)
load_dotenv(dotenv_path=env_path)

from .base import *

if os.getenv("DJANGO_ENV") == "production":
    from .production import *
else:
    from .development import *
