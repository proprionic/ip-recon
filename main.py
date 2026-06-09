from multiprocessing import Value

import requests
import json
from urllib.parse import urlparse
import ipaddress
import subprocess
from os import system, name

URL = "http://ipwho.is/"
from_file = str(input("Load from file? y/n "))

PROFILES = {
    "quick": ["--top-ports", "100"],
    "standard": ["--top-ports", "1000"],
    "aggressive": ["-p-"]
    }


def choose_mode():
    method = input("1. Quick\n2. Standard\n3. Aggressive (very slow)\n").strip().lower()

    if method in ["1", "quick"]:
        return "quick"
    elif method in ["2", "standard"]:
        return "standard"
    elif method in ["3", "aggressive"]:
        return "aggressive"
    else:
        print("Invalid mode.")
        return None

def scan_ports(ip):

    mode = choose_mode()
    if not mode:
        return

    args = PROFILES[mode]

    command = ["nmap", ip] + args

    print(f"\n[+] Running: {' '.join(command)}\n")

    result = subprocess.run(
        command,
        capture_output=True,
        text=True
    )

    if result.returncode != 0:
        print("[-] Nmap error:")
        print(result.stderr)
        return
    print(result.stdout)



def get_infos(ip):

    try:
        ipaddress.ip_address(ip)
        endpoint = URL + ip
    except ValueError:
        print(f"{ip} is not a valip IP address.")
        return


    try:
        response = requests.get(endpoint, timeout=5)
        response.raise_for_status()
    except requests.RequestException as e:
        print(f"Request failed for {ip}: {e}")
        return

    response_content = response.text

    ip_info = json.loads(response_content)

    if not ip_info["success"]:
        print(ip_info)
        print(f'Error: {ip_info["message"]}')
        return

    print(f'======= {ip} =======')

    print("----- GEO -----")
    print(f'Country: {ip_info["country"]} ({ip_info["country_code"]})')
    print(f'Region: {ip_info["region"]} ({ip_info["region_code"]})')
    print(f'City: {ip_info["city"]}')
    print(f'Latitude: {ip_info["latitude"]}')
    print(f'Longitude: {ip_info["longitude"]}')

    print("----- CONNECTION -----")
    print(f'asn: {ip_info["connection"]["asn"]}')
    print(f'org: {ip_info["connection"]["org"]}')
    print(f'isp: {ip_info["connection"]["isp"]}')
    print(f'domain: {ip_info["connection"]["domain"]}')

if from_file.lower() == "y":
    filename = input("Insert path: ")
    ips = []

    with open(filename, "r") as file:
        for line in file:
            line = line.strip()
            if line:
                ips.append(line)
    print(f"IPs: {len(ips)}")
    for ip in ips:
        ip = ip.strip() # remove \n
        if ip.startswith(("http://", "https://")):
            ip_parsed = urlparse(ip)
            ip = ip_parsed.hostname
        get_infos(ip)

    do_scan = input("Scan ports? y/n")

    if do_scan.lower() == "y":
        if name == "nt":
            _ = system("cls")
        system("clear")

        for ip in ips:
            print(f"===== {ip} =====")
            scan_ports(ip)

else:
    ip = input("Insert IP ---> ")
    get_infos(ip)

    scan_ports(ip)
