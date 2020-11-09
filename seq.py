import threading
import RPi.GPIO as GPIO
import MFRC522
import MFRC52202
import signal
import time
import pygame
import Queue

a = Queue.Queue(maxsize=10)
b = Queue.Queue(maxsize=10)
a.put(0)
b.put(0)
continue_reading = True

# Capture SIGINT for cleanup when the script is aborted
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

# This loop keeps checking for chips. If one is near it will get the UID and authenticate
def read():
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
            a1=str(uid[0])+str(uid[1])+str(uid[2])+str(uid[3])
            print (a1)
            a.put(a1)
            music()
            time.sleep(1)
            MIFAREReader2 = MFRC52202.MFRC52202()    
            (status2,TagType2) = MIFAREReader2.MFRC522_Request(MIFAREReader2.PICC_REQIDL)    
            (status2,uid2) = MIFAREReader2.MFRC522_Anticoll()
            if status2 == MIFAREReader2.MI_OK:
                print ("Card2 read UID: %s,%s,%s,%s" % (uid2[0], uid2[1], uid2[2], uid2[3]))
                b1=str(uid2[0])+str(uid2[1])+str(uid2[2])+str(uid2[3])
                print (b1)
                file2 = b1+".mp3"
                b.put(b1)
                music2()
        if status2 == MIFAREReader2.MI_OK and status != MIFAREReader.MI_OK:
            #time.sleep(1)
            print ("Card2 read UID: %s,%s,%s,%s" % (uid2[0], uid2[1], uid2[2], uid2[3]))
            b1=str(uid2[0])+str(uid2[1])+str(uid2[2])+str(uid2[3])
            print (b1)
            b.put(b1)
            file2 = b1+".mp3"
            music()
            
def music():
    pygame.init()
    pygame.mixer.init()
    screen=pygame.display.set_mode([640,480])
    pygame.time.delay(1000)
    if a.get():
        file1 = a.get()+".mp3"
        o1=open(file1)
        pygame.mixer.music.load(file1)
        pygame.mixer.music.play()
def music2():
    if a.get():
        file1 = a.get()+".mp3"
        o1=open(file1)
        pygame.mixer.music.load(file1)
        pygame.mixer.music.play()
        if b.get():
            file2 = b.get()+".mp3"
            try:            
                pygame.mixer.music.load(file2)
                pygame.mixer.music.play()
                while pygame.mixer.music.get_busy():
                    pygame.time.delay(100)
            except pygame.error as message:   
                print("Cannot load file")
                pygame.mixer.music.stop()
        
        
t1 = threading.Thread(target=read)
t2 = threading.Thread(target=music)

t1.start()
t2.start()
