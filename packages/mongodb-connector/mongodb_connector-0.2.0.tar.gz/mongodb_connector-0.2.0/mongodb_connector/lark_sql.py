import logging
from lark import Lark, logger, Transformer
from lark.lexer import Token
import mongodb_connector

"""
?start: value
 
?value: object
        | array
        | string
        | SIGNED_NUMBER      -> number
        | "true"             -> true
        | "false"            -> false
        | "null"             -> null
 
array  : "[" [value ("," value)*] "]"
object : "{" [pair ("," pair)*] "}"
pair   : string ":" value
 
string : ESCAPED_STRING
 
%import common.ESCAPED_STRING
%import common.SIGNED_NUMBER
%import common.WS
 
%ignore WS
"""

GRAMMAR = '''

?start: select_statement|insert_statement|update_statement|delete_statement|create_statement|drop_statement

//ルール
select_statement: SELECT columns [FROM table_name] [where_clause] [order_by_clause] [limit_clause]

//INSERT INTO テーブル名 (列名1, 列名2,...) VALUES (値1, 値2,...);
insert_statement: INSERT INTO table_name "(" columns ")" VALUES "(" values ")"

// UPDATE (表名) SET (カラム名1) = (値1), (カラム名2) = (値2) WHERE (条件);
update_statement: UPDATE table_name SET assigns [where_clause]

// DELETE (表名) FROM (テーブル名) WHERE (条件);
delete_statement: DELETE FROM table_name [where_clause]

//CREATE TABLE (テーブル名) (列名1 型1, 列名2 型2,...)
create_statement: CREATE TABLE table_name "(" COLUMN type ("," COLUMN type)* ")"

//DROP TABLE (テーブル名)
drop_statement: DROP TABLE table_name

columns:  ANY | COLUMN ("," COLUMN)*
values: value ("," value)*
order_by_clause: ORDER BY COLUMN [ASC|DESC]
where_clause: WHERE expression
limit_clause: LIMIT INT

expression: and_condition [OR and_condition]
and_condition: condition (AND condition)*
condition: compare | "(" expression ")"
compare: term COMPARE term

assigns: (COLUMN "=" value) ("," COLUMN "=" value)*

value: SIGNED_INT | SIGNED_FLOAT | STRING  |NULL | boolean
term: value | COLUMN
boolean: TRUE | FALSE
TRUE.2: "true"|"True"|"TRUE"
FALSE.3: "false"|"False"|"FALSE"
NULL.5: "NULL"|"null"|"Null"


//終端記号
table_name: WORD
ANY.10: "*"
COLUMN.1: WORD
STRING: ESCAPED_STRING

SELECT: "SELECT"|"select"
FROM: "FROM"|"from"
WHERE: "WHERE"|"where"
ORDER: "ORDER"|"order"
BY: "BY"|"by"
ASC: "ASC"|"asc"
DESC: "DESC"|"desc"
LIMIT: "LIMIT"|"limit"
INSERT: "INSERT"|"insert"
INTO: "INTO"|"into"
VALUES: "VALUES"|"values"
UPDATE: "UPDATE"|"update"
SET: "SET"|"set"
DELETE: "DELETE"|"delete"
OR: "OR"|"or"
AND: "AND"|"and"
NOT: "NOT"|"not"
COMPARE:"<>"|"<="|">="|"<"|">"|"="|"!="
CREATE: "CREATE"|"create"
DROP: "DROP"|"drop"
TABLE: "TABLE"|"table"

type:  TYPE_BOOLEAN| TYPE_INT | TYPE_DECIMAL | TYPE_VARCHAR | TYPE_TIME

// 型情報　ただし使われません
TYPE_BOOLEAN: "BOOLEAN"|"boolean"
TYPE_INT: "INT"|"int"
TYPE_DECIMAL: "DECIMAL"|"decimal"
TYPE_VARCHAR: "VARCHAR"|"varchar"
TYPE_TIME: "TIME"|"time"

// サポートできていないもの
// IS: "IS"|"is"
// LIKE: "LIKE"|"like"
// IN: "IN"|"in"
// BETWEEN: "BETWEEN"|"between"
// JOIN: "JOIN"|"join"

//共通記号
%import common.ESCAPED_STRING
%import common.SIGNED_FLOAT
%import common.SIGNED_INT
%import common.INT
%import common.WORD
%import common.WS
%ignore WS
'''

