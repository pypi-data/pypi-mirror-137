import os

from akinoncli.controllers.clusters import KubeMetricMonitor
from tinydb import TinyDB
from cement.utils import fs
from cement import App, TestApp, init_defaults
from cement.core.exc import CaughtSignal

from akinoncli.controllers.account import Domains, Certificates
from akinoncli.ext.output_renderer import AkinonOutputHandler
from akinoncli.client.client import AkinonCloudClient
from akinoncli.core.exc import AkinonCLIError, AkinonCLIWarning

from akinoncli.controllers.base import Base
from akinoncli.controllers.auth import Auth
# from .controllers.clusters import Clusters
from akinoncli.controllers.projects import Projects, ProjectApps, Addons
from akinoncli.controllers.applications import Applications, ApplicationTypes
# from .controllers.applications import ApplicationUsers
from akinoncli.controllers.public_keys import PublicKeys

# from .controllers.users import Users, Roles

# configuration defaults
CONFIG = init_defaults('akinoncli')
CONFIG['akinoncli']['db_file'] = '~/.akinoncli/db.json'


def extend_tinydb(app):
    db_file = app.config.get('akinoncli', 'db_file')
    db_file = fs.abspath(db_file)
    # ensure our parent directory exists
    db_dir = os.path.dirname(db_file)
    if not os.path.exists(db_dir):
        os.makedirs(db_dir)

    app.extend('db', TinyDB(db_file))


def extend_client(app):
    urls_table = app.db.table('urls')
    base_url = 'http://localhost:8000/api/v1/'
    if len(urls_table) > 0:
        base_url = urls_table.get(doc_id=1).get('base_url')
    user = app.db.get(doc_id=1)
    token = None
    if user:
        token = user.get('token')
    app.extend('client', AkinonCloudClient(base_url, token))


class AkinonCLI(App):
    """Akinon CLI primary application."""

    class Meta:
        label = 'akinoncli'

        # configuration defaults
        config_defaults = CONFIG

        # call sys.exit() on close
        exit_on_close = True

        # load additional framework extensions
        extensions = [
            'yaml',
            'colorlog',
        ]

        # configuration handler
        config_handler = 'yaml'

        # configuration file suffix
        config_file_suffix = '.yml'

        # set the log handler
        log_handler = 'colorlog'

        # set the output handler
        output_handler = 'akinon_output_handler'

        # register handlers
        handlers = [
            AkinonOutputHandler,
            Base,
            Auth,
            # Clusters,
            Projects,
            ProjectApps,
            Applications,
            # ApplicationUsers,
            ApplicationTypes,
            PublicKeys,
            # Users,
            # Roles,
            Domains,
            Certificates,
            Addons,
            KubeMetricMonitor,
        ]

        hooks = [
            ('post_setup', extend_tinydb),
            ('post_setup', extend_client),
        ]


class AkinonCLITest(TestApp, AkinonCLI):
    """A sub-class of AkinonCLI that is better suited for testing."""

    class Meta:
        label = 'akinoncli'


def main():
    with AkinonCLI() as app:
        try:
            app.run()

        except AssertionError as e:
            print(f'AssertionError > {e.args[0]}')
            app.exit_code = 1

            if app.debug is True:
                import traceback
                traceback.print_exc()

        except AkinonCLIError as e:
            app.log.error(f'{e.message}')
            app.exit_code = 1

            if e.response is not None:
                app.log.error(e.response.text)
            if app.debug is True:
                import traceback
                traceback.print_exc()
        except AkinonCLIWarning as e:
            app.log.warning(f'{e.message}')
        except CaughtSignal as e:
            # Default Cement signals are SIGINT and SIGTERM, exit 0 (non-error)
            print(f'\n{e}')
            app.exit_code = 0


if __name__ == '__main__':
    main()
