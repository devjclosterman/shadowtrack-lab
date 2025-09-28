import os
import re
import exifread
from typing import Dict, List, Any

# mock local breach lookup (for educational offline use)
LOCAL_BREACHES = {
    "alice@example.com": ["example-breach-2024", "old-service-leak"]
}

def check_email_local(email: str) -> List[str]:
    """Check against local breach dictionary. (Replaceable with HIBP API)"""
    return LOCAL_BREACHES.get(email.lower(), [])

def extract_exif(image_path: str) -> Dict[str, Any]:
    """Return EXIF tags for an image file."""
    with open(image_path, "rb") as f:
        tags = exifread.process_file(f, details=False)
    return {k: str(v) for k, v in tags.items()}

SECRET_REGEXES = {
    "aws_key": re.compile(r"AKIA[0-9A-Z]{16}"),
    "api_token": re.compile(r"(?i)token\s*[:=]\s*[A-Za-z0-9\-_]{20,}"),
    "basic_auth": re.compile(r"(?i)password\s*[:=]\s*.+")
}

def scan_text_for_secrets(text: str) -> List[Dict[str,str]]:
    findings = []
    for name, rx in SECRET_REGEXES.items():
        for m in rx.finditer(text):
            findings.append({"type": name, "match": m.group(0)})
    return findings
