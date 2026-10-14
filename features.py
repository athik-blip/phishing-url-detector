from urllib.parse import urlsplit
import ipaddress
import re

def extract_features(url):
    url = url.strip()
    parsed = urlsplit(url if '://' in url else 'http://' + url)
    host = (parsed.hostname or '').lower()
    path = parsed.path or ''
    try:
        ipaddress.ip_address(host)
        is_ip = 1
    except ValueError:
        is_ip = 0
    return {
        'url_length':len(url),
        'host_length':len(host),
        'dots':url.count('.'),
        'hyphens':url.count('-'),
        'at_signs':url.count('@'),
        'question_marks':url.count('?'),
        'equal_signs':url.count('='),
        'digits':sum(c.isdigit() for c in url),
        'slashes':url.count('/'),
        'subdomain_count':max(0,len(host.split('.'))-2),
        'is_ip':is_ip,
        'https_scheme':int(parsed.scheme.lower()=='https'),
        'path_length':len(path),
        'suspicious_words':len(re.findall(r'login|verify|secure|account|update|password|bank',url,re.I)),
    }
