import time
import os
import sys
import json
import random as r
import calendar
from datetime import datetime

import pygame as p
import pywhatkit as pk
import pyautogui as pg
import qrcode
from PIL import Image, ImageDraw, ImageFont
from reportlab.lib.pagesizes import A5
from reportlab.pdfgen import canvas as pdf_canvas
from reportlab.lib.utils import ImageReader

# --------------------------------------------------------------------------
#  CONFIG
# --------------------------------------------------------------------------
ASSETS_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "assets")
DB_FILE    = os.path.join(os.path.dirname(os.path.abspath(__file__)), "appointments.json")

LOGO_FILE   = os.path.join(ASSETS_DIR, "hospital_logo.jpg")
MUSIC_FILE  = os.path.join(ASSETS_DIR, "welcome.mp3")
DOCS_FILE   = os.path.join(ASSETS_DIR, "doctors.jpg")
DOC_IMG = {
    1: os.path.join(ASSETS_DIR, "dr_ponvanan.jpg"),
    2: os.path.join(ASSETS_DIR, "dr_vasudha.jpg"),
    3: os.path.join(ASSETS_DIR, "dr_sam.jpg"),
    4: os.path.join(ASSETS_DIR, "dr_nethra.jpg"),
}
DOC_NAME = {
    1: "Dr. Ponvanan  (Cardiologist)",
    2: "Dr. Vasudha   (Obstetrician)",
    3: "Dr. Sam       (General Medicine)",
    4: "Dr. Nethra    (Pediatrician)",
}
TIME_SLOT = {
    1: "DAY     (08:30 - 11:30)",
    2: "NOON    (12:00 - 02:30)",
    3: "EVENING (05:00 - 08:30)",
}


# --------------------------------------------------------------------------
#  small helpers
# --------------------------------------------------------------------------
def show_image(path, caption, seconds, size=(640, 640), with_music=False):

    p.init()
    p.display.init()
    p.display.set_caption(caption)
    screen = p.display.set_mode(size)
    # convert() makes the surface match the display format - needed on
    # Windows for the image to actually appear.
    raw = p.image.load(path)
    try:
        raw = raw.convert()
    except p.error:
        raw = raw.convert_alpha()
    img = p.transform.smoothscale(raw, size)

    if with_music and os.path.exists(MUSIC_FILE):
        try:
            p.mixer.init()
            p.mixer.music.load(MUSIC_FILE)
            p.mixer.music.play()
        except Exception as e:
            print("(music could not play:", e, ")")

    clock = p.time.Clock()
    end = time.time() + seconds
    while time.time() < end:
        for ev in p.event.get():
            if ev.type == p.QUIT:
                end = 0
        screen.fill((255, 255, 255))
        screen.blit(img, (0, 0))
        p.display.flip()        # flip() is more reliable than update()
        clock.tick(30)

    if with_music:
        try:
            p.mixer.music.stop()
        except Exception:
            pass
    p.quit()


def load_db():
    if os.path.exists(DB_FILE):
        with open(DB_FILE, "r") as f:
            return json.load(f)
    return {"appointments": []}


def save_db(db):
    with open(DB_FILE, "w") as f:
        json.dump(db, f, indent=2, default=str)


# --------------------------------------------------------------------------
#  STEP 1  -  LOGO + MUSIC
# --------------------------------------------------------------------------
print("Loading Salem Government Hospital ...")
show_image(LOGO_FILE, "SALEM GOVERNMENT HOSPITAL", seconds=10, size=(640, 640),
           with_music=True)

# --------------------------------------------------------------------------
#  STEP 2  -  WELCOME BANNER
# --------------------------------------------------------------------------
stars = "*" * 15
print()
print(stars + "  WELCOME TO SALEM GH APPOINTMENT SYSTEM  " + stars)
print()

