


class Lock:
    def __init__(self, site_id) -> None:
        self.site_id = site_id
        self.arraynum = 20
        self.failed = False
        self.just_recovery = False
        self.recover_time = 0
        self.last_fail_time = 0

        self.vartable = dict()

        for i in range(1, arraynum+1):
            if i%2 == 0:
                var = Variable(-1, 10*i)
                vartable[i] = list()
                vartable[i].append(var)
            else:
                if i%10+1==self.site_id:
                    var = Variable(-1, 10*i)
                    vartable[i] = list()
                    vartable[i].append(var)

        
        self.lock_table = dict() 
        self.waiting_for_locktable = dict()
    
    def get_value(variable_id):
        size = len(self.vartable[variable_id])
        return self.vartable[variable_id][size-1].value


    def has_variable(variable_id):
        if variable_id%2==0:
            return True
        return self.site_id == variable_id%10


    def get_var_last_commited_time(variable_id):
        size = len(self.vartable[variable_id])
        return self.vartable[variable_id][size-1].version

    
    def clear_wait_lock(transaction_id, var_id):
        if var_id in self.waiting_for_locktable.keys() and self.waiting_for_locktable[var_id].transaction_id == transaction_id:
            self.waiting_for_locktable.pop(var_id)

    def add_wait_lock(transaction_id, var_id, time_stamp):
        if var_id not in self.waiting_for_locktable.keys():
            lock_1 = lock('W', time_stamp, transaction_id)
            self.waiting_for_locktable[var_id] = lock_1 

    def add_write_lock(transaction_id, variable_id, time_stamp):
        if variable_id not in self.lock_table or len(self.lock_table[variable_id]) == 0:
            self.lock_table[variable_id] = list()
            lock_1 = lock('W', time_stamp, transaction_id)
            self.lock_table[variable_id].append(lock_1)
            return
        
        if self.lock_table[variable_id][0].type_of_lock=='W' and self.lock_table[variable_id][0].transaction_id == transaction_id:
            return 
        lock_2 = lock('W', time_stamp, transaction_id)
        self.lock_table[variable_id].insert(0,lock_2)
        return

    def can_get_write_lock(transaction_id, variable_id):
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
                    if lock_1[i].transaction_id!=transaction_id:
                        return False

                if variable_id not in self.waiting_for_locktable.keys() or self.waiting_for_locktable[variable_id].transaction_id = transaction_id:
                    return True
                return False

        
    def can_get_read_lock(transaction_id, variable_id):
        if variable_id not in self.lock_table.keys() or len(self.lock_table[variable_id]) == 0:
            return True
        else:
            if self.lock_table[variable_id][0].type_of_lock == 'W' and self.lock_table[variable_id][0].transaction_id != transaction_id:
                return False
            return True
    
    def get_waiting_id(variable_id, transaction_id):
        lists = self.lock_table[variable_id]
        for i in range(0, len(lists)):
            if lists[i].transaction_id != transaction_id:
                return lists[i].transaction_id
        
        if variable_id in self.waiting_for_locktable.keys():
            return self.waiting_for_locktable[variable_id].transaction_id
        
        return -1

    def add_read_lock(transaction_id, variable_id, time_stamp):
        if variable_id not in self.lock_table.keys() or len(self.lock_table[variable_id]) == 0:
            self.lock_table[variable_id] = list()
            lock_1 = lock('R', time_stamp, transaction_id)
            self.lock_table[variable_id].insert(0,lock)
            return
        
        if self.lock_table[variable_id][0].type_of_lock == 'W' and self.lock_table[variable_id][0].transaction_id == transaction_id:
            return 
        
        lock_2 = self.lock_table[variable_id]
        for i in range(0， len(lock_2)):
            if lock_2[i].transaction_id ==  transaction_id:
                return 
        
        lock_3 = lock('R', time_stamp, transaction_id)
        self.lock_table[variable_id].insert(0, lock_3)

    
    def site_fail():
        self.lock_table.clear()
        self.waiting_for_locktable.clear()
        failed = True
    

    def write(var_id, value, time_stamp):
        lists = self.vartable[var_id]
        v = Variable(time_stamp, value)
        self.vartable[var_id].append(v)

    def site_recover(time_stamp, last_fail_time):
        self.recover_time = time_stamp
        self.just_recovery = True
        self.fail = False
        self.last_fail_time = last_fail_time

    def release_lock(transaction_id):
        for i in list(self.lock_table.key()):
            lock = self.lock_table[i]
            for j in range(0, len(lock)):
                if lock[j].transaction_id == transaction_id:
                    self.lock_table[i].pop(j-1)