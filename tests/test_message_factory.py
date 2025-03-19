from app import MessageFactory


def test_create_message_ok():
    factory = MessageFactory(ok_ratio=1.0)
    message = factory.create_message()
    assert message._message == "good"


def test_create_message_bad():
    factory = MessageFactory(ok_ratio=0.0)
    message = factory.create_message()
    assert message._message == "bad"


def test_create_message_mixed():
    factory = MessageFactory(ok_ratio=0.5)
    messages = [factory.create_message()._message for _ in range(100)]
    assert "good" in messages
    assert "bad" in messages
