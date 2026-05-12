import time
from collections import defaultdict
import re

FILENAME = 'Linux_2k.log'
THRESHOLD = 10

failed_attempts = defaultdict(int)

with open(FILENAME, "r") as f:
    while True:
        line = f.readline()  
        if line:
            match = re.search(r"rhost=(\S+)", line)
            if match:
                ip = match.group(1)
                failed_attempts[ip] += 1
                if failed_attempts[ip] == THRESHOLD:
                    print(f"[ALERT] {ip} just crossed {THRESHOLD} attempts!")
        else:
            time.sleep(0.5) 