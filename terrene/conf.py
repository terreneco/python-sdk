"""
Configures the SDK
"""

import os
import ast


class Terrene:

    gui_server = {
        "host": "portal.terrene.co",
        "port": 443,
        "protocol": "https"
    }
    api_server = {
        "host": "api.terrene.co",
        "port": 443,
        "protocol": "https"
    }

    def __init__(self):
        if os.environ.get('GUI_SERVER', None) is not None:
            self.gui_server = ast.literal_eval(
                os.environ.get('GUI_SERVER', None))

        if os.environ.get('API_SERVER', None) is not None:
            self.api_server = ast.literal_eval(
                os.environ.get('API_SERVER', None))

    def configure(self, attr, val):
        setattr(self, attr, val)

terrene = Terrene()
