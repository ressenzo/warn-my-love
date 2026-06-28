from src.text import create_text

def test_create_text():
    # Act
    text = create_text()

    # Assert
    assert text == "Hoje, vai ter jogo."
