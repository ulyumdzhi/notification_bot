import re
import time
import logging

def email_checker(email: str):
    match = re.findall(r'[\w.+-]+@[\w-]+\.[\w.-]+', email)
    try:
        logging.info(f"email_checker at {time.strftime('%X %x')} find email = {match[0]}")
    except:
        logging.info(f"email_checker at {time.strftime('%X %x')} find NO email = {match}")
    return match, len(match)

def phone_checker(phone: str):
    match = re.findall(r'(([\+][7]|[8])(9\d{2}\d{3}\d{4}$))', phone.replace(' ', ''))
    try:
        logging.info(f"phone_checker at {time.strftime('%X %x')} find number = {match[0][0]}")
    except:
        logging.info(f"phone_checker at {time.strftime('%X %x')} find NO number = {match}")

    try: 
        return match[0][0], len(match)
    except: 
        return 0, 0



        
