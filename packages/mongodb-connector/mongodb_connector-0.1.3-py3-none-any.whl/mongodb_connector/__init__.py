__version__ = '0.1.0'
from . lark_sql import MongoSQLParser
from . mongodb_connector import *

__all__ = ['connect','MongoDBConnectorException', 'MongoSQLParser', 
'Warning', 'Error', 'InterfaceError','DataError','DatabaseError','OperationalError','IntegrityError','InternalError','ProgrammingError','NotSupportedError','MongoDBConnectorException']

"""

InterfaceError
   |__DatabaseError
      |__DataError
      |__OperationalError
      |__IntegrityError
      |__InternalError
      |__ProgrammingError
      |__NotSupportedError

"""