# --------------------------------------------------------------------------
#  STEP 3  -  REGISTER
# --------------------------------------------------------------------------
print("------------------------- REGISTRATION -------------------------")
name     = input("ENTER YOUR NAME      : ").strip()
age      = int(input("ENTER YOUR AGE       : "))
gender   = input("ENTER YOUR GENDER    : ").strip()
phone    = input("ENTER YOUR PHONE NO  : ").strip()      # kept as string
password = input("ENTER YOUR PASSWORD  : ").strip()
print("Registration completed successfully.\n")

# --------------------------------------------------------------------------
#  STEP 4  -  LOGIN
# --------------------------------------------------------------------------
print("---------------------------- LOGIN -----------------------------")

def login():
    user = input("USER     : ").strip()
    if user == name:
        pw = input("PASSWORD : ").strip()
        if pw == password:
            print("LOGIN SUCCESSFUL\n")
        else:
            print("PASSWORD INCORRECT - try again")
            login()
    else:
        print("USERNAME INCORRECT - try again")
        login()

login()

# --------------------------------------------------------------------------
#  STEP 5  -  WHATSAPP OTP
# --------------------------------------------------------------------------
print("------------------------- OTP VERIFY ---------------------------")
otp = r.randint(1000, 9999)
wa_phone = phone if phone.startswith("+") else "+91" + phone
otp_msg  = (f"Salem GH Appointment System\n"
            f"Hello {name}, your login OTP is : {otp}\n"
            f"(valid for 5 minutes)")

print(f"Sending OTP to WhatsApp {wa_phone} ...")
try:
    # opens WhatsApp Web and sends instantly
    pk.sendwhatmsg_instantly(wa_phone, otp_msg, wait_time=15, tab_close=True)
    time.sleep(8)
    pg.click()           # focus the WA window if needed
except Exception as e:
    # fallback - if WA Web fails (no internet / not logged-in) we still
    # print the OTP so the user can finish the flow.  This DOES NOT use
    # if/else for the whatsapp send itself - it is only an exception net.
    print("(WhatsApp send failed:", e, "- printing OTP locally)")
    print("YOUR OTP :", otp)

def verify_otp():
    e_otp = input("ENTER THE OTP RECEIVED : ").strip()
    if e_otp == str(otp):
        print("OTP VERIFIED - LOGIN COMPLETE\n")
    else:
        print("INVALID OTP")
        verify_otp()

verify_otp()

# --------------------------------------------------------------------------
#  STEP 6  -  4 DOCTORS GROUP PHOTO
# --------------------------------------------------------------------------
print("Available doctors today ...")
show_image(DOCS_FILE, "DOCTORS AVAILABLE TODAY", seconds=7, size=(800, 800))

# --------------------------------------------------------------------------
#  STEP 7 + 8  -  CHOOSE DOCTOR
# --------------------------------------------------------------------------
print("------------------------ CHOOSE DOCTOR -------------------------")
for k, v in DOC_NAME.items():
    print(f"  {k}. {v}")

doctor_choice = 0
while doctor_choice not in DOC_NAME:
    try:
        doctor_choice = int(input("ENTER DOCTOR NUMBER (1-4) : "))
    except ValueError:
        doctor_choice = 0
    if doctor_choice not in DOC_NAME:
        print("Invalid choice - please pick 1, 2, 3 or 4")

doctor_name = DOC_NAME[doctor_choice]
print(f"You selected -> {doctor_name}\n")
show_image(DOC_IMG[doctor_choice], doctor_name, seconds=5, size=(500, 500))

# --------------------------------------------------------------------------
#  STEP 9  -  MAY CALENDAR (current year)
# --------------------------------------------------------------------------
year_now = datetime.now().year
print(f"------------- MAY {year_now} CALENDAR -------------")
print(calendar.month(year_now, 5))

# --------------------------------------------------------------------------
#  STEP 10  -  PICK DATE
# --------------------------------------------------------------------------
day = 0
while not (1 <= day <= 31):
    try:
        day = int(input("ENTER APPOINTMENT DATE (1-31 of May) : "))
    except ValueError:
        day = 0
    if not (1 <= day <= 31):
        print("Invalid date - please enter again")

