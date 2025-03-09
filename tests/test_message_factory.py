from app import MessageFactory


def test_create_message_ok():
    factory = MessageFactory(success_count=10, error_count=0)
    message = factory.create_message()
    assert message._message == "ok"


def test_create_message_bad():
    factory = MessageFactory(success_count=0, error_count=10)
    message = factory.create_message()
    assert message._message == "bad"


def test_create_message_mixed():
    factory = MessageFactory(success_count=1, error_count=1)
    messages = [factory.create_message()._message for _ in range(100)]
    assert "ok" in messages
    assert "bad" in messages
