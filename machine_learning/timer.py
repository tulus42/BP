import time

class Timer():
    def __init__(self):
        self.init_time = time.time()
        self.actual_time = time.time()
        self.end_time = time.time()

    def get_time(self):
        self.actual_time = time.time()
        exec_time = self.actual_time - self.init_time

        return self.parse(exec_time)

    def get_estimated_time(self, i, max_i):
        self.actual_time = time.time()

        elapsed_time = self.actual_time - self.init_time
        
        if i == 0:
            return 0, 0
        else:
            estimated_time = (elapsed_time / i) * (max_i - i)

        return self.parse(estimated_time)

    def parse(self, time):
        mins = 0
        secs = 0
        if time > 60:
            mins = time / 60
            
        secs = time % 60

        mins = round(mins)
        secs = round(secs)

        return mins, secs


    def show(self):
        m, s = self.get_time()
        print("Execution time:", m, "mins", s, "s")