import numpy as np
import cv2 as cv
import pyautogui
import os
from time import time
from windowcapture import WindowCapture
import pytesseract as tess
tess.pytesseract.tesseract_cmd = r'C:\Users\---USER---\AppData\Local\Tesseract-OCR\tesseract.exe'
from PIL import Image

#windows needs to not be minamized else all black


wincap = WindowCapture('REALPOSEIDON · DLive - Brave')
#name found via windowcapture.py

loop_time = time()

#find full name of the window you want to capture without hex number
#uncomment this to find the names of the windows
##wincap.list_windows_names()
##exit()

cycle = 0
grab = 0

while True:
    #this is how you quit the window
    if cv.waitKey(1) == ord('q'):
        cv.destroyAllWindows()
        break

    screenshot = wincap.get_screenshot()

    cv.imshow('Computer Vision', screenshot)

    print('FPS {}'.format(1 / (time() - loop_time)))
    loop_time = time()

    #i compare a screen shot with the Claim now thing
    #img = Image.open('gifted2.png')
    img = Image.open('current.jpg')

    text = tess.image_to_string(img)
    #print(text)

    #makes a text file and saves the img text
    #watch out for user input.
    #most streaming/chat places aggressivly block out when people try to put code into the chat
    #however your gonna be saving that text.
    #so use at your own risk until futher development
    report = open('dlive_report.txt', 'w')
    report.write(text)
    report.close()
    #print(text)
    
    

   #opens and read text file. If finds Claim it clicks
    open('dlive_report.txt', 'r').read().find('Claim')
    with open('dlive_report.txt') as f:
        if "Claim" in f.read():
            print("true, Found Claim")
            #move and click to expected area.
            #could do some mouse event thing and draw a circle around it for feed back
            #currently running on a live dlive stream while testing
            #despite this dude having 10k viewers, no one has gifted a sub for 20+ minutes ~_~
            #I usually see subs flying out for streams with only 300 people.
            pyautogui.moveTo(x=141, y=200)
            pyautogui.click()
            grab += 1
            print("GOTTEM")

        else:
            #print("false")
            cycle += 1

  

# When everything done, release the capture
#cap.release()
print(" ")
print(" ")
print('Done.')
print(" ")
print("cycled this many times: ")
print(cycle)
print(" ")
print("this many subs grabbed: ")
print(grab)
print(" ")
print(" ")
