from cement import Controller, ex
from cement.utils.version import get_version_banner

from . import PaginationEnum
from ..core.version import get_version

VERSION_BANNER = """
CLI for Akinon Cloud Commerce %s
%s
""" % (get_version(), get_version_banner())


class PublicKeys(Controller):
    class Meta:
        label = 'publickey'
        stacked_type = 'nested'
        stacked_on = 'base'
        description = 'this is the public key controller namespace'

    @ex(
        help='Public Key List Command',
        arguments=[
            PaginationEnum.ARG
        ],
    )
    def list(self):
        response = self.app.client.get_public_keys(
            qs={"page": getattr(self.app.pargs, PaginationEnum.KEY)}
        )
        self.app.render(data=response.data, rows=response.data.get('results', []),
                        headers={'pk': 'ID', 'public_key': 'Public Key'},
                        is_succeed=response.is_succeed)

    @ex(
        help='Public Key Create Command',
        arguments=[
            (['key'], {
                'help': 'Public Key',
                'action': 'store',
            }),
        ]
    )
    def create(self):
        data = {
            'public_key': self.app.pargs.key,
        }
        response = self.app.client.create_public_key(data)
        if response.is_succeed:
            self.app.render({}, is_text=True, custom_text="Public Key added successfully.")
        else:
            self.app.render({}, is_text=True, custom_text=response.data.get('non_field_errors') or response.data.get('public_key'))

    @ex(
        help='Public Key Remove Command',
        arguments=[
            (['id'], {
                'help': 'Public Key ID',
                'action': 'store',
            }),
        ]
    )
    def remove(self):
        response = self.app.client.remove_public_key(self.app.pargs.id)
        if response.is_succeed:
            self.app.render({}, is_text=True, custom_text="Public Key removed successfully.")
        else:
            self.app.render({}, is_text=True,
                            custom_text=response.data.get('non_field_errors') or response.data)
