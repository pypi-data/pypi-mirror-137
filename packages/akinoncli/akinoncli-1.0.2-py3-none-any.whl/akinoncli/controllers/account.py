import json

from cement import Controller, ex
from cement.utils.version import get_version_banner

from . import PaginationEnum
from ..core.version import get_version


VERSION_BANNER = """
CLI for Akinon Cloud Commerce %s
%s
""" % (get_version(), get_version_banner())


class Domains(Controller):
    class Meta:
        label = 'domain'
        stacked_type = 'nested'
        stacked_on = 'base'
        description = 'this is the domain controller namespace'

    @ex(
        help='Domain List Command',
        arguments=[
            PaginationEnum.ARG
        ],
    )
    def list(self):
        response = self.app.client.get_domains(
            qs={"page": getattr(self.app.pargs, PaginationEnum.KEY)}
        )
        rows = response.data.get('results', [])
        for row in rows:
            row['extra'] = json.dumps(row['extra_data'], indent=4)
        self.app.render(data=response.data,
                        rows=response.data.get('results', []),
                        headers={'pk': 'ID',
                                 'hostname': 'Hostname',
                                 'is_usable': 'Is Usable',
                                 'is_managed': 'Is Managed',
                                 'extra': 'Extra Data'},
                        is_succeed=response.is_succeed)

    @ex(
        help='Domain Create Command',
        arguments=[
            (['hostname'], {
                'help': 'Hostname',
                'action': 'store',
            }),
            (['is_managed'], {
                'help': 'Is Managed',
                'action': 'store',
            }),
        ]
    )
    def create(self):
        data = {
            'hostname': self.app.pargs.hostname,
            'is_managed': self.app.pargs.is_managed,
        }
        response = self.app.client.create_domain(data)
        if response.is_succeed:
            self.app.render({}, is_text=True,
                            custom_text="Domain has been created.")
        else:
            custom_text = response.data.get('non_field_errors')
            if not custom_text:
                custom_text = response.data.get('hostname')[0]
            self.app.render({}, is_text=True, custom_text=custom_text)


class Certificates(Controller):
    class Meta:
        label = 'certificate'
        stacked_type = 'nested'
        stacked_on = 'base'
        description = 'this is the certificate controller namespace'

    @ex(
        help="Domain's Certificate List Command",
        arguments=[
            (['domain_id'], {
                'help': 'Domain ID',
                'action': 'store',
            }),
            PaginationEnum.ARG,
        ],
    )
    def list(self):
        domain_id = self.app.pargs.domain_id
        response = self.app.client.get_certificates(
            domain_id=domain_id,
            qs={"page": getattr(self.app.pargs, PaginationEnum.KEY)}
        )
        rows = response.data.get('results', [])
        for row in rows:
            row['hostname'] = row['domain']['hostname']
            row['extra'] = json.dumps(row['extra_data'], indent=4)
        self.app.render(data=response.data,
                        rows=response.data.get('results', []),
                        headers={'pk': 'ID',
                                 'fqdn': 'FQDN',
                                 'hostname': 'Hostname',
                                 'status': 'Status',
                                 'expire_date': 'Expire Date',
                                 'extra': 'Extra Data'},
                        is_succeed=response.is_succeed)

    @ex(
        help='Certificate Create Command',
        arguments=[
            (['domain_id'], {
                'help': 'Domain ID',
                'action': 'store',
            }),
            (['fqdn'], {
                'help': 'FQDN',
                'action': 'store',
            })
        ]
    )
    def create(self):
        data = {
            'fqdn': self.app.pargs.fqdn,
        }
        domain_id = self.app.pargs.domain_id
        response = self.app.client.create_certificate(domain_id=domain_id,
                                                      data=data)
        if response.is_succeed:
            self.app.render({}, is_text=True,
                            custom_text="Certificate has been created.")
        else:
            custom_text = response.data.get('non_field_errors')
            if not custom_text:
                custom_text = response.data.get('fqdn')[0]
            self.app.render({}, is_text=True, custom_text=custom_text)
