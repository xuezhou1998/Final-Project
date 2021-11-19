from typing_extensions import TypeVarTuple
import Data_Manager
import Lock
import Query_Parser
import Site
import Transaction
import Transaction_Manager
import Variable
import Constant


class Transaction_Manager:
    def __init__(self) -> None:
        self.time_stamp=0
        self.data_mgr=Data_Manager()
        self.trans_map={}##integer: transaction
        
    def get(self,trans_id):
        if trans_id not in self.trans_map.keys():
            raise Exception("The transaction %d does not exist",trans_id)
        else:
            return self.trans_map[trans_id]
    def begin(self,trans_id):
        self.trans_init_checker(trans_id)
        tr=Transaction(self.time_stamp,False)
        self.trans_map[trans_id]=tr
        return True

    def begin_read_only(self,trans_id):
        self.trans_init_checker(trans_id)
        tr=Transaction(self.time_stamp,True)
        self.trans_map[trans_id]=tr
        return True
    def read(self,trans_id, variable_id):
        if self.alive_checker(trans_id)==False:
            return True
        
        tr=self.trans_map[trans_id]
        if tr.blocked==True:
            return False
        if tr.aborted==True:
            return True
        if tr.read_only==True:
            return self.read_read_only(tr,variable_id)
        if variable_id in tr.cache.keys():
            variable_value=tr.cache[variable_id]
            print("X %s : %s",str(variable_id),str(variable_value))
            return True
        if self.is_replicated_variable(variable_id)==False:
            site_id=variable_id%Constant.NUMBER_OF_SITES+1
                ########
        else:
            for i in range(Constant.NUMBER_OF_SITES):
                ########
        return False
            
        
        
                

            

    def read_read_only(self,trans_id,variable_id):
        if self.is_replicated_variable(variable_id)==False:
            site_id=variable_id%Constant.NUMBER_OF_SITES+1

            if self.data_mgr.is_site_failed(site_id)==True:
                return False
            else:
                variable_value=self.data_mgr.read_only_non_replicated_read(variable_id,tr.start_time,site_id)
                print("X %s : %s",str(variable_id),str(variable_value))
                return True
        else:
            for i in range(Constant.NUMBER_OF_SITES):
                if self.data_mgr.is_site_failed(i)==True:
                    continue
                curr_site=self.data_mgr.get_site_instance(i)
                variable_value=self.data_mgr.read_only_replicated_read(variable_id,tr.start_time,i)
                if variable_value==-1:
                    continue
                else:
                    print("X %s : %s",str(variable_id),str(variable_value))
                    return True
        return False
    def write(self,trans_id):
        pass
    def block_trans(self,trans_id):
        pass
    def end(self,trans_id):
        pass
    def dump(self,trans_id):
        pass
    def get_read_lock(self,trans_id):
        pass
    def dead_lock_detect(self):
        pass
    def find_yongest(self,trans_id):
        pass
    def abort_trans_multi(self,trans_id):
        pass
    def abort_trans(self,trans_id):
        pass
    def release_locks(self,trans_id):
        pass
    def unblock_trans(self,trans_id):
        pass
    def trans_init_checker(self,trans_id):
        pass
    def alive_checker(self,trans_id):
        pass
    def recover(self,trans_id):
        pass
    def fail(self,trans_id):
        pass
    def is_replicated_variable(self,variable_id):
        if variable_id%2==1:
            return False
        else:
            return True
    