import logging
import sys
import os

logging.basicConfig(stream=sys.stderr)
sys.path.insert(0, '/var/www/garden-tracker/venv/')

print(sys.path)
from main import app as application

