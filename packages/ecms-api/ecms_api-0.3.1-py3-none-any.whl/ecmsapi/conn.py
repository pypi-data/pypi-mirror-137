import os
import pyodbc


class Conn:

    """
    Connection to ecms 
    """

    host = os.getenv('ECMS_HOST')
    uid = os.getenv('ECMS_UID')
    pwd = os.getenv('ECMS_PWD')
    connection_string = f'DSN={host}; UID={uid}; PWD={pwd}'

    def execute(self, command):
        """
        Base execution method
        """
        try:
            conn = pyodbc.connect(self.connection_string)
            cur = conn.cursor()
            cur.execute(command)
            if 'SELECT' in command:
                resp = cur.fetchall()
                return list(resp)
            if 'UPDATE' in command:
                conn.commit()
            if 'INSERT' in command:
                conn.commit()
        except Exception as e:
            print(e)