#  FROM_CLAUSE WHERE_CLAUSE
# %import common.SIGNED_NUMBER

# pymongo cursor


class SQLTransformer(Transformer):

    def __clear(self):
        self.parsed_data = {}

    def __init__(self):
        self._functions = {}
        self.parsed_data = {}


    def select_statement(self, parsed):
        print("Select statement", parsed)
        ret = {
            "statement": "select",
            "table": parsed[3],
            "columns": parsed[1],
        }
        # SELECT[0] *[1] FROM[2] table[3] [WHERE[4] condition[5]] [ORDER BY[6] column[7] [ASC|DESC[8]]] [LIMIT[9] limit[10]]

        for i in range(4, len( parsed )):
            clause = parsed[i][0]
            ret[clause] = parsed[i][1]
        print(ret)
        return ret

    def columns(self, parsed):
        print("columns ", parsed)
        if type(parsed[0]) == Token and parsed[0].type == "ANY":
            return [parsed[0].value]
        else:
            ret = []
            for i in range(len(parsed)):
                ret.append(parsed[i].value)
            return ret

    # exexpression: and_condition [OR and_condition]
    def expression(self, parsed):
        if len( parsed ) == 3:
            # OR condition
            return {
                "$or":[
                    parsed[0],
                    parsed[2]
                ]
            }
        else:
            return parsed[0]

    # condition: compare | "(" expression ")"
    def condition(self, parsed):
        if len(parsed) == 1:
            return parsed[0]
        else:
            return parsed[1] # parsed expression

    # and_condition: condition (AND condition)*
    def and_condition(self, parsed):
        print("And condition", parsed)
        if len( parsed ) >= 3:
            # AND condition
            return {
                [parsed[i] for i in range(len(parsed)) if i % 2 == 0]
            }
        else:
            print("return parsed[0]",parsed[0])
            return parsed[0]

    def where_clause(self,paserd):
        print("Where" , paserd)
        paserd[0] = "where"
        return paserd

    def __get_column(self, token):
        if type(token) is Token and token.type == "COLUMN":
            print("__get_column", token.value)
            return token.value
        return None
    

    # COMPARE:"<>"|"<="|">="|"<"|">"|"="|"!="
    def __to_mongo_condition(self, obj ):
        print(obj,)
        if obj["op"] == "<>" or obj["op"] == "!=":
            return {
                obj["left"]["value"]  : { "$ne": obj["right"]["value"] }
            }
        elif obj["op"] == "<=":
            return {
                obj["left"]["value"]  : { "$lte": obj["right"]["value"] }
            }
        elif obj["op"] == ">=":
            return {
                obj["left"]["value"] : { "$gte": obj["right"]["value"] }
            }
        elif obj["op"] == "<":
            return {
                obj["left"]["value"]: { "$lt": obj["right"]["value"] }
            }
        elif obj["op"] == ">":
            return {
                obj["left"]["value"]: { "$gt": obj["right"]["value"] }
            }
        elif obj["op"] == "=":
            return {
                obj["left"]["value"]: { "$eq": obj["right"]["value"] }
            }
        else:
            raise ValueError("Unknown operator")
    

    def compare(self, tokens):
        print("compare ", tokens, type(tokens[0]), type(tokens[1]), type(tokens[2]))

        ret = {
            "left": {},
            "op": None,
            "right": {}
        }

        c = self.__get_column(tokens[0])
        if c is None:
            ret["left"]["value"] = tokens[0]
        else:
            ret["left"] = {
                "type": "column",
                "value": c
            }

        # "<>"|"<="|">="|"<"|">"|"="|"!="
        ret["op"] = tokens[1].value
        
        c = self.__get_column(tokens[2])
        if c is None:
            ret["right"]["value"] = tokens[2]
        else:
            ret["right"] = {
                "type": "column",
                "value": c
            }

        v = self.__to_mongo_condition(ret)
        return v
    
    def order_by_clause(self,parsed):
        print("order by ",parsed)
        ret = {
            "sort": parsed[2].value,
        }
        if len(parsed)>2:
            ret["sort_order"] = parsed[3].value
        return ["order_by", ret]

    def limit_clause(self,tokens):
        print("limit", tokens)
        return ["limit", tokens[1].value]

    def insert_statement(self, parsed):
        print("Insert statement", parsed)
        ret ={
            "statement": "insert",
            "table": parsed[2],
            "columns": parsed[3],
            "values": parsed[5]
        }
        print(ret)
        return ret
    
    def values(self, parsed):
        print("Values", parsed)
        return parsed
    
    def update_statement(self, parsed):
        # UPDATE table SET assigns [where_clause]
        print("Update statement", parsed )

        ret = {
            "statement": "update",
            "table": parsed[1],
            "set": parsed[3]
        }

        if len(parsed) == 5:
            ret["where"] = parsed[4][1]

        return ret
    
    def assigns(self,parsed):
        ret = {}
        for i in range(0, len(parsed), 2):
            print(parsed[i], parsed[i+1])
            ret[parsed[i].value] = parsed[i+1]
        return ret

    def delete_statement(self, parsed):
        print("Delete statement", parsed)
        ret = {
            "statement": "delete",
            "table": parsed[2],
        }
        if len(parsed) > 3:
            ret["where"] = parsed[3][1]
        print(ret)
        return ret

    def create_statement(self, parsed):
        print("Create statement",parsed)
        ret = {
            "statement": "create",
            "table": parsed[2]
        }
        return ret


    def drop_statement(self, parsed):
        print("Drop statement")
        ret = {
            "statement": "drop",
            "table": parsed[2]
        }
        return ret

    def table_name(self, tree):
        print("table_func " , type(tree[0].value), tree[0])
        return tree[0].value

    def boolean(self, tokens):
        b = tokens[0].value
        ret = bool(b.upper())
        return ret

    def null(self, token ):
        return None
    
    def value(self, t):
        if type(t) is list:
            if t[0].type=='SIGNED_INT':
                return int(t[0].value)
            elif t[0].type == 'SIGNED_FLOAT':
                return float(t[0].value)
            elif t[0].type == 'STRING':
                s = t[0].value[1:-1]
                print("STRING", t[0].value, s)
                return s
            else:
                return t[0].value
        else:
            return t
    
    def term(self, t):
        return t[0]

