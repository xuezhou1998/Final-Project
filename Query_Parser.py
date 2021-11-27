from typing import List
from Data_Manager import Data_Manager
from Lock import Lock
from Site import Site
from Transaction import Transaction
from Variable import Variable
import Constant
from Transaction_Manager import Transaction_Manager


class Query_Parser:
    def __init__(self) -> None:
        self.res = []

    def parse_query(self, input_query: str) -> List:
        commd = input_query[:input_query.index("(")]
        self.res.append(commd)
        self.res += self.get_argument(input_query)
        print("parsed command is : %s", str(self.res))
        return self.res

    def get_argument(self, input_query: str) -> List:
        left = input_query.index("(")
        right = input_query.index(")")
        args = input_query[left + 1: right].split(",")
        return args
