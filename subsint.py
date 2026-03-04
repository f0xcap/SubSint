import argparse
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
    crtsh_url = f'https://crt.sh/?q={target}&output=json'
    
    try:
        response = requests.get(crtsh_url, timeout=15)
        response.raise_for_status()
        data = response.json()
    except Exception as e:
        print(f"Error fetching data for {target}: {e}")
        return set()

    domains = set()

    for entry in data:
        name_value = entry.get("name_value", "")
        
        # crt.sh may return multiple domains separated by newline
        for domain in name_value.splitlines():
            domain = domain.strip()
            if domain and not domain.startswith("*."):
                domains.add(domain)

    return domains

parser = argparse.ArgumentParser(
    description='Fetch subdomains from crt.sh (JSON) and resolve to IPs.'
)

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
