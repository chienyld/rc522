import RPi.GPIO as GPIO
import MFRC522
import MFRC52202
import signal
import time
import pygame


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
b="0"
b2="1"
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
        time.sleep(1)
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
            file2 = b+".mp3"
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
    if status2 == MIFAREReader2.MI_OK and status != MIFAREReader.MI_OK:
        #time.sleep(1)
        print ("Card2 read UID: %s,%s,%s,%s" % (uid2[0], uid2[1], uid2[2], uid2[3]))
        b=str(uid2[0])+str(uid2[1])+str(uid2[2])+str(uid2[3])
        print (b)
        file2 = b+".mp3"
        pygame.init()
        pygame.mixer.init()
        screen=pygame.display.set_mode([640,480])      
        pygame.mixer.music.load(file2)
        pygame.mixer.music.play()
        time.sleep(1)