from src.detector import is_blocked
from src.storage import DEFAULTS

def test_blocked_title_matches_case_insensitively():
    assert is_blocked("TikTok — For You", ["tiktok"], [])

def test_whitelist_has_priority():
    assert not is_blocked("TikTok", ["TikTok"], ["TikTok"])

def test_empty_title_is_not_blocked():
    assert not is_blocked(None, ["TikTok"], [])

def test_defaults_have_expected_sections():
    assert {"settings", "stats", "profiles", "whitelist"} == set(DEFAULTS)
