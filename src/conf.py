"""
Configures the SDK
"""

import os
import ast

GUI_SERVER = {
    "host": "portal.terrene.co",
    "port": "443",
    "protocol": "https"
}

API_SERVER = {
    "host": "api.terrene.co",
    "port": "443",
    "protocol": "https"
}

if os.environ.get('GUI_SERVER', None) is not None:
    GUI_SERVER = ast.literal_eval(os.environ.get('GUI_SERVER', None))

if os.environ.get('API_SERVER', None) is not None:
    API_SERVER = ast.literal_eval(os.environ.get('API_SERVER', None))
