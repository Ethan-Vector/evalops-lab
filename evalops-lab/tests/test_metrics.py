from evalops_lab.core.metrics import contains_any, exact_match

def test_contains_any_hit():
    ok, info = contains_any("hello world", ["world"])
    assert ok is True
    assert info["hits"] == ["world"]

def test_contains_any_miss():
    ok, info = contains_any("hello world", ["Rome"])
    assert ok is False

def test_exact_match():
    ok, _ = exact_match("x", "x")
    assert ok is True
