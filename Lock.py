from Data_Manager import Data_Manager
from Lock import Lock
from Query_Parser import Query_Parser
from Site import Site
from Transaction import Transaction
from Variable import Variable
import Constant
from Transaction_Manager import Transaction_Manager


class Lock:
# <<<<<<< Lock_class
    def __init__(self,  Type_of_Lock, Get_Time, Transaction_ID):
        self.Type_of_Lock = Type_of_Lock
        self.Get_Time = Get_Time
        self.Transaction_ID = Transaction_ID
        self.siteID = 0
        varId = 0
# =======
    
# >>>>>>> master
