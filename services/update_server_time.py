import datetime

from resources.now import now

def update_server_time():
    now.update()
    return 'true'
