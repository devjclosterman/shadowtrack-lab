from shadowtrack.scanner import scan_text_for_secrets, check_email_local

def test_check_email_local_hit():
    res = check_email_local("alice@example.com")
    assert isinstance(res, list) and "example-breach-2024" in res

def test_scan_text_for_secrets():
    txt = "api_token: token: abcd1234efgh5678ijkl9012"
    findings = scan_text_for_secrets(txt)
    assert isinstance(findings, list)
