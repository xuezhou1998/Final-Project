from typing_extensions import Self


class Transaction:
    def __init__(self,start_time,read_only) -> None:
        self.start_time=start_time
        self.read_only=read_only
        self.snapshot=None
        if self.read_only==True:
            self.snapshot={}
        self.sites_accessed={}
        self.cache={}
        self.sites={} 

