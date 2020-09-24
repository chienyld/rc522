import RPi.GPIO as GPIO
import MFRC522
import MFRC52202
import signal
import time
import pygame
import threading    #導入 threading 模組
from multiprocessing import Queue    #使用多核心的模組 Queue


#定義第一個線程工作

#num是給 job1 吃的參數，q是 Queue物件，而 lock 是線程鎖。

def job1(q1, q2, lock): 

    lock.acquire()    #鎖上這個線程，在完成之前不讓其他線程對變數做干擾。

    continue_reading = True

    # Capture SIGINT for cleanup when the script is aborted
    

    # This loop keeps checking for chips. If one is near it will get the UID and authenticate
    while continue_reading:
        MIFAREReader = MFRC522.MFRC522()
        # Scan for cards    
        (status,TagType) = MIFAREReader.MFRC522_Request(MIFAREReader.PICC_REQIDL)    
        # Get the UID of the card
        (status,uid) = MIFAREReader.MFRC522_Anticoll()
        # If we have the UID, continue
        MIFAREReader2 = MFRC52202.MFRC52202()
        (status2,TagType2) = MIFAREReader2.MFRC522_Request(MIFAREReader2.PICC_REQIDL)    
            # Get the UID of the card
        (status2,uid2) = MIFAREReader2.MFRC522_Anticoll()
            
        if status == MIFAREReader.MI_OK:
            # Print UID
            print ("Card1 read UID: %s,%s,%s,%s" % (uid[0], uid[1], uid[2], uid[3]))
            a=str(uid[0])+str(uid[1])+str(uid[2])+str(uid[3])
            print (a)
            q1.put(a) #把算出來的答案放入 Queue 中，後續再取出。
            time.sleep(0.1)
            MIFAREReader2 = MFRC52202.MFRC52202()
            pygame.init()
            pygame.mixer.init()
            screen=pygame.display.set_mode([640,480])
            pygame.time.delay(1000)
            file1 = a+".mp3"
            o1=open(file1)
            pygame.mixer.music.load(file1)
            pygame.mixer.music.play()
            
            #while continue_reading:
            # Scan for cards    
            (status2,TagType2) = MIFAREReader2.MFRC522_Request(MIFAREReader2.PICC_REQIDL)    
            # Get the UID of the card
            (status2,uid2) = MIFAREReader2.MFRC522_Anticoll()
            # If we have the UID, continue
            while pygame.mixer.music.get_busy():      
                pygame.time.delay(100)
            pygame.mixer.music.stop()
            o1.close()
            if status2 == MIFAREReader2.MI_OK:
            # Print UID
                print ("Card2 read UID: %s,%s,%s,%s" % (uid2[0], uid2[1], uid2[2], uid2[3]))
                b=str(uid2[0])+str(uid2[1])+str(uid2[2])+str(uid2[3])
                print (b)
                q2.put(b)
                file2 = b+".mp3"
                try:            
                    while pygame.mixer.music.get_busy():
                        pygame.time.delay(100)
                    pygame.mixer.music.load(file2)
                    pygame.mixer.music.play()
                    while pygame.mixer.music.get_busy():
                        pygame.time.delay(100)
                except pygame.error as message:   
                    print("Cannot load file")
                    pygame.mixer.music.stop()
        if status2 == MIFAREReader2.MI_OK and status != MIFAREReader.MI_OK:
            #time.sleep(1)
            print ("Card2 read UID: %s,%s,%s,%s" % (uid2[0], uid2[1], uid2[2], uid2[3]))
            b=str(uid2[0])+str(uid2[1])+str(uid2[2])+str(uid2[3])
            print (b)
            q2.put(b)
            file2 = b+".mp3"
            pygame.init()
            pygame.mixer.init()
            screen=pygame.display.set_mode([640,480])
            pygame.time.delay(1000)
            try:            
                while pygame.mixer.music.get_busy():
                    pygame.time.delay(100)
                    
                pygame.mixer.music.load(file2)
                pygame.mixer.music.play()
                while pygame.mixer.music.get_busy():
                    pygame.time.delay(100)
                pygame.mixer.stop()
            except pygame.error as message:   
                print("Cannot load file")
                pygame.mixer.music.stop()

    
    lock.release() #解鎖這個線程，開始其他線程。
    #Thread 裡面的 function 不可以有 return, 不然會出錯。


#定義第二個線程工作
def job2(q1, q2, lock):
    lock.acquire()
    
    # This loop keeps checking for chips. If one is near it will get the UID and authenticate
    while continue_reading:
        MIFAREReader = MFRC522.MFRC522()
        # Scan for cards    
        (status,TagType) = MIFAREReader.MFRC522_Request(MIFAREReader.PICC_REQIDL)    
        # Get the UID of the card
        (status,uid) = MIFAREReader.MFRC522_Anticoll()
        # If we have the UID, continue
        MIFAREReader2 = MFRC52202.MFRC52202()
        (status2,TagType2) = MIFAREReader2.MFRC522_Request(MIFAREReader2.PICC_REQIDL)    
            # Get the UID of the card
        (status2,uid2) = MIFAREReader2.MFRC522_Anticoll()

        if status == MIFAREReader.MI_OK or status2 == MIFAREReader2.MI_OK:
            # Print UID
            #print ("Card1 read UID: %s,%s,%s,%s" % (uid[0], uid[1], uid[2], uid[3]))
            checka=str(uid[0])+str(uid[1])+str(uid[2])+str(uid[3])
            print (checka)
            #print ("Card2 read UID: %s,%s,%s,%s" % (uid2[0], uid2[1], uid2[2], uid2[3]))
            checkb=str(uid2[0])+str(uid2[1])+str(uid2[2])+str(uid2[3])
            print (checkb)
            if checka != q1.get() or checkb != q2.get():
                pygame.mixer.stop()
                pygame.mixer.music.stop()
                pygame.event.clear()
    time.sleep(1) 
    lock.release()

#定義主程式
def main():
    continue_reading = True
    def end_read(signal,frame):
        global continue_reading
        print ("Ctrl+C captured, ending read.")
        continue_reading = False
        GPIO.cleanup()

        # Hook the SIGINT
        signal.signal(signal.SIGINT, end_read)

        # Create an object of the class MFRC522
        #MIFAREReader = MFRC522.MFRC522()

        # Welcome message
        print ("Welcome to the MFRC522 data read example")
        print ("Press Ctrl-C to stop.")
    lock = threading.Lock()  #命名一個 Lock 物件
    q1 = Queue() # 開一個 Queue 物件
    q2 = Queue() # 開一個 Queue 物件
    t1 = threading.Thread(target=job1, args=(q1,q2,lock)) 
                            #打開一個名字叫 t1 的線程物件
                            #這個物件會去呼叫 job1
                            #同時t1導入 q 跟 lock 做現成控制
    t2 = threading.Thread(target=job2, args=(q1,q2,lock))

    t1.start()  #啟動 t1 線程
    t2.start()  #啟動 t2 線程
    t1.join()  #在 t1線程結束前阻止程式繼續運行
    t2.join()  #在 t2線程結束前阻止程式繼續運行

 #確認Queue是否為空，如果不是就用 q.get() 取出值

  
print ("END Section!")

if __name__ == '__main__': main()