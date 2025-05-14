# SubSint

This Python script queries [crt.sh](https://crt.sh) for certificates issued for a domain, extracts associated subdomains, removes wildcards, and resolves them to IP addresses.

## Features

- Fetch subdomains and related identities from [crt.sh](https://crt.sh)
- Optionally resolve each domain to its IP address using `dnspython`
- Handles both single domains and lists of domains
- Skips wildcard entries (e.g., `*.example.com`)
- Graceful handling of DNS resolution failures

## Requirements

- Python 3.7+
- `requests`
- `beautifulsoup4`
- `dnspython`

Install dependencies using:

```bash
pip install -r requirements.txt

