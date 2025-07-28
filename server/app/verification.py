import pyotp
import asyncio
import os
from smtplib import SMTP
from dotenv import load_dotenv

load_dotenv()  # Load once at startup

def sync_send_mail(email: str, otp: str) -> bool:
    smtp_server = "smtp.gmail.com"
    smtp_port = 587
    sender_email = os.getenv('EMAIL')
    password = os.getenv('PASSWORD')
    
    if not sender_email or not password:
        raise ValueError("SMTP credentials missing")
    
    try:
        with SMTP(smtp_server, smtp_port) as server:
            server.starttls()
            server.login(sender_email, password)
            message = f"Subject: Your OTP Code\n\nYour OTP is: {otp}. Valid for 5 minutes."
            server.sendmail(sender_email, email, message)
        return True
    except Exception as e:
        print(f"SMTP error: {e}")
        return False

async def send_mail(email: str, otp: str) -> bool:
    return await asyncio.to_thread(sync_send_mail, email, otp)

async def send_otp(email: str) -> str:
    key = pyotp.random_base32()
    totp = pyotp.TOTP(key, digits=6, interval=300)
    otp = totp.now()
    await send_mail(email, otp)
    return key

async def verify_otp(user_otp: str, key: str) -> bool:
    if not user_otp:
        return False
    totp = pyotp.TOTP(key, digits=6, interval=300)
    return totp.verify(user_otp, valid_window=1)