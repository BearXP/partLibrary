# https://medium.com/mlearning-ai/use-python-to-send-outlook-emails-d673ce9e33e4
# https://learn.microsoft.com/en-us/office/vba/api/outlook.mailitem


import win32com.client as win32
from db import Database
import time
from datetime import datetime


def subject(user, part):
    userName = str(user["name"])
    itemName = str(part["name"])
    return f"ATTENTION {userName.upper()} - {itemName} IS OVERDUE"


def body(part):
    borrowtime = float(part["timestamp"])
    borrowtimeDT = datetime.fromtimestamp(borrowtime)
    dateFormat = "%d/%b/%Y"
    borrowtimeStr = borrowtimeDT.strftime(dateFormat)
    return f"{part['name']} was borrowed out on {borrowtimeStr}.<br>If you are still using this equipment please return it to the lab and borrow it again.<br><br> - Mark."


def receiver(user):
    return user["name"] + "@leicabiosystems.com"


def create_mail(text, subject, recipient, send=True):
    outlook = win32.Dispatch("outlook.application")
    mail = outlook.CreateItem(0)
    mail.To = recipient
    mail.Subject = subject
    mail.BodyFormat = 2
    mail.HtmlBody = text
    mail.Importance = 2

    if send:
        mail.send()
    else:
        mail.save()


db = Database()
equipment = db.getOverdueEquipment()

for item in equipment:
    # Part should be returned
    borrower = db.getId(item["status"])
    emailBody = body(item)
    emailSubject = subject(borrower, item)
    emailAddress = receiver(borrower)
    create_mail(emailBody, emailSubject, emailAddress, send=False)
