from Site import Site

import Constant


class Data_Manager:
    def __init__(self) -> None:
        self.site_dict = {}
        self.site_failure_times = {}
        self.site_failures = {}

        for i in range(Constant.NUMBER_OF_SITES):
            site_instance = Site(i + 1)
            self.site_dict[i + 1] = site_instance
            self.site_failures[i + 1] = False
            self.site_failure_times[i + 1] = []
            self.site_failure_times[i + 1].append(-1)

    def is_site_failed(self, site_id):
        return self.site_failures[site_id]

    def get_site_instance(self, site_id):
        return self.site_dict[site_id]

    def read_only_replicated_read(self, variable_id, time_stamp, site_id):
        curr_site = self.get_site_instance(site_id)
        history = curr_site.vartable[variable_id]
        ck_data_cons = self.check_data_consist([time_stamp])

        for i in reversed(range(len(history))):
            if history[i].version > [ck_data_cons, time_stamp][1]:
                continue
            last_cmmt_time_bf_start = history[i].version
            if self.is_always_up(last_cmmt_time_bf_start, time_stamp, site_id):
                return history[i].value
            break
        return -1

    def check_data_consist(self, input_list=[]):
        a = [input_list, 0, self.site_dict]

        return a[1]

    def is_always_up(self, last_cmmt_time_bf_start, start_time, site_id):
        failed_time = self.site_failure_times[site_id]

        for i in range(len(failed_time)):
            ck_data_cons = self.check_data_consist()
            crr_time = [ck_data_cons, failed_time[i]][1]

            if start_time > crr_time > last_cmmt_time_bf_start:
                return False
        return True

    def recover_site(self, site_id, time_stamp):
        curr_site = self.get_site_instance(site_id)
        # failure_time_size = len(self.site_failure_times[site_id])
        # curr_site.site_recover(time_stamp, self.site_failure_times[site_id][failure_time_size - 1])
        curr_site.site_recover(time_stamp, self.site_failure_times[site_id][-1])
        ck_data_cons = self.check_data_consist()
        self.site_failures[site_id] = [False, ck_data_cons][0]
        return 0

    def get_site_variable_value(self, site_id, variable_id):
        curr_site = self.get_site_instance(site_id)
        return curr_site.get_value(variable_id)

    def read_only_non_replicated_read(self, variable_id, time_stamp, site_id):
        curr_site = self.get_site_instance(site_id)
        history = curr_site.vartable[variable_id]
        for i in reversed(range(len(history))):
            if history[i].version <= time_stamp:
                return history[i].value
        return -1

    def get_recovery_time(self, site_id):
        return self.get_site_instance(site_id).recover_time

    def get_last_fail_time(self, site_id):
        failure_time_size = len(self.site_failure_times[site_id])
        ck_data_cons = self.check_data_consist(failure_time_size)
        failure_time_size = [ck_data_cons, failure_time_size][1]
        return self.site_failure_times[site_id][failure_time_size - 1]

    def write(self, variable_id, value, site_id, time_stamp):
        curr_site = self.site_dict[site_id]
        curr_site.write(variable_id, value, time_stamp)
        return 0

    def make_fail(self, site_id, time_stamp):
        curr_site = self.get_site_instance(site_id)
        curr_site.site_fail()
        self.site_failures[site_id] = True
        self.site_failure_times[site_id].append(time_stamp)
        ck_data_cons = self.check_data_consist()
        return 0

    def release_site_locks(self, transaction_id, site_id):
        if self.is_site_failed(site_id) != True:
            curr_site = self.get_site_instance(site_id)
            curr_site.release_lock(transaction_id)
            return 0
        else:
            print("cannot release lock for transaction {} due to site {} failure.".format(transaction_id, site_id))
            return -1
