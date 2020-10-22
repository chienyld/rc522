# -*- coding: utf8 -*-
import threading
import time
import RPi.GPIO as GPIO
import MFRC522
import MFRC52202
import signal
import pygame
import Queue

signal.signal(signal.SIGINT, signal.SIG_DFL)
#lock=threading.Lock()

a = Queue.Queue(maxsize=10)
b = Queue.Queue(maxsize=10)
a.put(0)
b.put(0)
uid1 = "0"
uid3 = "0"
continue_reading = True

def mfrc522():
    
    time.sleep(1)
    global continue_reading
    
    MIFAREReader = MFRC522.MFRC522()
    (status,TagType) = MIFAREReader.MFRC522_Request(MIFAREReader.PICC_REQIDL)
    (status,uid) = MIFAREReader.MFRC522_Anticoll()
    while continue_reading:
        if status == MIFAREReader.MI_OK:
            print ("Card1 read UID: %s,%s,%s,%s" % (uid[0], uid[1], uid[2], uid[3]))
            global uid1
            uid1=str(uid[0])+str(uid[1])+str(uid[2])+str(uid[3])
            print (uid1)
            a.put(uid1)
            if uid1 != a.get():
                music()
                

def mfrc52202():
    time.sleep(1)
    global continue_reading
    #lock.acquire()
    while continue_reading:
        MIFAREReader2 = MFRC52202.MFRC52202()
        (status2,TagType2) = MIFAREReader2.MFRC522_Request(MIFAREReader2.PICC_REQIDL)    
        (status2,uid2) = MIFAREReader2.MFRC522_Anticoll()
        if status2 == MIFAREReader2.MI_OK:
            print ("Card2 read UID: %s,%s,%s,%s" % (uid2[0], uid2[1], uid2[2], uid2[3]))
            global uid3
            uid3=str(uid2[0])+str(uid2[1])+str(uid2[2])+str(uid2[3])
            print (uid3)
            b.put(uid3)
            if uid3 != b.get():
                music2()              
def music():
    try:
        pygame.init()
        pygame.mixer.init()
        screen=pygame.display.set_mode([640,480])
        pygame.time.delay(1000)
        file1 = uid1+".mp3"
        o1=open(file1)
        pygame.mixer.music.load(file1)
        pygame.mixer.music.play(2)
        o1.close()
        pygame.quit()
        #pygame.mixer.music.stop()
    except pygame.error as message:   
        print("Cannot load file")
        pygame.mixer.music.stop()

def music2():
    try:
        pygame.init()
        pygame.mixer.init()
        screen=pygame.display.set_mode([640,480])
        pygame.time.delay(1000)
        file2 = uid3+".mp3"
        o2=open(file2)
        pygame.mixer.music.load(file2)
        pygame.mixer.music.play(2)
        o2.close()
        pygame.quit()

        #pygame.mixer.music.stop()
    except pygame.error as message:   
        print("Cannot load file")
        pygame.mixer.music.stop()
        
t1 = threading.Thread(target=mfrc522)
t2 = threading.Thread(target=mfrc52202)
t3 = threading.Thread(target=music)
t4 = threading.Thread(target=music2)

t1.start()
t2.start()
t3.start()
t4.start()