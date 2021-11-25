from Data_Manager import Data_Manager
from Lock import Lock
from Query_Parser import Query_Parser
from Site import Site
from Transaction import Transaction
from Variable import Variable
import Constant
from Transaction_Manager import Transaction_Manager
class Variable:
    def __init__(self, value, version):
        self.value = value
        self.version = version