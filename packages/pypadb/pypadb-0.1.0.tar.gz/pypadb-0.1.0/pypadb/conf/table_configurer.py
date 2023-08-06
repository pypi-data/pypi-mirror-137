import inspect

from pypadb.table.base_table import BaseTable


class TableConfigurer:
    __slots__ = ['tables']

    tables: dict[str, BaseTable]

    def __init__(self):
        self.tables = {}

    def __getattr__(self, item: str) -> BaseTable:
        return self.tables[item]

    def __getitem__(self, item: str) -> BaseTable:
        return self.tables[item]

    def init_tables(self, module_=None, **kwargs):
        if inspect.ismodule(module_):
            self.tables = {**self.tables, **{kv[0].lower(): BaseTable(kv[0].lower(), kv[1]) for kv in
                                             inspect.getmembers(__import__('entities')) if not kv[0].startswith('_')}}
        if kwargs:
            self.tables = {**self.tables, **{key: BaseTable(key, kwargs[key]) for key in kwargs}}


tables: TableConfigurer = TableConfigurer()
