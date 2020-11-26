from threading import Thread
import time
import signal
lock = True
c=True
def runA():
    while lock==True:
        time.sleep(1)
        print ('A')

def runB():
    while lock==False:
        time.sleep(1)
        print ('B')

def runC():
    while c==True:
        #for i in range(0,5):
        time.sleep(5)
        global lock
        lock = not lock
        print(lock)
        if lock:
            t1 = Thread(target = runA)
            t1.start()
        else:
            t2 = Thread(target = runB)
            t2.start()
if __name__ == "__main__":
    t1 = Thread(target = runA)
    t2 = Thread(target = runB)
    t3 = Thread(target = runC)
    t1.start()
    t2.start()
    t3.start()
    t1.join()
    t2.join()