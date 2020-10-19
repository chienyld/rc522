from multiprocessing import Process
import os
import time
import RPi.GPIO as GPIO
import MFRC522
import MFRC52202
import signal
import pygame


def long_time_task(i):
    while continue_reading:
        MIFAREReader = MFRC522.MFRC522()   
        (status,TagType) = MIFAREReader.MFRC522_Request(MIFAREReader.PICC_REQIDL)    
        (status,uid) = MIFAREReader.MFRC522_Anticoll()

        MIFAREReader2 = MFRC52202.MFRC52202()
        (status2,TagType2) = MIFAREReader2.MFRC522_Request(MIFAREReader2.PICC_REQIDL)    
        (status2,uid2) = MIFAREReader2.MFRC522_Anticoll()

        if status == MIFAREReader.MI_OK:
        # Print UID
            print ("Card1 read UID: %s,%s,%s,%s" % (uid[0], uid[1], uid[2], uid[3]))
            a=str(uid[0])+str(uid[1])+str(uid[2])+str(uid[3])
            print (a)
            
            if status2 == MIFAREReader2.MI_OK:
        # Print UID
                print ("Card2 read UID: %s,%s,%s,%s" % (uid2[0], uid2[1], uid2[2], uid2[3]))
                b=str(uid2[0])+str(uid2[1])+str(uid2[2])+str(uid2[3])
                print (b)
            
        if status2 == MIFAREReader2.MI_OK and status != MIFAREReader.MI_OK:
            print ("Card2 read UID: %s,%s,%s,%s" % (uid2[0], uid2[1], uid2[2], uid2[3]))
            b=str(uid2[0])+str(uid2[1])+str(uid2[2])+str(uid2[3])
            print (b)
   
        
if __name__=='__main__':

    continue_reading = True
# Capture SIGINT for cleanup when the script is aborted
    def end_read(signal,frame):
        global continue_reading
        print ("Ctrl+C captured, ending read.")
        continue_reading = False
        GPIO.cleanup()

# Hook the SIGINT
    signal.signal(signal.SIGINT, end_read)
    
    print ("Welcome to the MFRC522 data read example")
    print ("Press Ctrl-C to stop.")

    p1 = Process(target=long_time_task, args=(1,))
    p1.start()
    
    pygame.init()
    pygame.mixer.init()
    screen=pygame.display.set_mode([640,480])
    file2 = b+".mp3"
    try:
        pygame.mixer.music.load(file2)
        pygame.mixer.music.play()
        while pygame.mixer.music.get_busy():      
            pygame.time.delay(100)
        pygame.mixer.music.stop()
    except pygame.error as message:   
        print("Cannot load file")
        pygame.mixer.music.stop()
        
    p1.join()