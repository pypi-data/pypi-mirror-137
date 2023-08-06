
from cement import Controller, ex
from cement.utils.version import get_version_banner

from . import PaginationEnum
from ..core.version import get_version


VERSION_BANNER = """
CLI for Akinon Cloud Commerce %s
%s
""" % (get_version(), get_version_banner())


class Applications(Controller):
    class Meta:
        label = 'application'
        stacked_type = 'nested'
        stacked_on = 'base'
        description = 'this is the application controller namespace'

    @ex(
        help='Application List Command',
        arguments=[
            PaginationEnum.ARG
        ],
    )
    def list(self):
        response = self.app.client.get_applications(
            qs={"page": getattr(self.app.pargs, PaginationEnum.KEY)}
        )
        results = []
        for result in response.data.get("results", []):
            application_type_data = result["application_type"]
            result['application_type_slug'] = application_type_data["slug"] if application_type_data else ""
            results.append(result)
        self.app.render(data=response.data, rows=results,
                        headers={'pk': 'ID', 'slug': 'Slug', 'name': 'Name',
                                 'is_private': 'Is Private', 'status': 'Status',
                                 'clone_url': 'Clone URL',
                                 'application_type_slug': 'Application Type Slug'},
                        is_succeed=response.is_succeed)

    @ex(
        help='Application Create Command',
        arguments=[
            (['name'], {
                'help': 'Application name',
                'action': 'store',
            }),
            (['slug'], {
                'help': 'Application slug',
                'action': 'store',
            }),
            (['application_type_id'], {
                'help': 'Application type id',
                'action': 'store',
            }),
        ]
    )
    def create(self):
        data = {
            'name': self.app.pargs.name,
            'slug': self.app.pargs.slug,
            'application_type': self.app.pargs.application_type_id,
            'is_private': True,
        }
        response = self.app.client.create_application(data)
        if response.is_succeed:
            self.app.render({}, is_text=True, custom_text="App has been created.")
        else:
            self.app.render({}, is_text=True, custom_text=response.data['slug'][0])

    @ex(
        help='Application Update Command',
        arguments=[
            (['id'], {
                'help': 'Application ID',
                'action': 'store',
            }),
            (['name'], {
                'help': 'Application Name',
                'action': 'store',
            }),
            (['slug'], {
                'help': 'Application slug',
                'action': 'store',
            }),
        ]
    )
    def update(self):
        app_id = self.app.pargs.id
        data = {
            'name': self.app.pargs.name,
            'slug': self.app.pargs.slug,
        }
        response = self.app.client.update_application(app_id, data)
        if response.is_succeed:
            self.app.render({}, is_text=True, custom_text="App has been updated.")
        else:
            self.app.render({}, is_text=True, custom_text=response.data)

    @ex(
        help='Application Build Command',
        arguments=[
            (['id'], {
                'help': 'Application ID',
                'action': 'store',
            }),
            (['tag'], {
                'help': 'App Version',
                'action': 'store',
            })
        ]
    )
    def build(self):
        app_id = self.app.pargs.id
        data = {
            'tag': self.app.pargs.tag,
        }
        response = self.app.client.build_application(app_id, data)
        if response.is_succeed:
            self.app.render({}, is_text=True, custom_text="Build process has been started.")
        else:
            self.app.render({}, is_text=True, custom_text=response.data["non_field_errors"])

    @ex(
        help='Application Version List Command',
        arguments=[
            (['id'], {
                'help': 'Application ID',
                'action': 'store'
            }),
        ],
    )
    def versions(self):
        app_id = self.app.pargs.id
        response = self.app.client.get_app_versions(app_id)
        self.app.render(data=response.data, rows=response.data.get('results', []),
                        headers={'pk': 'ID', 'app': 'App', 'tag': 'Tag',
                                 'status': 'Status', 'created_date': 'CreatedDate'},
                        is_succeed=response.is_succeed)


class ApplicationTypes(Controller):
    class Meta:
        label = 'applicationtype'
        stacked_type = 'nested'
        stacked_on = 'base'
        description = 'this is the application type controller namespace'

    @ex(
        help='Application Type List Command',
        arguments=[
            PaginationEnum.ARG
        ],
    )
    def list(self):
        qs = {"is_visible_on_app_creation": True, "page": getattr(self.app.pargs, PaginationEnum.KEY)}
        response = self.app.client.get_application_types(qs=qs)
        self.app.render(data=response.data, rows=response.data.get('results', []),
                        headers={'pk': 'ID', 'slug': 'Slug', 'name': 'Name',
                                 'created_date': 'Created Date',
                                 'update_date': 'Updated Date'},
                        is_succeed=response.is_succeed)
