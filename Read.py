import RPi.GPIO as GPIO
import MFRC522
import MFRC52202
import signal
import time
import pygame
import Queue

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
print ("Welcome to the MFRC522 data read example")
print ("Press Ctrl-C to stop.")

q1 = Queue.Queue(maxsize=10)
q2 = Queue.Queue(maxsize=10)
q1.put(1)

pygame.init()
pygame.mixer.init()
screen=pygame.display.set_mode([640,480])
pygame.time.delay(1000)

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
        q1.put(a)
        time.sleep(0.1)
        
        #pygame.init()
        #pygame.mixer.init()
        #screen=pygame.display.set_mode([640,480])
        #pygame.time.delay(1000)
        file1 = a+".mp3"
        
        
        #MIFAREReader2 = MFRC52202.MFRC52202()
        #(status2,TagType2) = MIFAREReader2.MFRC522_Request(MIFAREReader2.PICC_REQIDL)    
        #(status2,uid2) = MIFAREReader2.MFRC522_Anticoll()
        if a != q1.get():
            #while pygame.mixer.music.get_busy():      
                #pygame.time.delay(100)
            pygame.mixer.music.stop()
            pygame.mixer.music.unload()
            pygame.mixer.music.load(file1)
            pygame.mixer.music.play(2)
        if status2 == MIFAREReader2.MI_OK:
            print ("Card2 read UID: %s,%s,%s,%s" % (uid2[0], uid2[1], uid2[2], uid2[3]))
            b=str(uid2[0])+str(uid2[1])+str(uid2[2])+str(uid2[3])
            print (b)
            q2.put(b)
            file2 = b+".mp3"
            #time.sleep(1)
            if b == q2.get():
                try:            
                    #while pygame.mixer.music.get_busy():
                        #pygame.time.delay(100) 
                    pygame.mixer.music.load(file2)
                    pygame.mixer.music.queue(file2)
                    #pygame.mixer.music.play(2)
                except pygame.error as message:   
                    print("Cannot load file")
                    pygame.mixer.music.stop()
    if status2 == MIFAREReader2.MI_OK and status != MIFAREReader.MI_OK:
        #time.sleep(0.5)
        print ("Card2 read UID: %s,%s,%s,%s" % (uid2[0], uid2[1], uid2[2], uid2[3]))
        b=str(uid2[0])+str(uid2[1])+str(uid2[2])+str(uid2[3])
        print (b)
        q2.put(b)
        file2 = b+".mp3"
        #pygame.init()
        #pygame.mixer.init()
        #screen=pygame.display.set_mode([640,480])
        #pygame.time.delay(1000)
        if b == q2.get() or q2.empty():
            try:            
                #while pygame.mixer.music.get_busy():
                    #pygame.time.delay(100)  
                pygame.mixer.music.load(file2)              
                pygame.mixer.music.play(2)
            except pygame.error as message:   
                print("Cannot load file")
                pygame.mixer.music.stop()
    if not pygame.mixer.music.get_busy(): 
        pygame.mixer.music.unload()
                
