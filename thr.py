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

a = Queue.Queue(maxsize=6)
a1 = Queue.Queue(maxsize=6)
b = Queue.Queue(maxsize=6)
b1 = Queue.Queue(maxsize=6)
a.put("0")
a.put("0")
b.put("0")
b.put("0")
continue_reading = True
uid1="0"
uid3="0"

pygame.init()
pygame.mixer.init()
screen=pygame.display.set_mode([640,480])
pygame.time.delay(1000)
def mfrc1():
    while continue_reading:
        time.sleep(0.5)
        MIFAREReader = MFRC522.MFRC522()
        (status,TagType) = MIFAREReader.MFRC522_Request(MIFAREReader.PICC_REQIDL)    
        (status,uid) = MIFAREReader.MFRC522_Anticoll()
        if status == MIFAREReader.MI_OK:
            print("read")
            print ("Card1 read UID: %s,%s,%s,%s" % (uid[0], uid[1], uid[2], uid[3]))
            global uid1
            uid1=str(uid[0])+str(uid[1])+str(uid[2])+str(uid[3])
            print (uid1)
            a.put(uid1)
            a1.put(uid)
            a.get()
def mfrc2():
    while continue_reading:
        time.sleep(0.5)
        MIFAREReader2 = MFRC52202.MFRC52202()
        (status2,TagType2) = MIFAREReader2.MFRC522_Request(MIFAREReader2.PICC_REQIDL)    
        (status2,uid2) = MIFAREReader2.MFRC522_Anticoll()
        if status2 == MIFAREReader2.MI_OK:
            print ("Card2 read UID: %s,%s,%s,%s" % (uid2[0], uid2[1], uid2[2], uid2[3]))
            global uid3
            uid3=str(uid2[0])+str(uid2[1])+str(uid2[2])+str(uid2[3])
            print (uid3)
            b.put(uid3)
            b1.put(uid3)
            b.get()
def music():
    while continue_reading:
        time.sleep(1)
        print("while")
        q1=a.get()
        print(q1+"is q1")
        #print(uid3+"is u1")
        q2=b.get()
        print(q2+"is q2")
        #print(uid3+"is u2")
        if uid1 != q1:
            try:
                print (uid1+"reading")
                time.sleep(0.1)
                pygame.init()
                pygame.mixer.init()
                screen=pygame.display.set_mode([640,480])
                pygame.time.delay(100)
                file1 = uid1+".mp3"
                o1=open(file1)
                pygame.mixer.music.load(file1)
                pygame.mixer.music.play()
                while pygame.mixer.music.get_busy():      
                    pygame.time.delay(100)
                pygame.mixer.music.stop()
                o1.close()
            except pygame.error as message:   
                print("Cannot load file")
                pygame.mixer.music.stop()
            if uid3 != q2:
                print (uid3+"reading")
                file2 = uid3+".mp3"
                #time.sleep(1)
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
            else:
                print("no card2")
        if uid3 != q2 and uid1 == q1:
            time.sleep(0.1)
            try:
                print (uid3+"reading")
                file2 = uid3+".mp3"
                pygame.init()
                pygame.mixer.init()
                screen=pygame.display.set_mode([640,480])      
                pygame.mixer.music.load(file2)
                pygame.mixer.music.play()
                time.sleep(0.1)
            except pygame.error as message:   
                print("Cannot load file")
                pygame.mixer.music.stop()
        elif q1 ==0 and q2==0:
            print("000")

        
t1 = threading.Thread(target=mfrc1)
t2 = threading.Thread(target=mfrc2)
t3 = threading.Thread(target=music)
t1.start()
t2.start()
t3.start()


