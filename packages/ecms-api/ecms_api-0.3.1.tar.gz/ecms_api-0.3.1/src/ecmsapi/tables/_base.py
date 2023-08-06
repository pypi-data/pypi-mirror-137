import os

__all__ = ['TableMixin']


class TableMixin:
    """
    Table Mixin class to get quick properties from the table
    """
    NAMESPACE = os.getenv('ECMS_HOST')
    FORIEGN_KEYS = {}

    def __init__(self):
        self.TABLE = self.__class__
        self.TABLE_NAME = self.__class__.__name__

    @property
    def namespace(self):
        return self.NAMESPACE

    @property
    def table(self):
        return self.TABLE.__class__.__name__

    @property
    def id(self):
        return f'{self.TABLE_NAME}ID'

    @property
    def cols(self):
        return [{k: v} for k, v in self.TABLE.__dict__.items() if '__' not in k]

    @property
    def column_names(self):
        return [col for cols in self.cols for col, _ in cols.items()]
