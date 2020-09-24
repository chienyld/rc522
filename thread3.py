from threading import Thread
import RPi.GPIO as GPIO
import MFRC522
import MFRC52202
import signal
import time
import pygame
import Queue

def end_read(signal,frame):
    global continue_reading
    print ("Ctrl+C captured, ending read.")
    continue_reading = False
    GPIO.cleanup()
signal.signal(signal.SIGINT, end_read)
print ("Welcome to the MFRC522 data read example")
print ("Press Ctrl-C to stop.")

pygame.init()
pygame.mixer.init()
screen=pygame.display.set_mode([640,480])
pygame.time.delay(1000)

q1 = Queue.Queue(maxsize=10)
q2 = Queue.Queue(maxsize=10)
q1.put(1)
q2.put(1)

def runA():
    while True:
        MIFAREReader = MFRC522.MFRC522()  
        (status,TagType) = MIFAREReader.MFRC522_Request(MIFAREReader.PICC_REQIDL)    
        (status,uid) = MIFAREReader.MFRC522_Anticoll()
            
        if status == MIFAREReader.MI_OK:
            # Print UID
            print ("Card1 read UID: %s,%s,%s,%s" % (uid[0], uid[1], uid[2], uid[3]))
            a=str(uid[0])+str(uid[1])+str(uid[2])+str(uid[3])
            print (a)
            q1.put(a)
            time.sleep(0.1)
            file1 = a+".mp3"
            if a != q1.get():
                runD(file1)

def runB():
    while True:
        MIFAREReader2 = MFRC52202.MFRC52202()
        (status2,TagType2) = MIFAREReader2.MFRC522_Request(MIFAREReader2.PICC_REQIDL)    
        (status2,uid2) = MIFAREReader2.MFRC522_Anticoll()

        if status2 == MIFAREReader2.MI_OK:
            print ("Card2 read UID: %s,%s,%s,%s" % (uid2[0], uid2[1], uid2[2], uid2[3]))
            b=str(uid2[0])+str(uid2[1])+str(uid2[2])+str(uid2[3])
            print (b)
            q2.put(b)
            file2 = b+".mp3"
            if b != q2.get():
                runC(file2)
            time.sleep(0.2)

def runC(file2):
    try:
        while pygame.mixer.music.get_busy():
            pygame.time.delay(100)
        pygame.mixer.music.load(file2)
        pygame.mixer.music.play(2)
    except pygame.error as message:   
        print("Cannot load file") 
        pygame.mixer.music.stop()
    time.sleep(0.1)
def runD(file1): 
    try:     
        while pygame.mixer.music.get_busy():      
            pygame.time.delay(100)
        pygame.mixer.music.stop()
        #pygame.mixer.music.unload()
        pygame.mixer.music.load(file1)
        pygame.mixer.music.play(2)
    except pygame.error as message:   
        print("Cannot load file")
        pygame.mixer.music.stop()
    time.sleep(0.1)

if __name__ == "__main__":
    t1 = Thread(target = runA)
    t2 = Thread(target = runB)
    t3 = Thread(target = runC)
    t1.setDaemon(True)
    t2.setDaemon(True)
    #t3.setDaemon(True)

    t1.start()
    t2.start()
    #t3.start()
    while True:
        pass