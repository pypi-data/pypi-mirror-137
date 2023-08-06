from cement import Controller, ex
from cement.utils.version import get_version_banner

from . import PaginationEnum
from ..core.version import get_version

VERSION_BANNER = """
CLI for Akinon Cloud Commerce %s
%s
""" % (get_version(), get_version_banner())


# class Clusters(Controller):
#     class Meta:
#         label = 'cluster'
#         stacked_type = 'nested'
#         stacked_on = 'base'
#         description = 'this is the cluster controller namespace'
#
#     @ex(
#         help='Cluster List Command',
#         arguments=[],
#     )
#     def list(self):
#         response = self.app.client.get_clusters()
#         self.app.render(data=response.data, rows=response.data.get('results', []),
#                         headers={'pk': 'ID', 'name': 'Name', 'code': 'Code',
#                                  'cloud_provider': 'Provider', 'zone': 'Zone'},
#                         is_succeed=response.is_succeed)
#
#
#

class KubeMetricMonitor(Controller):
    class Meta:
        label = 'metrics'
        stacked_type = 'nested'
        stacked_on = 'base'
        description = 'this is the kube metric monitor controller namespace'

    @ex(
        help='Metrics List Command',
        arguments=[
            (['cluster'], {
                'help': 'Application name',
                'action': 'store',
            }),
            (['namespace'], {
                'help': 'Application slug',
                'action': 'store',
            }),
            PaginationEnum.ARG
        ],
    )
    def list(self):
        response = self.app.client.get_metrics(
            cluster=self.app.pargs.cluster,
            namespace=self.app.pargs.namespace,
            qs={"page": getattr(self.app.pargs, PaginationEnum.KEY)}
        )
        self.app.render(data=response.data, rows=response.data,
                        headers={
                            'name': 'Name',
                            'containers': 'Containers',
                            'status': 'Status',
                        },
                        is_succeed=response.is_succeed)
