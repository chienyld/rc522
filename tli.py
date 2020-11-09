# -*- coding: utf8 -*-
import threading
import time
import RPi.GPIO as GPIO
import MFRC522
import MFRC52202
import signal
import pygame
#import Queue

signal.signal(signal.SIGINT, signal.SIG_DFL)
#lock=threading.Lock()

list1=[]
list1=list()
list2=[]
list2=list()
continue_reading = True
uid1="0"
uid2="0"
uid3="0"
uid4="0"
list1.append(0)
list1.append(0)
list2.append(0)
list2.append(0)
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
            global uid2
            uid1=str(uid[0])+str(uid[1])+str(uid[2])+str(uid[3])
            print (uid1)
            if uid1 != list1[0]:
                uid2=list1[0]
                list1.append(uid1)
                list1.pop(0)
def mfrc2():
    while continue_reading:
        time.sleep(0.5)
        MIFAREReader2 = MFRC52202.MFRC52202()
        (status2,TagType2) = MIFAREReader2.MFRC522_Request(MIFAREReader2.PICC_REQIDL)    
        (status2,uid2) = MIFAREReader2.MFRC522_Anticoll()
        if status2 == MIFAREReader2.MI_OK:
            print ("Card2 read UID: %s,%s,%s,%s" % (uid2[0], uid2[1], uid2[2], uid2[3]))
            global uid3
            global uid4
            uid3=str(uid2[0])+str(uid2[1])+str(uid2[2])+str(uid2[3])
            print (uid3)
            if uid3 != list2[0]:
                uid4=list2[0]
                list2.append(uid3)
                list2.pop(0)
def music():
    while continue_reading:
        time.sleep(1)
        print("while")
        print(list1[0])
        print(list1[1])
        print(list2[0])
        print(list2[1])
        global uid1
        uid1= str(list1[1])
        global uid3
        uid3= str(list2[1])
        if uid1 != uid2:
            try:
                print (uid1+"reading")
                time.sleep(0.1)
                #pygame.init()
                pygame.mixer.init()
                #screen=pygame.display.set_mode([640,480])
                pygame.time.delay(10)
                file1 = uid1+".mp3"
                o1=open(file1)
                pygame.mixer.music.load(file1)
                pygame.mixer.music.play()
                list1.append("0")
                list1.pop(0)
                while pygame.mixer.music.get_busy():      
                    pygame.time.delay(100)
                pygame.mixer.music.stop()
                o1.close()
            #except pygame.error as message:   
            except:
                print("Cannot load file")
                pygame.mixer.music.stop()
            if uid3 != uid4:
                print (uid3+"reading")
                file2 = uid3+".mp3"
                #time.sleep(1)
                try:            
                    while pygame.mixer.music.get_busy():
                        pygame.time.delay(100)
                    pygame.mixer.music.load(file2)
                    pygame.mixer.music.play()
                    list2.append("0")
                    list2.pop(0)
                    while pygame.mixer.music.get_busy():
                        pygame.time.delay(100)
                except:   
                    print("Cannot load file")
                    pygame.mixer.music.stop()
                
            else:
                print("no card2")
        #secondread = threading.Timer(5.0, threading_sub, args = ["sub thread"])
        secondread = threading.Timer(5.0, threading_sub)
        secondread.start()
        print("reading card 2...")
        secondread.join()
        #if uid3 != uid4 and uid1 == uid2:
        #elif q1 ==0 and q2==0:
            #print("000")
def threading_sub():
    if uid3 != uid4:
        #time.sleep(0.1)
        try:
            print (uid3+"reading")
            file2 = uid3+".mp3"
            #pygame.init()
            pygame.mixer.init()
            #screen=pygame.display.set_mode([640,480])      
            pygame.mixer.music.load(file2)
            pygame.mixer.music.play()
            time.sleep(0.1)
            list2.append("0")
            list2.pop(0)
        except:   
            print("Cannot load file")
            pygame.mixer.music.stop()
        
t1 = threading.Thread(target=mfrc1)
t2 = threading.Thread(target=mfrc2)
t3 = threading.Thread(target=music)
t1.start()
t2.start()
t3.start()



