import re
from pymongo import MongoClient
from . lark_sql import MongoSQLParser

class MongoDBConnectorException(Exception):
    pass

class MongoDBCursor():

    arraysize = 100
    """This read/write attribute specifies the number of rows to fetch at a time with .fetchmany(). It defaults to 1 meaning to fetch a single row at a time.
    Implementations must observe this value with respect to the .fetchmany() method, but are free to interact with the database a single row at a time. It may also be used in the implementation of .executemany().
    """

    def __init__(self, client , database):
        self.client = client
        self.database = database
        self.parser = MongoSQLParser.get_instance()
        print("MongoDB Cursor created")

    def callproc(procname, *args):
        raise MongoDBConnectorException("Not implemented")

    def close(self):
        self.client.close()

    def execute(self, operation, *args):
        print("execute", operation)

        try:
            parsed = self.parser.parse(operation)
            if parsed["statement"] == "select":
                print("select")
                collection = parsed["table"]
                print(collection)
                print(parsed["where"])
                self.cursor = self.client[self.database][collection].find(parsed["where"])
                print("select done.")
            elif parsed["statement"] == "insert":
                print("insert")
                collection = parsed["table"]
                k = parsed["columns"] # name, year
                v = parsed["values"]  # mike 30
                obj = {}
                for i in range(len(k)):
                    obj[ k[i] ] = v[i]
                self.client[self.database][collection].insert_one(obj)
                self.cursor = None
                print("insert done.")
            elif parsed["statement"] == "update":
                print("update")
                collection = parsed["table"]
                self.client[self.database][collection].update_many(parsed["where"],{'$set': parsed["set"]})
                self.cursor =  None
                print("update done!!")
            elif parsed["statement"] == "delete":
                print("delete")
                collection = parsed["table"]
                print("parsed[where]", parsed["where"])
                # self.client[self.database][collection].delete_many(parsed["where"])
                # {"name": {"$eq": "Charly"}}
                self.client[self.database][collection].delete_many({"name": {"$eq": "Charly"}})
                self.cursor = None
            elif parsed["statement"] == "create":
                collection = parsed["table"]
                self.client[self.database][collection]
            elif parsed["statement"] == "drop":
                collection = parsed["table"]
                self.client[self.database][collection].drop()
            else:
                raise MongoDBConnectorException("Not implemented")
        except Exception as e:
            raise MongoDBConnectorException("Invalid SQL statement", e)

    def executemany( self, operation, seq_of_parameter ):
        pass

    def fetchone(self):
        if self.cursor is not None:
            return self.cursor.next()
        else:
            return None

    def fetchmany(self):
        """ Fetch the next set of rows of a query result, returning a sequence of sequences (e.g. a list of tuples). An empty sequence is returned when no more rows are available.
            The number of rows to fetch per call is specified by the parameter. If it is not given, the cursor's arraysize determines the number of rows to be fetched. The method should try to fetch as many rows as indicated by the size parameter. If this is not possible due to the specified number of rows not being available, fewer rows may be returned.
            An Error (or subclass) exception is raised if the previous call to .execute*() did not produce any result set or no call was issued yet.
            Note there are performance considerations involved with the size parameter. For optimal performance, it is usually best to use the .arraysize attribute. If the size parameter is used, then it is best for it to retain the same value from one .fetchmany() call to the next.
        """
        ret = []
        if self.cursor is not None:
            for i in range(self.arraysize):
                try:
                    ret.append(self.cursor.next())
                except StopIteration:
                    break
        return ret

    def fetchall(self):
        """Fetches all (remaining) rows of a query result, returning them as a sequence of sequences (e.g. a list of tuples). Note that the cursor's arraysize attribute can affect the performance of this operation.
            An Error (or subclass) exception is raised if the previous call to .execute*() did not produce any result set or no call was issued yet.
        """
        ret = []
        if self.cursor is not None:
            for i in self.cursor:
                ret.append(i)
        return ret

    def setinputsizes(self, sizes):
        """
            This can be used before a call to .execute*() to predefine memory areas for the operation's parameters.
            sizes is specified as a sequence — one item for each input parameter. The item should be a Type Object that corresponds to the input that will be used, or it should be an integer specifying the maximum length of a string parameter. If the item is None, then no predefined memory area will be reserved for that column (this is useful to avoid predefined areas for large inputs).
            This method would be used before the .execute*() method is invoked.
            Implementations are free to have this method do nothing and users are free to not use it.
        """
        pass


    def setoutputsize(self, size, column):
        """
            Set a column buffer size for fetches of large columns (e.g. LONGs, BLOBs, etc.). The column is specified as an index into the result sequence. Not specifying the column will set the default size for all large columns in the cursor.
            This method would be used before the .execute*() method is invoked.
            Implementations are free to have this method do nothing and users are free to not use it.
        """
        pass



