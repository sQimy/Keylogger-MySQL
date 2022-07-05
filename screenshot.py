from mss import mss
from datetime import datetime


def capture_screen():
    time = datetime.now().strftime(r'%Y-%m-%d %H-%M-%S')
    filename = f'screenshots/{time}.png'

    with mss() as screenshot:
        screenshot.shot(mon=-1, output=filename)

    return filename, time

def current_time():
    timestamp = datetime.now().strftime(r'%Y-%m-%d %H-%M-%S')
    return(timestamp)

if __name__ == "__main__":
    capture_screen()