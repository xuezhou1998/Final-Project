import Data_Manager
import Lock
import Query_Parser
import Site
import Transaction
import Transaction_Manager
import Variable

class Transaction_Manager:
    def __init__(self) -> None:
        self.time_stamp=0
        self.data_mgr=Data_Manager()
        self.trans_map={}##integer: transaction
        
    def get(trans_id):
        pass
    def begin(trans_id):
        pass
    def begin_read_only(trans_id):
        pass
    def read(trans_id):
        pass

    def read_read_only(trans_id):
        pass
    def write(trans_id):
        pass
    def block_trans(trans_id):
        pass
    def end(trans_id):
        pass
    def dump(trans_id):
        pass
    def get_read_lock(trans_id):
        pass
    def dead_lock_detect():
        pass
    def find_yongest(trans_id):
        pass
    def abort_trans_multi(trans_id):
        pass
    def abort_trans(trans_id):
        pass
    def release_locks(trans_id):
        pass
    def unblock_trans(trans_id):
        pass
    def trans_init_checker(trans_id):
        pass
    def alive_checker(trans_id):
        pass
    def recover(trans_id):
        pass
    def fail(trans_id):
        pass
    