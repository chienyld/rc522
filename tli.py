# -*- coding: utf8 -*-
import threading
import time
import RPi.GPIO as GPIO
import MFRC522
import MFRC52202
import signal
import pygame

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
id1="0"
id2="0"
list1.append("0")
list1.append("0")
list2.append("0")
list2.append("0")
pygame.init()
pygame.mixer.init()
def mfrc1():
    while continue_reading:
        time.sleep(0.5)
        MIFAREReader = MFRC522.MFRC522()
        (status,TagType) = MIFAREReader.MFRC522_Request(MIFAREReader.PICC_REQIDL)    
        (status,uida) = MIFAREReader.MFRC522_Anticoll()
        if status == MIFAREReader.MI_OK:
            print("read")
            print ("Card1 read UID: %s,%s,%s,%s" % (uida[0], uida[1], uida[2], uida[3]))
            global uid1
            global uid2
            uid1=str(uida[0])+str(uida[1])+str(uida[2])+str(uida[3])
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
        (status2,uidb) = MIFAREReader2.MFRC522_Anticoll()
        if status2 == MIFAREReader2.MI_OK:
            print ("Card2 read UID: %s,%s,%s,%s" % (uidb[0], uidb[1], uidb[2], uidb[3]))
            global uid3
            global uid4
            uid3=str(uidb[0])+str(uidb[1])+str(uidb[2])+str(uidb[3])
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
        global uid1,uid2,uid3,uid4,id1,id2
        id1= str(list1[1])
        id2= str(list2[1])
        if id1 != uid2:
            time.sleep(0.1)
            if id2 != uid4:
                for i in range(0,3):
                    try:
                        print (id1+"card1 reading")
                        pygame.mixer.init()
                        pygame.time.delay(10)
                        file1 = id1+".mp3"
                        o1=open(file1)
                        pygame.mixer.music.load(file1)
                        pygame.mixer.music.play()
                        while pygame.mixer.music.get_busy():
                            pygame.time.delay(100)
                        pygame.mixer.music.stop()
                        o1.close()
                        #====================
                        print (id2+"card2 reading")
                        file2 = id2+".mp3"
                        o2=open(file2)
                        pygame.mixer.music.load(file2)
                        pygame.mixer.music.play()
                        pygame.mixer.music.stop()
                        o2.close()
                        uid2=id1
                        uid4=id2
                    except:   
                        print("Cannot load file")
                        pygame.mixer.music.stop()               
            else:
                print("no card2")
                try:
                    print (id1+"card1 reading")
                    time.sleep(0.1)
                    pygame.mixer.init()
                    file1 = id1+".mp3"
                    o1=open(file1)
                    pygame.mixer.music.load(file1)
                    pygame.mixer.music.play(2)
                    while pygame.mixer.music.get_busy():
                        pygame.time.delay(100)
                    pygame.mixer.music.stop()
                    o1.close()
                    uid2=id1
                except:
                    print("Cannot load file")
                    pygame.mixer.music.stop()
        elif id2 != uid4 and id1==uid1:
            print (id2+"card2 reading")
            file2 = id2+".mp3"
            o2=open(file2)
            pygame.mixer.music.load(file2)
            pygame.mixer.music.play(2)
            pygame.mixer.music.stop()
            o2.close()
            uid4=id2
def gap():
    while continue_reading:
        time.sleep(7)
        global uid2,uid4
        uid2 = "0"
        uid4 = "0"
>>>>>>> d24c179f2945dc9a9f328c377e94cb9db004e196
        
                
t1 = threading.Thread(target=mfrc1)
t2 = threading.Thread(target=mfrc2)
t3 = threading.Thread(target=music)
t4 = threading.Thread(target=gap)
t1.start()
t2.start()
t3.start()
t4.start()