appt_date = f"{day:02d}-MAY-{year_now}"
print(f"Date selected : {appt_date}\n")

# --------------------------------------------------------------------------
#  STEP 11  -  PICK TIME SLOT
# --------------------------------------------------------------------------
print("--------- AVAILABLE TIME SLOTS ---------")
for k, v in TIME_SLOT.items():
    print(f"  {k}. {v}")

slot = 0
while slot not in TIME_SLOT:
    try:
        slot = int(input("PICK A SLOT (1/2/3) : "))
    except ValueError:
        slot = 0
    if slot not in TIME_SLOT:
        print("Invalid slot - try again")

appt_time = TIME_SLOT[slot]
print(f"Time slot       : {appt_time}\n")

# --------------------------------------------------------------------------
#  STEP 12  -  PURPOSE OF VISIT
# --------------------------------------------------------------------------
purpose = input("PURPOSE OF VISIT : ").strip()
print()

# --------------------------------------------------------------------------
#  STEP 13  -  TOKEN ALLOCATION
# --------------------------------------------------------------------------
db = load_db()
slot_key = f"{doctor_choice}|{appt_date}|{slot}"

# count how many already booked in same doctor/date/slot
already = sum(1 for a in db["appointments"] if a["slot_key"] == slot_key)

if already >= 3:
    print("Sorry - all 3 tokens for this doctor/date/slot are already booked.")
    print("Please restart and choose a different slot.")
    sys.exit(0)

token_no = already + 1
print(f"YOUR TOKEN NO is .... {token_no}\n")

# --------------------------------------------------------------------------
#  STEP 14  -  PY-PAY QR
# --------------------------------------------------------------------------
fee = 100
upi_str = (f"upi://pay?pa=py-pay@hospital&pn=Salem%20GH&"
           f"am={fee}.00&cu=INR&tn=Token{token_no}-Dr{doctor_choice}")

qr = qrcode.QRCode(version=4, box_size=10, border=2)
qr.add_data(upi_str)
qr.make(fit=True)
qr_img = qr.make_image(fill_color="black", back_color="white").convert("RGB")

W, H = 500, 600
canvas_img = Image.new("RGB", (W, H), "white")
canvas_img.paste(qr_img.resize((480, 480)), (10, 80))
draw = ImageDraw.Draw(canvas_img)
try:
    font_big = ImageFont.truetype("arial.ttf", 40)
    font_sm  = ImageFont.truetype("arial.ttf", 22)
except Exception:
    font_big = ImageFont.load_default()
    font_sm  = ImageFont.load_default()
draw.text((170, 20), "PY-Pay", fill="#d6336c", font=font_big)
draw.text((90,  570), f"Pay Rs.{fee} to confirm appointment", fill="black",
          font=font_sm)

qr_path = os.path.join(ASSETS_DIR, "pypay_qr.png")
canvas_img.save(qr_path)

show_image(qr_path, "PY-Pay  -  Scan to Pay", seconds=15, size=(W, H))

# --------------------------------------------------------------------------
#  STEP 15  -  PAYMENT SUCCESS
# --------------------------------------------------------------------------
print("============================================================")
print("           THANK YOU !  PAYMENT SUCCESSFUL                  ")
print("============================================================\n")

# --------------------------------------------------------------------------
#  STEP 16  -  PILLOW SLIP IMAGE  +  PDF SLIP
# --------------------------------------------------------------------------
print("Enter the WhatsApp number to receive the appointment slip ...")
wa_target = input("WHATSAPP NUMBER (10 digit, +91 added auto) : ").strip()
wa_target = wa_target if wa_target.startswith("+") else "+91" + wa_target

# ---- Pillow slip image ----
SW, SH = 720, 900
slip = Image.new("RGB", (SW, SH), "white")
d    = ImageDraw.Draw(slip)
try:
    f_title = ImageFont.truetype("arialbd.ttf", 34)
    f_h     = ImageFont.truetype("arialbd.ttf", 22)
    f_t     = ImageFont.truetype("arial.ttf",   20)
