import threading
import time
import RPi.GPIO as GPIO
import MFRC522
import signal
import Queue
import pygame

signal.signal(signal.SIGINT, signal.SIG_DFL)
#lock=threading.Lock()

a = Queue.Queue(maxsize=10)

a.put(0)

uid1 = "0"

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
            uid1=str(uid[0])+str(uid[1])+str(uid[2])+str(uid[3])
            print (uid1)
            a.put(uid1)
            if uid1 != a.get():
                music()

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
        #pygame.mixer.music.stop()
    except pygame.error as message:   
        print("Cannot load file")
        pygame.mixer.music.stop()
        
        
t1 = threading.Thread(target=mfrc522)
t2 = threading.Thread(target=music)
t1.start()
t2.start()