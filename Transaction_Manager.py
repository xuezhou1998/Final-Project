# import typing_extensions
from Data_Manager import Data_Manager
from Lock import Lock
from Query_Parser import Query_Parser
from Site import Site
from Transaction import Transaction
from Variable import Variable
import Constant
from Transaction_Manager import Transaction_Manager

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
        curr_transaction=Transaction(self.time_stamp,False)
        self.trans_map[trans_id]=curr_transaction
        return True

    def begin_read_only(self,trans_id):
        self.trans_init_checker(trans_id)
        curr_transaction=Transaction(self.time_stamp,True)
        self.trans_map[trans_id]=curr_transaction
        return True
    def read(self,trans_id, variable_id):
        if self.alive_checker(trans_id)==False:
            return True
        
        curr_transaction=self.trans_map[trans_id]
        if curr_transaction.blocked==True:
            return False
        if curr_transaction.aborted==True:
            return True
        if curr_transaction.read_only==True:
            return self.read_read_only(curr_transaction,variable_id)
        if variable_id in curr_transaction.cache.keys():
            variable_value=curr_transaction.cache[variable_id]
            print("X %s : %s",str(variable_id),str(variable_value))
            return True
        if self.is_replicated_variable(variable_id)==False:
            site_id=variable_id%Constant.NUMBER_OF_SITES+1
            if self.get_read_lock(trans_id,variable_id,site_id)==True:
                if site_id not in curr_transaction.sites_accessed:
                    curr_transaction.site_accessed.add(site_id)
                variable_value=self.data_mgr.get_site_variable_value(site_id,variable_id)
                print("X %s : %s",str(variable_id),str(variable_value))
                return True
        else:
            for i in range(Constant.NUMBER_OF_SITES):
                if self.get_read_lock(trans_id,variable_id,i)==True:
                    curr_transaction.site_accessed.add(i)
                variable_value=self.data_mgr.get_site_variable_value(i,variable_id)
                print("X %s : %s",str(variable_id),str(variable_value))
                return True
        return False
            
        
        
                

            

    def read_read_only(self,curr_transaction,variable_id):
        if self.is_replicated_variable(variable_id)==False:
            site_id=variable_id%Constant.NUMBER_OF_SITES+1

            if self.data_mgr.is_site_failed(site_id)==True:
                return False
            else:
                variable_value=self.data_mgr.read_only_non_replicated_read(variable_id,curr_transaction.start_time,site_id)
                print("X %s : %s",str(variable_id),str(variable_value))
                return True
        else:
            for i in range(Constant.NUMBER_OF_SITES):
                if self.data_mgr.is_site_failed(i)==True:
                    continue
                curr_site=self.data_mgr.get_site_instance(i)
                variable_value=self.data_mgr.read_only_replicated_read(variable_id,curr_transaction.start_time,i)
                if variable_value==-1:
                    continue
                else:
                    print("X %s : %s",str(variable_id),str(variable_value))
                    return True
        return False
    def write(self,trans_id,variable_id,variable_value):
        if self.alive_checker(trans_id) !=True:
            return True
        curr_transaction=self.trans_map[trans_id]
        if curr_transaction.aborted==True:
            return True
        if curr_transaction.blocked==True:
            return False
        if self.is_replicated_variable(variable_id)==False:
            site_id=variable_id%Constant.NUMBER_OF_SITES+1
            if self.data_mgr.is_site_failed(site_id)==True:
                return False
            curr_site=self.data_mgr.get_site_instance(site_id)
            if curr_site.can_get_write_lock(trans_id,variable_id)==True:
                curr_site.add_write_lock(trans_id,variable_id,self.time_stamp)
                curr_site.clear_wait_lock(trans_id,variable_id)
                curr_transaction.sites_accessed.add(site_id)
                curr_transaction.cache[variable_id]=variable_value
                curr_transaction.sites[variable_id]=[site_id]
                return True
            else:
                curr_site.add_write_lock(trans_id,variable_id,self.time_stamp)
                wait_id=curr_site.get_waiting_id(variable_id,trans_id)
                curr_transaction.waiting_for_trans_id=wait_id
                curr_transaction.blocked=True
                return False

        else:
            


    def block_trans(self,trans_id):
        pass
    def end(self,trans_id):
        pass
    def dump(self,trans_id):
        pass
    def get_read_lock(self,trans_id,variable_id,site_id):
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
    