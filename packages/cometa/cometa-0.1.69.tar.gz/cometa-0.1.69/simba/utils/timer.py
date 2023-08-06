from dataclasses import dataclass
import time
@dataclass
class Timer:
    total_time: float = 0.0
    last_tic: float = 0.0
    def tic(self):
        """Start to time."""
        self.last_tic = time.time()
    def toc(self):
        """End the timing"""
        self.total_time = self.total_time + time.time()-self.last_tic
    def total(self):
        """Returnt he totral time"""
        return self.total_time

    