class MongoDBConnection():
    def __init__(self,host:str,port:int=None, user:str=None, password:str=None, database:str=None):
        self.host = host

        if port is not None:
            try:
                self.port = int(port)
            except Exception as e:
                raise MongoDBConnectorException("Invalid port number", e)
        else:
            self.port = 27017

        self.user = user
        self.password = password
        self.database = database

        if self.database is None:
            raise MongoDBConnectorException("Database name is not specified")
        
        user_pass =""
        if user is not None:
            user_pass = user + ":" + password + "@"

        uri = "mongodb://" + user_pass + host + ":" + str(port)
        try:
            self.client = MongoClient(uri)
        except Exception as e:
            raise MongoDBConnectorException("Invalid mongodb connection configuration", e)
    
    def close(self):
        self.client.close()
        print("MongoDB Connection closed")

    def commit(self):
        pass

    def rollback(self):
        pass

    def cursor(self)->MongoDBCursor:
        return MongoDBCursor(self.client, self.database)



def connect(uri:str)->MongoDBConnection:
    """Connect to MongoDB
    :param uri: MongoDB URI (e.g. mongodb://user:password@localhost:27017/db)
    :return: MongoDBConnection
    """
    match = re.match(r'^mongodb://((?P<user>.*):(?P<password>.*)@)?(?P<host>.*?)(:(?P<port>[1-9][0-9]*))?/(?P<database>.*)$', uri)
    d = match.groupdict()
    return MongoDBConnection(d["host"], int(d["port"]), d["user"], d["password"], d["database"])



apilevel = 2.0
threadsafety = 0
paramstyle = "qmark"


"""
Connection methods
.close()
Close the connection now (rather than whenever .__del__() is called).

The connection will be unusable from this point forward; an Error (or subclass) exception will be raised if any operation is attempted with the connection. The same applies to all cursor objects trying to use the connection. Note that closing a connection without committing the changes first will cause an implicit rollback to be performed.

.commit()
Commit any pending transaction to the database.

Note that if the database supports an auto-commit feature, this must be initially off. An interface method may be provided to turn it back on.

Database modules that do not support transactions should implement this method with void functionality.

.rollback()
This method is optional since not all databases provide transaction support. [3]

In case a database does provide transactions this method causes the database to roll back to the start of any pending transaction. Closing a connection without committing the changes first will cause an implicit rollback to be performed.

.cursor()
Return a new Cursor Object using the connection.

If the database does not provide a direct cursor concept, the module will have to emulate cursors using other means to the extent needed by this specification. [4]

"""

"""
Constructors
Access to the database is made available through connection objects. The module must provide the following constructor for these:

connect( parameters... )
Constructor for creating a connection to the database.

Returns a Connection Object. It takes a number of parameters which are database dependent. [1]

Globals
These module globals must be defined:

apilevel
String constant stating the supported DB API level.

Currently only the strings "1.0" and "2.0" are allowed. If not given, a DB-API 1.0 level interface should be assumed.

threadsafety
Integer constant stating the level of thread safety the interface supports. Possible values are:

threadsafety	Meaning
0	Threads may not share the module.
1	Threads may share the module, but not connections.
2	Threads may share the module and connections.
3	Threads may share the module, connections and cursors.
Sharing in the above context means that two threads may use a resource without wrapping it using a mutex semaphore to implement resource locking. Note that you cannot always make external resources thread safe by managing access using a mutex: the resource may rely on global variables or other external sources that are beyond your control.

paramstyle
String constant stating the type of parameter marker formatting expected by the interface. Possible values are [2]:

paramstyle	Meaning
qmark	Question mark style, e.g. ...WHERE name=?
numeric	Numeric, positional style, e.g. ...WHERE name=:1
named	Named style, e.g. ...WHERE name=:name
format	ANSI C printf format codes, e.g. ...WHERE name=%s
pyformat	Python extended format codes, e.g. ...WHERE name=%(name)s
"""