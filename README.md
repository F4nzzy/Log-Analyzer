# SSH Log Analyzer

A Python tool that parses SSH authentication logs to detect brute-force attacks, geolocate attacking IPs, and export results as a report.

## Features

- Detects brute-force attacks by counting failed login attempts per IP
- Tracks first and last seen timestamps for each attacker
- Identifies which usernames were targeted
- Geolocates attacking IPs using the ip-api.com API
- Exports results to a formatted CSV report
- Live monitoring mode that alerts in real time as new log entries appear

## Requirements

- Python 3.x
- `requests` library

Install dependencies:
```bash
pip install requests
```

## Usage

### Report mode
```bash
python analyzer.py
```

### Live monitoring mode
```bash
python monitor.py
```

## Configuration

| Variable | Default | Description |
|----------|---------|-------------|
| `FILENAME` | `Linux_2k.log` | Path to the log file |
| `THRESHOLD` | `10` | Failed attempts before an IP is flagged |

## Sample Data

The included `Linux_2k.log` is a sample SSH log from the [loghub dataset](https://github.com/logpai/loghub), containing 2,000 real log entries.
