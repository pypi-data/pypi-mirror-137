from calendar import c
import pandas as pd
import pyodbc
from .conn import Conn

__all__ = ['SQLQuery', ]


class QueryMixin:

    ALLOWABLE_OPERATORS = ['=', '<', '>', '<>', 'like']
    ALLOWABLE_METHODS = ['DELETE', 'SELECT', 'UPDATE', 'INSERT']

    def __init__(self, table):
        self.table = table()
        self.command = f"""
        {self.__class__.__name__.upper()} 
        COLS FROM {self.table.namespace}.{self.table.TABLE_NAME} 
        """
        if table.FORIEGN_KEYS:
            self.foriegn_keys = table.FORIEGN_KEYS
        else:
            self.foriegn_keys = {}
        super().__init__()

    def f_keys(self, column, value):
        """
        Checks to see if the Table has any foriegn keys and converts
        the provided column, value to that of the Parent table
        """
        if self.foriegn_keys:
            for f_key in self.foriegn_keys:
                if column.upper() in f_key.keys():
                    for col, ref in f_key.items():
                        query = SQLQuery(ref['table']).select().filter(col, value).to_df()
                        return {
                            'value': query[ref['ref']].head(1).item(),
                            'column' : ref['ref']}
        else:
            return None


    def filter(self, column: str, value, op: str = "="):
        """
        Accepts a column and value to add to the command
        Best used in situations that need an operator more specific
        than Equal To

        Base method for filters

        Column must be a column found witin the table or listed as 
        a Foreign key on the table    
        """
        f_keys = self.f_keys(column, value)
        if f_keys:
            column = f_keys['column']
            value = f_keys['value']
        
        if column.upper() in self.table.column_names:
            if op in self.ALLOWABLE_OPERATORS:
                if 'WHERE' not in self.command:
                    self.command += 'WHERE '
                else:
                    self.command += 'AND '
                self.command += f"{column.upper()} {op} '{value}' "
                return self
            else:
                raise ValueError(f'"{op}" is not an allowable operator')
        else:
            raise ValueError(
                f'{column.upper()} is not a column in {self.table}')

    def filters(self, **kwargs):
        """
        Accepts kwargs as column, value pairs to be used in 
        self.filter method
        """
        for col, val in kwargs.items():
            self.filter(col, val)
        return self

    def columns(self, columns: list):
        """
        Allows for columns to be narrowed down based on 
        columns available within the table
        """
        for col in columns:
            if col.upper() not in self.table.column_names:
                raise ValueError(f'{col} is not a column in {self.table}')
        self.columns = columns
        columns = ', '.join(columns).upper()
        self.command = self.command.replace('COLS', columns)

    def finalize_command(self):
        """
        Holder method to allow for each sub class to handle 
        the necessities specific to the query method
        """
        pass

    def query(self):
        """
        Pushing the query
        """
        self.finalize_command()
        return Conn().execute(self.command)

    def __str__(self):
        return self.command


class Select(QueryMixin):

    def __init__(self, table):
        super().__init__(table)
        

    def all(self):
        """
        Replaces current command with generall all command and runs the query
        """
        self.command = f'SELECT * FROM {self.table.NAMESPACE}.{self.table.TABLE_NAME} '
        return self.query()

    def order(self, by: str = '', order: str = 'ASC'):
        """
        Sets the order clause in the select statement
        """
        if not by:
            by = self.id
        self.command += f'ORDER BY {by} {order} '
        return self

    def limit(self, amount=1):
        """
        Sets the limit clause in the select statement
        """
        self.command += f'LIMIT {amount} '
        return self

    def head(self, amount=10):
        """
        Piggiebacks off the limit method but with a default of 10 
        """
        if 'LIMIT' not in self.command:
            self.limit(amount)
        return self

    def finalize_command(self):
        """
        Makes sure that if no columns were specified in the select
        that all columns are returned
        """
        if 'COLS' in self.command:
            self.command = self.command.replace('COLS', '*')
        print(self.command)
        

    def to_df(self):
        """
        Converts the select command returns into a pandas dataframe
        """
        self.finalize_command()
        conn = pyodbc.connect(Conn.connection_string)
        return pd.read_sql(self.command, conn)

    def to_excel(self, name='export', index=False, header=True):
        """
        Takes the Select query and exports it to an excel doc with the default 
        name of export
        """
        name = name + '.xlsx'
        self.to_df().to_excel(name, index=index, header=header)


