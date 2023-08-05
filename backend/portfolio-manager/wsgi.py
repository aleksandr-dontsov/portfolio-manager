# Flask development server can find any file named wsgi.py
# in the root directory, and since WSGI is a standard specification
# using it makes us sure that any HTTP server which might be used in production
# will be immediately working

import os

from app import create_app

# Use FLASK_CONFIG env variable to specify a config dynamically.
# It isn't a Flask environment variable and was added for the purpose
# described above
app = create_app(os.environ["FLASK_CONFIG"])
