import sched, datetime
s = sched.scheduler(time.time, time.sleep)

def sayhi(a='justin'):
    print("hi", a)

def delayd():
    print(time.time())
    s.enter(10, 1, sayhi)
    s.run()
    print(time.time())

delayd()
