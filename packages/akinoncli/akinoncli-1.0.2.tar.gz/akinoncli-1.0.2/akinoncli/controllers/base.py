
from cement import Controller, ex
from cement.utils.version import get_version_banner

from ..core.version import get_version


VERSION_BANNER = """
CLI for Akinon Cloud Commerce %s
%s
""" % (get_version(), get_version_banner())


class Base(Controller):
    class Meta:
        label = 'base-url'
        stacked_type = 'nested'
        stacked_on = 'base'
        description = 'this is the base controller namespace'

    @ex(
        help='Set URLCommand',
        arguments=[
            (['url'], {
                'help': 'Base URL',
                'action': 'store',
            }),
        ],
    )
    def set(self):
        table = self.app.db.table('urls')
        if len(table) != 0:
            table.remove(doc_ids=[1])
        table.insert({'base_url': self._format_base_url(self.app.pargs.url)})

    def _format_base_url(self, base_url: str):
        if not base_url.endswith("/"):
            base_url += "/"
        if not base_url.endswith(f"/{self._api_suffix}"):
            base_url += self._api_suffix
        return base_url

    @property
    def _api_suffix(self) -> str:
        return "api/v1/"
