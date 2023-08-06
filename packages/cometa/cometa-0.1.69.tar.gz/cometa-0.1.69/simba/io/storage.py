import os
import pickle
##Storage is simply a dicitonnary potentially pickle at the moment, can be changed ot hdf5
SIZE_BATCH = 500

class Storage:
    def __init__(self,path=None,save_interval=None):
        if path is None and save_interval is not None:
            raise ValueError("path can not be None is save_interval is not None.")
        if path is not None and save_interval:
            print("save_interval not specified and set to 500.")
            self.save_interval = SIZE_BATCH
        else:
            self.save_interval = save_interval
        self.path=path
        if self.path is not None and os.path.isfile(self.path):
            with open(self.path,"rb") as f:
                self.storage = pickle.load(f)
        else:
            self.storage={}
        self.counter = 0

    def __getitem__(self, item):
        return self.storage[item]

    def __contains__(self, item):
        return item in self.storage

    def __setitem__(self, key, value):
        self.storage[key]=value
        self.counter += 1
        if self.save_interval is not None:
            if self.counter >= self.save_interval:
                self.save()
                self.counter = 0

    def get_path(self):
        return self.path

    def __len__(self):
        return len(self.storage)

    def save(self):
        with open(self.path,"wb") as f:
            pickle.dump(self.storage,f)