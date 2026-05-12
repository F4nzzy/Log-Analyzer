# fake log file from    https://github.com/logpai/loghub

import re 
from collections import defaultdict
import csv
import requests

THRESHOLD = 10 
FILENAME = "Linux_2k.log"

failed_attempts = defaultdict(int)
flagged_users = defaultdict(set) 
first_seen = {}
last_seen = {}

with open(FILENAME, "r") as f:
    for i, line in enumerate(f): 
        match = re.search(r"rhost=(\S+)", line)
        if match:
            failed_attempts[match.group(1)] += 1
            user = re.search(r"user=(\S+)", line)
            date = re.search(r"(\w+ \d+ \d+:\d+:\d+)", line)
            if date: 
                if match.group(1) not in first_seen: 
                    first_seen[match.group(1)] = date.group(1)
                last_seen[match.group(1)] = date.group(1)
            if user: 
                flagged_users[match.group(1)].add(user.group(1))

geo = {}
for ip, count in failed_attempts.items():
    if count > THRESHOLD and re.match(r"^\d+\.\d+\.\d+\.\d+$", ip):
        try:
            response = requests.get(f"http://ip-api.com/json/{ip}", timeout=5)
            data = response.json()
            if data["status"] == "success":
                geo[ip] = {"country": data["country"], "city": data["city"]}
        except Exception:
            geo[ip] = {"country": "Lookup failed", "city": ""}

with open("report.csv", "w", newline="") as f:
    writer = csv.writer(f)
    writer.writerow(["IP", "Attempts", "First Seen", "Last Seen", "Users", "Country", "City"])
    for ip, count in sorted(failed_attempts.items(), key=lambda x: x[1], reverse=True):
        if count > THRESHOLD:
            writer.writerow([ip, count, first_seen.get(ip, 'N/A'), last_seen.get(ip, 'N/A'), ', '.join(flagged_users[ip]), geo.get(ip, {}).get("country", "Unknown"), geo.get(ip, {}).get("city", "Unknown")])

print(f"{'IP':<45} {'Attempts':>8}  {'First Seen':<18} {'Last Seen':<18} {'Users':<8} {'Country':<20} {'City':<40}")
print("-" * 135)
for ip, count in sorted(failed_attempts.items(), key=lambda x: x[1], reverse=True):
    if count > THRESHOLD:
        print(f"{ip:<45} {count:>8}  {first_seen.get(ip, 'N/A'):<18} {last_seen.get(ip, 'N/A'):<18} {', '.join(flagged_users[ip]):<8} {geo.get(ip, {}).get("country", "Unknown"):<20} {geo.get(ip, {}).get("city", "Unknown"):<40}")