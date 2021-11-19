import Data_Manager
import Lock
import Query_Parser
import Site
import Transaction
import Transaction_Manager
import Variable
import Constant
class Data_Manager:
    def __init__(self) -> None:
        self.site_dict={}
        self.site_failures={}
        self.site_failure_times={}
        for i in range(Constant.NUMBER_OF_SITES):
            site_instance = Site(i+1)
            self.site_dict[i+1]=site_instance
            self.site_failures[i+1]=False
            self.site_failure_times[i+1]=[]
            self.site_failure_times[i+1].append(-1)

    def is_site_failed(self,site_id):
        return self.site_failures[site_id]
    def get_site_instance(self,site_id):
        return self.site_dict[site_id]
    def read_only_non_replicated_read(self,variable_id,time_stamp,site_id):
        curr_site=self.get_site_instance(site_id)
        history = curr_site.variable_table[variable_id]
        for i in reversed(range(len(history))):
            if history[i].version<=time_stamp:
                return history[i].value
        return -1
    def read_only_replicated_read(self,variable_id,time_stamp,site_id):
        curr_site=self.get_site_instance(site_id)
        history = curr_site.variable_table[variable_id]
        for i in reversed(range(len(history))):
            if history[i].version>time_stamp:
                continue
            last_cmmt_time_bf_start=history[i].version
            if self.is_always_up(last_cmmt_time_bf_start,time_stamp,site_id):

                return history[i].value
            break
        return -1
        
    def is_always_up(self,last_cmmt_time_bf_start,start_time,site_id):
        failed_time = self.site_failure_times[site_id]

        for i in range(len(failed_time)):

            crr_time = failed_time[i]
            if crr_time< start_time and crr_time>last_cmmt_time_bf_start:
                return False
        return True