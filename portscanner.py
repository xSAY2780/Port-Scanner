import socket
from concurrent.futures import ThreadPoolExecutor, as_completed
import time
import sys
from threading import Event, Thread
import platform
import os
import ipaddress

image = """
  _____           _      _____                                 
 |  __ \         | |    / ____|                                
 | |__) |__  _ __| |_  | (___   ___ __ _ _ __  _ __   ___ _ __ 
 |  ___/ _ \| '__| __|  \___ \ / __/ _` | '_ \| '_ \ / _ \ '__|
 | |  | (_) | |  | |_   ____) | (_| (_| | | | | | | |  __/ |   
 |_|   \___/|_|   \__| |_____/ \___\__,_|_| |_|_| |_|\___|_|   
 
"""

print(image)

def ip_check(targetf):
    try:
        ipaddress.ip_address(targetf)
        return True
    except ValueError:
        return False

while True:
    targetf = input("Set Target: ")
    if ip_check(targetf):
        target = targetf
        break
    else:
        print("This Ip Addres is not valid, please enter a valid one.")
        

while True:
    yorn = input("Do you want to set port range (Y) or (N) ")
    if yorn == "Y":
        firstport = int(input("The first port you want to scan: "))
        lastport = int(input("The last port you want to scan: ")) + 1  # Ensure the last port is included
        ports = range(firstport, lastport)
        break
    elif yorn == "N":
        ports = range(1, 1025)
        break
    else:
        print("Please enter 'Y' for yes or 'N' for no.")
        
while True:
    threadinp = input("Do you want to set threads number (Y) or (N) ")
    if threadinp == "Y":
        threadnumber = int(input("The number of the threads: "))
        threadint = threadnumber
        break
    elif threadinp == "N":
        threadint = 100
        break
    else:
        print("Please enter 'Y' for yes or 'N' for no.")

start_time = time.time()

def clear_screen():
    if platform.system() == "Windows":
        os.system("cls")
    else:
        os.system("clear")

def loading_animation(event):
    animation_characters = ['|', '/', '-', '\\']
    i = 0
    while not event.is_set():
        sys.stdout.write('\rScanning ' + animation_characters[i % len(animation_characters)])
        sys.stdout.flush()
        time.sleep(0.1)
        i += 1
    sys.stdout.write('\r' + ' ' * 20)
    sys.stdout.flush()

def scan_port(port):
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.settimeout(1)
            if s.connect_ex((target, port)) == 0:
                clear_screen()
                print(image)
                return f"\rPort {port} is open!              "
    except Exception as e:
        return None

stop_animation = Event()
animation_thread = Thread(target=loading_animation, args=(stop_animation,))
animation_thread.start()

open_ports = []
with ThreadPoolExecutor(max_workers=threadint) as executor:
    future_to_port = {executor.submit(scan_port, port): port for port in ports}
    for future in as_completed(future_to_port):
        result = future.result()
        if result:
            open_ports.append(result)

stop_animation.set()
animation_thread.join()

print(f"Scanning results for IP {target}\n ")

for open_port in open_ports:
    print(open_port)

if not open_ports:
    clear_screen()
    print(image)
    print(f"No open ports found at IP {target}")

finish_time = time.time()
timem =  finish_time - start_time
minutes = int(timem // 60)
seconds = timem % 60

if seconds.is_integer():
    print(f"\nScanning completed {minutes} in minutes and {int(seconds)} seconds!")
else:
    print(f"\nScanning completed {minutes} in minutes and {seconds:.2f} seconds!")
