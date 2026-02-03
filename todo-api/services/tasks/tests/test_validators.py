from services.tasks.src.validators import validate_payload

def test_validate_create_requires_title():
    try:
        validate_payload({}, creating=True)
        assert False, "Expected ValueError"
    except ValueError:
        assert True

def test_validate_status_invalid():
    try:
        validate_payload({"titulo":"x","status":"NOPE"}, creating=True)
        assert False, "Expected ValueError"
    except ValueError:
        assert True
