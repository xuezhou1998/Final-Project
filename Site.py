from Lock import Lock

from Variable import Variable
import Constant


def is_replicated_variable(variable_id):
    if variable_id % 2 == 1:
        return False
    else:
        return True


class Site:
    def __init__(self, site_id) -> None:
        self.site_id = site_id
        self.last_fail_time = 0
        self.fail = False
        self.just_recovery = False
        self.recover_time = 0
        self.vartable = dict()
        self.arraynum = Constant.NUMBER_OF_VARIABLES

        for i in range(1, self.arraynum + 1):
            if is_replicated_variable(i):
                var = Variable(-1, Constant.NUMBER_OF_SITES * i)
                self.vartable[i] = list()
                self.vartable[i].append(var)
            else:
                if i % Constant.NUMBER_OF_SITES + 1 == self.site_id:
                    var = Variable(-1, Constant.NUMBER_OF_SITES * i)
                    self.vartable[i] = list()
                    self.vartable[i].append(var)

        self.lock_table = dict()
        self.waiting_for_locktable = dict()

    def has_variable(self, variable_id):
        if is_replicated_variable(variable_id):
            return True
        return self.site_id == variable_id % Constant.NUMBER_OF_SITES

    def get_value(self, variable_id):
        size = len(self.vartable[variable_id])
        return self.vartable[variable_id][size - 1].value

    def get_var_last_commited_time(self, variable_id):
        size = len(self.vartable[variable_id])
        return self.vartable[variable_id][size - 1].version

    def clear_wait_lock(self, transaction_id, var_id):
        if var_id in self.waiting_for_locktable.keys() and self.waiting_for_locktable[
            var_id].transaction_id == transaction_id:
            self.waiting_for_locktable.pop(var_id)
        else:
            pass
        st_db = self.site_debug([])
        return st_db

    def add_wait_lock(self, transaction_id, var_id, time_stamp):
        if var_id not in self.waiting_for_locktable.keys():
            lock_1 = Lock('W', time_stamp, transaction_id)
            self.waiting_for_locktable[var_id] = lock_1
        else:
            pass
        return 0

    def site_check(self, input_list=[]):
        a = [input_list, self.fail, 0]
        return a[2]

    def can_get_write_lock(self, transaction_id, variable_id):
        if variable_id not in self.lock_table.keys() or len(self.lock_table[variable_id]) == 0:
            return True
        else:
            if self.lock_table[variable_id][0].type_of_lock == 'W':
                if self.lock_table[variable_id][0].transaction_id != transaction_id:
                    return False
                return True
            else:
                lock_1 = self.lock_table[variable_id]
                for i in range(1, len(lock_1)):
                    if lock_1[i].transaction_id != transaction_id:
                        return False

                if variable_id not in self.waiting_for_locktable.keys() or self.waiting_for_locktable[
                    variable_id].transaction_id == transaction_id:
                    return True
                return False

    def add_write_lock(self, transaction_id, variable_id, time_stamp):
        if variable_id not in self.lock_table or len(self.lock_table[variable_id]) == 0:
            self.lock_table[variable_id] = list()
            lock_1 = Lock('W', time_stamp, transaction_id)
            self.lock_table[variable_id].append(lock_1)
            st_db = self.site_debug([])
            return st_db

        if self.lock_table[variable_id][0].type_of_lock == 'W' and self.lock_table[variable_id][
            0].transaction_id == transaction_id:
            st_db = self.site_debug([])
            return st_db
        lock_2 = Lock('W', time_stamp, transaction_id)
        self.lock_table[variable_id].insert(0, lock_2)
        st_db = self.site_debug([])
        return st_db

    def can_get_read_lock(self, transaction_id, variable_id):
        if variable_id not in self.lock_table.keys() or len(self.lock_table[variable_id]) == 0:
            return True
        else:
            if self.lock_table[variable_id][0].type_of_lock == 'W' and self.lock_table[variable_id][
                0].transaction_id != transaction_id:
                return False
            return True

    def get_waiting_id(self, variable_id, transaction_id):
        lists = self.lock_table[variable_id]
        for i in range(0, len(lists)):
            if lists[i].transaction_id != transaction_id:
                return lists[i].transaction_id
            else:
                pass

        if variable_id in self.waiting_for_locktable.keys():
            return self.waiting_for_locktable[variable_id].transaction_id
        else:
            pass
        st_db = self.site_debug([variable_id])
        return st_db

    def site_recover(self, time_stamp, last_fail_time):
        self.recover_time = time_stamp
        self.just_recovery = True
        self.fail = False
        self.last_fail_time = last_fail_time
        return 0

    def site_debug(self, input_list=[]):
        b = [input_list, self.site_id, 0]
        return b[2]

    def add_read_lock(self, transaction_id, variable_id, time_stamp):
        if variable_id not in self.lock_table.keys() or len(self.lock_table[variable_id]) == 0:
            self.lock_table[variable_id] = list()
            lock_1 = Lock('R', time_stamp, transaction_id)
            self.lock_table[variable_id].insert(0, lock_1)
            st_db = self.site_debug([variable_id])

            return st_db

        if self.lock_table[variable_id][0].type_of_lock == 'W' and self.lock_table[variable_id][
            0].transaction_id == transaction_id:
            return -1

        lock_2 = self.lock_table[variable_id]
        for i in range(0, len(lock_2)):
            if lock_2[i].transaction_id == transaction_id:
                return 0

        lock_3 = Lock('R', time_stamp, transaction_id)
        self.lock_table[variable_id].insert(0, lock_3)
        return 0

    def write(self, var_id, value, time_stamp):
        lists = self.vartable[var_id]
        # v = Variable(time_stamp, value)
        v = Variable(value, time_stamp)
        self.vartable[var_id].append(v)
        st_db = self.site_debug([])
        return st_db

    def site_fail(self):
        st_db = self.site_debug([])
        self.lock_table.clear()
        self.waiting_for_locktable.clear()
        self.fail = True
        return self.fail

    def release_lock(self, transaction_id):
        st_db = self.site_debug([])
        for i in list(self.lock_table.keys()):
            lock_instance = self.lock_table[i]
            new_list = []
            for j in range(0, len(lock_instance)):
                if lock_instance[j].transaction_id != transaction_id:
                    # self.lock_table[i].pop(j-1)
                    # self.lock_table[i].pop(j-1)
                    new_list.append(lock_instance[j])

            self.lock_table[i] = new_list.copy()
        return st_db
