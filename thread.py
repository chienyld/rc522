import threading    #導入 threading 模組
from multiprocessing import Queue    #使用多核心的模組 Queue


#定義第一個線程工作

#num是給 job1 吃的參數，q是 Queue物件，而 lock 是線程鎖。

def job1(num, q, lock): 

    lock.acquire()    #鎖上這個線程，在完成之前不讓其他線程對變數做干擾。

    sum = 0           
    for i in range(num):
        sum += i

    q.put(sum) #把算出來的答案放入 Queue 中，後續再取出。
    if sum==0:
        print(sum)
    else:
        print("more than 0")
    lock.release() #解鎖這個線程，開始其他線程。
    #Thread 裡面的 function 不可以有 return, 不然會出錯。


#定義第二個線程工作
def job2(num, q, lock):
    lock.acquire()
    sum = 0
    for i in range(num):
        sum += i**10

    q.put(sum)
    lock.release()

#定義主程式
def main():
    lock = threading.Lock()  #命名一個 Lock 物件
    q = Queue() # 開一個 Queue 物件
    t1 = threading.Thread(target=job1, args=(8,q,lock)) 
                            #打開一個名字叫 t1 的線程物件
                            #這個物件會去呼叫 job1
                            #同時t1導入 q 跟 lock 做現成控制
                            #為什麼要這樣做...我也不知道XD

    t2 = threading.Thread(target=job2, args=(8,q,lock))

    t1.start()  #啟動 t1 線程
    t2.start()  #啟動 t2 線程
    t1.join()  #在 t1線程結束前阻止程式繼續運行
    t2.join()  #在 t2線程結束前阻止程式繼續運行

 #確認Queue是否為空，如果不是就用 q.get() 取出值
    while not q.empty():   
        print(q.get())
  
print("END Section!")

if __name__ == '__main__': main()

