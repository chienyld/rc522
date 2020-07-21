import threading
import time


def long_time_task(i):
    print('sub thread: {} mission{}'.format(threading.current_thread().name, i))
    time.sleep(2)
    print("result: {}".format(8 ** 20))


if __name__=='__main__':
    start = time.time()
    print('main thread:{}'.format(threading.current_thread().name))
    thread_list = []
    for i in range(1, 3):
        t = threading.Thread(target=long_time_task, args=(i, ))
        thread_list.append(t)

    for t in thread_list:
        t.start()

    for t in thread_list:
        t.join()

    end = time.time()
    print("tatal {} seconds".format((end - start)))