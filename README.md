# IP-Recon

A simple Python reconnaissance tool that gathers public information about IP addresses and optionally performs a port scan using Nmap.

> **Disclaimer:** This project is intended for educational purposes and authorized security assessments only.

## Features

- IP geolocation
- ASN, ISP and organization lookup
- Domain information
- Single IP or batch processing from a file
- Optional Nmap port scanning
- Three scan profiles:
  - Quick (Top 100 ports)
  - Standard (Top 1000 ports)
  - Aggressive (All TCP ports)

## Requirements

- Python 3.10+
- Nmap installed and available in your PATH

## Python requirements
- requests (`pip install requests`)

## Usage

Run the script:

```bash
python ip-recon.py
```

### Scan a single IP

```
Load from file? y/n n
Insert IP ---> 8.8.8.8
```

### Scan multiple IPs

Create a text file containing one IP address per line.

HTTPS and HTTP URLs are also supported and their hostnames will be extracted automatically.

Example:

```
8.8.8.8
1.1.1.1
https://example.com
http://google.com
```

Then run:

```
Load from file? y/n y
Insert path: ips.txt
```

URLs are automatically parsed and their hostnames extracted before lookup.

## Scan Profiles

| Mode | Description |
|------|-------------|
| Quick | Top 100 ports |
| Standard | Top 1000 ports |
| Aggressive | All TCP ports (`-p-`) |

## Example Output

```
======= 8.8.8.8 =======

----- GEO -----
Country: United States (US)
Region: California (CA)
City: Mountain View

----- CONNECTION -----
ASN: AS15169
ISP: Google LLC
Organization: Google LLC
Domain: google.com
```

## Data Sources

IP information is retrieved using:

- https://ipwho.is/

Port scanning is performed using:

- Nmap

## Disclaimer

This software is provided for educational purposes only.

Only scan systems that you own or have explicit permission to test. The author assumes no responsibility for misuse.

## License

MIT License
