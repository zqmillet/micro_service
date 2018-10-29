import datetime

from resources.now import now

def update_now():
    global now
    now = datetime.datetime.now()
