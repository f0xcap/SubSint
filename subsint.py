import argparse
from bs4 import BeautifulSoup
import requests
import dns.resolver
import sys
import os

def resolve_domain(domain):
    try:
        answer = dns.resolver.resolve(domain, 'A')
        return ', '.join([ip.address for ip in answer])
    except Exception:
        return "Resolution Failed"

def fetch_domains(target):
    crtsh_url = f'https://crt.sh/?q={target}'
    response = requests.get(crtsh_url)
    soup = BeautifulSoup(response.text, "html.parser")
    domains = set()

    rows = soup.find_all("tr")[2:]  # Skip headers
    for row in rows:
        cells = row.find_all('td')
        if len(cells) >= 6:
            identities_cell = cells[5]
            for entry in identities_cell.stripped_strings:
                if not entry.startswith("*."):
                    domains.add(entry)

    return domains

parser = argparse.ArgumentParser(description='Fetch subdomains from crt.sh and resolve to IPs.')
group = parser.add_mutually_exclusive_group(required=True)
group.add_argument('domain', nargs='?', help='Single domain to query (e.g., example.com)')
group.add_argument('-l', '--list', help='File containing a list of domains (one per line)')
args = parser.parse_args()

input_domains = []

if args.list:
    if not os.path.isfile(args.list):
        print(f"File not found: {args.list}")
        sys.exit(1)
    with open(args.list, 'r') as f:
        input_domains = [line.strip() for line in f if line.strip()]
else:
    input_domains = [args.domain]

all_found_domains = set()

for domain in input_domains:
    print(f"Fetching subdomains for: {domain}")
    found = fetch_domains(domain)
    all_found_domains.update(found)

print(f"\n{'Domain':<40} {'IP Address':<30}")
print("-" * 70)

for dom in sorted(all_found_domains):
    ip = resolve_domain(dom)
    print(f"{dom:<40} {ip:<30}")

