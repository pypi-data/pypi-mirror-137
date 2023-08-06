from cement.core.output import OutputHandler

from tabulate import tabulate


class AkinonOutputHandler(OutputHandler):
    class Meta:
        label = 'akinon_output_handler'

    def _render_data(self, rows, headers):
        table = []
        for datum in rows:
            row = []
            for col in headers.keys():
                value = datum[col]
                if isinstance(value, bool):
                    value = 'Yes' if value else 'No'
                row.append(value)
            table.append(row)

        print(tabulate(table, headers=headers.values(), tablefmt="grid", numalign="center"))

    def render(self, data, *args, **kwargs):
        is_text = kwargs.get('is_text', False)
        if is_text:
            print(kwargs.get('custom_text'))
            return
        headers = kwargs.get('headers')
        rows = kwargs.get('rows')
        is_succeed = kwargs.get('is_succeed', False)
        assert rows is not None
        assert isinstance(rows, list)
        assert headers is not None
        assert isinstance(headers, dict)

        if is_succeed:
            self._render_data(rows, headers)
        else:
            # self._render_error()
            self.app.log.error(data)

