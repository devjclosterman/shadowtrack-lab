# ShadowTrack Lab

Hands-on cybersecurity lab combining vulnerable apps (OWASP Juice Shop) with a defensive scanner **ShadowTrack**.

## Quickstart

1. Build and run lab:
```bash
cd lab
docker-compose up --build
```

2. Or run the scanner locally:
```bash
python -m venv .venv && source .venv/bin/activate
pip install -r shadowtrack/requirements.txt
python -m shadowtrack.cli scan --email alice@example.com --images examples/images/ --out report.html
```