class Update(QueryMixin):

    def __init__(self, table):
        super().__init__(table)

    def set(self, column, value):
        """
        Adds the SET command to the update query
        """
        if 'SET' not in self.command:
            self.command += 'SET '
        else:
            self.command += ', '
        self.command += f"{column.upper()} = '{value}' "
        return self

    def sets(self, **kwargs):
        """
        Sends kwargs to the self.set method to allow for multiple values
        """
        for col, val in kwargs.items():
            self.set(col, val)
        return self

    def finalize_command(self):
        """
        Makes sure that COLS and FROM are not present in the query
        Makes sure that a SET method was called
        Makes sure that a filter was placed on the query
        """
        if 'COLS' in self.command:
            self.command = self.command.replace('COLS ', '')
        if 'FROM' in self.command:
            self.command = self.command.replace('FROM ', '')
        if 'SET' not in self.command:
            raise SyntaxError('SET method missing from query')
        if 'WHERE' not in self.command:
            raise SyntaxError('Filter need to prevent query overload')

class Insert(QueryMixin):
    def __init__(self, table):
        super().__init__(table)
        self.command += '(COLS) VALUES (VALS) ' 
        self.insert_cols = []
        self.insert_vals = []
        if table().DEFAULTS:
            self.insert_defaults(table().DEFAULTS)
            
    def insert_defaults(self, defaults):
        """
        Inserts default column values into the query if not 
        specified 
        """
        for default in defaults:
            self.insert_cols.append(f'"{default[0]}"')
            self.insert_vals.append(f"'{default[1]}'")

    def insert(self, column: str, value):
        """
        Accepts a column and value to add to the command
        Base method for insert

        Column must be a column found witin the table or
        listed as a foreign key       
        """
        f_keys = self.f_keys(column, value)
        if f_keys:
            column = f_keys['column']
            value = f_keys['value']

        if column.upper() in self.table.column_names:
            self.insert_cols.append(f'"{column.upper()}"')
            self.insert_vals.append(f"'{value}'")
        else:
            raise ValueError(
                f'{column.upper()} is not a column in {self.table}')

    def inserts(self, **kwargs):
        """
        Accepts kwargs as column, value pairs to be used in 
        self.insert method
        """
        for col, val in kwargs.items():
            self.insert(col, val)
        return self


    def finalize_command(self):
        """
        Makes sure that COLS and FROM are not present in the query
        Makes sure that a SET method was called
        Makes sure that a filter was placed on the query
        """
        
        if 'COLS' in self.command:
            self.command = self.command.replace('COLS ', '')
        if 'FROM' in self.command:
            self.command = self.command.replace('FROM ', 'INTO ')
        if 'INSERT' not in self.command:
            raise SyntaxError('INSERT missing from query')
        if 'WHERE' in self.command:
            raise SyntaxError('Incorrect syntax, please remove filters')

        self.command = self.command.replace('COLS', ', '.join(self.insert_cols))
        self.command = self.command.replace('VALS', ', '.join(self.insert_vals))


class Delete(QueryMixin):
    pass


class SQLQuery:
    """
    Factory method that returns a query method with a table parameter
    """

    def __init__(self, table):
        self.table = table

    def select(self):
        return Select(self.table)

    def update(self):
        return Update(self.table)

    def delete(self):
        return Delete(self.table)

    def insert(self):
        return Insert(self.table)