except Exception:
    f_title = f_h = f_t = ImageFont.load_default()

# header band
d.rectangle([(0, 0), (SW, 90)], fill="#d6336c")
d.text((35, 25), "SALEM GOVERNMENT HOSPITAL", fill="white", font=f_title)

# logo
try:
    logo = Image.open(LOGO_FILE).resize((110, 110))
    slip.paste(logo, (SW - 130, 110))
except Exception:
    pass

# body
y = 130
fields = [
    ("Patient Name  ", name),
    ("Age           ", str(age)),
    ("Gender        ", gender),
    ("Mobile        ", phone),
    ("Doctor        ", doctor_name),
    ("Appt Date     ", appt_date),
    ("Appt Time     ", appt_time),
    ("Purpose       ", purpose),
    ("Token No      ", str(token_no)),
    ("Fee Paid      ", f"Rs. {fee}"),
]
for label, val in fields:
    d.text((40, y), f"{label}: {val}", fill="#222222", font=f_t)
    y += 40

# footer
d.rectangle([(0, SH - 90), (SW, SH)], fill="#12b886")
d.text((140, SH - 65), "PAYMENT SUCCESSFUL  -  THANK YOU !", fill="white",
       font=f_h)

slip_img_path = os.path.join(ASSETS_DIR, f"slip_{token_no}.png")
slip.save(slip_img_path)
print("Slip image saved at :", slip_img_path)

# ---- ReportLab PDF slip ----
slip_pdf_path = os.path.join(ASSETS_DIR, f"slip_{token_no}.pdf")
c = pdf_canvas.Canvas(slip_pdf_path, pagesize=A5)
c.drawImage(ImageReader(slip_img_path), 20, 20,
            width=A5[0] - 40, height=A5[1] - 40, preserveAspectRatio=True)
c.showPage()
c.save()
print("Slip PDF saved at  :", slip_pdf_path)

# save to local DB for availability tracking
db["appointments"].append({
    "slot_key"   : slot_key,
    "name"       : name,
    "age"        : age,
    "gender"     : gender,
    "phone"      : phone,
    "doctor"     : doctor_name,
    "date"       : appt_date,
    "time"       : appt_time,
    "purpose"    : purpose,
    "token"      : token_no,
    "wa_target"  : wa_target,
    "created_at" : datetime.now().isoformat(),
})
save_db(db)

# --------------------------------------------------------------------------
#  STEP 17  -  SEND SLIP ON WHATSAPP
# --------------------------------------------------------------------------
print("\nSending appointment slip to", wa_target, "via WhatsApp ...")
caption = (f"Salem GH Appointment Slip\n"
           f"Patient : {name}\nDoctor : {doctor_name}\n"
           f"Date : {appt_date}  |  Slot : {appt_time}\n"
           f"Token No : {token_no}\nPayment : SUCCESSFUL")

try:
    # Primary attempt - sends the slip image (needs pywin32 on Windows)
    pk.sendwhats_image(wa_target, slip_img_path, caption=caption,
                       wait_time=20, tab_close=True)
    time.sleep(10)
    pg.click()
except Exception as e:
    # Fallback - if pywin32 / clipboard is missing, send a TEXT message
    # with all the slip info so the user still gets the appointment on
    # WhatsApp.  The image + PDF are already saved locally.
    print("(image send failed:", e, "- sending text instead)")
    try:
        pk.sendwhatmsg_instantly(wa_target, caption,
                                 wait_time=20, tab_close=True)
        time.sleep(8)
        pg.click()
        print("Slip details sent as text message.")
        print("Slip image saved locally at :", slip_img_path)
    except Exception as e2:
        print("(text send also failed:", e2, ")")
        print("Slip image is still saved at :", slip_img_path)

print("\n============================================================")
print("   APPOINTMENT BOOKED - SEE YOU AT SALEM GOVT HOSPITAL !    ")
print("============================================================")
