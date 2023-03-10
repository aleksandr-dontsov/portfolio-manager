# Flask development server can find any file named wsgi.py
# in the root directory, and since WSGI is a standard specification
# using it makes us sure that any HTTP server which might be used in production
# will be immediately working

import os

from app import create_app

# Read config name
app = create_app(os.environ["FLASK_CONFIG"])
