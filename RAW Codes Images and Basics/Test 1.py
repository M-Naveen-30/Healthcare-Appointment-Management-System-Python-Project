import time
import calendar
import random as r
import pygame as p
import qrcode
import pywhatkit as pk
import pyautogui as pg
from PIL import Image, ImageDraw, ImageFont
from datetime import datetime

# STEP 1 : HOSPITAL LOGO
p.init()
p.display.set_caption("H.A.S (HOSPITAL APPOINTMENT SYSTEM)")
ps1 = p.display.set_mode((500, 500))
ps = p.image.load(r"C:\Users\Naveen M\OneDrive\Desktop\HAS (Hospital Appointment System)\hospital_logo.jpeg")
ps = p.transform.scale(ps, (500, 500)
ps1.blit(ps, (0, 0))
p.display.update()
time.sleep(4)
p.quit()

# STEP 2 : WELCOME PAGE
print("****************** WELCOME TO SALEM GH APPOINTMENT SYSTEM ******************")

# STEP 3 : REGISTER
name = input("ENTER YOUR NAME : ")
age = int(input("ENTER YOUR AGE : "))
phone = int(input("ENTER YOUR PHONE NUMBER : "))
password = int(input("ENTER YOUR PASSWORD : "))

# STEP 4 : USER LOGIN
print("------------------- LOGIN FORM -------------------")
def login():
    user = input("USER NAME : ")
    if user == name:
        p1 = int(input("ENTER YOUR PASSWORD : "))
        if p1 == password:
            print("LOGIN SUCCESSFUL")
        else:
            print("PASSWORD INCORRECT"); login()
    else:
        print("USERNAME INCORRECT"); login()
login()

# STEP 5 : OTP GENERATION
otp = r.randint(1000, 9999)
print("SENDING OTP TO YOUR WHATSAPP NUMBER ...")
try:
    pk.sendwhatmsg_instantly(f"+91{phone}", f"Your Salem GH OTP is : {otp}", wait_time=15, tab_close=True)
    time.sleep(5); pg.doubleClick()
except Exception as e:
    print("(WhatsApp OTP could not be sent. Debug OTP:", otp, ")")

def otp_check():
    attempts = 0
    while attempts < 3:
        u = int(input("ENTER THE OTP RECEIVED ON WHATSAPP : "))
        if u == otp:
            print("OTP VERIFIED.  LOGIN SUCCESSFUL"); return
        print("INCORRECT OTP, TRY AGAIN"); attempts += 1
    print("TOO MANY WRONG ATTEMPTS"); exit()
otp_check()

# STEP 6 : DOCTORS IMAGE
p.init()
p.display.set_caption("AVAILABLE DOCTORS - SALEM GH")
ps1 = p.display.set_mode((600, 600))
ps1.blit(ps, (0, 0))
p.display.update()
time.sleep(5)
p.quit()

# STEP 7 : LIST DOCTORS
print("================ AVAILABLE DOCTORS ================")
for d in ["1.DR.PONVANAN  (CARDIOLOGIST)",
          "2.DR.VASUDHA   (OBSTETRICIAN)",
          "3.DR.SAM       (GENERAL MEDICINE)",
          "4.DR.NETHRA    (PEDIATRICIAN)"]:
    print(d)

# STEP 8 : MAY CALENDAR
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

# STEP 9 : TIMING
def pick_timing():
    print("\nAVAILABLE TIMINGS :")
    for t in ["1.DAY     (8:30 - 11:30)",
              "2.NOON    (12:00 - 2:30)",
              "3.EVENING (5:00 - 8:30)"]:
        print(t)
    while True:
        try:
            c = int(input("SELECT TIMING (1/2/3) : "))
            if c == 1: return "DAY (8:30 - 11:30)"
            if c == 2: return "NOON (12:00 - 2:30)"
            if c == 3: return "EVENING (5:00 - 8:30)"
            print("INVALID TIMING, TRY AGAIN")
        except ValueError:
            print("ENTER 1, 2 OR 3")

# STEP 10 : TOKEN
def get_token():
        while True:
            try:
                t = int(input("ENTER PREFERRED TOKEN NUMBER (1 / 2 / 3) : "))
                if t in (1, 2, 3): return t
                print("ONLY TOKENS 1, 2 OR 3 ARE ALLOWED")
            except ValueError:
                print("ENTER A VALID NUMBER")

# STEP 11 : BOOK APPOINTMENT
def book_appointment():
    global doctor_name, appointment_date, appointment_time, purpose, token
    while True:
            try:
                ch = int(input("\nENTER DOCTOR NUMBER (1/2/3/4) : "))
            except ValueError:
                print("ENTER A NUMBER")
                continue
            if ch == 1:
                doctor_name = "DR.PONVANAN (CARDIOLOGIST)"; break
            elif ch == 2:
                doctor_name = "DR.VASUDHA (OBSTETRICIAN)"; break
            elif ch == 3:
                doctor_name = "DR.SAM (GENERAL MEDICINE)"; break
            elif ch == 4:
                doctor_name = "DR.NETHRA (PEDIATRICIAN)"; break
            else:
                print("INVALID DOCTOR, TRY AGAIN")
                print("YOU SELECTED :", doctor_name)
                appointment_date = show_may_calendar()
                appointment_time = pick_timing()
                purpose = input("PURPOSE OF VISIT : ")
                token = get_token()
                print("TOKEN ALLOCATED :", token)

    book_appointment()

# STEP 12 : PY-PAY QR
    def show_payment_qr():
        pay_id = "PY-Pay-" + str(r.randint(100000, 999999))
        qr = qrcode.QRCode(version=2, box_size=10, border=4)
        qr.add_data(f"PY-Pay | Salem GH | {pay_id} | Token:{token}")
        qr.make(fit=True)
        img = qr.make_image(fill_color="black", back_color="white").convert("RGB")
        canvas = Image.new("RGB", (img.size[0], img.size[1] + 80), "white")
        canvas.paste(img, (0, 80))
        draw = ImageDraw.Draw(canvas)
        try:
            font = ImageFont.truetype("arial.ttf", 40)
        except:
            font = ImageFont.load_default()
        draw.text((canvas.size[0] // 2 - 80, 20), "PY-Pay", fill="green", font=font)
        canvas.save("py_pay_qr.png")
        p.init()
        p.display.set_caption("PY-Pay - SCAN TO PAY")
        ps1 = p.display.set_mode(canvas.size)
        ps1.blit(p.image.load("py_pay_qr.png"), (0, 0))
        p.display.update()
        time.sleep(5)
        p.quit()

    show_payment_qr()
    print("==================== THANK YOU !  PAYMENT SUCCESSFUL ====================")

# STEP 13 : APPOINTMENT IMAGE
wa_mobile = input("ENTER YOUR WHATSAPP MOBILE NUMBER : ")
def make_slip():
    W, H = 700, 600
    img = Image.new("RGB", (W, H), "white")
    d = ImageDraw.Draw(img)
    try:
        tf = ImageFont.truetype("arialbd.ttf", 30)
        hf = ImageFont.truetype("arialbd.ttf", 22)
        bf = ImageFont.truetype("arial.ttf", 20)
    except:
        tf = hf = bf = ImageFont.load_default()
    d.rectangle([(0,0),(W,70)], fill=(220,30,80))
    d.text((20,18),"SALEM GOVERNMENT HOSPITAL",fill="white",font=tf)
    y = 100
    d.text((30,y),"APPOINTMENT SLIP",fill=(220,30,80),font=hf); y += 50
    for line in [f"NAME             : {name}",
                 f"AGE              : {age}",
                 f"MOBILE NUMBER    : {wa_mobile}",
                 f"DOCTOR           : {doctor_name}",
                 f"APPOINTMENT DATE : {appointment_date}",
                 f"APPOINTMENT TIME : {appointment_time}",
                 f"PURPOSE OF VISIT : {purpose}",
                 f"TOKEN NUMBER     : {token}"]:
        d.text((30, y), line, fill="black", font=bf)
        y += 40
    d.rectangle([(0, H - 70), (W, H)], fill=(0, 150, 80))
    d.text((140, H - 55), "PAYMENT SUCCESSFUL - THANK YOU !", fill="white", font=hf)
    img.save("appointment_slip.png")
    return "appointment_slip.png"


slip_path = make_slip()
print("APPOINTMENT SLIP GENERATED :", slip_path)

# STEP 14 : SEND APPOINTMENT IMAGE ON WHATSAPP
print("SENDING APPOINTMENT SLIP TO WHATSAPP ...")
try:
    pk.sendwhats_image(
        receiver=f"+91{wa_mobile}",
        img_path=slip_path,
        caption=f"Salem GH Appointment\nName: {name}\nDoctor: {doctor_name}\nDate: {appointment_date}\nTime: {appointment_time}\nToken: {token}\nPAYMENT SUCCESSFUL",
        wait_time=20, tab_close=True)
    time.sleep(5); pg.doubleClick()
    print("APPOINTMENT SLIP SENT SUCCESSFULLY ON WHATSAPP")
except Exception as e:
    print("(Could not auto-send via WhatsApp:", e, ")")
    print("Slip saved locally at :", slip_path)

print("****************** THANK YOU FOR USING SALEM GH APPOINTMENT SYSTEM ******************")




