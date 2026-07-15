from src.infrastructure.ai.groq_client import GroqClient


def test_groq_client_sin_clave_no_esta_configurado():
    client = GroqClient(api_key=None)
    assert client.is_configured() is False


def test_groq_client_con_clave_esta_configurado():
    client = GroqClient(api_key="clave_de_prueba")
    assert client.is_configured() is True
