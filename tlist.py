# -*- coding: utf8 -*-
import threading
import time
import RPi.GPIO as GPIO
import MFRC522
import MFRC52202
import signal
import pygame

pygame.mixer.init()
screen=pygame.display.set_mode([640,480])
pygame.time.delay(500)

signal.signal(signal.SIGINT, signal.SIG_DFL)
continue_reading = True
list1=[]
list1=list()
list2=[]
list2=list()
def reader1():
    time.sleep(0.5)
    MIFAREReader = MFRC522.MFRC522()
    (status,TagType) = MIFAREReader.MFRC522_Request(MIFAREReader.PICC_REQIDL)
    (status,uid) = MIFAREReader.MFRC522_Anticoll()
    while continue_reading:
        if status == MIFAREReader.MI_OK:
            print ("Card1 read UID: %s,%s,%s,%s" % (uid[0], uid[1], uid[2], uid[3]))
            id1=str(uid[0])+str(uid[1])+str(uid[2])+str(uid[3])
            print (id1)
            if id1 != list1[0]:
                list1.append(id1)
                music()
            else:
                list1.pop(0)
def reader2():
    time.sleep(1.5)
    while continue_reading:
        MIFAREReader2 = MFRC52202.MFRC52202()
        (status2,TagType2) = MIFAREReader2.MFRC522_Request(MIFAREReader2.PICC_REQIDL)    
        (status2,uid2) = MIFAREReader2.MFRC522_Anticoll()
        if status2 == MIFAREReader2.MI_OK:
            print ("Card2 read UID: %s,%s,%s,%s" % (uid2[0], uid2[1], uid2[2], uid2[3]))
            id2=str(uid2[0])+str(uid2[1])+str(uid2[2])+str(uid2[3])
            print (id2)
            if id2 != list2[0]:
                list2.append(id2)
                music2() 
            else:
                list2.pop(0)             
def music():
    try:
        pygame.mixer.music.stop()
        pygame.quit()
        pygame.init()
        pygame.mixer.init()
        screen=pygame.display.set_mode([640,480])
        pygame.time.delay(300)
        f1=list1[1]
        file1 = f1+".mp3"
        o1=open(file1)
        pygame.mixer.music.load(file1)
        pygame.mixer.music.play(2)
        o1.close()
        list1.pop(0)       
        #pygame.mixer.music.stop()
    except pygame.error as message:   
        print("Cannot load file")
        pygame.mixer.music.stop()

def music2():
    try:
        #if list1[0]!=list[1]:
        while pygame.mixer.music.get_busy():
            pygame.time.delay(100)
        f2=list2[1]
        file2 = f2+".mp3"
        o2=open(file2)
        pygame.mixer.music.load(file2)
        pygame.mixer.music.play(2)
        o2.close()
        list2.pop(0)       
    except pygame.error as message:   
        print("Cannot load file")
        pygame.mixer.music.stop()
        
t1 = threading.Thread(target=reader1)
t2 = threading.Thread(target=reader2)

t1.start()
t2.start()