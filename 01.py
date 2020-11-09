import threading
import time
import RPi.GPIO as GPIO
import MFRC522
import MFRC52202
import signal
import pygame
import Queue
a= True
def one():
    while a:
        print("1")
def two():
    while a:
        print("2")
t1=threading.Thread(target=one)
t2=threading.Thread(target=two)
t1.start()
t2.start()
