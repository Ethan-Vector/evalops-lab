from evalops_lab.metrics import contains_all, is_refusal, citations_any

def test_contains_all():
    ok, missing = contains_all("hello world", ["hello"])
    assert ok is True
    ok2, missing2 = contains_all("hello world", ["bye"])
    assert ok2 is False
    assert missing2 == ["bye"]

def test_refusal():
    assert is_refusal("I don't have enough evidence to answer.") is True

def test_citations_any():
    assert citations_any(["passwords.md#chunk:0"], ["passwords.md"]) is True
