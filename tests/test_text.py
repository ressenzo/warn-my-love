from text import create_text

def test_create_text():
    """Create text to be sent in notification"""
    text = create_text()

    assert text == "Hoje, vai ter jogo."
