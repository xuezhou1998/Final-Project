
class Transaction:
    def __init__(self, start_time, read_only) -> None:
        self.blocked = False
        self.aborted = False
        self.read_only = read_only
        self.start_time = start_time

        if self.read_only == True:
            self.snapshot = {}
        else:
            self.snapshot = None
        self.sites_accessed = set()
        self.cache = {}
        self.sites = {}
        self.waiting_for_trans_id = -1
