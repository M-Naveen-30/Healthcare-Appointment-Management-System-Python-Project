import time
import calendar
import random as r
import pygame as p
import qrcode
import pywhatkit as pk
import pyautogui as pg
from PIL import Image, ImageDraw, ImageFont
from datetime import datetime

#STEP 1 : HOSPITAL LOGO
p.init()
p.display.set_caption("H.A.S (HOSPITAL APPOINTMENT SYSTEM)")
ps1 = p.display.set_mode((500, 500))
ps = p.image.load(r"C:\Users\Naveen M\OneDrive\Desktop\HAS (Hospital Appointment System)\hospital_logo.jpeg")
ps = p.transform.scale(ps, (500, 500))
ps1.blit(ps, (0, 0))
p.display.update()
time.sleep(4)
p.quit()

#STEP 2 : WELCOME PAGE
print("****************** WELCOME TO SALEM GH APPOINTMENT SYSTEM ******************")

#STEP 3 : REGISTER
name = input("ENTER YOUR NAME : ")
age = int(input("ENTER YOUR AGE : "))
phone = int(input("ENTER YOUR PHONE NUMBER : "))
gender=input("ENTER YOUR GENDER :")
password=input(("ENTER YOUR PASSWORD :"))

print("LOGIN FORM")

#STEP 4 : USER LOGIN FORM
print("------------------- LOGIN FORM -------------------")
def login():
     user = input("USER NAME : ")
     if user == name:
         p1 = input(("ENTER YOUR PASSWORD : "))
         if p1 == password:
             otp = r.randint(1000, 9999)
             print("SENDING OTP TO YOUR WHATSAPP NUMBER ...")
             try:
                 pk.sendwhatmsg_instantly(f"+91{8870737287}", f"Your Salem GH OTP is : {otp}", wait_time=15,
                                          tab_close=True)
                 time.sleep(5);
                 pg.doubleClick()
             except Exception as e:
                 print("(WhatsApp OTP could not be sent. Debug OTP:", otp, ")")
                 print("LOGIN SUCCESSFUL")
         else:
             print("PASSWORD INCORRECT"); login()
     else:
         print("USERNAME INCORRECT")
         login()
login()

#STEP 5 : OTP GENERATION
# otp = r.randint(1000, 9999)
# print("SENDING OTP TO YOUR WHATSAPP NUMBER ...")
# try:
#      pk.sendwhatmsg_instantly(f"+91{8870737287}", f"Your Salem GH OTP is : {otp}", wait_time=15, tab_close=True)
#      time.sleep(5); pg.doubleClick()
# except Exception as e:
#     print("(WhatsApp OTP could not be sent. Debug OTP:", otp, ")")

def otp_check():
     attempts = 0
     while attempts < 3:
         u = int(input("ENTER THE OTP RECEIVED ON WHATSAPP : "))
         if u == otp:
             print("OTP VERIFIED.  LOGIN SUCCESSFUL"); return
         print("INCORRECT OTP, TRY AGAIN"); attempts += 1
     print("TOO MANY WRONG ATTEMPTS")
     exit()

#STEP 6 : DOCTORS IMAGE
p.init()
p.display.set_caption("AVAILABLE DOCTORS - SALEM GH")
ps1 = p.display.set_mode((900, 900))
ps = p.image.load(r"C:\Users\Naveen M\OneDrive\Desktop\HAS (Hospital Appointment System)\doctors.jpeg")
ps = p.transform.scale(ps, (900, 900))
ps1.blit(ps, (0, 0))
p.display.update()
time.sleep(10)
p.quit()

#STEP 7 : LIST DOCTORS
print("================ AVAILABLE DOCTORS ================")
for d in ["1.DR.PONVANAN  (CARDIOLOGIST)",
           "2.DR.VASUDHA   (OBSTETRICIAN)",
           "3.DR.SAM       (GENERAL MEDICINE)",
           "4.DR.NETHRA    (PEDIATRICIAN)"]:
     print(d)

#STEP 8: SELECT THE DOCTORS

#STEP  : MAY CALENDAR
def show_may_calendar():
    y = datetime.now().year
    print("\n--------- MAY", y, "APPOINTMENT CALENDAR ---------")
    print(calendar.month(y, 5))
    while True:
         try:
             d = int(input("SELECT THE DATE (1-31) : "))
             if 1 <= d <= 31: return f"{d:02d}-05-{y}"
             print("INVALID DATE, TRY AGAIN")
         except ValueError:
             print("ENTER A VALID NUMBER")