class MongoSQLParser():

    def __init__(self):
        self.parser = Lark(GRAMMAR, parser='lalr', debug=True, transformer=SQLTransformer())

    @classmethod
    def get_instance(cls)->'MongoSQLParser':
        if not hasattr(cls, "_instance"):
            cls._instance = MongoSQLParser()
        return cls._instance
    
    def parse(self, statement:str):
        try:
            return self.parser.parse(statement)
        except Exception as e:
            raise mongodb_connector.MongoDBConnectorException("Parse Failed.", statement)

if __name__ == "__main__":
    print("lark sql") 
    print(GRAMMAR)

    # logger.setLevel(logging.DEBUG)
    # p = Lark(GRAMMAR, parser='lalr', debug=True, transformer=SQLTransformer())
    parser = MongoSQLParser.get_instance()

    # select
    # print(p.parse('SELECT hoge,hage FROM hoge WHERE ((hoge > 10)AND(hoge <10)OR(c>10))'))
    # print(p.parse('SELECT hoge,hage FROM hoge WHERE hoge > 10 AND hoge <10 OR x > -10'))
    # print(p.parse('SELECT hoge,hage FROM hoge WHERE hoge  != 20 ORDER BY hoge ASC LIMIT 10'))
    # print(p.parse('SELECT * FROM csv WHERE year!= 20 ORDER BY year ASC LIMIT 10'))
    # parsed = parser.parse('SELECT * FROM csv WHERE year!= 20 ORDER BY year ASC LIMIT 10')


    # # inseret
    # print(p.parse('INSERT INTO hoge (a, b, c) VALUES (1,2,3)'))
    # parsed = parser.parse('INSERT INTO hoge (a, b, c) VALUES (1,2,3)')
 
    # # delete
    # print(p.parse('DELETE FROM hoge WHERE x > 10'))
    # print(parser.parse('DELETE FROM hoge WHERE x > 10'))

    # # update
    print(parser.parse('UPDATE hoge SET a=19, b=20, c=30 WHERE x > 20'))

    # create table
    # print(p.parse('CREATE TABLE hoge (a INT, b INT, c INT)'))

    # drop table
    # print(p.parse('DROP TABLE hoge'))
    # https://docs.mongodb.com/manual/reference/method/db.collection.drop/


