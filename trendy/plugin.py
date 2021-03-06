"""
Plugin definition for the trendy Opal plugin
"""
from __future__ import unicode_literals


from opal.core import plugins, menus

from trendy.urls import urlpatterns


class TrendyPlugin(plugins.OpalPlugin):
    """
    Main entrypoint to expose this plugin to our Opal application.
    """
    urls = urlpatterns
    javascripts = {
        # Add your javascripts here!
        'opal.trendy': [
            'js/trendy/app.js',
            'js/trendy/directives.js',
            # 'js/trendy/app.js',
            # 'js/trendy/controllers/larry.js',
            # 'js/trendy/services/larry.js',
        ]
    }

    def list_schemas(self):
        """
        Return any patient list schemas that our plugin may define.
        """
        return {}

    def roles(self, user):
        """
        Given a (Django) USER object, return any extra roles defined
        by our plugin.
        """
        return {}

    menuitems = [
        menus.MenuItem(
            href="/trendy", display="Trendy", icon="fa fa-tasks",
            activepattern='/trendy', index=1)
    ]
