import signal
import pygame
import time
import RPi.GPIO as GPIO
pygame.mixer.init()
pygame.time.delay(10)
file1 = "5249230101"+".mp3"
o1=open(file1)
file2 = "15324111246"+".mp3"
o2=open(file2)
pygame.mixer.music.load(file1)
pygame.mixer.music.play()
while pygame.mixer.music.get_busy():
    pygame.time.delay(10)
pygame.mixer.music.stop()
o1.close()
#====================
time.sleep(0.1)
pygame.mixer.init()
pygame.mixer.music.load(file2)
pygame.mixer.music.play()
while pygame.mixer.music.get_busy():
    pygame.time.delay(10)
pygame.mixer.music.stop()
o2.close()
